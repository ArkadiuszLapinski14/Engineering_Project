import csv
import cv2
import mediapipe as mp
import time
import numpy as np
import HandTrackingModule as htm
from Keyboard import Keyboard
from HandMovingKeyboard import HandMovingKeyboard
import HandMovingKeyboardStatic as static
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import EightPen as ep
import FaceMeshModuleEP as mtmep
from screeninfo import get_monitors
from Feedback import Feedback
from HeadMovingKeyboard import HeadMovingKeyboard 
import sys

from dashboard.Dashboard import Dashboard

SCREEN_WIDTH = get_monitors()[0].width
SCREEN_HEIGHT = get_monitors()[0].height

def isHandNumber(point):
    try:
        if (int(point)<=20 and int(point)>=0):
            return int(point)
        else:
            return 8 
    except ValueError:
        return 8

def generateText(file_name = 'textGenerated.csv'):
    with open(file_name, 'r') as file:
        csvreader = csv.reader(file)
        for index, row in enumerate(csvreader):
            if index == 0:
                chosen_row = row
            else:
                r = np.random.randint(0, index)
                if r == 0:
                    chosen_row = row


    print(chosen_row[0])
    print(chosen_row[1])
    return chosen_row

class Menu(QMainWindow):
    def __init__(self):
        ###WINDOW INIT###
        super(Menu, self).__init__()
        self.setWindowTitle("Hand Tracking Program Menu")
        self.width = int(SCREEN_WIDTH - (SCREEN_WIDTH * 0.4))
        self.height = int(SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.4))
        self.setGeometry(int((SCREEN_WIDTH - self.width) / 2), (int((SCREEN_HEIGHT - self.height) / 2)), self.width, self.height)
        #################

        ####UI INIT######
        self.UIComponents()
        #################

    def UIComponents(self):
        dashboard = Dashboard()
        self.setCentralWidget(dashboard)

