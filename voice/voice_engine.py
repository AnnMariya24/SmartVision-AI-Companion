# voice/voice_engine.py
from matplotlib import text
import pyttsx3
import threading
import speech_recognition as sr

class VoiceEngine:
    def __init__(self, rate=160, volume=1.0):

        # 🔊 Text To Speech (Windows)
        self.engine = pyttsx3.init('sapi5')
        self.engine.setProperty('rate', rate)
        self.engine.setProperty('volume', volume)

        voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', voices[0].id)

        # prevents "run loop already started"
        self.lock = threading.Lock()

        # 🎤 Speech To Text
        self.recognizer = sr.Recognizer()
        self.mic = sr.Microphone()

    # ---------------- SPEAK ---------------- #
    def speak(self, text):
        if not text:
            return

        print("🔊 Speaking:", text)

        with self.lock:
            self.engine.say(text)
            self.engine.runAndWait()


    # ---------------- LISTEN ---------------- #
    def listen_once(self):
        """
        Listen from microphone and return spoken text
        """
        try:
            with self.mic as source:
                print("🎤 Listening...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source)

            text = self.recognizer.recognize_google(audio)
            print("You said:", text)
            return text.lower()

        except:
            return ""

    # ---------------- OPTIONAL HELPER ---------------- #
    def speak_objects(self, objects):
        if not objects:
            self.speak("I do not see any objects in front.")
        else:
            object_list = ", ".join(objects)
            self.speak(f"In front of you, I see {object_list}.")
