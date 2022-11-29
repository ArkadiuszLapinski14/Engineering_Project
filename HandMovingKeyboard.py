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
        self.is_calibrated = False

    def cut_by_4(self):
        '''Cut unecessary part of keyboard when len(keayboard) > 2'''
        try:
            if (self.Finger and self.prevFinger):
                if self.Finger[1] < self.prevFinger[1] - 250:
                    self.keys = self.keys[0:int(len(self.keys)/4)]
                    self.keyboard.set_keys(self.keys)
                elif self.Finger[1] > self.prevFinger[1] + 250:
                    self.keys = self.keys[int(len(self.keys)*(3/4)):len(self.keys)]
                    self.keyboard.set_keys(self.keys)
                elif self.Finger[2] > self.prevFinger[2] + 200:
                    self.keys = self.keys[int(len(self.keys)*(1/4)):int(len(self.keys)*(2/4))]
                    self.keyboard.set_keys(self.keys)
                elif self.Finger[2] < self.prevFinger[2] - 200:
                    self.keys = self.keys[int(len(self.keys)*(2/4)):int(len(self.keys)*(3/4))]
                    self.keyboard.set_keys(self.keys)
        except:
            print("Cut by 3/4 doesnt work/Fingers lists out of range")
    
    def cut_by_2(self):
        '''Cut unecessary part of keyboard when len(keayboard) == 2'''
        try:
            if (self.Finger and self.prevFinger):
                if self.Finger[1] < self.prevFinger[1] - 250:
                    self.keys = self.keys[0:1]
                    self.keyboard.set_keys(self.keys)
                elif self.Finger[1] > self.prevFinger[1] + 250:
                    self.keys = self.keys[1:2]
                    self.keyboard.set_keys(self.keys)
        except:
            print("Final cut by 1/2 doesnt work/Fingers lists out of range")
    
    def update(self, lms):
        '''Updates a keyboard according to our algorithm when calibrated'''
        try:
            if (lms):
                self.prevFinger = self.Finger
                self.Finger = lms[8]
                if len(self.keys) == 1:
                    self.set_result(self.keys[0])
                if self.is_calibrated == True:
                    if len(self.keys) != 2:
                        self.cut_by_4()
                    elif len(self.keys) == 1:
                        self.set_result(self.keys[0])
                    else:
                        self.cut_by_2()
        except:
            print("Hand Moving Keyboard algorith doesnt work/lms out of range")
    
    def calibrate(self, screen):
        '''Checks if finger is inside the calibration box'''
        y, x, c = screen.shape
        w, h = 200, 200
        y, x = int((y-h)/2), int((x-w)/2)
        try:
            if (self.Finger):
                if (self.Finger[1] > x and self.Finger[1] < x + w) and (self.Finger[2] > y and self.Finger[2] < y + h):    
                    screen = self.draw_rec(screen, (0,255,0), x, y, w, h)
                    self.is_calibrated = True
                else:
                    print(self.Finger[1], self.Finger[2])
                    screen = self.draw_rec(screen, (0,0,189), x, y, w, h)
                    self.is_calibrated = False
            else:
                screen = self.draw_rec(screen, (0,0,189), x, y, w, h)
                self.is_calibrated = False
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
        screen = self.calibrate(screen)
        return screen

    def draw_rec(self, screen, color,x, y, w, h):
        '''Draw calibration box''' #moze sie przydac
        cv2.rectangle(screen, (x, y), (x + w, y + h),color, 0)
        cv2.line(screen, (x, y), (x + 30, y), color, 6)
        cv2.line(screen, (x, y), (x, y + 30 ), color, 6)
        cv2.line(screen, (x+w, y), (x+w - 30, y), color, 6)
        cv2.line(screen, (x+w, y), (x+w, y + 30), color, 6)
        cv2.line(screen, (x, y+h), (x + 30, y+h), color, 6)
        cv2.line(screen, (x, y+h), (x, y+h - 30 ), color, 6)
        cv2.line(screen, (x+w, y+h), (x + w - 30, y+h), color, 6)
        cv2.line(screen, (x+w, y+h), (x+w, y+h - 30), color, 6)
        return screen