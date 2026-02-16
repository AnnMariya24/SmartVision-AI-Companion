import cv2
import time
import threading

from vision.camera import Camera
from vision.object_detection import ObjectDetector
from vision.face_emotion import FaceEmotionDetector
from vision.distance_estimator import DistanceEstimator
from safety.safety_system import SmartVisionSafety
from navigation.guide import NavigationGuide
from voice.voice_engine import VoiceEngine


print("🚶 Walking Mode Starting...")

# 🔊 Voice
voice = VoiceEngine()

def speak_async(text):
    threading.Thread(target=voice.speak, args=(text,), daemon=True).start()

speak_async("Walking mode activated")

# 📷 Modules
camera = Camera() #camera=Camera() for laptop webcam,and camera=Camera(source="phone", phone_ip="http:// for phone camera)
detector = ObjectDetector()
emotion = FaceEmotionDetector()
distance_estimator = DistanceEstimator()
safety = SmartVisionSafety()
navigator = NavigationGuide()

# 🧠 SMART SPEECH MEMORY
last_spoken_time = 0
last_spoken_message = ""
SPEECH_COOLDOWN = 4          # seconds
CLEAR_PATH_COOLDOWN = 10     # don't spam "path clear"

last_clear_time = 0


# ================= MAIN LOOP ================= #

while True:
    frame = camera.get_frame()
    if frame is None:
        continue

    # 🔵 YOLO Detection
    yolo_results = detector.model(frame, conf=0.35, verbose=False)[0]
    objects = detector.detect_objects(frame)

    # 😊 Emotion detection (future use)
    emotions = emotion.detect_emotions(frame)

    # 📏 Distance estimation
    distance_data = distance_estimator.analyze_scene(yolo_results)

    # 🧭 Navigation decision
    navigation_message = navigator.decide_movement(distance_data)

    # 🚨 Safety decision
    safety_input = []
    for item in distance_data:
        if item["meters"] is not None:
            safety_input.append({"label": item["object"], "dist": item["meters"]})

    safety_message = safety.process_camera_feed(safety_input)

    # ==========================================================
    # 🧠 SMART SPEECH DECISION ENGINE
    # ==========================================================

    message_to_speak = None

    # 🚨 PRIORITY 1 — SAFETY
    if safety_message:
        message_to_speak = safety_message

    # 🧭 PRIORITY 2 — NAVIGATION
    elif navigation_message:
        message_to_speak = navigation_message

    # 🌿 PRIORITY 3 — PATH CLEAR (rarely)
    elif objects:
        current_time = time.time()
        if current_time - last_clear_time > CLEAR_PATH_COOLDOWN:
            message_to_speak = "Path looks clear"
            last_clear_time = current_time

    # ==========================================================
    # 🔊 SPEECH CONTROLLER (ANTI-SPAM)
    # ==========================================================

    current_time = time.time()

    if message_to_speak:

        # Speak only if:
        # 1) Enough time passed
        # 2) Message changed

        if (current_time - last_spoken_time > SPEECH_COOLDOWN and
                message_to_speak != last_spoken_message):

            print("🗣️ Speaking:", message_to_speak)
            speak_async(message_to_speak)

            last_spoken_time = current_time
            last_spoken_message = message_to_speak

    # ==========================================================
    # 🖥️ DISPLAY WINDOW
    # ==========================================================

    display_frame = yolo_results.plot()

    y = 30
    if navigation_message:
        cv2.putText(display_frame, navigation_message,
                    (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
        y += 30

    if safety_message:
        cv2.putText(display_frame, safety_message,
                    (10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 3)

    cv2.imshow("Walking Mode", display_frame)

    # Press Q to quit manually
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break


# ================= CLEANUP ================= #

camera.release()
cv2.destroyAllWindows()
print("🛑 Walking Mode Stopped")
