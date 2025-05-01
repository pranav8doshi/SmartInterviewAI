import cv2
import mediapipe as mp
from deepface import DeepFace
import time
import numpy as np
from collections import Counter, defaultdict
from datetime import datetime
import os
import logging
import traceback

# Initialize logging
logging.basicConfig(
    filename='posture_analysis.log',
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize mediapipe components
mp_face_detection = mp.solutions.face_detection
mp_face_mesh = mp.solutions.face_mesh
mp_pose = mp.solutions.pose

# Constants
EAR_THRESHOLD = 0.2
LOOK_AWAY_THRESHOLD = 10
MOOD_CHECK_INTERVAL = 5
MULTI_FACE_THRESHOLD = 2
MIN_RUNTIME = 30  # Minimum runtime in seconds
MAX_RUNTIME = 600  # Maximum runtime in seconds (10 minutes)

# Landmark indices
LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]
LEFT_IRIS = 468
RIGHT_IRIS = 473
LEFT_EYE_TOP = 159
LEFT_EYE_BOTTOM = 145
RIGHT_EYE_TOP = 386
RIGHT_EYE_BOTTOM = 374
LEFT_SHOULDER = 11
RIGHT_SHOULDER = 12

def get_default_metrics():
    """Return default metrics structure with zeros"""
    return {
        'person_counter': 0,
        'multi_face_events': [],
        'current_multi_face_start': None,
        'not_looking_in_webcam': 0,
        'eyes_looking_away': 0,
        'prolonged_look_away': 0,
        'look_away_events': [],
        'mood_history': [get_default_emotion_data()],
        'blink_count': 0,
        'confidence_level': 0,
        'nervous_indicators': 0,
        'shoulder_analysis': [get_default_shoulder_data()],
        'expression_changes': 0,
        'last_expression': None
    }

def get_default_emotion_data():
    """Return default emotion data"""
    return {
        'dominant_emotion': 'neutral',
        'emotion_scores': {
            'angry': 0,
            'disgust': 0,
            'fear': 0,
            'happy': 0,
            'sad': 0,
            'surprise': 0,
            'neutral': 100
        },
        'emotion_confidence': 100,
        'nervous_indicators': 0,
        'confidence_level': 1
    }

def get_default_shoulder_data():
    """Return default shoulder data"""
    return {
        'shoulder_angle': 0,
        'shoulder_confidence_score': 1,
        'shoulder_position': 'neutral',
        'shoulder_ratio': 0.1,
        'left_shoulder': (0.4, 0.5),
        'right_shoulder': (0.6, 0.5)
    }

