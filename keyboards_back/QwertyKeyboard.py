import cv2
import numpy as np


class QwertyKeyboard:
    def __init__(self, margin=20):
        self.alphabet = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
                         ["A", "S", "D", "F", "G", "H", "J", "K", "L", "!"],
                         ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "?"]]
        self.margin = None
        self.alpha = 0.5
        self.overlay = None
        self.img = None
        self.overlay = None
        self.spacebar_y = None
        self.spacebar_x = None
        self.x1 = None
        self.tileSize = None
        self.fontScale = None
        self.innerMargin = None
        self.old_w = None

    def updateSizes(self, w):
        self.margin=int(w/100)
        self.tileSize = int(w / (len(self.alphabet[0])) - self.margin * 4)
        self.fontScale = int(self.tileSize / 20)
        self.innerMargin = int(self.tileSize / 20 - self.margin / 5)
        self.x1 = self.margin * len(self.alphabet[0]) + self.tileSize * len(self.alphabet[0])
        self.spacebar_x = self.margin * (len(self.alphabet[0]) - 2) + self.tileSize * (len(self.alphabet[0]) - 3)
        self.spacebar_y = self.margin * (len(self.alphabet) + 1) + self.tileSize * len(self.alphabet)

    def generateKeyboard(self, img):
        self.img = img
        h, w, d = img.shape
        if self.old_w != w:
            self.old_w = w
            self.updateSizes(w)
        self.overlay = self.img.copy()
        SP_x = w / 2 - 5 * self.tileSize - (len(self.alphabet[0]) + 0.5) * self.margin
        SP_y = h / 2 - 2 * self.tileSize - (len(self.alphabet) + 1) * self.margin
        for i in range(0, len(self.alphabet)):
            for j in range(0, len(self.alphabet[0])):
                x = int(self.margin * (j + 1) + self.tileSize * j + SP_x)
                y = int(self.margin * (i + 1) + self.tileSize * i + SP_y)
                cv2.rectangle(self.img, (x, y), (x + self.tileSize, y + self.tileSize), (150, 0, 0), 3)
                cv2.rectangle(self.overlay, (x, y), (x + self.tileSize, y + self.tileSize), (50, 0, 0), -1)
                cv2.putText(self.img, self.alphabet[i][j], (x + self.innerMargin, y + self.tileSize - self.innerMargin),
                            cv2.FONT_HERSHEY_PLAIN, self.fontScale, (255, 0, 0), 3)

        # space
        cv2.rectangle(self.img, (int(self.margin + SP_x), int(self.spacebar_y + SP_y)),
                      (int(self.spacebar_x + SP_x - self.margin), int(self.spacebar_y + SP_y)), (150, 0, 0), 3)
        cv2.rectangle(self.overlay, (int(self.margin + SP_x), int(self.spacebar_y + SP_y)),
                      (int(self.spacebar_x + SP_x - self.margin), int(self.spacebar_y + self.tileSize + SP_y)),
                      (150, 0, 0), -1)
        cv2.putText(self.img, "Space", (
        int(x / 2 - self.tileSize * 2.5), int(self.spacebar_y + self.tileSize - self.margin - self.innerMargin + SP_y)),
                    cv2.FONT_HERSHEY_PLAIN, self.fontScale, (255, 0, 0), 3)

        # backspace
        cv2.rectangle(self.img, (int(self.spacebar_x + SP_x), int(self.spacebar_y + SP_y)),
                      (int(self.x1 + SP_x), int(self.spacebar_y + self.tileSize + SP_y)), (150, 0, 0), 3)
        cv2.rectangle(self.overlay, (int(self.spacebar_x + SP_x), int(self.spacebar_y + SP_y)),
                      (int(self.x1 + SP_x), int(self.spacebar_y + self.tileSize + SP_y)), (150, 0, 0), -1)
        cv2.putText(self.img, "<-", (int((x + self.x1) / 2 - self.tileSize * 3.5 + SP_x),
                                     int(self.spacebar_y + self.tileSize - self.margin - self.innerMargin + SP_y)),
                    cv2.FONT_HERSHEY_PLAIN, self.fontScale, (255, 0, 0), 3)

        self.img = cv2.addWeighted(self.overlay, self.alpha, self.img, 1 - self.alpha, 0)

        return self.img
