import cv2
import time
import numpy as np
import FaceMeshModule as mtm
import HandTrackingModule as htm

# CLASS FOR SENTANCE HANDLING
class writing: 
    def __init__(self):             # INITIATE OBJECT INSTANCE
        self.sentance=[]
    
    def writeLetter(self, letter):  # INSERT LETTER TO SENTANCE ARRAY
        self.sentance.append(letter)
    
    def printSentance(self):        # PRINT OUT SENTANCE
        self.out=""
        for i in range(0,np.size(self.sentance)):
            self.out+=self.sentance[i]
        print(self.out)
        
    def flushSentance(self):        # SET SENTANCE ARRAY TO EMPTY ARRAY
        self.sentance=[]
    
    def deleteLetter(self):         # DELETE LAST ELEMENT OF SENTANCE ARRAY
        self.sentance.pop()

# CLASS FOR SAVING MARKER MOVEMENT
class positionHolder: 
    def __init__(self):             # INITIATE OBJECT INSTANCE
        self.pos=[]

    def givePosition(self, newPos): # APPEND NEW POSITION TO THE END OF LIST
        self.pos.append(newPos)

    def getHolder(self):            # RETURN ARRAY FOR PROCESSING
        return self.pos

    def flushHolder(self):          # SET ARRRAY TO EMPTY ARRAY
        self.pos=[]

    def printHolder(self):          # PRINT OUT CONTENTS OF ARRAY LINE BY LINE
        for x in range(0, np.size(self.pos)):
            print(self.pos[x], "Size: ", np.size(self.pos), " Test: ",self.getHolder()[np.size(self.pos)-1])

