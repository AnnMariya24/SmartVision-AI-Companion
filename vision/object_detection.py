from ultralytics import YOLO

class ObjectDetector:
    def __init__(self, model_path="yolov8n.pt"):
        print("🔄 Loading YOLO...")
        self.model = YOLO(model_path)
        self.class_names = self.model.names
        print("✅ YOLO Ready")

    def detect_objects(self, results):
        """
        Takes YOLO results and returns only object names (strings)
        """

        detected_objects = []

        if results.boxes is not None:
            for box in results.boxes:
                cls_id = int(box.cls[0])
                label = self.class_names[cls_id]
                detected_objects.append(label)

        return list(set(detected_objects))