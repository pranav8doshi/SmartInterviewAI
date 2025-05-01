from flask import Flask, render_template, request, jsonify
import os
import json
import together
import time
import sounddevice as sd
import numpy as np
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from datetime import datetime
import random
import threading
import re
import signal
import sys
import atexit
import subprocess
import psutil

app = Flask(__name__)

# Load configuration
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    raise ValueError("TOGETHER_API_KEY is missing from .env")

client = together.Together(api_key=TOGETHER_API_KEY)

# Global variables
engine = None  # Will be initialized in ensure_feminine_voice()
interview_active = False
current_interview_thread = None
interview_data = {
    "questions": [],
    "answers": [],
    "scores": [],
    "current_question": None
}
posture_process = None

def ensure_feminine_voice():
    """Initialize or reinitialize engine with feminine voice"""
    global engine
    if engine:
        try:
            engine.stop()
            engine = None
        except:
            pass
    
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    
    # Try to find the best feminine voice
    preferred_voices = [
        'Microsoft Zira Desktop',  # Windows
        'Microsoft Hazel Desktop', # Windows
        'com.apple.speech.synthesis.voice.samantha',  # Mac
        'english-us',  # Linux common
        'english_rp',  # Linux alternative
        'female'       # Generic
    ]
    
    for voice_name in preferred_voices:
        for voice in voices:
            if voice_name.lower() in voice.name.lower():
                engine.setProperty("voice", voice.id)
                break
    
    # Set default properties if no preferred voice found
    for voice in voices:
        if "female" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break
    
    engine.setProperty("rate", 180)
    engine.setProperty("volume", 1.0)
    return engine

def _speak(text):
    """Speaks the given text using pyttsx3 with proper handling of the engine loop."""
    global engine
    try:
        # Ensure we have a working engine with feminine voice
        if not engine:
            engine = ensure_feminine_voice()
        
        # Ensure voice is still feminine (in case of engine reset)
        current_voice = engine.getProperty('voice')
        if 'male' in current_voice.lower():
            engine = ensure_feminine_voice()
        
        # Avoid speaking if already busy
        if engine.isBusy():
            engine.stop()
        
        engine.say(text)
        engine.runAndWait()

    except RuntimeError:
        engine = ensure_feminine_voice()
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Error in speech synthesis: {e}")
        # Attempt complete reinitialization
        engine = ensure_feminine_voice()
        try:
            engine.say(text)
            engine.runAndWait()
        except:
            pass
        try:
            engine.stop()
        except:
            pass

def speak(text):
    """Thread-safe speaking function with guaranteed feminine voice"""
    threading.Thread(target=_speak, args=(text,)).start()

# def _speak(text):
#     """Speaks the given text using pyttsx3 with proper handling of the engine loop."""
#     global engine
#     try:
#         # Ensure we have a working engine with feminine voice
#         if not engine:
#             engine = ensure_feminine_voice()
        
#         # Ensure voice is still feminine (in case of engine reset)
#         current_voice = engine.getProperty('voice')
#         if 'male' in current_voice.lower():
#             engine = ensure_feminine_voice()
            
#         if engine._inLoop:
#             engine.endLoop()
        
#         engine.say(text)
#         engine.runAndWait()
#     except RuntimeError:
#         engine = ensure_feminine_voice()
#         engine.say(text)
#         engine.runAndWait()
#     except Exception as e:
#         print(f"Error in speech synthesis: {e}")
#         # Attempt complete reinitialization
#         engine = ensure_feminine_voice()
#         try:
#             engine.say(text)
#             engine.runAndWait()
#         except:
#             pass
#     finally:
#         try:
#             engine.stop()
#         except:
#             pass

def speak(text):
    """Thread-safe speaking function with guaranteed feminine voice"""
    threading.Thread(target=_speak, args=(text,)).start()

# def listen(max_attempts=2):
#     """Listen to user input with limited retries and better continuous speech handling"""
#     recognizer = sr.Recognizer()
#     recognizer.pause_threshold = 3.0  # Increased pause threshold to allow for natural pauses
#     recognizer.dynamic_energy_threshold = True  # Adjust for ambient noise changes
#     recognizer.operation_timeout = None  # No timeout on operations
    
