# voice_commands.py
import speech_recognition as sr
from .voice_engine import VoiceEngine

class VoiceCommands:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.voice = VoiceEngine()
        self.active = False

    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)

        try:
            command = self.recognizer.recognize_google(audio).lower()
            print("Command:", command)
            return command
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            self.voice.speak("Speech service is unavailable.")
            return ""

    def process_command(self, command, detected_objects=None):
        if "start" in command:
            self.active = True
            self.voice.speak("Voice assistant started.")

        elif "stop" in command:
            self.active = False
            self.voice.speak("Voice assistant stopped.")

        elif "help" in command:
            self.voice.speak(
                "Available commands are start, stop, help, and what is in front."
            )

        elif "what is in front" in command and self.active:
            self.voice.speak_objects(detected_objects)

        else:
            if self.active:
                self.voice.speak("Command not recognized.")

    def run(self, detected_objects_callback):
        self.voice.speak("Voice assistant ready.")
        while True:
            command = self.listen()
            objects = detected_objects_callback()
            self.process_command(command, objects)
