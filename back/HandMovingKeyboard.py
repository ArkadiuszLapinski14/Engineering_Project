import cv2
import string
from back.modules import HandTrackingModule as htm

class HandMovingKeyboard:
    def __init__(self, point=8):
        self.Finger = None
        self.detector = htm.handDetector(maxHands=1)
        self.KEYS = list(string.ascii_uppercase + "!" + '?' + ',' + '.' + '<' + "_")
        self.res = []
        self.point = point
        self.restart = False
        self.last_gesture = None

    def update(self, screen, keyboard):
        self.keyboard = keyboard
        self.keys = self.keyboard.get_keys()
        screen = self.detector.findHands(screen, draw=False)
        lms = self.detector.findPosition(screen, draw=False)
        
        x, y, w, h = self.centerCoo(screen, 100, 100)
        try:
            screen = self.keyboard.generateKeyboard(screen, 10, 100, 30, 30)
            screen = self.drawRec(screen, (0, 255, 0), x, y, w, h)
            screen = self.backToDefault(screen)
            if len(self.keys) > 0:
                self.FingerUpdate(lms)            
            if self.restart == False:
                if len(self.keys) != 2:
                    self.cutBy4(screen)
                elif len(self.keys) == 2:
                    self.cutBy2(screen)
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
        if res == "<":
            if len(self.res) > 0:
                del self.res[-1]
        elif res == "_":
            self.res.append(" ")
        else:
            self.res.append(res)
        self.keys = self.KEYS
        self.keyboard.set_keys(self.KEYS)

    def FingerUpdate(self, lms):
        if (lms):
            self.Finger = lms[self.point]
            if len(self.keys) == 1:
                self.setResult(self.keys[0])

    def backToDefault(self, screen):
        '''Back to the startin settings of keyboard after clicking button "Back"'''
        screen, x, y = self.drawBackButton(screen)
        if (self.Finger):
            if (self.Finger[1] < x and self.Finger[1] > (x - 75)) and (self.Finger[2] > y and self.Finger[2] < (y + 23)):
                self.keys = self.KEYS
                self.keyboard.set_keys(self.KEYS)
        return screen
    
    def drawBackButton(self, screen):
        '''Draws button "Back"'''
        y, x , c = screen.shape
        x = int(x - 10)
        y = 10
        screen = cv2.rectangle(screen, (x, y), (x - 75, y + 23), (0, 0, 0), 3)
        screen = cv2.rectangle(screen, (x, y), (x - 75, y + 23), (192,192,192), -1)
        cv2.putText(screen, "Back", (x-75, y+23), cv2.FONT_HERSHEY_PLAIN, 2 ,(255,255,255), 2)
        return screen, x, y
    
    def centerCoo(self, screen, w, h):
        y, x, c = screen.shape
        w, h = 100, 100
        y, x = int((y-h)/2), int((x-w)/2)
        return x, y, w, h
    
    def drawResult(self, screen, x, y):
        screen, x, y = self.drawResultBox(screen)
        for el in self.res:
            cv2.putText(screen, el, (x, y), cv2.FONT_HERSHEY_PLAIN, 3 ,(255,255,255), 2)
            x += 30
        return screen
    
    def drawResultBox(self, screen):
        y, x, c = screen.shape
        x = int((x - 400)/2)
        y = int((y - 200))
        screen = cv2.rectangle(screen, (x, y), (x + 400, y + 40), (255,255,255), 2)
        return screen, x, y + 37
    
    def cutBy4(self, screen):
        x, y, w, h = self.centerCoo(screen, 100, 100)
        try:
            if self.Finger:
                if (x - 100 < self.Finger[1] < x + w + 100) and (y - 100 < self.Finger[2] < y + h + 100):
                    self.last_gesture = None
                    return
                elif self.last_gesture == None:
                    if self.Finger[1] < x - 100:
                        self.keys = self.keys[0:int(len(self.keys) / 4)]
                        self.keyboard.set_keys(self.keys)
                        self.last_gesture = "left"
                    elif self.Finger[1] > x + w + 100:
                        self.keys = self.keys[int(len(self.keys) * (3 / 4)):len(self.keys)]
                        self.keyboard.set_keys(self.keys)
                        self.last_gesture = "right"
                    elif self.Finger[2] > y + h + 100:
                        self.keys = self.keys[int(len(self.keys) * (1 / 4)):int(len(self.keys) * (2 / 4))]
                        self.keyboard.set_keys(self.keys)
                        self.last_gesture = "up"
                    elif self.Finger[2] < y - 100:
                        self.keys = self.keys[int(len(self.keys) * (2 / 4)):int(len(self.keys) * (3 / 4))]
                        self.keyboard.set_keys(self.keys)
                        self.last_gesture = "down"
        except:
            print("Cut by 3/4 doesnt work/Fingers lists out of range") 

    def cutBy2(self, screen):
        x, y, w, h = self.centerCoo(screen, 100, 100)
        try:
            if self.Finger:
                if (x - 100 < self.Finger[1] < x + w + 100) and (y - 100 < self.Finger[2] < y + h + 100):
                    self.last_gesture = None
                    return
                elif self.last_gesture == None:
                    if self.Finger[1] < x - 100:
                        self.keys = self.keys[:1]
                    elif self.Finger[1] > x + w + 100:
                        self.keys = self.keys[1:]
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