def analyze_posture(user_name):
    """Main function to analyze posture and eye contact"""
    try:
        logging.info(f"Starting posture analysis for {user_name}")
        
        # Initialize metrics with default values
        metrics = get_default_metrics()
        start_time = time.time()
        
        # Initialize mediapipe instances with error handling
        try:
            face_detection = mp_face_detection.FaceDetection()
            face_mesh = mp_face_mesh.FaceMesh(
                max_num_faces=1,
                refine_landmarks=True,
                min_detection_confidence=0.5,
                min_tracking_confidence=0.5
            )
            pose = mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        except Exception as e:
            logging.error(f"Mediapipe initialization failed: {str(e)}")
            save_text_report(metrics, user_name)
            return

        # Start webcam with error handling
        try:
            cap = cv2.VideoCapture(0)
            if not cap.isOpened():
                raise RuntimeError("Could not open webcam")
                
            # Set camera resolution
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        except Exception as e:
            logging.error(f"Webcam initialization failed: {str(e)}")
            save_text_report(metrics, user_name)
            return

        current_mood = "Detecting..."
        last_emotion_check = 0
        is_looking_away = False
        look_away_start_time = 0

        while cap.isOpened():
            # Check runtime limits
            elapsed_time = time.time() - start_time
            if elapsed_time < MIN_RUNTIME:
                continue
            if elapsed_time > MAX_RUNTIME:
                break

            try:
                ret, frame = cap.read()
                if not ret:
                    logging.warning("Failed to capture frame")
                    break

                frame = cv2.flip(frame, 1)
                h, w, _ = frame.shape
                rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                # Face detection
                face_results = face_detection.process(rgb_frame)
                faces = face_results.detections if face_results.detections else []

                # Track multiple faces
                if len(faces) > 1:
                    if metrics['current_multi_face_start'] is None:
                        metrics['current_multi_face_start'] = time.time()
                else:
                    if metrics['current_multi_face_start'] is not None:
                        duration = time.time() - metrics['current_multi_face_start']
                        if duration >= MULTI_FACE_THRESHOLD:
                            metrics['multi_face_events'].append({
                                'timestamp': time.time(),
                                'duration': duration,
                                'face_count': len(faces)
                            })
                        metrics['current_multi_face_start'] = None

                # Pose detection (for shoulders)
                pose_results = pose.process(rgb_frame)
                
                # Shoulder analysis
                shoulder_data = analyze_shoulders(pose_results.pose_landmarks, w, h)
                metrics['shoulder_analysis'].append({
                    'timestamp': time.time(),
                    **shoulder_data
                })

                if len(faces) == 1:
                    face = faces[0]
                    bboxC = face.location_data.relative_bounding_box
                    x, y, width, height = int(bboxC.xmin * w), int(bboxC.ymin * h), int(bboxC.width * w), int(bboxC.height * h)
                    
                    # Ensure face crop is valid
                    if width > 0 and height > 0:
                        face_crop = frame[y:y+height, x:x+width]
                        
                        # Face mesh processing
                        face_mesh_results = face_mesh.process(rgb_frame)
                        if face_mesh_results.multi_face_landmarks:
                            for face_landmarks in face_mesh_results.multi_face_landmarks:
                                # Check if person is centered in frame
                                nose = face_landmarks.landmark[1]
                                x_nose = int(nose.x * w)
                                y_nose = int(nose.y * h)
                                
                                if x_nose < w * 0.3 or x_nose > w * 0.7 or y_nose < h * 0.3 or y_nose > h * 0.7:
                                    metrics['not_looking_in_webcam'] += 1
                                
                                # Blink detection
                                ear = calculate_eye_aspect_ratio(face_landmarks)
                                if ear < EAR_THRESHOLD:
                                    metrics['blink_count'] += 1
                                
                                # Gaze detection
                                gaze_data = detect_gaze_direction(face_landmarks, w, h)
                                
                                if gaze_data['is_looking_away']:
                                    if not is_looking_away:
                                        look_away_start_time = time.time()
                                        is_looking_away = True
                                    
                                    current_look_away_duration = time.time() - look_away_start_time
                                    
                                    if current_look_away_duration > LOOK_AWAY_THRESHOLD:
                                        metrics['prolonged_look_away'] += 1
                                    
                                    metrics['eyes_looking_away'] += 1
                                    metrics['look_away_events'].append({
                                        'timestamp': time.time(),
                                        'direction': gaze_data['direction'],
                                        'duration': current_look_away_duration if is_looking_away else 0
                                    })
                                else:
                                    if is_looking_away:
                                        look_away_duration = time.time() - look_away_start_time
                                        if look_away_duration > LOOK_AWAY_THRESHOLD:
                                            metrics['prolonged_look_away'] += 1
                                        is_looking_away = False
                        
                        # Mood detection at intervals
                        if time.time() - last_emotion_check >= MOOD_CHECK_INTERVAL:
                            emotion_data = detect_emotion_with_confidence(face_crop, metrics)
                            current_mood = emotion_data['dominant_emotion']
                            metrics['mood_history'].append(emotion_data)
                            last_emotion_check = time.time()

            except Exception as e:
                logging.error(f"Error during frame processing: {str(e)}")
                traceback.print_exc()
                continue

        # Cleanup
        cap.release()
        face_detection.close()
        face_mesh.close()
        pose.close()

    except Exception as e:
        logging.error(f"Critical error in posture analysis: {str(e)}")
        traceback.print_exc()
        metrics = get_default_metrics()

    finally:
        save_text_report(metrics, user_name)
        logging.info(f"Completed posture analysis for {user_name}")


