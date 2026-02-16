import queue
import sounddevice as sd
import json
from vosk import Model, KaldiRecognizer

class SpeechToText:
    def __init__(self):
        self.model = Model("vosk-model-small-en-us-0.15")
        self.q = queue.Queue()

    def callback(self, indata, frames, time, status):
        self.q.put(bytes(indata))

    def listen(self):
        rec = KaldiRecognizer(self.model, 16000)

        with sd.RawInputStream(samplerate=16000, blocksize=8000,
                               dtype='int16', channels=1,
                               callback=self.callback):

            print("🎤 Listening offline...")
            while True:
                data = self.q.get()
                if rec.AcceptWaveform(data):
                    result = json.loads(rec.Result())
                    text = result.get("text", "")
                    if text:
                        print("User:", text)
                        return text.lower()
