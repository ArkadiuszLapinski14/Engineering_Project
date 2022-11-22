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

    def cut_by_4(self):
        '''Cut unecessary part of keyboard when len(keayboard) > 2'''
        try:
            if (self.Finger and self.prevFinger):
                if self.Finger[1] < self.prevFinger[1] - 300:
                    self.keys = self.keys[0:int(len(self.keys)/4)]
                    self.keyboard.set_keys(self.keys)
                elif self.Finger[1] > self.prevFinger[1] + 300:
                    self.keys = self.keys[int(len(self.keys)*(3/4)):len(self.keys)]
                    self.keyboard.set_keys(self.keys)
                elif self.Finger[2] > self.prevFinger[2] + 300:
                    self.keys = self.keys[int(len(self.keys)*(1/4)):int(len(self.keys)*(2/4))]
                    self.keyboard.set_keys(self.keys)
                elif self.Finger[2] < self.prevFinger[2] - 300:
                    self.keys = self.keys[int(len(self.keys)*(2/4)):int(len(self.keys)*(3/4))]
                    self.keyboard.set_keys(self.keys)
        except:
            print("Cut by 3/4 doesnt work/Fingers lists out of range")
    
    def cut_by_2(self):
        '''Cut unecessary part of keyboard when len(keayboard) == 2'''
        try:
            if (self.Finger and self.prevFinger):
                if self.Finger[1] < self.prevFinger[1] - 300:
                    self.keys = self.keys[0:1]
                    self.keyboard.set_keys(self.keys)
                elif self.Finger[1] > self.prevFinger[1] + 300:
                    self.keys = self.keys[1:2]
                    self.keyboard.set_keys(self.keys)
        except:
            print("Final cut by 1/2 doesnt work/Fingers lists out of range")
    
    def update(self, lms):
        '''Updates a keyboard according to our algorithm'''
        try:
            if (lms):
                self.prevFinger = self.Finger
                self.Finger = lms[8]
                if len(self.keys) == 1:
                    self.set_result(self.keys[0])
                elif len(self.keys) != 2:
                    self.cut_by_4()
                elif len(self.keys) == 1:
                    self.set_result(self.keys[0])
                else:
                    self.cut_by_2()
        except:
            print("Hand Moving Keyboard algorith doesnt work/lms out of range")

    def set_result(self, res):
        '''Append the result by the letter we picked, then set a keyboard to default values'''
        self.res.append(res)
        self.keys = self.KEYS
        self.keyboard.set_keys(self.KEYS)

    def draw_result(self, screen, x, y):
        '''Draws a result on the screen'''
        for el in self.res:
            x += 30
            cv2.putText(screen, el, (x,y), cv2.FONT_HERSHEY_PLAIN, 3 ,(255,255,255), 2)
        return screen
