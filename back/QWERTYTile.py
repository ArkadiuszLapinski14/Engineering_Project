import string
import time
import cv2
import numpy as np
import back.modules.FaceMeshModule as mtm
import back.modules.HandTrackingModule as htm

class tilesData:
    def __init__(self, x1, x2, y1, y2, letter):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2
        self.letter = letter

    def compare(self, x, y):
        return self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2

    def getLetter(self):
        return self.letter

class QWERTYTile:
    def __init__(self, methode="palec", margin=20):
        self.deadZone = None
        self.spacebar_y = None
        self.spacebar_x = None
        self.x1 = None
        self.innerMargin = None
        self.fontScale = None
        self.tileSize = None
        self.Y = []
        self.X = []

        self.alphabet = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                         ["A", "S", "D", "F", "G", "H", "J", "K", "L", "!"],
                         ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "?"]]
        
        self.keys_list = ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P",
                         "A", "S", "D", "F", "G", "H", "J", "K", "L", "!",
                         "Z", "X", "C", "V", "B", "N", "M", ",", ".", "?",
                         "spacebar", "backspace"]
        self.keyboard_bin_tab = np.zeros(32)
        self.tiles = []
        self.sentence = []
        self.img = None
        self.methode = methode
        self.old_w = 0
        self.margin = None
        self.start = True
        self.last_gesture_time = time.time()
        self.last_gesure = None
        self.gesturePause = 1.5
        self.gesturePauseConfirm = 0.5
        self.lms = None
        self.prevFinger = []
        self.point = 8
        self.detector = htm.handDetector()        
        self.key_to_highlight = None
        self.Finger = None

    def updateSizes(self, w):
        self.margin = int(w / 100)
        self.tileSize = int(w / (len(self.alphabet[0])) - self.margin * 4)
        self.fontScale = int(self.tileSize / 20)
        self.innerMargin = int(self.tileSize / 20 - self.margin / 5)
        self.x1 = self.margin * len(self.alphabet[0]) + self.tileSize * len(self.alphabet[0])
        self.spacebar_x = self.margin * (len(self.alphabet[0]) - 2) + self.tileSize * (len(self.alphabet[0]) - 3)
        self.spacebar_y = self.margin * (len(self.alphabet) + 1) + self.tileSize * len(self.alphabet)
        self.deadZone = int(self.tileSize / 2)

    def fillTiles(self, w, h):
        SP_x = w / 2 - 5 * self.tileSize - (len(self.alphabet[0]) + 0.5) * self.margin
        SP_y = h / 2 - 2 * self.tileSize - (len(self.alphabet) + 1) * self.margin
        for i in range(0, len(self.alphabet)):
            for j in range(0, len(self.alphabet[0])):
                x = int(self.margin * (j + 1) + self.tileSize * j + SP_x)
                y = int(self.margin * (i + 1) + self.tileSize * i + SP_y)
                self.tiles.append(
                    tilesData(x1=x, x2=x + self.tileSize, y1=y, y2=y + self.tileSize, letter=self.alphabet[i][j]))

        self.tiles.append(tilesData(x1=int(self.margin + SP_x), x2=int(self.spacebar_x + SP_x - self.margin),
                                    y1=int(self.spacebar_y + SP_y), y2=int(self.spacebar_y + SP_y + self.tileSize),
                                    letter="spacebar"))
        self.tiles.append(
            tilesData(x1=int(self.spacebar_x + SP_x), x2=int(self.x1 + SP_x), y1=int(self.spacebar_y + SP_y),
                      y2=int(self.spacebar_y + self.tileSize + SP_y), letter="backspace"))

    def updateKeyboardBinTab(self, keys_to_highlight):
        for i, tile in enumerate(self.tiles):
            if tile.getLetter() in keys_to_highlight:
                self.keyboard_bin_tab[i] = 1  # Highlight key
            else:
                self.keyboard_bin_tab[i] = 0

    def highlightPreviousKey(self):
        current_index = np.argmax(self.keyboard_bin_tab)
        if current_index > 0:
            new_index = current_index - 1
            self.key_to_highlight = self.tiles[new_index]
            self.keyboard_bin_tab[current_index] = 0
            self.keyboard_bin_tab[new_index] = 1

    def highlightNextKey(self):
        current_index = np.argmax(self.keyboard_bin_tab)
        if current_index < len(self.keyboard_bin_tab) - 1:
            new_index = current_index + 1
            self.key_to_highlight = self.tiles[new_index]
            self.keyboard_bin_tab[current_index] = 0
            self.keyboard_bin_tab[new_index] = 1

    def highlightKeyAbove(self):
        current_index = np.argmax(self.keyboard_bin_tab)
        if current_index >= 30:
            if current_index == 30:
                self.keyboard_bin_tab[23] = 1
                self.keyboard_bin_tab[current_index] = 0
            elif current_index == 31:
                self.keyboard_bin_tab[28] = 1
                self.keyboard_bin_tab[current_index] = 0
        elif current_index - 10 >= 0:
            new_index = current_index - 10
            self.key_to_highlight = self.tiles[new_index]            
            self.keyboard_bin_tab[new_index] = 1        
            self.keyboard_bin_tab[current_index] = 0
        
    def highlightKeyBelow(self):
        current_index = np.argmax(self.keyboard_bin_tab)
        if current_index + 10 < len(self.keyboard_bin_tab):
            new_index = current_index + 10
            self.key_to_highlight = self.tiles[new_index]
            self.keyboard_bin_tab[current_index] = 0
            self.keyboard_bin_tab[new_index] = 1
        elif 20 <= current_index <= 26:
            self.keyboard_bin_tab[30] = 1
            self.keyboard_bin_tab[current_index] = 0
        elif 27 <= current_index <= 29:
            self.keyboard_bin_tab[31] = 1
            self.keyboard_bin_tab[current_index] = 0

    def setResult(self, key):
        if key == "backspace":
            if len(self.sentence) > 0:
                del self.sentence[-1]
        elif key == "spacebar":
            self.sentence.append(" ")
        else:
            self.sentence.append(key)

    def findGesture(self, screen):
        current_time_gesture = time.time()
        
        if np.sqrt((self.lms[8][1] - self.lms[4][1]) ** 2 + (self.lms[8][2] - self.lms[4][2]) ** 2) < self.deadZone:
            if current_time_gesture - self.last_gesture_time < self.gesturePauseConfirm:
                return
            self.start = False
            index_of_highlighted_key = np.argmax(self.keyboard_bin_tab)
            if self.keyboard_bin_tab[index_of_highlighted_key] == 1:
                self.setResult(self.keys_list[index_of_highlighted_key])
            self.last_gesture_time = current_time_gesture
        else:
            if current_time_gesture - self.last_gesture_time < self.gesturePause:
                return
            else:
                x, y, w, h = self.centerCoo(screen, 100, 100)
                if (x - 100 < self.Finger[1] < x + w + 100) and (y - 100 < self.Finger[2] < y + h + 100):
                    self.last_gesure = None
                    return
                elif self.last_gesure == None:
                    # left
                    if self.Finger[1] < x - 100:
                        self.start = False
                        #print("left")
                        self.highlightPreviousKey()
                        self.last_gesure = "left"
                    # right
                    elif self.Finger[1] > x + w + 100:
                        self.start = False
                        #print("right")
                        self.highlightNextKey()
                        self.last_gesure = "right"
                    # up
                    elif self.Finger[2] < y - 100:
                        self.start = False
                        #print("up")
                        self.highlightKeyAbove()
                        self.last_gesure = "up"
                    # down
                    elif self.Finger[2] > y + h + 100:
                        self.start = False
                        #print("down")
                        self.highlightKeyBelow()
                        self.last_gesure = "down"
                    self.last_gesture_time = current_time_gesture

    def centerCoo(self, screen, w, h):
        y, x, c = screen.shape
        w, h = 100, 100
        y, x = int((y - h) / 2), int((x - w) / 2)
        return x, y, w, h

    def FingerUpdate(self):
        if self.lms:
            self.Finger = self.lms[self.point]

    def drawRec(self, screen, color, x, y, w, h):
        cv2.line(screen, (x - 100, y), (x - 100, y + h), (0, 255, 0), 2)
        cv2.line(screen, (x + w + 100, y), (x + w + 100, y + h), (0, 255, 0), 2)
        cv2.line(screen, (x, y - 100), (x + w, y - 100), (0, 255, 0), 2)
        cv2.line(screen, (x, y + h + 100), (x + w, y + h + 100), (0, 255, 0), 2)
        return screen

    def update(self, screen, keyboard):
        h, w, d = screen.shape
        if self.old_w != w:
            self.old_w = w
            self.tiles = []
            self.updateSizes(w)
            self.fillTiles(w, h)

        x, y, w, h = self.centerCoo(screen , 100, 100)
        screen = self.detector.findHands(screen, False)
        self.lms = self.detector.findPosition(screen, 0, False)
        for i, tile in enumerate(self.tiles):
            if self.keyboard_bin_tab[i] == 1:
                cv2.rectangle(screen, (tile.x1, tile.y1), (tile.x2, tile.y2), (0, 0, 255), cv2.FILLED)
        screen = keyboard.generateKeyboard(screen)
        screen = self.drawRec(screen, (0,255,0), x, y, w, h)
        self.FingerUpdate()
        if self.start == True:
            self.keyboard_bin_tab[14] = 1 #highlight letter "G" at the start
        if (len(self.lms) > 0):                 
            self.findGesture(screen)            
            cv2.circle(screen, (self.lms[8][1], self.lms[8][2]), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(screen, (self.lms[4][1], self.lms[4][2]), 7, (0, 255, 0), cv2.FILLED)
         
        #print(self.keyboard_bin_tab)
        return screen, list(self.sentence)