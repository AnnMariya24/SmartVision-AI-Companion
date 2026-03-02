from groq import Groq
from voice.voice_engine import VoiceEngine


class ChatBot:
    def __init__(self):
        # 🔑 Groq client
        self.client = Groq(
            api_key="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"
        )

        # 🔊 Voice engine
        self.voice = VoiceEngine()

        print("🤖 SmartVision Groq Chatbot ready")

    def ask(self, text):
        """
        Ask Groq + Speak reply
        """
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",  # Fast + good quality
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

            # 🔊 Speak the reply

            return reply

        except Exception as e:
            print("Groq Chatbot error:", e)

            fallback = "Sorry, I am having trouble connecting to the internet."
            self.voice.speak(fallback)

            return fallback