# METHODE FOR GENERATING KEYBOARD ON SCREEN
def keyboard(img, rad, alphabet):
    h,w,c=img.shape
    c_h=int(h/2) 
    c_w=int(w/2)
    m=max(c_w,c_h) # ENSURE THAT KEYBOARD IS A SQUARE

    cv2.circle(img, (c_w,c_h),rad,(0,0,0),-1)                                   # PLACE CICRCLE IN THE MIDDLE OF THE SQUARE
    cv2.line(img,(c_w-int(m/2),c_h-int(m/2)),(c_w-rad,c_h-rad),(255,0,0),10)    # TOP-LEFT DIAGONAL
    cv2.line(img,(c_w+int(m/2),c_h-int(m/2)),(c_w+rad,c_h-rad),(0,0,255),10)    # TOP-RIGHT DIAGONAL
    cv2.line(img,(c_w+int(m/2),c_h+int(m/2)),(c_w+rad,c_h+rad),(0,255,255),10)  # BOTTOM-RIGHT DIAGONAL
    cv2.line(img,(c_w-int(m/2),c_h+int(m/2)),(c_w-rad,c_h+rad),(0,255,0),10)    # BOTTOM-LEFT DIAGONAL
    
    # GENERATING LETTERS ALONG DIAGONALS
    for i in range(1,int(np.size(alphabet)/2)+1):
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

        cv2.putText(img, alphabet[i-1], (x_1, y_1), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
        cv2.putText(img, alphabet[i+int(np.size(alphabet)/2)-1], (x_2, y_2), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)

    return img

# METHODE FOR GETTING POSITION OF MARKER
def comparePosition(img, lm, rad):
    h,w,c=img.shape
    x,y = lm[1], lm[2]
    c_h=int(h/2)
    c_w=int(w/2)
    
    r=np.sqrt((c_w-x)**2+(c_h-y)**2) # DISTANCE OF MARKER FROM IMAGE CENTER
    angle=np.arctan2([x-c_w],[y-c_h])*180/np.pi+135 # ANGLE OF MARKER IN 2D CARTESIAN PLANE WITH CENTER IN IMAGE CENTER
    if np.floor(angle) in range(180, 270) and r>rad:    # RIGHT QUARTER
        return 2
    elif np.floor(angle) in range(0,90) and r>rad:      # LEFT QUARTER
        return 4 
    elif np.floor(angle) in range(90,180) and r>rad:    # DOWN QUARTER
        return 3 
    elif np.floor(angle) in range(270, 360) and r>rad:  # TOP QUARTER
        return 1 
    elif r<rad:                                         # CENTER
        return 0 
    else:                                               #FIX FOR LEFT -> UP TURN
        return 1

'''def main(methode=False):
    
    # SETTING BASE PARAMETERS 
    pTime = 0
    alphabet = ['I','O','E','.','D','U','L','S','G','W','P','C','Z','!','Q','V','Y','A','T',',','X','R','H','N','K','F','B','M','\'','?','@','J']
    cap = cv2.VideoCapture(0)
    rad=30
    holder=positionHolder()
    sentance=writing()
    X=0
    Y=0
    start=False
    if methode==False:
        detector = mtm.FaceMeshDetector()
        lm_index=2
    else:
        detector=htm.handDetector()
        lm_index=8

    while True:
        success, img = cap.read()
        img = cv2.flip(img, 1)
        
        #CHECK DETECTION METHODE
        if methode==False: # PICK FACEMESH AS MARKER
            img, faces = detector.findFaceMesh(img,False)
        else: # PICK TIP OF INDEX FINGER AS MARKER
            img = detector.findHands(img,False)
        
        overlay = img.copy()
        lmList = detector.findPosition(img,0,False)
        
        if len(lmList) > 0: # CHECK IF MARKER IS MISSING
        
            X=lmList[lm_index][1]
            Y=lmList[lm_index][2]
            newPosition=comparePosition(img, lmList[lm_index], rad)
            if start==False:
                if newPosition==0:
                    holder.givePosition(newPosition)
                    start=True
            else:
                if np.size(holder.getHolder())==4: 
                    if holder.getHolder()[1]==4 and holder.getHolder()[3]==4: # PRINT SENTANCE
                        print("sentance:")
                        sentance.printSentance()
                        sentance.flushSentance()
                        holder.flushHolder()
                        start=False
                    elif holder.getHolder()[1]==2 and holder.getHolder()[3]==2: # INSERT SPACE
                        print("space")
                        sentance.writeLetter(" ")
                        holder.flushHolder()
                        start=False
                    elif holder.getHolder()[1]==1 and holder.getHolder()[3]==1: # BACKSPACE
                        print("backspace")
                        if len(sentance.sentance)>0:
                            sentance.deleteLetter()
                        holder.flushHolder()
                        start=False
                    elif holder.getHolder()[1]==3 and holder.getHolder()[3]==3: # DELETE SENTANCE
                        print("sentance deleted")
                        sentance.flushSentance()
                        holder.flushHolder()
                        start=False
                if start==True:
                    if newPosition==0 and np.size(holder.getHolder())>3:
                        index=holder.getHolder()[1]
                        turns=np.count_nonzero(holder.getHolder())-2
                        if ((holder.getHolder()[1]<holder.getHolder()[2]) and (holder.getHolder()[1]!=1 or holder.getHolder()[2]!=4)) or (holder.getHolder()[1]==4 and holder.getHolder()[2]==1): #RIGHT TURNS
                            index+=turns*4
                        elif holder.getHolder()[1]>holder.getHolder()[2] or (holder.getHolder()[1]==1 and holder.getHolder()[2]==4): #LEFT TURNS
                            index+= turns * 4 + int(np.size(alphabet) / 2)
                        if index>32 or index<=0 or np.size(holder.getHolder())>6:
                            print("Incorrect input")
                        else:
                            sentance.writeLetter(alphabet[index-1])
                            print(alphabet[index-1], " turns: ", turns)
                            print("End of type")
                        holder.flushHolder()
                        start=False
                    elif newPosition is not holder.getHolder()[np.size(holder.getHolder())-1]:
                        holder.givePosition(newPosition)
                        holder.printHolder()
        
        img = keyboard(img,rad, alphabet)
        alpha = 0.7
        img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
        ###FPS###
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime

        cv2.putText(img, str(int(fps)),(0,15), cv2.FONT_HERSHEY_PLAIN, 1 ,(255,0,255), 2)
        cv2.circle(img, (X, Y), 7, (255, 0, 0), cv2.FILLED)
        cv2.imshow("Image", img)
        cv2.waitKey(1)
        #########
'''

#if __name__ == '__main__':
 #   main()