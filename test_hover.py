import cv2
import time
from Modules.HandTrackingModule import handDetector
from keyboards_back.Hover import Hover
from keyboards_back.Keyboard import Keyboard
cap = cv2.VideoCapture(0)  # Video capture from webcam
cap.set(3, 1280)  # Set the width of the capture
cap.set(4, 720)   # Set the height of the capture

hover = Hover()
keyboard = Keyboard()
while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img, hover_res = hover.update(img, keyboard)

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
