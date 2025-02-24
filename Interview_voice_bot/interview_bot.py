import os
import google.generativeai as genai
import speech_recognition as sr
import pyttsx3
import random
from datetime import datetime

# Set your Google Gemini API key
os.environ["GOOGLE_API_KEY"] = "AIzaSyCqbCG9gJpYp3aRVQe216t9qj9WPrIuL4A"

genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
model = genai.GenerativeModel('gemini-pro')

# Initialize text-to-speech engine
engine = pyttsx3.init()
engine.setProperty('rate', 190)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # 0 for male; 1 for female



def speak_text(text):
    """Converts text to speech"""
    engine.say(text)
    engine.runAndWait()

def append2log(text, filename):
    """Appends text to a log file"""
    with open(filename, "a") as f:
        f.write(text + "\n")

def load_questions(filename="questions.txt"):
    """Loads questions from a file, categorized by difficulty"""
    questions = {"easy": [], "medium": [], "hard": []}
    current_level = "easy"
    with open(filename, "r") as f:
        for line in f:
            line = line.strip()
            if line in ["[Easy]", "[Medium]", "[Hard]"]:
                current_level = line[1:-1].lower()
            else:
                questions[current_level].append(line)
    return questions

def select_questions(questions):
    """Selects a random number of questions between 8 and 15"""
    num_questions = random.randint(5, 6)
    all_selected = []
    used_questions = set()
    levels = ["easy", "medium", "hard"]

    while len(all_selected) < num_questions:
        for level in levels:
            if len(all_selected) < num_questions and questions[level]:
                question = random.choice(questions[level])
                while question in used_questions:
                    question = random.choice(questions[level])
                used_questions.add(question)
                all_selected.append((level, question))
    
    return all_selected

import re

def evaluate_answer(question, response, difficulty):
    """Uses AI to evaluate the answer and return a score based on difficulty"""
    difficulty_weights = {"easy": 0.8, "medium": 1, "hard": 1.2}  # Adjusted multipliers
    
    try:
        prompt = f"""
        Evaluate this response to the question on a scale of 1 to 10.
        - 10 = Excellent (Complete, clear, and correct)
        - 7-9 = Good (Mostly correct but missing minor details)
        - 4-6 = Average (Partially correct, lacks clarity)
        - 1-3 = Poor (Incorrect or very unclear)
        - The response will be **concise**, so do not penalize for length.

        Provide ONLY the numerical score.

        Question: {question}
        Answer: {response}
        """
        eval_response = model.generate_content(prompt)
        score_text = eval_response.text.strip()

        # Extract the first number from AI response
        match = re.search(r'\d+', score_text)
        score = int(match.group()) if match else random.randint(5, 10)  # Default to mid-range if parsing fails

        # Apply difficulty scaling
        weighted_score = round(score * difficulty_weights[difficulty])
        return max(0, min(10, weighted_score))  # Keep score between 0 and 10

    except Exception as e:
        print(f"Evaluation Error: {e}")
        return random.randint(5, 10)  # Assign a reasonable fallback score

def main():
    rec = sr.Recognizer()
    mic = sr.Microphone()
    rec.energy_threshold = 400
    rec.dynamic_energy_threshold = True

    client_name = input("Enter client's name: ").strip()
    questions = load_questions()
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')

    # Log files
    interview_log = f'interview-{client_name}-{timestamp}.txt'
    scorecard_file = f'scorecard-{client_name}.txt'  # One per client
    final_scorecard = 'clients_interviews.txt'  # Stores all client scores

    selected_questions = select_questions(questions)
    total_score = 0
    total_easy, total_medium, total_hard = 0, 0, 0
    count_easy, count_medium, count_hard = 0, 0, 0

    # Start interview
    speak_text(f"Hi {client_name}, let's begin the interview.")
    print(f"Bot: Hi {client_name}, let's begin the interview.")

    for level, question in selected_questions:
        while True:
            speak_text(question)
            append2log(f"Question ({level.capitalize()}): {question}", interview_log)

            with mic as source:
                rec.adjust_for_ambient_noise(source, duration=0.5)
                print("Listening for response...")
                try:
                    audio = rec.listen(source, timeout=10, phrase_time_limit=15)
                    response = rec.recognize_google(audio, language="en-IN")

                    if "repeat" in response.lower():
                        speak_text("Ok, sure.")
                        continue  # Repeat the question
                    
                    if "move on" in response.lower():
                        speak_text("Okay, moving to the next question.")
                        append2log(f"Answer: Skipped (User requested to move on)", interview_log)
                        break  # Skip to next question
                    
                    append2log(f"Answer: {response}", interview_log)

                    # Evaluate answer properly
                    score = evaluate_answer(question, response, level)
                    append2log(f"Score: {score}", scorecard_file)
                    total_score += score

                    # Track difficulty-level scores
                    if level == "easy":
                        total_easy += score
                        count_easy += 1
                    elif level == "medium":
                        total_medium += score
                        count_medium += 1
                    else:
                        total_hard += score
                        count_hard += 1

                    break  # Move to next question
                except Exception as e:
                    print(f"Error: {e}")
                    speak_text("Could not recognize your response. Moving to the next question.")
                    append2log(f"Error recognizing response", interview_log)
                    break  # Move to next question

    avg_easy = total_easy / count_easy if count_easy else 0
    avg_medium = total_medium / count_medium if count_medium else 0
    avg_hard = total_hard / count_hard if count_hard else 0
    overall_avg = total_score / len(selected_questions)

    # Store client's interview details in final scorecard
    with open(final_scorecard, "a") as f:
        f.write(f"Client: {client_name} | Date: {timestamp}\n")
        f.write(f"Easy Avg: {avg_easy:.2f}, Medium Avg: {avg_medium:.2f}, Hard Avg: {avg_hard:.2f}\n")
        f.write(f"Final Interview Score: {overall_avg:.2f} (Out of 10)\n\n")

    speak_text(f"{client_name}, your interview is complete. Thank you for your time!")
    print(f"Bot: {client_name}, your interview is complete. Thank you for your time!")

if __name__ == "__main__":
    main()
