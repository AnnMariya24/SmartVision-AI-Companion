# voice_main.py
from voice_commands import VoiceCommands

def get_detected_objects():
    # This will later come from YOLO / OpenCV
    return ["person", "chair", "table"]

assistant = VoiceCommands()
assistant.run(get_detected_objects)
