import threading
import queue
import pyttsx3

# Initialize global engine and lock
engine = None
engine_lock = threading.Lock()

# Queue for speech tasks
speech_queue = queue.Queue()

def ensure_feminine_voice():
    global engine
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        if 'female' in voice.name.lower() or 'zira' in voice.name.lower():
            engine.setProperty('voice', voice.id)
            break
    return engine

def _speech_worker():
    global engine
    while True:
        text = speech_queue.get()
        if text is None:
            break  # Exit signal to stop thread

        try:
            with engine_lock:
                # Ensure engine is ready and feminine
                if not engine:
                    engine = ensure_feminine_voice()

                current_voice = engine.getProperty('voice')
                if 'male' in current_voice.lower():
                    engine = ensure_feminine_voice()

                engine.say(text)
                engine.runAndWait()

        except Exception as e:
            print(f"Error in speech synthesis: {e}")
            try:
                engine.stop()
            except:
                pass
            # Reinitialize engine if needed
            engine = ensure_feminine_voice()

        speech_queue.task_done()

# Start background speech thread
speech_thread = threading.Thread(target=_speech_worker, daemon=True)
speech_thread.start()

def speak(text):
    """Thread-safe speak: adds text to queue"""
    speech_queue.put(text)

def stop_speech():
    """Stops the speech thread cleanly"""
    speech_queue.put(None)
    speech_thread.join()
