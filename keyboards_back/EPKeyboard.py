import cv2
import numpy as np


class EPKeyboard:
    def __init__(self):
        self.alphabet = ['I','O','E','.','D','U','L','S','G','W','P','C','Z','!','Q','V','Y','A','T',',','X','R','H','N','K','F','B','M','\'','?','@','J']
        self.rad=30
        self.alpha = 0.7
        
    def generateKeyboard(self,img):
        # self.overlay = img.copy()
        h,w,c=img.shape
        c_h=int(h/2) 
        c_w=int(w/2)
        m=max(c_w,c_h) # ENSURE THAT KEYBOARD IS A SQUARE
        cv2.circle(img, (c_w,c_h),self.rad,(0,0,0),-1)                                        # PLACE CICRCLE IN THE MIDDLE OF THE SQUARE
        cv2.line(img,(c_w-int(m/2),c_h-int(m/2)),(c_w-self.rad,c_h-self.rad),(255,0,0),10)    # TOP-LEFT DIAGONAL
        cv2.line(img,(c_w+int(m/2),c_h-int(m/2)),(c_w+self.rad,c_h-self.rad),(0,0,255),10)    # TOP-RIGHT DIAGONAL
        cv2.line(img,(c_w+int(m/2),c_h+int(m/2)),(c_w+self.rad,c_h+self.rad),(0,255,255),10)  # BOTTOM-RIGHT DIAGONAL
        cv2.line(img,(c_w-int(m/2),c_h+int(m/2)),(c_w-self.rad,c_h+self.rad),(0,255,0),10)    # BOTTOM-LEFT DIAGONAL
        
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

            cv2.putText(img, self.alphabet[i-1], (x_1, y_1), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
            cv2.putText(img, self.alphabet[i+int(np.size(self.alphabet)/2)-1], (x_2, y_2), cv2.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 3)
        
        # img = cv2.addWeighted(self.overlay, self.alpha, img, 1 - self.alpha, 0)
        return img