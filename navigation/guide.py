class NavigationGuide:
    def __init__(self):
        self.blocking_distance = 2.0  # meters

        self.dangerous_objects = [
            "person","car","bus","truck","motorbike",
            "bicycle","chair","table","dog"
        ]

    def decide_movement(self, distance_data):
        """
        Returns navigation instruction string
        """

        left_blocked = False
        center_blocked = False
        right_blocked = False

        for item in distance_data:
            obj = item["object"]
            dist = item["meters"]
            direction = item["direction"]

            if dist is None:
                continue

            if obj in self.dangerous_objects and dist < self.blocking_distance:
                if direction == "left":
                    left_blocked = True
                elif direction == "center":
                    center_blocked = True
                elif direction == "right":
                    right_blocked = True

        # 🛑 If center blocked → must avoid
        if center_blocked:
            if not left_blocked:
                return "Move slightly left"
            elif not right_blocked:
                return "Move slightly right"
            else:
                return "Stop. Path blocked."

        # If only side blocked → continue forward
        if left_blocked and not right_blocked:
            return "Keep right"

        if right_blocked and not left_blocked:
            return "Keep left"

        return "Path clear. Move forward"
