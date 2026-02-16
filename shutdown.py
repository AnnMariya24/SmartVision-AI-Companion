from voice.voice_engine import VoiceEngine
import time

voice = VoiceEngine()
voice.speak("System shutting down. Goodbye.")

time.sleep(4)
