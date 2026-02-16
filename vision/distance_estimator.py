class DistanceEstimator:
    def __init__(self, frame_width=640):
        """
        frame_width helps us know LEFT / CENTER / RIGHT direction
        """
        self.focal_length = 700
        self.frame_width = frame_width

        # Average real-world widths (meters)
        self.known_widths = {
            "person": 0.45,
            "car": 1.8,
            "bus": 2.5,
            "truck": 2.5,
            "motorbike": 0.8,
            "bicycle": 0.6,
            "chair": 0.5,
            "sofa": 1.5,
            "bed": 1.6,
            "tv": 1.0,
            "laptop": 0.35,
            "dog": 0.5,
            "cat": 0.3,
            "bench": 1.2,
            "dining table": 1.6
        }

        # Objects that can be dangerous
        self.dangerous_objects = [
            "car", "bus", "truck", "motorbike", "bicycle"
        ]

    # ---------- Distance in meters ----------
    def estimate_distance_meters(self, object_name, bbox_width):
        if object_name not in self.known_widths:
            return None

        real_width = self.known_widths[object_name]
        distance = (real_width * self.focal_length) / bbox_width
        return round(distance, 2)

    # ---------- Convert to human words ----------
    def distance_category(self, meters):
        if meters is None:
            return "unknown"
        if meters < 1:
            return "very close"
        elif meters < 3:
            return "near"
        elif meters < 6:
            return "far"
        else:
            return "very far"

    # ---------- Detect direction ----------
    def get_direction(self, x1, x2):
        center_x = (x1 + x2) / 2

        if center_x < self.frame_width * 0.33:
            return "left"
        elif center_x < self.frame_width * 0.66:
            return "center"
        else:
            return "right"

    # ---------- Priority level ----------
    def get_priority(self, obj, meters):
        if meters is None:
            return "low"

        if obj in self.dangerous_objects and meters < 5:
            return "high"

        if meters < 1.5:
            return "medium"

        return "low"

    # ---------- Main function ----------
    def analyze_scene(self, yolo_results):
        """
        Final output for whole team.
        Returns structured walking guidance data.
        """
        output = []

        if yolo_results.boxes is None:
            return output

        for box in yolo_results.boxes:
            cls_id = int(box.cls[0])
            label = yolo_results.names[cls_id]

            x1, y1, x2, y2 = map(int, box.xyxy[0])
            bbox_width = x2 - x1

            meters = self.estimate_distance_meters(label, bbox_width)
            category = self.distance_category(meters)
            direction = self.get_direction(x1, x2)
            priority = self.get_priority(label, meters)

            output.append({
                "object": label,
                "meters": meters,
                "distance_label": category,
                "direction": direction,
                "priority": priority
            })

        return output
