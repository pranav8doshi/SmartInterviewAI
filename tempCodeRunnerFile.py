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
                        print("Bot: Cannot repeat the question more than once. Moving on to the next question.")
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
                           print("Bot: Cannot repeat the question more than once. Moving on to the next question.")
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
                    break
            break  # ✅ End of main question & follow-up

        speak("Okay, moving on to the next question.")
        print("Bot: Okay, moving on to the next question.")
        question_index += 1