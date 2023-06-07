import cv2
from Modules.HandTrackingModule import handDetector
from keyboards_back.Keyboard import Keyboard

class Hover:
    def __init__(self, point=8):
        self.Finger = None
        self.prevFinger = []
        self.detector = handDetector()
        self.keyboard = Keyboard()
        self.keys = self.keyboard.get_keys()
        self.KEYS = self.keyboard.get_keys()
        self.res = []
        self.point = point

    def get_result(self):
        return self.res

    def update(self, screen):
        screen = self.detector.findHands(screen, draw=False)
        lms = self.detector.findPosition(screen)

        try:
            self.FingerUpdate(lms)
            x, y, w, h = 10, 100, 30, 30  # Adjust these values as per your requirements
            screen = self.keyboard.draw_update_hover(screen, x, y, w, h)
            screen = self.keyboard.highlight(screen, self.keys, x, y, w, h)
            screen = self.drawResult(screen, 600, 600)
            return screen, self.res
        except Exception as e:
            print("Hover algorithm doesn't work/lms out of range:", e)

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
        self.keys = self.keyboard.get_keys()

    def drawResult(self, screen, x, y):
        screen, x, y = self.drawResultBox(screen)
        for el in self.res:
            cv2.putText(screen, el, (x, y), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)
            x += 30
        return screen

    def drawResultBox(self, screen):
        y, x, c = screen.shape
        x = int((x - 400) / 2)
        y = int((y - 200))
        screen = cv2.rectangle(screen, (x, y), (x + 400, y + 40), (255, 255, 255), 2)
        return screen, x, y + 37

    def FingerUpdate(self, lms):
        if lms and len(lms) > self.point:
            self.Finger = lms[self.point]
            self.updatePrevFingerList()
            if len(self.keys) == 1:
                self.setResult(self.keys[0])

    def updatePrevFingerList(self, capacity=20):
        if len(self.prevFinger) < capacity:
            self.prevFinger.append(self.Finger)
        else:
            self.prevFinger.append(self.Finger)
            del self.prevFinger[0]

    def prevFingerListReset(self):
        self.prevFinger = []
