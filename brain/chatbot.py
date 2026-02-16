from openai import OpenAI
from voice.voice_engine import VoiceEngine

class ChatBot:
    def __init__(self):
        # 🔑 OpenAI client
        self.client = OpenAI(
            api_key="PUT_YOUR_NEW_KEY_HERE"
        )

        # 🔊 Voice engine
        self.voice = VoiceEngine()

        print("🤖 SmartVision Chatbot ready")

    def ask(self, text):
        """
        Ask OpenAI + Speak reply
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are SmartVision, a friendly AI companion "
                            "helping visually impaired people. "
                            "Reply in short, simple sentences."
                        )
                    },
                    {"role": "user", "content": text}
                ],
                max_tokens=80
            )

            reply = response.choices[0].message.content.strip()

            print("🤖 Bot:", reply)

            # 🔊 SPEAK THE REPLY HERE
            self.voice.speak(reply)

            return reply

        except Exception as e:
            print("Chatbot error:", e)

            fallback = "Sorry, I am having trouble connecting to the internet."
            self.voice.speak(fallback)

            return fallback