class Menu1(QWidget):

    def __init__(self, parent = None):
        ###WINDOW INIT###
        super(Menu1, self).__init__(parent)        
        self.setWindowTitle("Hand Tracking Program Menu")
        self.width = int(SCREEN_WIDTH - (SCREEN_WIDTH * 0.4))
        self.height = int(SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.4))
        self.setGeometry(int((SCREEN_WIDTH - self.width) / 2), (int((SCREEN_HEIGHT - self.height) / 2)), self.width, self.height)
        self.showMaximized()
        ##################

        ###PARAMS###
        self.point = 8
        self.textToInsert = ''
        self.whichKeyboard = 'hand'
        self.isGenerated = False    #zmienna mowiaca czy generowac text
        self.resultsTableEP = []
        self.text_written = ' '
        self.text_to_write = ' '
        self.detectionFlag = True
        #############

        ###UI INIT###
        self.UIComponents()
        #############

    def UIComponents(self):
        layout = QGridLayout()
        self.setLayout(layout)

        #label - text question
        self.text_question = QLabel("Do you want a generated text or your own?")
        self.text_question.setMaximumHeight(20)
        layout.addWidget(self.text_question, 3, 0, 1, 1)


        #button activating the launch function
        self.buttonGenereted = QPushButton("I want genereted text")
        self.buttonGenereted.clicked.connect( self.generatedTextOnClick) #metoda generujaca text 
        self.buttonGenereted.setMaximumWidth(200)
        layout.addWidget(self.buttonGenereted, 4, 0,1,1)
       

        #label (text)
        self.labelPoint=QLabel("Enter the main point of hand to detect:")
        self.labelPoint.setMaximumHeight(20)
        layout.addWidget(self.labelPoint, 1, 0,1,1)
        
        #text line
        self.point_text = QLineEdit()
        self.point_text.setMaximumWidth(200)
        layout.addWidget(self.point_text, 2, 0,1,1)


        #label
        self.ownTextLabel= QLabel("Type your own text.")
        self.ownTextLabel.setMaximumHeight(20)
        layout.addWidget(self.ownTextLabel, 5, 0,1,1)

       
        #text line
        self.ownText = QLineEdit()
        self.ownText.setMaximumWidth(200)
        layout.addWidget(self.ownText, 6, 0,1,1)
        
        self.keyboardLabel= QLabel("Choose your keyboard")
        self.keyboardLabel.setMaximumHeight(20)
        layout.addWidget(self.keyboardLabel, 8, 0,1,1)

        #camera widget
        self.cameraWidget = QLabel()
        layout.addWidget(self.cameraWidget, 0, 0,2,2)


        #Widgety podczas detekcji--------------------

        self.insertTextLabel= QLabel("Text to insert: "+ self.textToInsert)
        self.insertTextLabel.setMaximumHeight(20)
        self.insertTextLabel.hide()
        layout.addWidget(self.insertTextLabel, 3, 2,1,1)

        self.insertedEPLabel= QLabel("Text inserted in 8Pen: "+ str(self.resultsTableEP))
        self.insertedEPLabel.setMaximumHeight(20)
        layout.addWidget(self.insertedEPLabel, 4, 2,1,1)

        self.buttonStopDetection = QPushButton("Stop detection")
        self.buttonStopDetection.clicked.connect( self.stop_detection)
        self.buttonStopDetection.setMaximumWidth(200)
        layout.addWidget(self.buttonStopDetection, 5, 2,1,1)

        self.buttonHandKeyboardStatic = QPushButton("HAND STATIC triple keyboard ")
        self.buttonHandKeyboardStatic.clicked.connect( self.isGeneratedHandStatic)
        layout.addWidget(self.buttonHandKeyboardStatic, 9, 0,1,1)

        self.buttonHandKeyboard = QPushButton("HAND triple keyboard")
        self.buttonHandKeyboard.clicked.connect( self.isGeneratedHand)
        layout.addWidget(self.buttonHandKeyboard, 10, 0,1,1)

        self.buttonHeadKeyboard = QPushButton("HEAD triple keyboard")
        self.buttonHeadKeyboard.clicked.connect( self.isGeneratedHead)
        layout.addWidget(self.buttonHeadKeyboard, 11, 0,1,1)
        
        self.button8penKeyboard = QPushButton("HEAD 8PEN keyboard")
        self.button8penKeyboard.clicked.connect( self.isGeneratedEP)
        layout.addWidget(self.button8penKeyboard, 12, 0,1,1)
        #-------------------------------------



    def generatedTextOnClick(self): #metoda do genrowania textu
        self.isGenerated = True
        
    def head_keyboard(self,text='k'):

        self.text_to_write = []
        self.text_written = str(text)
        
        self.hide_components()
        self.textToInsert = text
        self.insertTextLabel.setText("Text to insert: "+str(text))

        self.insertTextLabel.show()

        if (self.point_text.text() != ''):
            self.point = isHandNumber(self.point_text.text())
            
        pTime = 0

        cap = cv2.VideoCapture(0)
        #detector = htm.handDetector(maxHands=1)
        classic_keyboard = Keyboard()
        headMovingKeyboard = HeadMovingKeyboard(classic_keyboard)
        mp_face_mesh = mp.solutions.face_mesh
        face_mesh = mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5)
        
        while (self.detectionFlag == True):
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img = cv2.resize(img, (1024,768 ))  
            results = face_mesh.process(img)
          #  img = detector.findHands(img)
           # lmList = detector.findPosition(img)

            img_h, img_w, img_c = img.shape
            face_3d = []
            face_2d = []

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    for idx, lm in enumerate(face_landmarks.landmark):
                        if idx == 33 or idx == 263 or idx == 1 or idx == 61 or idx == 291 or idx == 199:
                            if idx == 1:
                                nose_2d = (lm.x * img_w, lm.y * img_h)
                                nose_3d = (lm.x * img_w, lm.y * img_h, lm.z * 3000)

                            x, y = int(lm.x * img_w), int(lm.y * img_h)

                            # Get the 2D Coordinates
                            face_2d.append([x, y])

                            # Get the 3D Coordinates
                            face_3d.append([x, y, lm.z])       
            
                    # Convert it to the NumPy array
                    face_2d = np.array(face_2d, dtype=np.float64)

                    # Convert it to the NumPy array
                    face_3d = np.array(face_3d, dtype=np.float64)

                    # The camera matrix
                    focal_length = 1 * img_w

                    cam_matrix = np.array([ [focal_length, 0, img_h / 2],
                                            [0, focal_length, img_w / 2],
                                            [0, 0, 1]])

                    # The distortion parameters
                    dist_matrix = np.zeros((4, 1), dtype=np.float64)

                    # Solve PnP
                    success, rot_vec, trans_vec = cv2.solvePnP(face_3d, face_2d, cam_matrix, dist_matrix)

                    # Get rotational matrix
                    rmat, jac = cv2.Rodrigues(rot_vec)

                    # Get angles
                    angles, mtxR, mtxQ, Qx, Qy, Qz = cv2.RQDecomp3x3(rmat)

                    # Get the y rotation degree
                    x = angles[0] * 360
                    y = angles[1] * 360
                    z = angles[2] * 360
                    
                    if y < -8:
                        text = "Looking Left"
                    elif y > 8:
                        text = "Looking Right"
                    elif x < -8:
                        text = "Looking Down"
                    elif x > 8:
                        text = "Looking Up"
                    else:
                        text = "Forward"

                
                    #cv2.putText(img, text, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

                    angles2 = [x, y]

                    headMovingKeyboard.update(img, angles2)
                   # handMovingKeyboard.update(img, lmList)

                    isCalibrated = " "
                    if(headMovingKeyboard.is_calibrated==True):
                        isCalibrated="Calibrated"
                    else:
                        isCalibrated="False"

                    cv2.putText(img, isCalibrated, (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

              

                    #cv2.putText(img, str(headMovingKeyboard.angles[0]), (600, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)
                    #cv2.putText(img, str(headMovingKeyboard.angles[1]), (600, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 2)

                    img = classic_keyboard.draw_update(img, 10, 100, 30, 30)

                    ###FPS###
                    cTime = time.time()
                    fps = 1/(cTime - pTime)
                    pTime = cTime

                    ###DRAW RESULT###
                    img = headMovingKeyboard.drawResult(img, 600, 600)
                    img_height, img_width, img_colors = img.shape

                    #################
        
                    cv2.putText(img, str(int(fps)),(0,15), cv2.FONT_HERSHEY_PLAIN, 1 ,(255,0,255), 2)
                    #cv2.imshow("Image", img)
                    self.update_image(img)
                    cv2.waitKey(1)
                    #########

    def stop_detection(self):
        self.cameraWidget.hide()
        self.detectionFlag = False
        self.insertedEPLabel.setText("Text inserted in 8Pen: "+str(self.resultsTableEP))

        self.close()
        ############

    def ownTextMethodHand(self):
        own_text = self.ownText.text()
        

        if(own_text != ''):
            self.launch(own_text)
        else:
            self.launch()
                     
    def ownTextMethodHead(self):

        own_text = self.ownText.text()

        if (own_text !=''):
            self.head_keyboard(own_text)

        else:
            self.head_keyboard()

    def ownTextMethodEP(self):

        own_text = self.ownText.text()

        if (own_text !=''):
            self.launchEP(text = own_text)

        else:
            self.launchEP()

    #-------------------------------------NOWE---------------------------------
    def isGeneratedHand(self):
        if(self.isGenerated == False):
            self.ownTextMethodHand()
        else:
            random_text = generateText()
            self.launch(random_text[0])

    def isGeneratedHandStatic(self):  
  
        if(self.isGenerated == False):
            own_text = self.ownText.text()

            if (own_text !=''):
                self.launch(own_text, isStatic = True)
            else:
                self.launch(isStatic = True)
                
        else:
            random_text = generateText()
            self.launch(random_text[0], isStatic = True)
           

    def isGeneratedHead(self):
        if(self.isGenerated ==False):
            self.ownTextMethodHead()
        else:
            random_text = generateText()
            self.head_keyboard(random_text[0])


    def isGeneratedEP(self):
        if(self.isGenerated ==False):
            self.ownTextMethodEP()
        else:
            random_text = generateText()
            self.launchEP(text = random_text[0])
    #--------------------------------------nowe----------------------------------


    def launch(self,text = "k", isStatic = False):
        
        self.text_to_write = []
        self.text_written = str(text)
        
        self.hide_components()
       
        self.textToInsert = text
        self.insertTextLabel.setText("Text to insert: "+str(text))

        self.insertTextLabel.show()
       
        #Getting the point of hand
        if (self.point_text.text() != ''):
            self.point = isHandNumber(self.point_text.text())   # tu jest punkt do lms
            
            
        pTime = 0

        cap = cv2.VideoCapture(0)
        detector = htm.handDetector(maxHands=1)
        classic_keyboard = Keyboard()
        if (isStatic == True):
            handMovingKeyboard = static.HandMovingKeyboardStatic(classic_keyboard,self.point)
        else:
            handMovingKeyboard = HandMovingKeyboard(classic_keyboard,self.point)

        print("PUNKT: " + str(self.point))

        self.text_written = str(text)


        while (self.detectionFlag == True):
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img = cv2.resize(img, (1024,768 ))  
            img = detector.findHands(img)
            lmList = detector.findPosition(img)

            img = handMovingKeyboard.update(img,lmList,classic_keyboard)

            #img = classic_keyboard.draw_update(img, 10, 100, 30, 30)

            ###FPS###
            cTime = time.time()
            fps = 1/(cTime - pTime)
            pTime = cTime

            ###DRAW RESULT###
            img = handMovingKeyboard.drawResult(img, 600, 600)
            #################
           
            
            self.text_to_write = handMovingKeyboard.get_result()
            
            img_height, img_width, img_colors = img.shape
           
            cv2.putText(img, str(int(fps)),(0,15), cv2.FONT_HERSHEY_PLAIN, 1 ,(255,0,255), 2)

            cv2.putText(img, str(self.text_written),(300,80), cv2.FONT_HERSHEY_PLAIN, 3 ,(0,0,255), 2) #------------------------------
            cv2.putText(img, str(self.text_to_write),(300,200), cv2.FONT_HERSHEY_PLAIN, 3 ,(0,255,0), 2) #-----------------------------

            self.update_image(img)

            cv2.waitKey(1)
            #########
    
    def launchEP(self,methode = True,text='dom'):
        
        # SETTING BASE PARAMETERS 
        
        self.text_to_write = []
        self.bad_text = str(text)
        
        self.hide_components()
        self.textToInsert = text
        self.insertTextLabel.setText("Text to insert: "+str(text))

        self.insertTextLabel.show()
        print("start")
        pTime = 0
        alphabet = ['I','O','E','.','D','U','L','S','G','W','P','C','Z','!','Q','V','Y','A','T',',','X','R','H','N','K','F','B','M','\'','?','@','J']
        cap = cv2.VideoCapture(0)
        rad=30
        holder=ep.positionHolder()
        sentance=ep.writing()
        X=0
        Y=0
        start=False
        if methode==False:
            detector = mtmep.FaceMeshDetector()
            lm_index=2
        else:
            detector=htm.handDetector()
            lm_index=8

        while (self.detectionFlag == True):
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img = cv2.resize(img, (1024,768 ))  
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
                newPosition=ep.comparePosition(img, lmList[lm_index], rad)
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
                                self.resultsTableEP.append(alphabet[index-1])
                                print(alphabet[index-1], " turns: ", turns)
                                print("End of type")
                            holder.flushHolder()
                            start=False
                        elif newPosition is not holder.getHolder()[np.size(holder.getHolder())-1]:
                            holder.givePosition(newPosition)
                            holder.printHolder()
        
            img = ep.keyboard(img,rad, alphabet)
            alpha = 0.7
            img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)
            ###FPS###
            cTime = time.time()
            fps = 1/(cTime - pTime)
            pTime = cTime
            

            cv2.putText(img, str(int(fps)),(0,15), cv2.FONT_HERSHEY_PLAIN, 1 ,(255,0,255), 2)
            cv2.circle(img, (X, Y), 7, (255, 0, 0), cv2.FILLED)
            #cv2.imshow("Image", img)
            self.update_image(img)
            
            cv2.waitKey(1)
            
    def hide_components(self):
        self.text_question.hide()
        self.buttonGenereted.hide()
        self.ownText.hide()
        self.point_text.hide()
        self.ownTextLabel.hide()
        self.labelPoint.hide()
       

    def ConvertCvToQt(self, img):
        """Convert from an opencv image to QPixmap"""
        h, w, ch = img.shape
        bytes_per_line = ch * w
        converted_img = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        return QPixmap(converted_img)

    ###TO NIE PRZEJDZIE IMO
    def update_image(self, img):
        """Updates the image_label with a new opencv image"""
        img = self.ConvertCvToQt(img)
        self.cameraWidget.setPixmap(img)

def main():
    app = QApplication(sys.argv)
    menu = Menu()
    menu.show()
    sys.exit(app.exec())

    

if __name__ == '__main__':
    main()
	
