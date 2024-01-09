import cv2
import time
import string
import back.modules.HandTrackingModule as htm

class Hover:
    def __init__(self, point=8):
        self.Finger = None
        self.prevFinger = []
        self.detector = htm.handDetector(maxHands=1)
        self.res = []
        self.KEYS = list(string.ascii_uppercase + "!" + '?'+','+'.'+'<'+"_")
        self.point = point
        self.typing_delay = 0.8
        self.prev_time = 0

    def get_result(self):
        return self.res

    def update(self, screen, keyboard):
        self.keyboard = keyboard
        self.keys = self.keyboard.get_keys()
        screen = self.detector.findHands(screen, draw=False)
        lms = self.detector.findPosition(screen, draw=False)

        try:
            screen = self.keyboard.generateKeyboardHover(screen, 10, 100, 30, 30)
            self.FingerUpdate(lms)
            screen = self.backToDefault(screen)
            screen = self.keyboard.highlight(screen, self.keys, 10, 100, 30, 30)

            if lms:
                finger_pos = (lms[8][1], lms[8][2])
                key = self.keyboard.get_key_at_position(finger_pos)
                if key:
                    screen = self.keyboard.highlight(
                        screen, [1 if k == key else 0 for k in self.keyboard.get_keys()], 50, 400, 30, 40
                    )
                    curr_time = time.time()
                    if curr_time - self.prev_time > self.typing_delay:
                        if key == "<":
                            self.setResult("<")
                        elif key == "_":
                            self.setResult(" ")
                        else:
                            self.setResult(key)
                        self.prev_time = curr_time
        except Exception as e:
            print("Hover algorithm doesn't work/lms out of range:", e)

        screen = self.drawResult(screen, 600, 600)  # Assign the updated screen to the variable

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

    def backToDefault(self, screen):
        '''Back to the startin settings of keyboard after clicking button "Back"'''
        screen, x, y = self.drawBackButton(screen)
        if (self.Finger):
            if (self.Finger[1] < x and self.Finger[1] > (x - 75)) and (self.Finger[2] > y and self.Finger[2] < (y + 23)):
                self.res=[]
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