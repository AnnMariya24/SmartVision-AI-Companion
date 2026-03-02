import cv2

class Camera:
    def __init__(self, source="phone",
                 phone_ip="http://30.10.13.54:8080/video",
                 width=640, height=480):

        if source == "phone":
            print("📱 Connecting to phone camera...")
            self.cap = cv2.VideoCapture(phone_ip)
        else:
            print("💻 Starting laptop webcam...")
            self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

        if not self.cap.isOpened():
            raise Exception("❌ Could not open camera")

        # Reduce internal buffering (VERY IMPORTANT)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)

        self.width = width
        self.height = height

        print("✅ Camera started successfully")

    def get_frame(self):
        # 🔥 CLEAR OLD BUFFER FRAMES
        for _ in range(2):
            self.cap.grab()

        ret, frame = self.cap.read()

        if not ret:
            return None

        frame = cv2.resize(frame, (self.width, self.height))
        return frame

    def release(self):
        if self.cap:
            self.cap.release()
        cv2.destroyAllWindows()
        print("📷 Camera released")