import cv2
import numpy as np
import collections
import string
import back.modules.HandTrackingModule as htm

class HandMovingKeyboardStatic:
    def __init__(self, point = 8):
        self.Finger = None
        self.prevFinger = [] #zmiana na liste, aby sledzic ostanie x zmian polozenia palca w celu optymalizacji 
        self.detector = htm.handDetector(maxHands=1)
        self.KEYS = list(string.ascii_uppercase + "!" + '?'+','+'.'+'<'+"_") #const idk jak zrobic w pythonie
        self.res = []
        self.point = point
        self.restart = False
        self.last_gesture = None
        self.keyboard_bin_tab = np.ones(32)
        self.mask = np.ones(32)

    def update(self, screen, keyboard):
        self.keyboard = keyboard
        self.keys = self.keyboard.get_keys()
        screen = self.detector.findHands(screen, draw=False)
        lms = self.detector.findPosition(screen, draw=False)        
        x, y, w, h = self.centerCoo(screen, 100, 100)
        try:
            screen = self.keyboard.generateKeyboard(screen, 10, 100, 30, 30)
            screen = self.keyboard.highlight(screen, self.keyboard_bin_tab, 10, 100, 30, 30)
            screen = self.drawRec(screen, (0, 255, 0), x, y, w, h)
            screen = self.backToDefault(screen)
            if len(self.keys) > 0:
                self.FingerUpdate(lms)            
            if self.restart == False:
                if collections.Counter(self.keyboard_bin_tab)[1] == 32:
                    self.cutBy4(screen)
                elif collections.Counter(self.keyboard_bin_tab)[1] == 8: 
                    self.cutBy2(screen)
                elif collections.Counter(self.keyboard_bin_tab)[1] == 2:
                    self.cutBy1(screen)
                screen = self.drawResult(screen, 600, 600)
            else:
                screen = self.drawResult(screen, 600, 600)
                self.restart = False
            return screen, self.res
        except Exception as e:
            print("Hand Moving Keyboard algorithm doesn't work:", e)
            screen = self.drawResult(screen, 600, 600)
            return screen, self.res

    def setResult(self, res):
        '''Append the result by the letter we picked or delete last of them, then set a keyboard to default values'''
        ###Usuwanie
        if res == "<":
            if len(self.res) > 0:
                del self.res[-1]
        elif res == "_":
            self.res.append(" ")
        ###Dodawanie
        else:
            self.res.append(res)
        self.keyboard_bin_tab = np.ones(32)
        self.mask = np.ones(32)

    def backToDefault(self, screen):
        '''Back to the startin settings of keyboard after clicking button "Back"'''
        screen, x, y = self.drawBackButton(screen)
        if (self.Finger):
            if (self.Finger[1] < x and self.Finger[1] > (x - 78)) and (self.Finger[2] > y and self.Finger[2] < (y + 25)):        
                screen = cv2.rectangle(screen, (x, y), (x - 78, y + 25), (0,252,124), -1)
                cv2.putText(screen, "Back", (x-78, y+23), cv2.FONT_HERSHEY_PLAIN, 2 ,(255,255,255), 2)
                self.keyboard_bin_tab = np.ones(32)
                self.mask = np.ones(32)
        return screen

    def drawBackButton(self, screen):
        '''Draws button "Back"'''
        y, x , c = screen.shape
        x = int(x - 10)
        y = 10
        screen = cv2.rectangle(screen, (x, y), (x - 78, y + 25), (0, 0, 0), 3)
        screen = cv2.rectangle(screen, (x, y), (x - 78, y + 25), (192,192,192), -1)
        cv2.putText(screen, "Back", (x-78, y+23), cv2.FONT_HERSHEY_PLAIN, 2 ,(255,255,255), 2)
        return screen, x, y

    def drawResult(self, screen, x, y):
        '''Draws a result on the screen'''
        screen, x, y = self.drawResultBox(screen)
        for el in self.res:
            cv2.putText(screen, el, (x,y), cv2.FONT_HERSHEY_PLAIN, 3 ,(255,255,255), 2)
            x += 30
        return screen

    def drawResultBox(self, screen):
        '''Draws Result Box'''
        y, x , c = screen.shape
        x = int((x - 400)/2)
        y = int((y - 200))
        screen = cv2.rectangle(screen, (x, y), (x + 400, y + 40), (255,255,255), 2)
        return screen, x, y + 37

    def centerCoo(self, screen, w, h):
        '''return x, y at the center of the screen, based on width and height of your shape'''
        y, x, c = screen.shape
        w, h = 100, 100
        y, x = int((y-h)/2), int((x-w)/2)
        return x, y, w, h

    def FingerUpdate(self, lms):
        '''Updates current finger's landmark'''
        if (lms):
            self.Finger = lms[self.point]

    def cutBy4(self, screen):
        x, y, w, h = self.centerCoo(screen, 100, 100)
        try:
            tab_len = len(self.keyboard_bin_tab)
            if self.Finger:
                if (x - 100 < self.Finger[1] < x + w + 100) and (y - 100 < self.Finger[2] < y + h + 100):
                    self.last_gesture = None
                    return
                elif self.last_gesture == None:
                    if self.Finger[1] < x - 100:
                        self.mask = np.concatenate((np.ones(int(tab_len / 4)), np.zeros(int((tab_len / 4)*3))), axis=None)
                        self.keyboard_bin_tab *= np.array(self.mask)
                        self.last_gesture = "left"
                    elif self.Finger[1] > x + w + 100:
                        self.mask = np.concatenate((np.zeros(int((tab_len / 4) * 3)), np.ones(int(tab_len/4))), axis = None)
                        self.keyboard_bin_tab *= np.array(self.mask)
                        self.last_gesture = "right"
                    elif self.Finger[2] > y + h + 100:
                        self.mask = np.concatenate((np.zeros(int(tab_len/4)), np.ones(int(tab_len/4)), np.zeros(int((tab_len/4) *2))), axis = None)
                        self.keyboard_bin_tab *= np.array(self.mask)
                        self.last_gesture = "up"
                    elif self.Finger[2] < y - 100:
                        self.mask = np.concatenate((np.zeros(int((tab_len/4)*2)), np.ones(int(tab_len/4)), np.zeros(int(tab_len/4))), axis=None)
                        self.keyboard_bin_tab *= np.array(self.mask)
                        self.last_gesture = "down"
        except Exception as e:
            print("Cut by 3/4 doesn't work:", e)

    def cutBy2(self, screen):
        x, y, w, h = self.centerCoo(screen, 100, 100)
        try:
            tab_len = len(self.keyboard_bin_tab)
            if self.Finger:
                if (x - 100 < self.Finger[1] < x + w + 100) and (y - 100 < self.Finger[2] < y + h + 100):
                    self.last_gesture = None
                    return
                elif self.last_gesture == None:
                    if self.Finger[1] < x - 100:
                        idxs = np.where(self.keyboard_bin_tab == 1)
                        self.keyboard_bin_tab = np.delete(self.keyboard_bin_tab, idxs, None)
                        self.mask = np.array([1,1,0,0,0,0,0,0])
                        self.keyboard_bin_tab = np.insert(self.keyboard_bin_tab, [idxs[0][0] for i in range(len(idxs))], self.mask)
                        self.last_gesture = "left"
                    elif self.Finger[1] > x + w + 100:
                        idxs = np.where(self.keyboard_bin_tab == 1)
                        self.keyboard_bin_tab = np.delete(self.keyboard_bin_tab, idxs, None)
                        self.mask = np.array([0,0,0,0,0,0,1,1])
                        self.keyboard_bin_tab = np.insert(self.keyboard_bin_tab, [idxs[0][0] for i in range(len(idxs))], self.mask)
                        self.last_gesture = "right"
                    elif self.Finger[2] > y + h + 100:
                        idxs = np.where(self.keyboard_bin_tab == 1)
                        self.keyboard_bin_tab = np.delete(self.keyboard_bin_tab, idxs, None)
                        self.mask = np.array([0,0,1,1,0,0,0,0])
                        self.keyboard_bin_tab = np.insert(self.keyboard_bin_tab, [idxs[0][0] for i in range(len(idxs))], self.mask)
                        self.last_gesture = "up"
                    elif self.Finger[2] < y - 100:
                        idxs = np.where(self.keyboard_bin_tab == 1)
                        self.keyboard_bin_tab = np.delete(self.keyboard_bin_tab, idxs, None)
                        self.mask = np.array([0,0,0,0,1,1,0,0])
                        self.keyboard_bin_tab = np.insert(self.keyboard_bin_tab, [idxs[0][0] for i in range(len(idxs))], self.mask)
                        self.last_gesture = "down"
        except Exception as e:
            print("Cut by 1/8 doesn't work:", e)

    def cutBy1(self, screen):
        x, y, w, h = self.centerCoo(screen, 100, 100)
        try:
            if self.Finger:
                if (x - 100 < self.Finger[1] < x + w + 100) and (y - 100 < self.Finger[2] < y + h + 100):
                    self.last_gesture = None
                    return
                elif self.last_gesture == None:
                    if self.Finger[1] < x - 100:
                        idxs = np.where(self.keyboard_bin_tab == 1)
                        self.setResult(self.keys[idxs[0][0]])
                    elif self.Finger[1] > x + w + 100:
                        idxs = np.where(self.keyboard_bin_tab == 1)
                        self.setResult(self.keys[idxs[0][1]])
                    self.keyboard.set_keys(self.keys)
                    self.restart = True
                    self.last_gesture = "left" if self.Finger[1] < x - 100 else "right"
        except Exception as e:
            print("Final cut by 1/2 doesn't work:", e)
    
    def drawRec(self, screen, color, x, y, w, h):
        cv2.line(screen, (x - 100, y), (x - 100, y + h), (0, 255, 0), 2)
        cv2.line(screen, (x + w + 100, y), (x + w + 100, y + h), (0, 255, 0), 2)
        cv2.line(screen, (x, y - 100), (x + w, y - 100), (0, 255, 0), 2)
        cv2.line(screen, (x, y + h + 100), (x + w, y + h + 100), (0, 255, 0), 2)
        return screen