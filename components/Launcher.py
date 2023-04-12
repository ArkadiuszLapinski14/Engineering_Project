import cv2
import mediapipe as mp
import time
from keyboards_back.HandMovingKeyboard import HandMovingKeyboard
from keyboards_back.HandMovingKeyboardStatic import HandMovingKeyboardStatic
from PyQt5.QtCore import *

class Launcher(QThread):
    data_ready = pyqtSignal(list)

    def __init__(self, keyboardType):
        super().__init__()
        self.keyboardType = keyboardType

    def run(self):
        pTime = 0
        cap = cv2.VideoCapture(0)
        print("Chodze")
        handMovingKeyboard = self.keyboardType

        while True:
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img = cv2.resize(img, (1080, 768))

            img, res = handMovingKeyboard.update(img)

            ###FPS###
            cTime = time.time()
            fps = 1/(cTime - pTime)
            pTime = cTime
            
            cv2.putText(img, str(int(fps)),(0,15), cv2.FONT_HERSHEY_PLAIN, 1 ,(255,0,255), 2)
            cv2.imshow("Image", img)
            cv2.waitKey(1)
            self.data_ready.emit(res)
            #########

