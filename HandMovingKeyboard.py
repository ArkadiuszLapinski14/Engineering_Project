import cv2
import mediapipe as mp
import Modules.HandTrackingModule as htm
import string
import asyncio

class HandMovingKeyboard:
    def __init__(self, keyboard):
        self.Finger = None
        self.prevFinger = []
        self.keyboard = keyboard
        self.keys = keyboard.get_keys()
        self.KEYS = keyboard.get_keys() #const idk jak zrobic w pythonie
        self.res = []
        self.is_calibrated = False
        self.cnt = 0
        self.cnt1 = 0

    def cut_by_4(self):
        '''Cut unecessary part of keyboard when len(keayboard) > 2'''
        try:
            print(self.prevFinger[0][1], self.Finger[1])
            if (self.Finger and self.prevFinger):
                if self.Finger[1] < self.prevFinger[0][1] - 300:
                    self.keys = self.keys[0:int(len(self.keys)/4)]
                    self.keyboard.set_keys(self.keys)
                    self.prevFinger = []
                elif self.Finger[1] > self.prevFinger[0][1] + 300:
                    self.keys = self.keys[int(len(self.keys)*(3/4)):len(self.keys)]
                    self.keyboard.set_keys(self.keys)
                    self.prevFinger = []
                elif self.Finger[2] > self.prevFinger[0][2] + 200:
                    self.keys = self.keys[int(len(self.keys)*(1/4)):int(len(self.keys)*(2/4))]
                    self.keyboard.set_keys(self.keys)
                    self.prevFinger = []
                elif self.Finger[2] < self.prevFinger[0][2] - 180:
                    self.keys = self.keys[int(len(self.keys)*(2/4)):int(len(self.keys)*(3/4))]
                    self.keyboard.set_keys(self.keys)
                    self.prevFinger = []
        except:
            print("Cut by 3/4 doesnt work/Fingers lists out of range")  
    
    def cut_by_2(self):
        '''Cut unecessary part of keyboard when len(keayboard) == 2'''
        try:
            if (self.Finger and self.prevFinger):
                if self.Finger[1] < self.prevFinger[0][1] - 300:
                    self.keys = self.keys[0:1]
                    self.keyboard.set_keys(self.keys)
                    self.prevFinger = []
                elif self.Finger[1] > self.prevFinger[0][1] + 300:
                    self.keys = self.keys[1:2]
                    self.keyboard.set_keys(self.keys)
                    self.prevFinger = []
        except:
            print("Final cut by 1/2 doesnt work/Fingers lists out of range")
    
    def update(self, lms):
        '''Updates a keyboard according to our algorithm when calibrated'''
        try:
            if (lms):
                self.Finger = lms[8]
                # if (self.cnt == 7 or self.cnt == 0):
                if len(self.prevFinger) < 20:
                    self.prevFinger.append(self.Finger)
                else:
                    self.prevFinger.append(self.Finger)
                    del self.prevFinger[0]
                    # self.cnt = 0
                # self.cnt += 1
                if len(self.keys) == 1:
                    self.set_result(self.keys[0])
                if self.is_calibrated == True:
                    if len(self.keys) != 2:
                        self.cut_by_4()
                    elif len(self.keys) == 2:
                        self.cut_by_2()
                    # elif len(self.keys) == 1:
                    #     self.set_result(self.keys[0])
        except:
            print("Hand Moving Keyboard algorith doesnt work/lms out of range")
    
    def calibrate(self, screen):
        '''Checks if finger is inside the calibration box'''
        y, x, c = screen.shape
        w, h = 100, 100
        y, x = int((y-h)/2), int((x-w)/2)
        try:
            if (self.Finger):
                if (self.Finger[1] > x and self.Finger[1] < x + w) and (self.Finger[2] > y and self.Finger[2] < y + h):
                    if self.cnt1 > 30:
                        screen = self.draw_rec(screen, (0,255,0), x, y, w, h)
                        self.is_calibrated = True
                    else:
                        screen = self.draw_rec(screen, (0,0,189), x, y, w, h)
                        self.cnt1 += 1
                        self.is_calibrated = False
                else:
                    screen = self.draw_rec(screen, (0,0,189), x, y, w, h)
                    self.is_calibrated = False
                    self.cnt1 = 0
            else:
                screen = self.draw_rec(screen, (0,0,189), x, y, w, h)
                self.is_calibrated = False
                self.cnt1 = 0

        except:
            print("?")
        return screen

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
        if self.is_calibrated == True:
            if self.cnt > 0:
                self.cnt -= 1
                screen = self.draw_rec(screen, (0,255,0), 490, 334, 100, 100)
            else: 
                self.is_calibrated = False
                screen = self.draw_rec(screen, (0,255,0), 490, 334, 100, 100)
        else:
            self.cnt = 12
            screen = self.calibrate(screen)
        return screen

    def draw_rec(self, screen, color,x, y, w, h):
        '''Draw calibration box''' #moze sie przydac
        cv2.rectangle(screen, (x, y), (x + w, y + h),color, 0)
        cv2.line(screen, (x, y), (x + 20, y), color, 4)
        cv2.line(screen, (x, y), (x, y + 20 ), color, 4)
        cv2.line(screen, (x+w, y), (x+w - 20, y), color, 4)
        cv2.line(screen, (x+w, y), (x+w, y + 20), color, 4)
        cv2.line(screen, (x, y+h), (x + 20, y+h), color, 4)
        cv2.line(screen, (x, y+h), (x, y+h - 20 ), color, 4)
        cv2.line(screen, (x+w, y+h), (x + w - 20, y+h), color, 4)
        cv2.line(screen, (x+w, y+h), (x+w, y+h - 20), color, 4)
        return screen