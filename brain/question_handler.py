import datetime
import socket

class QuestionHandler:
    def __init__(self, chatbot):
        self.bot = chatbot

    # 🌐 Check basic internet connection
    def internet_available(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=2)
            return True
        except:
            return False

    # 🤖 Offline fallback answers (for demo reliability)
    def offline_answers(self, question):

        question = question.lower()

        if "time" in question:
            return "The time is " + datetime.datetime.now().strftime("%I %M %p")

        if "date" in question or "day" in question:
            return "Today is " + datetime.datetime.now().strftime("%B %d")

        if "your name" in question:
            return "I am Smart Vision, your AI companion."

        if "who made you" in question or "who created you" in question:
            return "I was created to help visually impaired people navigate safely."

        if "what can you do" in question:
            return "I can detect objects, guide walking, recognize emotions and answer your questions."

        if "where am i" in question:
            return "You are in a safe indoor environment."

        if "hello" in question or "hi" in question:
            return "Hello! I am here with you."

        # default fallback
        return "I am offline right now, but I am still here to help you move safely."

    # 🧠 MAIN PROCESS (HYBRID MODE)
    # 🧠 MAIN PROCESS (OFFLINE DEMO MODE)
    def process(self, question):

        # If internet available → use Groq
        if self.internet_available():
            print("🌐 Internet available → Using Groq")
            return self.bot.ask(question)

        # Otherwise → fallback
        print("⚠️ No internet → Using offline mode")
        return self.offline_answers(question)

