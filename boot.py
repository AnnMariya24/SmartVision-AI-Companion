from voice.voice_engine import VoiceEngine
import time

voice = VoiceEngine()
voice.speak("Smart Vision system powered on and ready.")

time.sleep(5)   # ⬅ VERY IMPORTANT (lets speech finish)