#     for attempt in range(max_attempts):
#         try:
#             with sr.Microphone() as source:
#                 print("Adjusting for ambient noise...")
#                 recognizer.adjust_for_ambient_noise(source, duration=1)
#                 print(f"Listening (attempt {attempt + 1})...")
                
#                 # Listen with longer phrase time limit and no timeout
#                 audio = recognizer.listen(
#                     source, 
#                     phrase_time_limit=15,  # Increased to 15 seconds
#                     timeout=None  # No timeout while waiting for speech
#                 )
                
#                 print("Processing speech...")
#                 text = recognizer.recognize_google(audio)
#                 print(f"You said: {text}")
#                 return text.lower()
                
#         except sr.WaitTimeoutError:
#             print("No speech detected")
#             if attempt < max_attempts - 1:
#                 speak("I didn't hear anything. Please answer the question.")
#         except sr.UnknownValueError:
#             print("Could not understand audio")
#             if attempt < max_attempts - 1:
#                 speak("Sorry, I didn't catch that. Could you repeat your answer?")
#         except sr.RequestError as e:
#             print(f"Could not request results; {e}")
#             if attempt < max_attempts - 1:
#                 speak("There was an error processing your answer. Please try again.")
#         except Exception as e:
#             print(f"Unexpected error: {e}")
#             if attempt < max_attempts - 1:
#                 speak("There was a problem. Please answer again.")
    
#     return None

