import cv2
import time
from Modules.HandTrackingModule import handDetector
from keyboards_back.Hover import Hover

cap = cv2.VideoCapture(0)  # Video capture from webcam
cap.set(3, 1280)  # Set the width of the capture
cap.set(4, 720)   # Set the height of the capture

detector = handDetector()
hover = Hover()
hover.typing_delay = 0.8  # Modify the typing delay as a class attribute
prev_time = 0

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    img, hover_res = hover.update(img)

    if lmList:
        finger_pos = (lmList[8][1], lmList[8][2])
        key = hover.keyboard.get_key_at_position(finger_pos)
        if key:
            img = hover.keyboard.highlight(img, [1 if k == key else 0 for k in hover.keyboard.get_keys()], 50, 400, 30, 40)

            curr_time = time.time()
            if curr_time - prev_time > hover.typing_delay:
                if key == "<":
                    hover.setResult("<")  # Use the set_results method to handle backspace
                elif key == "_":
                    hover.setResult(" ")  # Use the set_results method to handle space
                else:
                    hover.setResult(key)  # Use the set_results method to handle other keys

                prev_time = curr_time

    cv2.putText(img, " ".join(hover_res), (50, 380), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)

    cv2.imshow("Hand Tracking", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
