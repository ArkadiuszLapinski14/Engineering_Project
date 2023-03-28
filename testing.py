import cv2
import mediapipe as mp
import time
import Modules.HandTrackingModule as htm
from keyboards_back.Keyboard import Keyboard
from keyboards_back.HandMovingKeyboard import HandMovingKeyboard
from keyboards_back.HandMovingKeyboardStatic import HandMovingKeyboardStatic

def main():
    pTime = 0

    cap = cv2.VideoCapture(0)
    detector = htm.handDetector(maxHands=1)
    classic_keyboard = Keyboard()
    handMovingKeyboard = HandMovingKeyboardStatic(classic_keyboard)

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (1080, 768))
        img = detector.findHands(img, draw = False)
        lmList = detector.findPosition(img)

        img = handMovingKeyboard.update(img, lmList, classic_keyboard)

        ###FPS###
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        ###DRAW RESULT###
        img = handMovingKeyboard.drawResult(img, 600, 600)
        #################
        
        cv2.putText(img, str(int(fps)),(0,15), cv2.FONT_HERSHEY_PLAIN, 1 ,(255,0,255), 2)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        #########

if __name__ == '__main__':
    main()