def listen(max_attempts=2):
    """Listen to user input using sounddevice instead of PyAudio"""
    recognizer = sr.Recognizer()
    samplerate = 16000  # 16kHz works well with Google API and speech_recognition
    duration = 10  # seconds
    
    for attempt in range(max_attempts):
        try:
            print(f"Listening (attempt {attempt + 1})...")
            speak("Please answer now.")

            # Record audio with sounddevice
            recording = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype='int16')
            sd.wait()  # Wait until recording is finished
            audio_data = np.squeeze(recording)

            # Convert numpy array to AudioData object
            audio = sr.AudioData(audio_data.tobytes(), samplerate, 2)

            print("Processing speech...")
            text = recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()

        except sr.UnknownValueError:
            print("Could not understand audio")
            if attempt < max_attempts - 1:
                speak("Sorry, I didn't catch that. Could you repeat your answer?")
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            if attempt < max_attempts - 1:
                speak("There was an error processing your answer. Please try again.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            if attempt < max_attempts - 1:
                speak("There was a problem. Please answer again.")

    return None

def get_llama_response(prompt):
    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo-Free",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=256
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        return "Sorry, I couldn't generate a response."

def load_questions():
    with open("interview_questions.json", "r", encoding="utf-8") as file:
        return json.load(file)

def score_answer(question, answer):
    if not answer:
        return 0
    prompt = f"""
You are a strict evaluator.

Question: {question}
Answer: {answer}

Evaluate the answer on:
- Relevance
- Completeness
- Accuracy
Then, give a final score from 0 (irrelevant/wrong) to 10 (perfectly relevant and accurate). 

Respond in this format:
Relevance: __/1 
Completeness: __/4  
Accuracy: __/5  
Total Score: __/10
"""
    try:
        response = get_llama_response(prompt)
        print("Scoring response:", response)
        match = re.search(r"Total Score:\s*(\d+)/10", response)
        return int(match.group(1)) if match else 0
    except Exception as e:
        print(f"Scoring error: {e}")
        return 0

def generate_report(user_name, role, questions, answers, scores, log_file):
    """Generate a comprehensive report"""
    try:
        print(f"Attempting to create report at: {log_file}")  # Debug
        print(f"Directory exists: {os.path.exists(os.path.dirname(log_file))}")  # Debug
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        report_content = f"""
Interview Report
===============
Candidate: {user_name}
Role: {role}
Date: {timestamp}
Total Questions: {len(questions)}
Total Score: {sum(scores)}/{len(questions)*10}

Detailed Results:
"""
    
        for i, (q, a, s) in enumerate(zip(questions, answers, scores)):
            report_content += f"""
Question {i+1}: {q}
Answer: {a}
Score: {s}/10
{'='*40}
"""
    # Ensure directory exists
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
    # Save to file
        with open(log_file, "w", encoding="utf-8") as f:
            f.write(report_content)
        
        print(f"Successfully created report at: {log_file}")  # Debug
        return report_content
    except Exception as e:
        print(f"Error generating report: {e}")
        raise  # Re-raise to handle in conduct_interview

def conduct_interview(role, log_file, summary_file, user_name):
    """Main interview logic with proper report file handling"""
    global interview_active, interview_data
    
    try:
        questions = load_questions().get(role, [])
        selected_questions = random.sample(questions, min(10, len(questions)))
        total_questions = 0
        total_score = 0
        
        # Reset interview data
        interview_data = {
            "questions": [],
            "answers": [],
            "scores": [],
            "current_question": None
        }
        
        # Create properly formatted file paths
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        safe_role = re.sub(r'[^\w\-_]', '_', role)
        
        # Ensure directories exist
        os.makedirs("logs", exist_ok=True)
        role_log_dir = os.path.join("logs", safe_role)
        os.makedirs(role_log_dir, exist_ok=True)
        
        # Define file paths
        log_file = os.path.join(role_log_dir, f"{user_name}_{timestamp}.txt")
        summary_file = os.path.join("logs", "summary.txt")
        
        # Initial greeting
        greeting = f"Hello {user_name}, let's begin your interview for {role}."
        print(f"Interviewer: {greeting}")
        speak(greeting)
        time.sleep(2)  # Give time for speech to complete
        
        i = 0
        while i < len(selected_questions) and interview_active:
            question = selected_questions[i]
            interview_data["current_question"] = question
            
            # Ask main question (ensure it's spoken)
            print(f"\nQuestion {i+1}/{len(selected_questions)}")
            speak(question)
            print(f"Interviewer: {question}")
            interview_data["questions"].append(question)
            
            answer = None
            for attempt in range(2):  # Try twice to get an answer
                answer = listen()
                if answer:
                    break
                
                # Handle repeat request
                if answer and any(phrase in answer for phrase in ["repeat", "say that again", "repeat the question"]):
                    speak("I'll repeat the question.")
                    speak(question)
                    continue
                
                # Handle move to next question request
                if answer and any(phrase in answer for phrase in ["next question", "move on", "skip this"]):
                    speak("Okay, let's move to the next question.")
                    interview_data["answers"].append("Requested to skip question")
                    interview_data["scores"].append(0)
                    total_questions += 1
                    break
            
            if not answer:  # If no answer after attempts, move on
                interview_data["answers"].append("No answer provided")
                interview_data["scores"].append(0)
                total_questions += 1
                i += 1
                continue
            
            interview_data["answers"].append(answer)
            
            # Score the answer
            score = score_answer(question, answer)
            total_score += score
            interview_data["scores"].append(score)
            print(f"Score: {score}/10")
            total_questions += 1
            
            # Ask follow-up question (without indicating it's a follow-up)
            if interview_active and i < len(selected_questions) - 1:
                follow_up = get_llama_response(
                    f"Candidate answered: {answer}. Ask one relevant follow-up question."
                )
                if follow_up and "sorry" not in follow_up.lower():
                    interview_data["current_question"] = follow_up
                    
                    print(f"\nQuestion {i+1}.1")
                    speak(follow_up)  # Ensure follow-up is spoken
                    print(f"Interviewer: {follow_up}")
                    interview_data["questions"].append(follow_up)
                    
                    follow_up_answer = None
                    for attempt in range(2):  # Try twice to get follow-up answer
                        follow_up_answer = listen()
                        if follow_up_answer:
                            break
                    
                    if follow_up_answer:
                        interview_data["answers"].append(follow_up_answer)
                        follow_up_score = score_answer(follow_up, follow_up_answer)
                        total_score += follow_up_score
                        interview_data["scores"].append(follow_up_score)
                        print(f"Score: {follow_up_score}/10")
                        total_questions += 1
                    else:
                        interview_data["answers"].append("No answer provided")
                        interview_data["scores"].append(0)
                        total_questions += 1
            
            i += 1
        
        report_content = generate_report(
            user_name,
            role,
            interview_data["questions"],
            interview_data["answers"],
            interview_data["scores"],
            log_file
        )
        
        # Verify report was created
        if not os.path.exists(log_file):
            raise Exception(f"Failed to create report at {log_file}")
            
        print(f"Successfully created report: {log_file}")
        
    except Exception as e:
        print(f"Error in interview: {e}")
        # Emergency save
        emergency_file = f"emergency_{user_name}_{timestamp}.txt"
        with open(emergency_file, "w", encoding="utf-8") as f:
            f.write(f"Emergency Report\nUser: {user_name}\nRole: {role}\n")
            if interview_data["questions"]:
                for i, (q, a, s) in enumerate(zip(
                    interview_data["questions"],
                    interview_data["answers"],
                    interview_data["scores"]
                )):
                    f.write(f"\nQ{i+1}: {q}\nA: {a}\nScore: {s}/10\n")
        print(f"Created emergency report: {emergency_file}")
        
    finally:
        interview_active = False
        
def start_posture_analysis(user_name):
    """Start the posture analysis script in a subprocess"""
    global posture_process
    if posture_process is None:
        posture_process = subprocess.Popen(
            ["python", "posture_eye_analysis.py", user_name],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        print(f"Started posture analysis with PID: {posture_process.pid}")

def stop_posture_analysis():
    """Stop the posture analysis script"""
    global posture_process
    if posture_process:
        try:
            # Try to terminate gracefully
            posture_process.terminate()
            try:
                posture_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Force kill if not responding
                posture_process.kill()
        except Exception as e:
            print(f"Error stopping posture analysis: {e}")
        finally:
            posture_process = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_interview', methods=['POST'])
def start_interview():
    global interview_active, current_interview_thread
    
    data = request.get_json() if request.is_json else request.form
    user_name = data.get('username', '').strip()
    role = data.get('role', '').strip()
    
    if not user_name or not role:
        return jsonify({"error": "Missing username or role"}), 400
    
    if interview_active:
        return jsonify({"error": "An interview is already in progress"}), 400
    
    interview_active = True
    
    # Start posture analysis
    start_posture_analysis(user_name)
    
    
    
    # Prepare summary file
    summary_file = "logs/summary.txt"
    
    # Start interview in a new thread (log file path will be generated within conduct_interview)
    current_interview_thread = threading.Thread(
        target=conduct_interview,
        args=(role, None, summary_file, user_name )# log_file will be generated inside
    )
    current_interview_thread.daemon = True
    current_interview_thread.start()
    
    return jsonify({
        "status": "started",
        "message": f"Interview started for {user_name} ({role})"
    })

@app.route('/end_interview', methods=['POST'])
def end_interview():
    global interview_active
    data = request.get_json()
    print(f"Received termination request: {data.get('reason', 'No reason provided')}")
    interview_active = False
    
    # Stop posture analysis
    stop_posture_analysis()
    
    # Allow time for report generation
    report_timeout = 10  # Increased timeout
    if current_interview_thread and current_interview_thread.is_alive():
        current_interview_thread.join(timeout=report_timeout)
        
    # Verify report was created
    if not os.path.exists("logs") or not os.listdir("logs"):
        print("WARNING: No reports found in logs directory")
        
    # Then shutdown
    os.kill(os.getpid(), signal.SIGINT)
    
    return jsonify({"status": "termination_requested"})

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/meeting')
def meeting():
    return render_template('meeting.html')

def cleanup():
    global interview_active
    print("Performing cleanup before exit...")
    interview_active = False
    try:
        if engine:
            engine.stop()
    except:
        pass
    # Forcefully terminate the application
    os._exit(0)

atexit.register(cleanup)
signal.signal(signal.SIGINT, lambda *args: cleanup())
signal.signal(signal.SIGTERM, lambda *args: cleanup())

if __name__ == '__main__':
    app.run()