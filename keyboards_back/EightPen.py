import cv2
import numpy as np
import Modules.FaceMeshModule as mtm
import Modules.HandTrackingModule as htm

class EightPen:

    def __init__(self, methode="palec"):
        self.methode=methode
        self.sentance=[]
        self.marker_pos=[]
        self.alphabet = ['I','O','E','.','D','U','L','S','G','W','P','C','Z','!','Q','V','Y','A','T',',','X','R','H','N','K','F','B','M','\'','?','@','J']
        self.rad=30
        self.X=None
        self.Y=None
        self.alpha = 0.7
        self.start=False
        self.lmList=[]
        self.newPosition=None
        self.index=None
        self.turns=None
        self.overlay=None
        if methode=="palec":
            self.detector=htm.handDetector()
            self.lm_index=8
        else:
            self.detector = mtm.FaceMeshDetector()
            self.lm_index=2
   
    def printHolder(self):          # PRINT OUT CONTENTS OF ARRAY LINE BY LINE #METODA DO DEBUGOWANIA
        for x in range(0, np.size(self.marker_pos)):
            print(self.marker_pos[x], "Size: ", np.size(self.marker_pos), " Test: ",self.marker_pos[np.size(self.marker_pos)-1])
    
    def printSentance(self):        # PRINT OUT SENTANCE # DEBUG METHODE
        self.out=""
        for i in range(0,np.size(self.sentance)):
            self.out+=self.sentance[i]
        print(self.out)

    def generateKeyboard(self):
        h,w,c=self.img.shape
        c_h=int(h/2) 
        c_w=int(w/2)
        m=max(c_w,c_h) # ENSURE THAT KEYBOARD IS A SQUARE
        cv2.circle(self.img, (c_w,c_h),self.rad,(0,0,0),-1)                                        # PLACE CICRCLE IN THE MIDDLE OF THE SQUARE
        cv2.line(self.img,(c_w-int(m/2),c_h-int(m/2)),(c_w-self.rad,c_h-self.rad),(255,0,0),10)    # TOP-LEFT DIAGONAL
        cv2.line(self.img,(c_w+int(m/2),c_h-int(m/2)),(c_w+self.rad,c_h-self.rad),(0,0,255),10)    # TOP-RIGHT DIAGONAL
        cv2.line(self.img,(c_w+int(m/2),c_h+int(m/2)),(c_w+self.rad,c_h+self.rad),(0,255,255),10)  # BOTTOM-RIGHT DIAGONAL
        cv2.line(self.img,(c_w-int(m/2),c_h+int(m/2)),(c_w-self.rad,c_h+self.rad),(0,255,0),10)    # BOTTOM-LEFT DIAGONAL
        
        # GENERATING LETTERS ALONG DIAGONALS
        for i in range(1,int(np.size(self.alphabet)/2)+1):
            if(i%4==1):                                 # TOP-RIGHT DIAGONAL #TOP
                x_1 = c_w + int(m/10) * int(i / 4)
                y_1 = c_h - int(m/10) * (int(i / 4)+1)
                x_2 = c_w - int(m/10) * (int(i / 4)+1)
                y_2 = c_h - int(m/10) * (int(i / 4)+1)
            elif(i%4==2):                               # BOTTOM-RIGHT DIAGONAL #RIGHT
                x_1 = c_w + int(m/10) * (int(i / 4)+1)
                y_1 = c_h + int(m/10) * (int(i / 4)+1)
                x_2 = c_w + int(m/10) * (int(i / 4)+1)
                y_2 = c_h - int(m/10) * int(i / 4)
            elif(i%4==3):                               # BOTTOM-LEFT DIAGONAL #BOTTOM
                x_1 = c_w - int(m/10) * (int(i / 4)+1)
                y_1 = c_h + int(m/10) * (int(i / 4)+2)
                x_2 = c_w + int(m/10) * int(i / 4)
                y_2 = c_h + int(m/10) * (int(i / 4)+2)
            else:                                       # TOP-LEFT DIAGONAL #LEFT
                x_1 = c_w - int(m/10) * (int(i / 4)+1)
                y_1 = c_h - int(m/10) * (int(i / 4)-1)
                x_2 = c_w - int(m/10) * (int(i / 4)+1)
                y_2 = c_h + int(m/10) * (int(i / 4))

            cv2.putText(self.img, self.alphabet[i-1], (x_1, y_1), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
            cv2.putText(self.img, self.alphabet[i+int(np.size(self.alphabet)/2)-1], (x_2, y_2), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    # METHODE FOR GETTING POSITION OF MARKER
    def comparePosition(self, lm):
        h,w,c=self.img.shape
        x,y = lm[1], lm[2]
        c_h=int(h/2)
        c_w=int(w/2)
        
        r=np.sqrt((c_w-x)**2+(c_h-y)**2)                         # DISTANCE OF MARKER FROM IMAGE CENTER
        angle=np.arctan2([x-c_w],[y-c_h])*180/np.pi+135          # ANGLE OF MARKER IN 2D CARTESIAN PLANE WITH CENTER IN IMAGE CENTER
        if np.floor(angle) in range(180, 270) and r>self.rad:    # RIGHT QUARTER
            return 2
        elif np.floor(angle) in range(0,90) and r>self.rad:      # LEFT QUARTER
            return 4 
        elif np.floor(angle) in range(90,180) and r>self.rad:    # DOWN QUARTER
            return 3 
        elif np.floor(angle) in range(270, 360) and r>self.rad:  # TOP QUARTER
            return 1 
        elif r<self.rad:                                         # CENTER
            return 0 
        else:                                                   #FIX FOR LEFT -> UP TURN
            return 1
        

    def update(self, img):
        self.img=img
        self.overlay = self.img.copy()
        if self.methode=="palec":
            self.img = self.detector.findHands(self.img,False)
        else:
            self.img, faces = self.detector.findFaceMesh(self.img,False)

        self.lmList = self.detector.findPosition(self.img,0,False)

        if(len(self.lmList)>0):
            self.X=self.lmList[self.lm_index][1]
            self.Y=self.lmList[self.lm_index][2]
            self.newPosition=self.comparePosition(self.lmList[self.lm_index])

            if self.start==False:
                if self.newPosition==0:
                    self.marker_pos.append(self.newPosition)
                    self.start=True
            else:
                #########################
                #ZMIENIC W RAZIE POTRZEB#
                #########################
                if np.size(self.marker_pos)==4: 
                    if self.marker_pos[1]==4 and self.marker_pos[3]==4: # PRINT SENTANCE
                        print("sentance:")
                        self.printSentance()
                        self.sentance=[]
                        self.marker_pos=[]
                        self.start=False
                    elif self.marker_pos[1]==2 and self.marker_pos[3]==2: # INSERT SPACE
                        print("space")
                        self.sentance.append(" ")
                        self.marker_pos=[]
                        self.start=False
                    elif self.marker_pos[1]==1 and self.marker_pos[3]==1: # BACKSPACE
                        print("backspace")
                        if np.size(self.sentance)>0:
                            self.sentance.pop()
                        self.marker_pos=[]
                        self.start=False
                    elif self.marker_pos[1]==3 and self.marker_pos[3]==3: # DELETE SENTANCE
                        print("sentance deleted")
                        self.sentance=[]
                        self.marker_pos=[]
                        self.start=False
                #########################
                #ZMIENIC W RAZIE POTRZEB#
                #########################
                
                if self.start==True:
                    if self.newPosition==0 and np.size(self.marker_pos)>3:
                        self.index=self.marker_pos[1]
                        self.turns=np.count_nonzero(self.marker_pos)-2
                        if ((self.marker_pos[1]<self.marker_pos[2]) and (self.marker_pos[1]!=1 or self.marker_pos[2]!=4)) or (self.marker_pos[1]==4 and self.marker_pos[2]==1): #RIGHT TURNS
                            self.index+=int(self.turns*4)
                        elif self.marker_pos[1]>self.marker_pos[2] or (self.marker_pos[1]==1 and self.marker_pos[2]==4): #LEFT TURNS
                            self.index+= int(self.turns * 4 + np.size(self.alphabet) / 2)
                        if self.index>32 or self.index<=0 or np.size(self.marker_pos)>6:
                            print("Incorrect input")
                        else:
                            self.sentance.append(self.alphabet[self.index-1])
                            print(self.alphabet[self.index-1], " turns: ", self.turns)
                            print("End of type")
                        self.marker_pos=[]
                        self.start=False
                    elif self.newPosition is not self.marker_pos[np.size(self.marker_pos)-1]:
                        self.marker_pos.append(self.newPosition)
                        # self.printHolder()
        
        self.generateKeyboard()
        self.img = cv2.addWeighted(self.overlay, self.alpha, self.img, 1 - self.alpha, 0)
        cv2.circle(self.img, (self.X, self.Y), 7, (255, 0, 0), cv2.FILLED)

        return self.img, self.sentance
