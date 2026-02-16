#safety_system.py
import platform
import time

class SmartVisionSafety:
    def __init__(self):
        # High-priority labels that trigger SOS
        self.critical_threats = ["car", "bus", "truck", "motorcycle", "train"]

        # Distance Thresholds
        self.DANGER_ZONE = 1.2   # Meters (Immediate stop)
        self.WARNING_ZONE = 2.5  # Meters (Caution/Information)

        self.guardian_contact = "+91-98765-43210"

    def process_camera_feed(self, detections):
        """
        Processes EVERY object detected by the AI.
        detections: List of dicts [{'label': 'any_object', 'dist': 0.5}]
        """
        if not detections:
            return "Path clear."

        # 1. Sort by distance so the closest thing is handled first
        detections.sort(key=lambda x: x['dist'])

        # 2. Analyze the closest object
        closest_item = detections[0]
        name = closest_item['label']
        dist = closest_item['dist']

        # --- LOGIC 1: CRITICAL VEHICLE DANGER ---
        if name in self.critical_threats and dist <= self.DANGER_ZONE:
            self.trigger_alarm(type="emergency")
            self.send_sos(name, dist)
            return f"EMERGENCY! {name.upper()} AT {dist}m. STOP NOW!"

        # --- LOGIC 2: UNIVERSAL OBSTACLE DETECTION ---
        # This catches "anything" (chair, dog, box, person) if it's too close
        elif dist <= self.DANGER_ZONE:
            self.trigger_alarm(type="warning")
            return f"Watch out! {name} is very close. {dist} meters."

        # --- LOGIC 3: GENERAL NAVIGATION ---
        elif dist <= self.WARNING_ZONE:
            return f"{name} ahead at {dist} meters."

        # --- LOGIC 4: DISTANT OBJECTS ---
        else:
            return f"I see a {name} in the distance."

    def trigger_alarm(self, type="warning"):
        """Plays different sounds based on danger level."""
        try:
            if platform.system() == "Windows":
                import winsound
                if type == "emergency":
                    winsound.Beep(2500, 1000) # Long, high pitch
                else:
                    winsound.Beep(1000, 200)  # Short, lower pitch
            else:
                print('\a') # System bell for Mac/Linux
        except:
            print("🔊 [BEEP]")

    def send_sos(self, item, dist):
        """Simulates the emergency communication layer."""
        print(f"\n[SOS] 📡 Alerting Guardian: User is near a {item} ({dist}m)!")

# ==========================================
# TEST IN VS CODE
# ==========================================
if __name__ == "__main__":
    safety = SmartVisionSafety()

    print("--- 🚀 Universal Detection Active ---")

    # Test with a random object not in the 'critical' list
    # This proves it detects "anything"
    print("\nScenario: Walking towards a 'Unknown Box'")
    ai_data = [{'label': 'box', 'dist': 0.8}]
    print(f"Voice Output: {safety.process_camera_feed(ai_data)}")

    time.sleep(1)

    # Test with a critical threat
    print("\nScenario: Street Traffic")
    ai_data_2 = [{'label': 'bus', 'dist': 1.1}]
    print(f"Voice Output: {safety.process_camera_feed(ai_data_2)}")