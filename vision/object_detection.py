from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path="yolov8n.pt"):
        print("🔄 Loading YOLO...")
        self.model = YOLO(model_path)
        self.class_names = self.model.names
        print("✅ YOLO Ready")

    def detect_objects(self, frame):
        """
        Returns only object names (strings)
        """
        results = self.model(frame, conf=0.35, verbose=False)[0]

        detected_objects = []

        if results.boxes is not None:
            for box in results.boxes:
                cls_id = int(box.cls[0])
                label = self.class_names[cls_id]
                detected_objects.append(label)

        # remove duplicates
        detected_objects = list(set(detected_objects))

        return detected_objects
