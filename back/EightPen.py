import cv2
import numpy as np
import back.modules.FaceMeshModule as mtm
import back.modules.HandTrackingModule as htm

class EightPen:

    def __init__(self, methode="palec"):
        self.methode=methode
        self.sentence=[]
        self.marker_pos=[]
        self.alphabet = ['I','O','E','.','D','U','L','S','G','W','P','C','Z','!','Q','V','Y','A','T',',','X','R','H','N','K','F','B','M','\'','?','@','J']
        self.rad=30
        self.X=None
        self.Y=None
        self.alpha = 0.3
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
   
    '''    
    def printHolder(self):          # PRINT OUT CONTENTS OF ARRAY LINE BY LINE #METODA DO DEBUGOWANIA
        for x in range(0, np.size(self.marker_pos)):
            print(self.marker_pos[x], "Size: ", np.size(self.marker_pos), " Test: ",self.marker_pos[np.size(self.marker_pos)-1])
    '''
    
    def printSentence(self):        # PRINT OUT SENTENCE
        out=""
        for i in range(0,np.size(self.sentence)):
            out+=self.sentence[i]
        print(out)

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
        

    def update(self, img, keyboard):
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
                    if self.marker_pos[1]==4 and self.marker_pos[3]==4: # INSERT SPACE
                        #print("space")
                        self.sentence.append(" ")
                        self.marker_pos=[]
                        self.start=False
                    elif self.marker_pos[1]==2 and self.marker_pos[3]==2: # BACKSPACE
                        #print("backspace")
                        if np.size(self.sentence)>0:
                            self.sentence.pop()
                        self.marker_pos=[]
                        self.start=False
                    elif self.marker_pos[1]==1 and self.marker_pos[3]==1: # DELETE sentence
                        #print("sentence deleted")
                        self.sentence=[]
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
                        self.sentence.append(self.alphabet[self.index-1])
                        #print(self.alphabet[self.index-1], " turns: ", self.turns)
                        print("End of type")
                    self.marker_pos=[]
                    self.start=False
                elif self.newPosition is not self.marker_pos[np.size(self.marker_pos)-1]:
                    self.marker_pos.append(self.newPosition)
                    #self.printHolder()
        
        self.img=keyboard.generateKeyboard(img)
        self.img = cv2.addWeighted(self.overlay, self.alpha, self.img, 1 - self.alpha, 0)
        cv2.circle(self.img, (self.X, self.Y), 7, (255, 0, 0), cv2.FILLED)

        return self.img, self.sentence
