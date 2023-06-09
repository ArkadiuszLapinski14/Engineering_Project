import cv2
import mediapipe as mp
import time
from keyboards_back.HandMovingKeyboard import HandMovingKeyboard
from keyboards_back.HandMovingKeyboardStatic import HandMovingKeyboardStatic
from keyboards_back.HeadMovingKeyboardUpdated import HeadMovingKeyboard
from keyboards_back.Hover import Hover
def main():
    pTime = 0

    cap = cv2.VideoCapture(0)
    handMovingKeyboard = HandMovingKeyboard()
    hover = Hover()
    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        img = cv2.resize(img, (1080, 768))

        img = hover.update(img)

        ###FPS###
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        ###DRAW RESULT###
        #################
        
        cv2.putText(img, str(int(fps)),(0,15), cv2.FONT_HERSHEY_PLAIN, 1 ,(255,0,255), 2)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        #########

if __name__ == '__main__':
    main()

