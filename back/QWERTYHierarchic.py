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
        if self.x1 <= x <= self.x2 and self.y1 <= y <= self.y2:
            return True
        else:
            return False

    def getLetter(self):
        return self.letter

class QWERTYHierarchic:
    def __init__(self, methode="palec",margin=20):
        self.deadZone = None
        self.spacebar_y = None
        self.spacebar_x = None
        self.x1 = None
        self.innerMargin = None
        self.fontScale = None
        self.tileSize = None
        self.Y = []
        self.X = []
        self.lmList = []
        self.alphabet = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                         ["A", "S", "D", "F", "G", "H", "J", "K", "L", "!"],
                         ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "?"]]
        self.keys_list = [
            ["Q", "W", "E", "R", "T", "A", "S", "D", "F", "G", "Z", "X", "C", "V", "B"],
            ["Y", "U", "I", "O", "P", "H", "J", "K", "L", "!", "N", "M", ",", ".", "?"],
            ["spacebar", "backspace"]
        ]
        self.keyboard_bin_tab = np.ones(32)
        self.tiles = []
        self.sentence = ""
        self.img = None
        self.methode = methode
        self.old_w=0
        self.typable = True
        self.margin=None
        self.gesture = False
        self.last_gesture_time = time.time()
        self.gesturePause = 0.5
        self.firstChoice = False
        self.secondChoice = False
        self.thirdChoice = False
        self.firstChoiceNum = None
        self.secondChoiceNum = None     
        self.detector = htm.handDetector()
        self.lm_index = [8, 4]

    def updateSizes(self,w):
        self.margin=int(w/100)
        self.tileSize = int(w / (len(self.alphabet[0])) - self.margin * 4)
        self.fontScale = int(self.tileSize / 20)
        self.innerMargin = int(self.tileSize / 20 - self.margin / 5)
        self.x1 = self.margin * len(self.alphabet[0]) + self.tileSize * len(self.alphabet[0])
        self.spacebar_x = self.margin * (len(self.alphabet[0]) - 2) + self.tileSize * (len(self.alphabet[0]) - 3)
        self.spacebar_y = self.margin * (len(self.alphabet) + 1) + self.tileSize * len(self.alphabet)
        self.deadZone=int(self.tileSize/2)

    def fillTiles(self,w,h):
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
    
    def findGesture(self, iteration):
        current_time_gesture = time.time()
        if current_time_gesture - self.last_gesture_time < self.gesturePause:
            return
        if np.sqrt((self.lmList[8][1] - self.lmList[4][1]) ** 2 + (
                     self.lmList[8][2] - self.lmList[4][2]) ** 2) < self.deadZone:
                self.gesture = True
                #print(iteration)
                if self.firstChoice == False:
                    self.firstChoice = True
                    self.firstChoiceNum = iteration
                elif self.secondChoice == False:
                    self.secondChoice = True
                    self.secondChoiceNum = iteration
                elif self.thirdChoice == False:
                    self.thirdChoice = True
                self.last_gesture_time = current_time_gesture

    def update(self, img, keyboard):
        self.img = img
        global key_to_highlight
        keys_to_highlight = []
        h,w, d = img.shape
        if self.old_w != w:
            self.old_w = w
            self.tiles=[]
            self.updateSizes(w)
            self.fillTiles(w,h)

        self.img = self.detector.findHands(self.img, False)
        self.lmList = self.detector.findPosition(self.img, 0, False) 
        current_time = int(time.time()) % 3 
        iteration = current_time + 1

        if self.firstChoice == False:
            keys_to_highlight = self.keys_list[(iteration - 1) % len(self.keys_list)]
            #print("Keys to highlight:", keys_to_highlight)
            self.updateKeyboardBinTab(keys_to_highlight)
            #print("Updated Keyboard Bin Tab:", self.keyboard_bin_tab)
        if  self.firstChoice == True and self.secondChoice == False:
            #print("dziala")
            key_mapping = {
                (1, 1): ["Q", "W", "E", "R", "T"],
                (1, 2): ["A", "S", "D", "F", "G"],
                (1, 3): ["Z", "X", "C", "V", "B"],
                (2, 1): ["Y", "U", "I", "O", "P"],
                (2, 2): ["H", "J", "K", "L", "!"],
                (2, 3): ["N", "M", ",", ".", "?"],
                (3, 1): ["spacebar"],
                (3, 2): ["backspace"],
            }
            if self.firstChoiceNum == 3:
                current_time = int(time.time()) % 2
                iteration = current_time + 1
                if iteration % 2 == 1:
                    key_to_highlight = "spacebar"
                else:
                    key_to_highlight = "backspace"
                self.updateKeyboardBinTab([key_to_highlight])                    
            else:
                keys_to_highlight = key_mapping.get((self.firstChoiceNum, iteration), [])              
                self.updateKeyboardBinTab(keys_to_highlight)
                    
        elif self.firstChoice == True and self.secondChoice == True and self.thirdChoice == False:
            #print("dziala2")
            current_time = int(time.time()) % 5
            iteration = current_time
            key_mapping = {
                (1, 1): ["Q", "W", "E", "R", "T"],
                (1, 2): ["A", "S", "D", "F", "G"],
                (1, 3): ["Z", "X", "C", "V", "B"],
                (2, 1): ["Y", "U", "I", "O", "P"],
                (2, 2): ["H", "J", "K", "L", "!"],
                (2, 3): ["N", "M", ",", ".", "?"],
            }
            
            keys_to_highlight = key_mapping.get((self.firstChoiceNum, self.secondChoiceNum), [])
            if keys_to_highlight and iteration in range(len(keys_to_highlight)):
                key_to_highlight = keys_to_highlight[iteration]
                #print("Key to highlight:", key_to_highlight)
                self.updateKeyboardBinTab(key_to_highlight)

        if self.firstChoiceNum == 3 and self.secondChoice == True:
            #print(key_to_highlight)
            if key_to_highlight == "spacebar":
                self.sentence += " "
            elif key_to_highlight == "backspace":
                self.sentence = self.sentence[0:-1]
            self.firstChoice = False
            self.secondChoice = False
            self.thirdChoice = False
            key_to_highlight = None

        if self.thirdChoice == True:
            #print(key_to_highlight)
            self.sentence += key_to_highlight
            self.firstChoice=False
            self.secondChoice=False
            self.thirdChoice=False   
            key_to_highlight=None

        if (len(self.lmList) > 0):                 
            self.findGesture(iteration)            
            cv2.circle(self.img, (self.lmList[8][1], self.lmList[8][2]), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(self.img, (self.lmList[4][1], self.lmList[4][2]), 7, (0, 255, 0), cv2.FILLED)

        for i, tile in enumerate(self.tiles):
            if self.keyboard_bin_tab[i] == 1:
                cv2.rectangle(self.img, (tile.x1, tile.y1), (tile.x2, tile.y2), (0, 0, 255), cv2.FILLED)

        self.img = keyboard.generateKeyboard(img)
        return self.img, list(self.sentence)