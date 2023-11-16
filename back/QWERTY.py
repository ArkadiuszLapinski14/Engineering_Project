import cv2
import string
import numpy as np
import back.modules.FaceMeshModule as mtm
import back.modules.HandTrackingModule as htm
import time

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
        self.tiles = []
        self.sentance = ""
        self.img = None
        self.methode = methode
        self.old_w=0
        self.typable = True
        self.margin=None
        self.keyboard_bin_tab = np.ones(32)
        self.mask = np.ones(32)
        self.choice = 0
        if methode == "palec":
            self.detector = htm.handDetector()
            self.lm_index = [8, 4]
        else:
            self.detector = mtm.FaceMeshDetector()
            self.lm_index = 2

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

        # for i in range(0,len(self.tiles)): print(self.tiles[i].letter, self.tiles[i].x1,self.tiles[i].x2,self.tiles[i].y1,self.tiles[i].y2)

    def getText(self):
        return self.sentance
    
    '''Highlight part of keyboard'''
    def cutBy3(self, iteration):        
        if iteration==1:
            try:
                # Define the indices of the keys to highlight
                keys_to_highlight = ["Q", "W", "E", "R", "T", "A", "S", "D", "F", "G", "Z", "X", "C", "V", "B"]

                # Update the keyboard_bin_tab with the highlighted keys
                for i, tile in enumerate(self.tiles):
                    if tile.getLetter() in keys_to_highlight:
                        self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                    else:
                        self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

            except:
                print("Cut by 3 doesn't work / Keys not found")
        elif iteration==2:
            try:
                # Define the indices of the keys to highlight
                keys_to_highlight = ["Y", "U", "I", "O", "P", "H", "J", "K", "L", "!", "N", "M", ",", ".", "?"]

                # Update the keyboard_bin_tab with the highlighted keys
                for i, tile in enumerate(self.tiles):
                    if tile.getLetter() in keys_to_highlight:
                        self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                    else:
                        self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

            except:
                print("Cut by 3 doesn't work / Keys not found")

        elif iteration==3:
            try:
                # Define the indices of the keys to highlight
                keys_to_highlight = ["spacebar", "backspace"]

                # Update the keyboard_bin_tab with the highlighted keys
                for i, tile in enumerate(self.tiles):
                    if tile.getLetter() in keys_to_highlight:
                        self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                    else:
                        self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

            except:
                print("Cut by 3 doesn't work / Keys not found")
    
    '''Highlights rows from chosen part'''
    def cutBy3Row(self, firstChoice, iteration):        
        if firstChoice==1:
            if iteration==1:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["Q", "W", "E", "R", "T"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 3 rows doesn't work / Keys not found")
            
            elif iteration==2:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["A", "S", "D", "F", "G"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 3 rows doesn't work / Keys not found")

            elif iteration==3:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["Z", "X", "C", "V", "B"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 3 rows doesn't work / Keys not found")
        elif firstChoice==2:
            if iteration==1:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["Y", "U", "I", "O", "P"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 3 rows doesn't work / Keys not found")
            
            elif iteration==2:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["H", "J", "K", "L", "!"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 3 rows doesn't work / Keys not found")

            elif iteration==3:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["N", "M", ",", ".", "?"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 3 rows doesn't work / Keys not found")
        elif firstChoice==3:
            if iteration==1:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["spacebar"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 3 rows doesn't work / Keys not found")
            
            elif iteration==2:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["backspace"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 3 rows doesn't work / Keys not found")

    '''Highlights single letters from chosen row'''
    def cutBy5(self, firstChoice, secondChoice, iteration):
        if firstChoice==1 and secondChoice==1:
            if iteration==1:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["Q"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
            
            elif iteration==2:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["H"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")

            elif iteration==3:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["E"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
                
            elif iteration==4:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["R"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")

            elif iteration==5:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["T"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
        if firstChoice==1 and secondChoice==2:
            if iteration==1:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["A"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
            
            elif iteration==2:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["S"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")

            elif iteration==3:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["D"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
                
            elif iteration==4:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["F"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")

            elif iteration==5:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["G"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
        if firstChoice==1 and secondChoice==3:
            if iteration==1:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["Z"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
            
            elif iteration==2:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["X"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")

            elif iteration==3:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["C"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
                
            elif iteration==4:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["V"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")

            elif iteration==5:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["B"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
        if firstChoice==2 and secondChoice==1:
            if iteration==1:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["Y"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
            
            elif iteration==2:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["U"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")

            elif iteration==3:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["I"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
                
            elif iteration==4:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["O"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")

            elif iteration==5:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["P"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
        if firstChoice==2 and secondChoice==2:
            if iteration==1:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["H"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
            
            elif iteration==2:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["J"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")

            elif iteration==3:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["K"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
                
            elif iteration==4:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["L"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")

            elif iteration==5:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["!"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
        if firstChoice==2 and secondChoice==3:
            if iteration==1:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["N"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
            
            elif iteration==2:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["M"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")

            elif iteration==3:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = [","]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
                
            elif iteration==4:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["."]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")

            elif iteration==5:
                try:
                    # Define the indices of the keys to highlight
                    keys_to_highlight = ["?"]

                    # Update the keyboard_bin_tab with the highlighted keys
                    for i, tile in enumerate(self.tiles):
                        if tile.getLetter() in keys_to_highlight:
                            self.keyboard_bin_tab[i] = 1  # Set the key as highlighted (active)
                        else:
                            self.keyboard_bin_tab[i] = 0  # Set other keys as not highlighted (inactive)

                except:
                    print("Cut by 5 doesn't work / Keys not found")
        
    def update(self, img, keyboard):
        self.img = img
        h, w, d = img.shape
        if self.old_w != w:
            self.old_w = w
            self.tiles = []
            self.updateSizes(w)
            self.fillTiles(w, h)

        if self.methode == "palec":
            self.img = self.detector.findHands(self.img, False)
        else:
            self.img, faces = self.detector.findFaceMesh(self.img, False)

        self.lmList = self.detector.findPosition(self.img, 0, False)
        
        # Toggle between iterations of cutBy3
        current_time = int(time.time()) % 12
        current_time2 = int(time.time()) % 20
        if self.firstChoice == 0:  # Duza czesc
            iteration = (current_time // 4) + 1
            self.cutBy3(iteration)

        elif self.firstChoice != 0 and self.secondChoice == 0:  # Wiersze w duzej czesci
            iteration = (current_time // 4) + 1
            self.cutBy3Row(self.firstChoice, iteration)

        elif self.firstChoice != 0 and self.secondChoice != 0:  # Pojedyncze znaki
            iteration = (current_time2 // 4) + 1
            self.cutBy5(self.firstChoice, self.secondChoice, iteration)

        # Change the color of the highlighted keys
        for i, tile in enumerate(self.tiles):
            if self.keyboard_bin_tab[i] == 1:
                cv2.rectangle(self.img, (tile.x1, tile.y1), (tile.x2, tile.y2), (0, 0, 255), cv2.FILLED)

        self.img = keyboard.generateKeyboard(img)
        return self.img, list(self.sentance)