def detect_emotion_with_confidence(face_img, metrics):
    """Enhanced emotion detection with confidence and nervousness analysis"""
    try:
        analysis = DeepFace.analyze(
            face_img, 
            actions=['emotion'], 
            enforce_detection=False,
            detector_backend='opencv',
            silent=True
        )
        
        emotion_data = analysis[0]['emotion']
        dominant_emotion = analysis[0]['dominant_emotion']
        emotion_score = emotion_data[dominant_emotion]
        
        # Calculate confidence indicators (0-3 scale)
        confidence_level = 0
        if emotion_data['happy'] > 40:
            confidence_level += 1
        if emotion_data['neutral'] > 60:
            confidence_level += 1
        if emotion_data['angry'] < 20 and emotion_data['fear'] < 20:
            confidence_level += 1
            
        # Calculate nervousness indicators (0-3 scale)
        nervous_indicators = 0
        if emotion_data['fear'] > 30:
            nervous_indicators += 1
        if emotion_data['sad'] > 30:
            nervous_indicators += 1
        if emotion_data['surprise'] > 40:
            nervous_indicators += 1
            
        # Track expression changes
        if metrics['last_expression'] and metrics['last_expression'] != dominant_emotion:
            metrics['expression_changes'] += 1
        metrics['last_expression'] = dominant_emotion
            
        return {
            'dominant_emotion': dominant_emotion,
            'emotion_scores': emotion_data,
            'emotion_confidence': emotion_score,
            'nervous_indicators': nervous_indicators,
            'confidence_level': confidence_level
        }
    except Exception as e:
        print(f"Emotion detection error: {e}")
        return {
            'dominant_emotion': 'undetected',
            'emotion_scores': {},
            'emotion_confidence': 0,
            'nervous_indicators': 0,
            'confidence_level': 0
        }

def calculate_eye_aspect_ratio(face_landmarks):
    """Calculate Eye Aspect Ratio for blink detection"""
    # Left eye
    l_vert1 = face_landmarks.landmark[159].y - face_landmarks.landmark[145].y
    l_vert2 = face_landmarks.landmark[158].y - face_landmarks.landmark[153].y
    l_horiz = face_landmarks.landmark[33].x - face_landmarks.landmark[133].x
    
    # Right eye
    r_vert1 = face_landmarks.landmark[386].y - face_landmarks.landmark[374].y
    r_vert2 = face_landmarks.landmark[385].y - face_landmarks.landmark[380].y
    r_horiz = face_landmarks.landmark[362].x - face_landmarks.landmark[263].x
    
    left_ear = (abs(l_vert1) + abs(l_vert2)) / (2 * abs(l_horiz))
    right_ear = (abs(r_vert1) + abs(r_vert2)) / (2 * abs(r_horiz))
    
    return (left_ear + right_ear) / 2

