import re
from flask import Flask, render_template, request, jsonify, redirect, url_for
import os
import json
import together
import time
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
from datetime import datetime
import random
from generate_report import generate_report
from posture_eye_analysis import analyze_posture_and_eyes
import threading
# Load API key from .env
# Load API key from .env
load_dotenv()
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")

if not TOGETHER_API_KEY:
    raise ValueError("TOGETHER_API_KEY is missing. Add it to the .env file.")

client = together.Together(api_key=TOGETHER_API_KEY)

engine = pyttsx3.init()

def set_feminine_voice():
    voices = engine.getProperty("voices")
    for voice in voices:
        if "female" in voice.name.lower() or "zira" in voice.name.lower() or "samantha" in voice.name.lower():
            engine.setProperty("voice", voice.id)
            break
    engine.setProperty("rate", 180)
    engine.setProperty("volume", 1.0)

set_feminine_voice()

if not os.path.exists("logs"):
    os.makedirs("logs")

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen_short():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 0.8
    recognizer.dynamic_energy_threshold = True
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=2.5)
        except sr.WaitTimeoutError:
            speak("Timeout. Moving on.")
            print(" Timeout! No speech detected.")
            return None
    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
        return None
    except sr.RequestError:
        print("Could not request results, check your internet.")
        return None
    
      

def listen_long():
    recognizer = sr.Recognizer()
    recognizer.pause_threshold = 1.5
    recognizer.dynamic_energy_threshold = True

    with sr.Microphone(device_index=0) as source:
        print("Listening (long)...")
        recognizer.adjust_for_ambient_noise(source, duration=0.5)

        try:
            audio = recognizer.listen(source, timeout=2, phrase_time_limit=8)
        except sr.WaitTimeoutError:
            print("Timeout! No speech detected.")
            return None

    try:
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text.strip() if text else None

    except sr.UnknownValueError:
        print("Sorry, I couldn't understand.")
        return None
    except sr.RequestError:
        print("Could not request results; check your internet.")
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
    with open("C:/Users/PAVAN/Downloads/verbal_bot/verbal_bot/interview_questions.json", "r", encoding="utf-8") as file:
        return json.load(file)

# def select_job_role():
#     questions = load_questions()
#     job_roles = list(questions.keys())
#     speak("Please select a job role from the following:")
#     print("Bot: Please select a job role from the following:")
#     for i, role in enumerate(job_roles, 1):
#         speak(f"Option {i}: {role}")
#         print(f"Option {i}: {role}")
#     while True:
#         response = listen()
#         for i, role in enumerate(job_roles, 1):
#             if response and (str(i) in response or role.lower() in response):
#                 speak(f"You selected {role}.")
#                 print(f"Bot: You selected {role}.")
#                 return role
#         speak("Sorry, I didn't catch that. Please say the job title from the options given.")

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
        print("Raw Score Response:", response)  # For debugging

        # Extract the total score using regex
        match = re.search(r"Total Score:\s*(\d+)/10", response)
        if match:
            return int(match.group(1))
        else:
            return 0
    except Exception as e:
        print(f"Scoring error: {e}")
        return 0

def conduct_interview(role, log_file, summary_file, user_name):
    questions = load_questions().get(role, [])
    selected_questions = random.sample(questions, min(10, len(questions)))
    total_score = 0
    question_index = 0
    
    while question_index < 10:
        question = selected_questions[question_index]
        speak(question)
        print("Bot:", question)
        repeat_count=0
        
        while True:  # Loop until a valid answer is given
            answer = listen_long()
            
            if answer:
                if any(phrase in answer.lower() for phrase in ["repeat", "repeat the question", "can you repeat the question"]):
                    repeat_count +=1
                    if repeat_count >=2:
                        speak("Cannot repeat the question more than once. Moving on to the next question.")
                        print("Bot: Cannot repeat the question more than once.Moving on to the next question.")
                        break
            
                    speak("Sure, I'll repeat the question.")
                    print("Bot: Sure, I'll repeat the question.")
                    speak(question)
                    print("Bot:", question)
            
                    continue
             
                log_conversation(question, answer, log_file)
                print("Evaluating your response...")
                score = score_answer(question, answer)
                total_score += score
                log_score(score, log_file)
                print(f"Score: {score}/10")
                speak("Okay, moving on to the next question.")
                print("Bot: Okay, moving on to the next question.")

                # Ask a follow-up
                follow_up = get_llama_response(f"Candidate answered: {answer}. Ask a relevant follow-up question. Not more than one question.")
                speak(follow_up)
                print("Bot:", follow_up)

                # Get follow-up answer
                follow_up_answer = listen_long()
                if follow_up_answer:
                    if any(phrase in follow_up_answer.lower() for phrase in ["repeat", "repeat the question", "can you repeat the question"]):
                        repeat_count +=1
                        if repeat_count >=2:
                           speak("Cannot repeat the question more than once. Moving on to the next question.")
                           print("Bot: Cannot repeat the question more than once.Moving on to the next question.")
                           break
                        speak("Sure, I'll repeat the question.")
                        print("Bot: Sure, I'll repeat the question.")
                        speak(follow_up)
                        print("Bot:", follow_up)
                        continue

                    log_conversation(follow_up, follow_up_answer, log_file)
                    print("Evaluating your response...")
                    score = score_answer(follow_up, follow_up_answer)
                    total_score += score
                    log_score(score, log_file)
                    print(f"Score: {score}/10", flush=True)
                    speak("Okay, moving on to the next question.")
                    print("Bot: Okay, moving on to the next question.")
                    break
                break  # ✅ End of main question & follow-up

        
        question_index += 1
        

    # Wrap up
    log_final_score(summary_file, role, total_score, user_name)
    speak("Thank you for your time. The interview is now complete.")
    print("Bot: Thank you for your time. The interview is now complete.")

def log_conversation(question, answer, log_file):
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"Q: {question}\nA: {answer}\n")

def log_score(score, log_file):
    with open(log_file, "a", encoding="utf-8") as file:
        file.write(f"Score: {score}/10\n{'-' * 40}\n")

def log_final_score(summary_file, role, total_score, user_name, posture_score, eye_score):
    with open(summary_file, "a", encoding="utf-8") as file:
        file.write(f"Candidate Name: {user_name}, Role: {role}, Final Score: {total_score}/120, Posture Score: {posture_score}/10, Eye Score: {eye_score}/10\n")
    # Generate PDF Report
    generate_report(user_name, role, total_score, posture_score, eye_score)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/start_interview', methods=['POST'])
def start_interview():
    user_name = request.form['username']
    role = request.form['role']  # Get the job role from the form
    role_folder = f"logs/{role}"
    os.makedirs(role_folder, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file = f"{role_folder}/{user_name}_{timestamp}.txt"
    summary_file = "logs/final_scores.txt"
    print(f"Logging conversation to: {log_file}\n")
    conduct_interview(role, log_file, summary_file, user_name)
    return redirect(url_for('result'))

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/meeting')
def meeting():
    return render_template('meeting.html')
    
if __name__ == '__main__':
    app.run(debug=True)
    