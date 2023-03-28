import cv2

class HeadMovingKeyboard:
    def __init__(self, keyboard):
        self.angles = []
        self.keyboard = keyboard
        self.keys = keyboard.get_keys()
        self.KEYS = keyboard.get_keys()
        self.res = []
        self.is_calibrated = False

    def update(self, screen, angles):
        try:
            self.headUpdate(angles)
            if self.is_calibrated == True:
                if len(self.keys) != 2:
                        self.cutBy4()
                elif len(self.keys) == 2:
                        self.cutBy2()
                return screen
            else:
                screen = self.calibrate(screen)
        except:
            print("Hand Moving Keyboard algorith doesnt work/lms out of range")
        return screen 

    def calibrate(self, screen):
        try:
            if (self.angles):
                if ((self.angles[1] > -5 and self.angles[1] < 5) and (self.angles[0] > -5 and self.angles[0] <5)):
                    #screen = self.CalibrationLoading(screen, x, y, w, h)
                    self.is_calibrated = True
               
   

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

        self.keys = self.KEYS
        self.keyboard.set_keys(self.KEYS)

    def drawResult(self, screen, x, y):
        '''Draws a result on the screen'''
        screen, x, y = self.drawResultBox(screen)
        for el in self.res:
            cv2.putText(screen, el, (x,y), cv2.FONT_HERSHEY_PLAIN, 3 ,(255,255,255), 2)
            x += 30
        return screen

    def drawResultBox(self, screen):
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

    def headUpdate(self, angles):
        if (angles):
            self.angles = angles
            for ang in self.angles:
                self.angles = self.angles*360
            if len(self.keys) == 1:
                self.setResult(self.keys[0])


    def cutBy4(self):
        '''Cut unecessary part of keyboard when len(keayboard) > 2'''
        try:
            if (self.angles and self.is_calibrated==True):
                if self.angles[0] <  -8 and self.angles[1]<8 and self.angles>-8: 
                    self.keys = self.keys[0:int(len(self.keys)/4)]
                    self.keyboard.set_keys(self.keys)
                    self.is_calibrated = False
                  
                elif self.angles[1] > 8 and self.angles[0]<8 and self.angles[0]>-8:
                    self.keys = self.keys[int(len(self.keys)*(3/4)):len(self.keys)]
                    self.keyboard.set_keys(self.keys)
                    self.is_calibrated = False
                   
                elif self.angles[1] < -8 and self.angles[0]<8 and self.angles[0]>-8:
                    self.keys = self.keys[int(len(self.keys)*(1/4)):int(len(self.keys)*(2/4))]
                    self.keyboard.set_keys(self.keys)
                    self.is_calibrated = False
                    
                elif self.angles[0] > 8 and self.angles[1]<8 and self.angles[1]>-8:
                    self.keys = self.keys[int(len(self.keys)*(2/4)):int(len(self.keys)*(3/4))]
                    self.keyboard.set_keys(self.keys)
                    self.is_calibrated = False
                    
        except:
            print("Cut by 3/4 doesnt work/Fingers lists out of range")  

    def cutBy2(self):
        '''Cut unecessary part of keyboard when len(keayboard) == 2'''
        try:
            if (self.angles and self.is_calibrated==True):
                if self.angles[1] < - 10:
                    self.keys = self.keys[0:1]
                    self.keyboard.set_keys(self.keys)
                    self.is_calibrated = False
                  
                elif self.angles[1] >  10:
                    self.keys = self.keys[1:2]
                    self.keyboard.set_keys(self.keys)
                    self.is_calibrated = False
                  
        except:
            print("Final cut by 1/2 doesnt work/Fingers lists out of range")