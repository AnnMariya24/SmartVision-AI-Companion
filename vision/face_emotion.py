from deepface import DeepFace
import cv2
import os

# ❗ Disable DeepFace progress bars & logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class FaceEmotionDetector:
    def __init__(self):
        print("🔄 Loading DeepFace emotion model...")
        
        # Warm-up run (loads model once at startup)
        try:
            dummy = cv2.imread("vision/blank.jpg")  # if not exists, it will fail safely
            DeepFace.analyze(dummy, actions=['emotion'], enforce_detection=False)
        except:
            pass

        print("✅ Emotion model ready")

    def detect_emotions(self, frame):
        """
        Detect faces and emotions from frame
        Returns list like: ["happy", "sad"]
        """
        emotions = []

        try:
            # Convert BGR → RGB
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = DeepFace.analyze(
                rgb_frame,
                actions=['emotion'],
                enforce_detection=False,
                silent=True   # ⭐ VERY IMPORTANT (stops console spam)
            )

            if isinstance(results, list):
                for face in results:
                    emotions.append(face['dominant_emotion'])
            else:
                emotions.append(results['dominant_emotion'])

        except:
            # Never crash main app
            return []

        # remove duplicates
        return list(set(emotions))