def detect_gaze_direction(face_landmarks, frame_width, frame_height):
    """Detect eye gaze direction with iris tracking"""
    try:
        # Get iris landmarks
        left_iris = face_landmarks.landmark[LEFT_IRIS]
        right_iris = face_landmarks.landmark[RIGHT_IRIS]
        
        # Get eye corner landmarks
        left_eye_left = face_landmarks.landmark[LEFT_EYE[0]]
        left_eye_right = face_landmarks.landmark[LEFT_EYE[1]]
        right_eye_left = face_landmarks.landmark[RIGHT_EYE[0]]
        right_eye_right = face_landmarks.landmark[RIGHT_EYE[1]]
        
        # Calculate eye widths and heights
        left_eye_width = abs(left_eye_left.x - left_eye_right.x)
        right_eye_width = abs(right_eye_left.x - right_eye_right.x)
        left_eye_height = abs(face_landmarks.landmark[LEFT_EYE_TOP].y - face_landmarks.landmark[LEFT_EYE_BOTTOM].y)
        right_eye_height = abs(face_landmarks.landmark[RIGHT_EYE_TOP].y - face_landmarks.landmark[RIGHT_EYE_BOTTOM].y)
        
        # Calculate iris position relative to eye corners
        left_iris_pos_x = (left_iris.x - left_eye_left.x) / left_eye_width
        right_iris_pos_x = (right_iris.x - right_eye_left.x) / right_eye_width
        left_iris_pos_y = (left_iris.y - face_landmarks.landmark[LEFT_EYE_TOP].y) / left_eye_height
        right_iris_pos_y = (right_iris.y - face_landmarks.landmark[RIGHT_EYE_TOP].y) / right_eye_height
        
        # Determine gaze direction
        direction = []
        center_range_x = (0.35, 0.65)
        center_range_y = (0.35, 0.65)
        
        # Horizontal gaze
        if left_iris_pos_x < center_range_x[0] and right_iris_pos_x < center_range_x[0]:
            direction.append("Left")
        elif left_iris_pos_x > center_range_x[1] and right_iris_pos_x > center_range_x[1]:
            direction.append("Right")
        
        # Vertical gaze
        if left_iris_pos_y < center_range_y[0] and right_iris_pos_y < center_range_y[0]:
            direction.append("Up")
        elif left_iris_pos_y > center_range_y[1] and right_iris_pos_y > center_range_y[1]:
            direction.append("Down")
        
        return {
            'direction': " & ".join(direction) if direction else "Center",
            'left_iris_pos': (left_iris_pos_x, left_iris_pos_y),
            'right_iris_pos': (right_iris_pos_x, right_iris_pos_y),
            'is_looking_away': bool(direction)
        }
    except Exception as e:
        print(f"Gaze detection error: {e}")
        return {
            'direction': "undetected",
            'left_iris_pos': (0, 0),
            'right_iris_pos': (0, 0),
            'is_looking_away': False
        }

def analyze_shoulders(pose_landmarks, frame_width, frame_height):
    """Improved shoulder analysis with better position detection"""
    if not pose_landmarks:
        return {
            'shoulder_angle': 0,
            'shoulder_confidence_score': 0,
            'shoulder_position': 'undetected',
            'shoulder_ratio': 0
        }
    
    try:
        left_shoulder = pose_landmarks.landmark[LEFT_SHOULDER]
        right_shoulder = pose_landmarks.landmark[RIGHT_SHOULDER]
        
        # Calculate shoulder angle (horizontal alignment)
        angle = np.degrees(np.arctan2(
            right_shoulder.y - left_shoulder.y,
            right_shoulder.x - left_shoulder.x
        ))
        
        # Calculate shoulder height ratio (for slump detection)
        shoulder_height_diff = abs(left_shoulder.y - right_shoulder.y)
        shoulder_width = abs(left_shoulder.x - right_shoulder.x)
        shoulder_ratio = shoulder_height_diff / shoulder_width
        
        # Confidence scoring based on shoulder position (0-3 scale)
        confidence_score = 0
        position = ""
        
        # Squared shoulders (confident)
        if abs(angle) < 10 and shoulder_ratio < 0.05:
            confidence_score = 3
            position = "squared"
        # Neutral shoulders
        elif abs(angle) < 20 and shoulder_ratio < 0.1:
            confidence_score = 2
            position = "neutral"
        # Slightly uneven
        elif abs(angle) < 30 and shoulder_ratio < 0.15:
            confidence_score = 1
            position = "slightly uneven"
        # Slumped or very uneven
        else:
            confidence_score = 0
            position = "slumped" if shoulder_ratio > 0.15 else "uneven"
        
        return {
            'shoulder_angle': angle,
            'shoulder_confidence_score': confidence_score,
            'shoulder_position': position,
            'shoulder_ratio': shoulder_ratio,
            'left_shoulder': (left_shoulder.x, left_shoulder.y),
            'right_shoulder': (right_shoulder.x, right_shoulder.y)
        }
    except Exception as e:
        print(f"Shoulder analysis error: {e}")
        return {
            'shoulder_angle': 0,
            'shoulder_confidence_score': 0,
            'shoulder_position': 'undetected',
            'shoulder_ratio': 0
        }

