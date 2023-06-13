import cv2
import numpy as np
import Modules.FaceMeshModule as mtm
import Modules.HandTrackingModule as htm


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


class QWERTY:
    def __init__(self, methode, img_size, margin=20):
        self.Y = []
        self.X = []
        self.lmList = []
        self.alphabet = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                         ["A", "S", "D", "F", "G", "H", "J", "K", "L", "!"],
                         ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "?"]]
        self.tiles = []
        self.sentance = ""
        self.img = None
        self.methode = methode
        self.img_size = img_size
        self.margin = margin
        self.tileSize = int(self.img_size[0] / (len(self.alphabet[0])) - self.margin * 4)
        self.fontScale = int(self.tileSize / 20)
        self.innerMargin = int(self.tileSize / 20 - self.margin / 5)
        self.deadZone=int(self.tileSize/2)
        self.x1 = self.margin * len(self.alphabet[0]) + self.tileSize * len(self.alphabet[0])
        self.spacebar_x = self.margin * (len(self.alphabet[0]) - 2) + self.tileSize * (len(self.alphabet[0]) - 3)
        self.spacebar_y = self.margin * (len(self.alphabet) + 1) + self.tileSize * len(self.alphabet)
        self.typable=True
        self.fillTiles()

        if methode == "palec":
            self.detector = htm.handDetector()
            self.lm_index = [8, 4]
        else:
            self.detector = mtm.FaceMeshDetector()
            self.lm_index = 2

    def fillTiles(self):
        SP_x = self.img_size[0] / 2 - 5 * self.tileSize - (len(self.alphabet[0]) + 0.5) * self.margin
        SP_y = self.img_size[1] / 2 - 2 * self.tileSize - (len(self.alphabet) + 1) * self.margin
        for i in range(0, len(self.alphabet)):
            for j in range(0, len(self.alphabet[0])):
                x = int(self.margin * (j + 1) + self.tileSize * j + SP_x)
                y = int(self.margin * (i + 1) + self.tileSize * i + SP_y)
                self.tiles.append(
                    tilesData(x1=x, x2=x + self.tileSize, y1=y, y2=y + self.tileSize, letter=self.alphabet[i][j]))

        self.tiles.append(tilesData(x1=int(self.margin + SP_x), x2=int(self.spacebar_x + SP_x - self.margin),
                                    y1=int(self.spacebar_y + SP_y), y2=int(self.spacebar_y + SP_y+self.tileSize), letter="spacebar"))
        self.tiles.append(
            tilesData(x1=int(self.spacebar_x + SP_x), x2=int(self.x1 + SP_x), y1=int(self.spacebar_y + SP_y),
                      y2=int(self.spacebar_y + self.tileSize + SP_y), letter="backspace"))
        
        # for i in range(0,len(self.tiles)): print(self.tiles[i].letter, self.tiles[i].x1,self.tiles[i].x2,self.tiles[i].y1,self.tiles[i].y2)

    def getText(self):
        return self.sentance

    def update(self, img, keyboard):
        self.img = img

        if self.methode == "palec":
            self.img = self.detector.findHands(self.img, False)
        else:
            self.img, faces = self.detector.findFaceMesh(self.img, False)

        self.lmList = self.detector.findPosition(self.img, 0, False)

        if (len(self.lmList) > 0):
            if self.typable == True:
                if np.sqrt((self.lmList[8][1] - self.lmList[4][1]) ** 2 + (self.lmList[8][2] - self.lmList[4][2]) ** 2) < self.deadZone:
                    for i in range(0, int(len(self.tiles))):
                        if self.tiles[i].compare(self.lmList[8][1], self.lmList[8][2]):
                            if(self.tiles[i].letter=="spacebar"): self.sentance= self.sentance+" "
                            elif (self.tiles[i].letter=="backspace"): 
                                self.sentance=self.sentance[0:-1]
                                print("też jej")
                            else: self.sentance += self.tiles[i].getLetter()
                    self.typable=False
            elif self.typable==False:
                if np.sqrt((self.lmList[8][1] - self.lmList[4][1]) ** 2 + (self.lmList[8][2] - self.lmList[4][2]) ** 2) > self.deadZone+self.margin:
                    self.typable=True

            # print(self.lmList[8][1],self.lmList[8][2],np.sqrt((self.lmList[8][1] - self.lmList[4][1]) ** 2 + (self.lmList[8][2] - self.lmList[4][2]) ** 2))
            cv2.circle(self.img, (self.lmList[8][1], self.lmList[8][2]), 7, (255, 0, 0), cv2.FILLED)
            cv2.circle(self.img, (self.lmList[4][1], self.lmList[4][2]), 7, (0, 255, 0), cv2.FILLED)
            
        self.img=keyboard.generateKeyboard(img)
        return self.img, list(self.sentance)
