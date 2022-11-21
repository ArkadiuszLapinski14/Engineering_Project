import cv2
import mediapipe as mp
import string
import numpy as np

class Keyboard:
    def __init__(self, keys = list(string.ascii_uppercase + "." + ','+'/'+';'+'['+']')):
        self.keys = keys
        
    def draw(self, img):
        self.img = img.copy()
        x, y, w, h = 10, 100, 20, 20
        for el in self.keys:
            cv2.rectangle(self.img, (x, y), (x + w, y + h), (192,192,192), -1)
            cv2.putText(self.img, el, (x + 5,y + 15), cv2.FONT_HERSHEY_PLAIN, 1 ,(255,255,255), 2)
            x += 25

    def update(self):
        return self.img

    def change_keys(self, keys):
        self.keys = keys

    def get_keys(self):
        return self.keys