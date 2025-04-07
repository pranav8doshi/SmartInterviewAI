def conduct_interview(role, log_file, summary_file, user_name):
    questions = load_questions().get(role, [])
    selected_questions = random.sample(questions, min(10, len(questions)))
    total_score = 0
    question_index = 0

    while question_index < 10:
        question = selected_questions[question_index]
        speak(question)
        print("Bot:", question)

        while True:  # Loop until a valid answer is given
            answer = listen_long()
            if answer:
                if any(phrase in answer.lower() for phrase in ["repeat", "repeat the question", "can you repeat the question"]):
                    speak("Sure, I'll repeat the question.")
                    print("Bot: Sure, I'll repeat the question.")
                    speak(question)
                    print("Bot:", question)
                    continue

                log_conversation(question, answer, log_file)
                score = score_answer(question, answer)
                total_score += score
                log_score(score, log_file)
                print(f"Score: {score}/10")

                # Ask a follow-up
                follow_up = get_llama_response(f"Candidate answered: {answer}. Ask a relevant follow-up question. Not more than one question.")
                speak(follow_up)
                print("Bot:", follow_up)

                # Get follow-up answer
                follow_up_answer = listen_long()
                if follow_up_answer:
                    log_conversation(follow_up, follow_up_answer, log_file)
                    score = score_answer(follow_up, follow_up_answer)
                    total_score += score
                    log_score(score, log_file)
                    print(f"Score: {score}/10")

                # ✅ Say moving on regardless
                speak("Okay, moving on to the next question.")
                print("Bot: Okay, moving on to the next question.")
                break  # move to next question

        question_index += 1

    # Wrap up
    log_final_score(summary_file, role, total_score, user_name)
    speak("Thank you for your time. The interview is now complete.")
    print("Bot: Thank you for your time. The interview is now complete.")
