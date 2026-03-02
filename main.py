import cv2
import time
import threading
import queue
import random

# Vision
from vision.camera import Camera
from vision.object_detection import ObjectDetector
from vision.face_emotion import FaceEmotionDetector
from vision.distance_estimator import DistanceEstimator

# Voice + Safety
from voice.voice_engine import VoiceEngine
from voice.voice_commands import VoiceCommands
from safety.safety_system import SmartVisionSafety
from navigation.guide import NavigationGuide

# AI Brain
from brain.speech_to_text import SpeechToText
from brain.chatbot import ChatBot
from brain.question_handler import QuestionHandler

print("🤖 SmartVision AI Companion Starting...")

# Initialize modules
camera = Camera()
detector = ObjectDetector()
emotion_detector = FaceEmotionDetector()
distance_estimator = DistanceEstimator()
voice_engine = VoiceEngine()
voice_commands = VoiceCommands()
safety_system = SmartVisionSafety()
navigator = NavigationGuide()

speech_ai = SpeechToText()
chatbot = ChatBot()
qa_system = QuestionHandler(chatbot)

speech_queue = queue.Queue()

assistant_active = True
is_listening = False
current_objects = []

last_spoken_time = 0
last_alert_message = ""
last_alert_time = 0
last_smalltalk_time = 0

ALERT_COOLDOWN = 6
WARNING_COOLDOWN = 4
EMERGENCY_COOLDOWN = 2
SMALLTALK_INTERVAL = 40
assistant_state = "IDLE"

running = True


# 🔊 SPEECH THREAD
def speech_worker():
    while True:
        message = speech_queue.get()
        if message is None:
            break
        voice_engine.speak(message)


# 🎤 LISTENING THREAD
def listen_worker():
    global assistant_state

    WAKE_WORD = "vision"

    while running:

        if assistant_state != "IDLE":
            time.sleep(0.5)
            continue

        command = voice_commands.listen()
        if not command:
            continue

        print("Heard:", command)

        if WAKE_WORD in command:
            assistant_state = "LISTENING"
            speech_queue.put("Yes, I am listening")

            question = voice_commands.listen()
            if not question:
                assistant_state = "IDLE"
                continue

            assistant_state = "THINKING"
            speech_queue.put("Let me think")

            answer = qa_system.process(question)

            assistant_state = "SPEAKING"

            if answer and str(answer).strip() != "":
                print("🤖 Speaking:", answer)
                speech_queue.put(answer)
            else:
                speech_queue.put("Sorry, I could not understand that.")

            assistant_state = "IDLE"


# 👁️ VISION THREAD (Your Original Loop Unchanged)
def vision_worker():
    global running
    global last_spoken_time, last_alert_message, last_alert_time
    global last_smalltalk_time, current_objects

    while running:

        if not assistant_active:
            time.sleep(0.1)
            continue

        frame = camera.get_frame()
        if frame is None:
            break

        yolo_results = detector.model(frame, conf=0.35, verbose=False)[0]
        objects = detector.detect_objects(frame)
        current_objects = objects

        distance_data = distance_estimator.analyze_scene(yolo_results)
        navigation_message = navigator.decide_movement(distance_data)

        safety_input = []
        for item in distance_data:
            if item["meters"] is not None:
                safety_input.append({"label": item["object"], "dist": item["meters"]})

        safety_message = safety_system.process_camera_feed(safety_input)
        emotions = emotion_detector.detect_emotions(frame)

        message_parts = []
        if objects:
            message_parts.append("I can see " + ", ".join(objects))
        if emotions:
            message_parts.append("Someone looks " + ", ".join(emotions))
        if navigation_message:
            message_parts.append(navigation_message)

        final_message = ". ".join(message_parts)

        # 🚨 SMART ALERT SYSTEM
        danger_mode = "normal"
        current_time = time.time()

        if safety_message:
            if "EMERGENCY" in safety_message:
                danger_mode = "emergency"
            elif "Watch out" in safety_message:
                danger_mode = "warning"

        cooldown = ALERT_COOLDOWN
        if danger_mode == "warning":
            cooldown = WARNING_COOLDOWN
        elif danger_mode == "emergency":
            cooldown = EMERGENCY_COOLDOWN

        if safety_message:
            if (safety_message != last_alert_message) or (current_time - last_alert_time > cooldown):
                speech_queue.put(safety_message)
                if danger_mode == "emergency":
                    speech_queue.put("Please stop moving")
                last_alert_message = safety_message
                last_alert_time = current_time

        elif current_time - last_spoken_time > 7 and final_message:
            speech_queue.put(final_message)
            last_spoken_time = current_time

        if current_time - last_smalltalk_time > SMALLTALK_INTERVAL and not safety_message:
            speech_queue.put(random.choice([
                "Everything looks fine.",
                "You are doing great.",
                "I am here with you.",
                "Path looks clear.",
                "All safe around you."
            ]))
            last_smalltalk_time = current_time

        cv2.imshow("SmartVision", yolo_results.plot())

        if cv2.waitKey(1) & 0xFF == ord('q'):
            running = False
            break

        time.sleep(0.12)

    camera.release()
    cv2.destroyAllWindows()


# 🌍 STARTUP NARRATION (UNCHANGED)
def describe_scene_once():
    speech_queue.put("Scanning surroundings")
    frame = camera.get_frame()
    if frame is None:
        return

    yolo_results = detector.model(frame, conf=0.35, verbose=False, imgsz=416)[0]
    objects = detector.detect_objects(yolo_results)
    emotions = emotion_detector.detect_emotions(frame)
    distance_data = distance_estimator.analyze_scene(yolo_results)
    navigation_message = navigator.decide_movement(distance_data)

    narration = ["Hello. I am your Smart Vision assistant."]

    if objects:
        narration.append("I can see " + ", ".join(objects))
    else:
        narration.append("I do not see major objects nearby")

    if emotions:
        narration.append("Someone looks " + ", ".join(emotions))

    if navigation_message:
        narration.append(navigation_message)

    speech_queue.put(". ".join(narration))


# START THREADS
threading.Thread(target=speech_worker, daemon=True).start()
threading.Thread(target=listen_worker, daemon=True).start()
threading.Thread(target=vision_worker, daemon=True).start()

describe_scene_once()

# KEEP MAIN THREAD ALIVE
while running:
    time.sleep(1)