def save_text_report(metrics, user_name):
    """Save text report with username and timestamp"""
    try:
        os.makedirs("posture_reports", exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"posture_reports/{user_name}_posture.txt"
        
        with open(filename, "w") as f:
            f.write(f"Posture Analysis Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"User: {user_name}\n")
            f.write("="*50 + "\n")
            
            # Emotion analysis
            if metrics['mood_history']:
                emotion_counter = Counter([m['dominant_emotion'] for m in metrics['mood_history']])
                dominant_emotion = emotion_counter.most_common(1)[0][0]
                
                f.write(f"Dominant Emotion: {dominant_emotion}\n")
                
                avg_confidence = sum(m['confidence_level'] for m in metrics['mood_history']) / len(metrics['mood_history'])
                avg_nervous = sum(m['nervous_indicators'] for m in metrics['mood_history']) / len(metrics['mood_history'])
                f.write(f"\nAverage Confidence Level: {avg_confidence:.1f}/3\n")
                f.write(f"Average Nervous Indicators: {avg_nervous:.1f}/3\n")
            else:
                f.write("No emotion data collected\n")
            
            # Gaze analysis
            f.write("\nGaze Analysis:\n")
            f.write(f"Eyes Looking Away: {metrics['eyes_looking_away']} times\n")
            f.write(f"Prolonged Look Away Events (>10s): {metrics['prolonged_look_away']}\n")
            f.write(f"Total Blinks: {metrics['blink_count']}\n")
            
            if metrics['look_away_events']:
                direction_counter = Counter([e['direction'] for e in metrics['look_away_events']])
                f.write("Gaze Direction Distribution:\n")
                for direction, count in direction_counter.items():
                    f.write(f"- {direction}: {count} times\n")
            
            # Multiple face detection analysis
            f.write("\nMultiple Face Detection:\n")
            f.write(f"Total Events: {len(metrics['multi_face_events'])}\n")
            if metrics['multi_face_events']:
                for event in metrics['multi_face_events']:
                    f.write(f"- Duration: {event['duration']:.2f}s | Face Count: {event['face_count']}\n")
            else:
                f.write("No multiple face events detected.\n")
                       
            # Shoulder analysis
            f.write("\nShoulder Analysis:\n")
            if metrics['shoulder_analysis']:
                positions = [s['shoulder_position'] for s in metrics['shoulder_analysis'] if s['shoulder_position'] != 'undetected']
                if positions:
                    position_counter = Counter(positions)
                    f.write("Shoulder Position Distribution:\n")
                    for pos, count in position_counter.items():
                        f.write(f"- {pos}: {count} times\n")
                    
                    avg_confidence = sum(s['shoulder_confidence_score'] for s in metrics['shoulder_analysis']) / len(metrics['shoulder_analysis'])
                    f.write(f"\nAverage Shoulder Confidence: {avg_confidence:.1f}/3\n")
                else:
                    f.write("No valid shoulder data collected\n")
    except Exception as e:
        logging.error(f"Error saving report: {str(e)}")
        traceback.print_exc()

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('user_name', help='Name of the user being analyzed')
    args = parser.parse_args()
    
    analyze_posture(args.user_name)