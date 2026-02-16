import cv2
from vision.camera import Camera

cam = Camera()

while True:
    frame = cam.get_frame()
    if frame is None:
        break

    cv2.imshow("Camera Test", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cam.release()
