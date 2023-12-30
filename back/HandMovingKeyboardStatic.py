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
        self.is_calibrated = False
        self.calibration_delay = 0  #zmienna potrzebna do zatrzymania stanu kalibracji na kilka milisekund //optymalizacja
        self.calibration_loading = 0 #zmienna potrzebna do zaladowania kalibracji (podobnie ma to zajmowac kilka milisekund) //optymalizacja
        self.point = point
        self.keyboard_bin_tab = np.ones(32)
        self.mask = np.ones(32)

    def update(self, screen, keyboard):
        '''Updates a keyboard according to our algorithm when calibrated'''
        self.keyboard = keyboard
        self.keys = self.keyboard.get_keys()
        screen = self.detector.findHands(screen, draw = False)
        lms = self.detector.findPosition(screen, draw = False)
        try:
            screen = self.keyboard.generateKeyboard(screen, 10, 100, 30, 30)
            screen = self.keyboard.highlight(screen, self.keyboard_bin_tab, 10, 100, 30, 30)
            self.FingerUpdate(lms)
            screen = self.backToDefault(screen)
            if self.is_calibrated == True:
                screen = self.afterCalibrationDelay(screen, 100, 100)
                if collections.Counter(self.keyboard_bin_tab)[1] == 32:
                    self.cutBy4()
                elif collections.Counter(self.keyboard_bin_tab)[1] == 8: 
                    self.cutBy2()
                elif collections.Counter(self.keyboard_bin_tab)[1] == 2:
                    self.cutBy1()
                screen = self.drawResult(screen, 600, 600)
            else:
                self.calibration_delay = 10 #długość delaya (10 najlepiej dziala)
                screen = self.calibrate(screen)
                screen = self.drawResult(screen, 600, 600)
            return screen, self.res
        except:
            print("Hand Moving Keyboard algorith doesnt work/lms out of range")

        screen = self.drawResult(screen, 600, 600)
        return screen, self.res
    
    def get_result(self):
        return self.res

    def calibrate(self, screen):
        '''Checks if finger is inside the calibration box'''
        x, y, w, h = self.centerCoo(screen, 100, 100)
        try:
            if (self.Finger):
                if (self.Finger[1] > x and self.Finger[1] < x + w) and (self.Finger[2] > y and self.Finger[2] < y + h):
                    screen = self.CalibrationLoading(screen, x, y, w, h)
                else:
                    screen = self.drawRec(screen, (0,0,189), x, y, w, h)
                    self.is_calibrated = False
                    self.calibration_loading = 0
            else:
                screen = self.drawRec(screen, (0,0,189), x, y, w, h)
                self.is_calibrated = False
                self.calibration_loading = 0

        except:
            print("Calibration doesnt work")
        return screen

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
            self.updatePrevFingerList()

    def updatePrevFingerList(self, capacity = 20):
        '''Updates prevFinger[], capacity - length of list'''
        if len(self.prevFinger) < capacity:
            self.prevFinger.append(self.Finger)
        else:
            self.prevFinger.append(self.Finger)
            del self.prevFinger[0]

    def prevFingerListReset(self):
        '''Clear prevFinger []'''
        self.prevFinger = []

    def CalibrationLoading(self, screen, x, y, w, h, iters = 30):
        '''Set a delay before succesfully calibration (ex. 30 iterations)'''
        if self.calibration_loading > iters:
            screen = self.drawRec(screen, (0,255,0), x, y, w, h)
            self.is_calibrated = True
        else:
            screen = self.drawRec(screen, (0,0,189), x, y, w, h)
            self.calibration_loading += 1
            self.is_calibrated = False     
        return screen 

    def afterCalibrationDelay(self, screen, width, height):
        '''Set a small delay after calibration is succesfull to optimize the algorithm'''
        x, y, w, h = self.centerCoo(screen , width, height)
        if self.calibration_delay > 0:
            self.calibration_delay -= 1
            screen = self.drawRec(screen, (0,255,0), x, y, w, h)
        else: 
            self.is_calibrated = False
            screen = self.drawRec(screen, (0,255,0), x, y, w, h)
        return screen

    def cutBy4(self):
        '''Highlight part of keyboard'''
        try:
            tab_len = len(self.keyboard_bin_tab)
            if (self.Finger and self.prevFinger):
                if self.Finger[1] < self.prevFinger[0][1] - 300: #sprawdzanie ostatniego elementu listy (do listy elementy sa dodawane od tylu stad indeks 0)
                    self.mask = np.concatenate((np.ones(int(tab_len / 4)), np.zeros(int((tab_len / 4)*3))), axis=None)
                    self.keyboard_bin_tab *= np.array(self.mask)
                    self.prevFingerListReset() 
                elif self.Finger[1] > self.prevFinger[0][1] + 300:
                    self.mask = np.concatenate((np.zeros(int((tab_len / 4) * 3)), np.ones(int(tab_len/4))), axis = None)
                    self.keyboard_bin_tab *= np.array(self.mask)
                    self.prevFingerListReset()
                elif self.Finger[2] > self.prevFinger[0][2] + 200:
                    self.mask = np.concatenate((np.zeros(int(tab_len/4)), np.ones(int(tab_len/4)), np.zeros(int((tab_len/4) *2))), axis = None)
                    self.keyboard_bin_tab *= np.array(self.mask)
                    self.prevFingerListReset()
                elif self.Finger[2] < self.prevFinger[0][2] - 180:
                    self.mask = np.concatenate((np.zeros(int((tab_len/4)*2)), np.ones(int(tab_len/4)), np.zeros(int(tab_len/4))), axis=None)
                    self.keyboard_bin_tab *= np.array(self.mask)
                    self.prevFingerListReset()
        except:
            print("Cut by 3/4 doesnt work/Fingers lists out of range")  

    def cutBy2(self): ###ZNALEZC INDEKSY 1 i ZROBIC MASKA * TE INDEKSY
        '''Highlight part of keyboard'''
        try:
            tab_len = len(self.keyboard_bin_tab)
            if (self.Finger and self.prevFinger):
                if self.Finger[1] < self.prevFinger[0][1] - 300: #sprawdzanie ostatniego elementu listy (do listy elementy sa dodawane od tylu stad indeks 0)
                    idxs = np.where(self.keyboard_bin_tab == 1)
                    self.keyboard_bin_tab = np.delete(self.keyboard_bin_tab, idxs, None)
                    self.mask = np.array([1,1,0,0,0,0,0,0])
                    self.keyboard_bin_tab = np.insert(self.keyboard_bin_tab, [idxs[0][0] for i in range(len(idxs))], self.mask)
                    self.prevFingerListReset() 
                elif self.Finger[1] > self.prevFinger[0][1] + 300:
                    idxs = np.where(self.keyboard_bin_tab == 1)
                    self.keyboard_bin_tab = np.delete(self.keyboard_bin_tab, idxs, None)
                    self.mask = np.array([0,0,0,0,0,0,1,1])
                    self.keyboard_bin_tab = np.insert(self.keyboard_bin_tab, [idxs[0][0] for i in range(len(idxs))], self.mask)
                    self.prevFingerListReset() 
                elif self.Finger[2] > self.prevFinger[0][2] + 200:
                    idxs = np.where(self.keyboard_bin_tab == 1)
                    self.keyboard_bin_tab = np.delete(self.keyboard_bin_tab, idxs, None)
                    self.mask = np.array([0,0,1,1,0,0,0,0])
                    self.keyboard_bin_tab = np.insert(self.keyboard_bin_tab, [idxs[0][0] for i in range(len(idxs))], self.mask)
                    self.prevFingerListReset() 
                elif self.Finger[2] < self.prevFinger[0][2] - 180:
                    idxs = np.where(self.keyboard_bin_tab == 1)
                    self.keyboard_bin_tab = np.delete(self.keyboard_bin_tab, idxs, None)
                    self.mask = np.array([0,0,0,0,1,1,0,0])
                    self.keyboard_bin_tab = np.insert(self.keyboard_bin_tab, [idxs[0][0] for i in range(len(idxs))], self.mask)
                    self.prevFingerListReset() 
        except:
            print("Cut by 1/8 doesnt work/Fingers lists out of range")  
            
    def cutBy1(self):
        '''Higlight part of a keyboard and append result list of given value'''
        try:
            if self.Finger[1] < self.prevFinger[0][1] - 300: #sprawdzanie ostatniego elementu listy (do listy elementy sa dodawane od tylu stad indeks 0)
                idxs = np.where(self.keyboard_bin_tab == 1)
                self.setResult(self.keys[idxs[0][0]])
                self.prevFingerListReset() 
            elif self.Finger[1] > self.prevFinger[0][1] + 300:
                idxs = np.where(self.keyboard_bin_tab == 1)
                self.setResult(self.keys[idxs[0][1]])
                self.prevFingerListReset() 
        except:
            print("Cut by 1/16 doesnt work/Fingers lists out of range")
    
    def drawRec(self, screen, color, x, y, w, h):
        '''Draw calibration box''' #moze sie przydac pozniej
        cv2.rectangle(screen, (x, y), (x + w, y + h),color, 0)
        cv2.line(screen, (x, y), (x + 20, y), color, 4)
        cv2.line(screen, (x, y), (x, y + 20 ), color, 4)
        cv2.line(screen, (x+w, y), (x+w - 20, y), color, 4)
        cv2.line(screen, (x+w, y), (x+w, y + 20), color, 4)
        cv2.line(screen, (x, y+h), (x + 20, y+h), color, 4)
        cv2.line(screen, (x, y+h), (x, y+h - 20 ), color, 4)
        cv2.line(screen, (x+w, y+h), (x + w - 20, y+h), color, 4)
        cv2.line(screen, (x+w, y+h), (x+w, y+h - 20), color, 4)
        return screen