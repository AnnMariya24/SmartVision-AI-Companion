import cv2
from vision.camera import Camera
from vision.object_detection import ObjectDetector
from vision.face_emotion import FaceEmotionDetector
from vision.distance_estimator import DistanceEstimator

class SmartVisionSystem:
    def __init__(self):
        print("🚀 Starting Smart Vision System...")

        self.camera = Camera()
        self.detector = ObjectDetector()
        self.emotion_detector = FaceEmotionDetector()
        self.distance_estimator = DistanceEstimator()

        print("✅ All Vision Modules Loaded")

    def analyze_frame(self, frame):
        """
        Runs full vision pipeline on a frame
        Returns structured data for other engineers
        """

        # 1️⃣ Object detection
        yolo_results = self.detector.model(frame, conf=0.35, verbose=False)[0]
        detected_objects = self.detector.detect_objects(frame)

        # 2️⃣ Distance + direction analysis
        distance_info = self.distance_estimator.analyze_scene(yolo_results)

        # 3️⃣ Emotion detection
        emotions = self.emotion_detector.detect_emotions(frame)

        # 4️⃣ Final structured output
        scene_data = {
            "objects_detected": detected_objects,
            "distance_analysis": distance_info,
            "emotions_detected": emotions
        }

        return scene_data, yolo_results

    def run(self):
        """
        Main loop (for testing vision engineer side)
        """
        while True:
            frame = self.camera.get_frame()
            if frame is None:
                break

            scene_data, yolo_results = self.analyze_frame(frame)

            # Show preview window (for testing only)
            frame = yolo_results.plot()
            cv2.imshow("Smart Vision", frame)

            # Print structured data in terminal
            print(scene_data)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.camera.release()


# Run standalone test
if __name__ == "__main__":
    system = SmartVisionSystem()
    system.run()
