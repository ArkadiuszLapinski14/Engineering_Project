import cv2
import mediapipe as mp
import Modules.HandTrackingModule as htm
import string

class HandMovingKeyboard:
    def __init__(self, keyboard):
        self.Finger = None
        self.keyboard = keyboard
        self.keys = keyboard.get_keys()
        self.KEYS = keyboard.get_keys() #const idk jak zrobic w pythonie
        self.res = []

    def is_movedDivBy4(self):
        try:
            if self.Finger[1] < self.prevFinger[1] - 300:
                self.keys = self.keys[0:int(len(self.keys)/4)]
                self.keyboard.change_keys(self.keys)
            elif self.Finger[1] > self.prevFinger[1] + 300:
                self.keys = self.keys[int(len(self.keys)*(3/4)):len(self.keys)]
                self.keyboard.change_keys(self.keys)
            elif self.Finger[2] > self.prevFinger[2] + 300:
                self.keys = self.keys[int(len(self.keys)*(1/4)):int(len(self.keys)*(2/4))]
                self.keyboard.change_keys(self.keys)
            elif self.Finger[2] < self.prevFinger[2] - 300:
                self.keys = self.keys[int(len(self.keys)*(2/4)):int(len(self.keys)*(3/4))]
                self.keyboard.change_keys(self.keys)
        except:
            return False
    
    def is_movedDivBy2(self):
        try:
            if self.Finger[1] < self.prevFinger[1] - 300:
                self.keys = self.keys[0:1]
                self.keyboard.change_keys(self.keys)
            elif self.Finger[1] > self.prevFinger[1] + 300:
                self.keys = self.keys[1:2]
                self.keyboard.change_keys(self.keys)
        except:
            return False
    
    def update(self, lms):
        try:
            self.prevFinger = self.Finger
            self.Finger = lms[8]
            if len(self.keys) == 1:
                self.set_result(self.keys[0])
            elif len(self.keys) != 2:
                self.is_movedDivBy4()
            elif len(self.keys) == 1:
                self.set_result(self.keys[0])
            else:
                self.is_movedDivBy2()
        except:
            pass

    def set_result(self, res):
        self.res.append(res)
        self.keys = self.KEYS
        self.keyboard.change_keys(self.KEYS)

    def draw_result(self, img):
        x, y = 300, 300
        for el in self.res:
            x += 30
            cv2.putText(img, el, (x,y), cv2.FONT_HERSHEY_PLAIN, 3 ,(255,255,255), 2)
        return img
