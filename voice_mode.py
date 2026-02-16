from voice.voice_engine import VoiceEngine
from brain.chatbot import ChatBot
from brain.question_handler import QuestionHandler
import time
import os

voice = VoiceEngine()
bot = ChatBot()

# ⭐ Connect QuestionHandler (VERY IMPORTANT)
qa = QuestionHandler(bot)

voice.speak("Companion mode activated. I am listening.")

STOP_FILE = "stop_signal.txt"

while True:

    # 🛑 shutdown signal
    if os.path.exists(STOP_FILE):
        voice.speak("Stopping companion mode")
        os.remove(STOP_FILE)
        break

    text = voice.listen_once()

    if text == "":
        continue

    print("You said:", text)

    if "stop" in text or "sleep" in text:
        voice.speak("Going back to standby mode")
        break

    # ⭐ USE QUESTION HANDLER (offline brain)
    reply = qa.process(text)

    print("Bot:", reply)

    # 🔊 Speak reply
    voice.speak(reply)

    time.sleep(1)
