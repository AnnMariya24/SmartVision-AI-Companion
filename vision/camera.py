import cv2

class Camera:
    def __init__(self, source="phone",
    phone_ip="http://30.10.13.54:8080/video", width=640, height=480):
        """
        SmartVision Camera Module

        source options:
        - "webcam"  → laptop webcam
        - "phone"   → mobile camera via IP Webcam

        phone_ip example:
        "http://192.168.1.5:8080/video"
        """

        if source == "phone":
            if phone_ip is None:
                raise Exception("❌ Phone IP not provided")
            print("📱 Connecting to phone camera...")
            self.cap = cv2.VideoCapture(phone_ip)

        else:
            print("💻 Starting laptop webcam...")
            self.cap = cv2.VideoCapture(0)
            self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

        if not self.cap.isOpened():
            raise Exception("❌ Could not open camera")

        print("✅ Camera started successfully")

    def get_frame(self):
        for _ in range(3):  # retry reading frame
            ret, frame = self.cap.read()
            if ret:
                return frame
            return None

        # Flip only for webcam (not for phone)
        if frame is not None:
            frame = cv2.resize(frame, (640, 480))

        return frame

    def release(self):
        """Release camera safely"""
        self.cap.release()
        cv2.destroyAllWindows()
        print("📷 Camera released")

#for laptop webcam only (legacy code, not used in main app)
# class Camera:
#     def __init__(self, width=640, height=480):
#         """
#         SmartVision Laptop Webcam Module
#         """

#         print("💻 Starting laptop webcam...")

#         # 0 = default laptop webcam
#         self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

#         # Set resolution
#         self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
#         self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

#         if not self.cap.isOpened():
#             raise Exception("❌ Could not open laptop webcam")

#         print("✅ Webcam started successfully")

#     def get_frame(self):
#         """Capture a frame safely"""
#         ret, frame = self.cap.read()

#         if not ret:
#             return None

#         # Flip horizontally for mirror effect (natural view)
#         frame = cv2.flip(frame, 1)

#         # Ensure fixed size
#         frame = cv2.resize(frame, (640, 480))

#         return frame

#     def release(self):
#         """Release camera safely"""
#         if self.cap:
#             self.cap.release()
#         cv2.destroyAllWindows()
#         print("📷 Webcam released")