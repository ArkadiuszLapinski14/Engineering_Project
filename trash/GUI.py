# %% imports
import csv
import cv2
import mediapipe as mp
import time
import numpy as np
import Modules.HandTrackingModule as htm
from keyboards_back.Keyboard import Keyboard
from keyboards_back.HandMovingKeyboard import HandMovingKeyboard
import keyboards_back.HandMovingKeyboardStatic as static
import PyQt5.QtWidgets as pq
from PyQt5 import QtGui as qtgui
from PyQt5.QtGui import QPixmap, QColor
import trash.EightPen as ep


from trash.Feedback import Feedback

from keyboards_back.HeadMovingKeyboard import HeadMovingKeyboard 

class Menu():

    def __init__(self):
        
        self.app = pq.QApplication([])
        self.detectionFlag = True
        
        self.window = pq.QWidget()
        self.window.setWindowTitle("Hand Tracking Program Menu")
        
        self.windowWidth = 1600
        self.windowHeight = 1000

        self.window.setFixedSize(self.windowWidth, self.windowHeight)
        self.layout = pq.QVBoxLayout()
        self.grid = pq.QGridLayout()
        self.point = 8
        # self.textToInsert = ''
        # self.whichKeyboard = 'hand'
        # self.isGenerated = False    #zmienna mowiaca czy generowac text
        # self.resultsTableEP = []
        # self.text_written = ' '
        # self.text_to_write = ' '

        #label - text question
        # self.text_question = pq.QLabel("Do you want a generated text or your own?")
        # self.grid.addWidget(self.text_question, 3, 0,1,1 )
        # self.text_question.setMaximumHeight(20)


         #button activating the launch function
        # self.buttonGenereted = pq.QPushButton("I want genereted text")
        # self.grid.addWidget(self.buttonGenereted, 4, 0,1,1)
        # self.buttonGenereted.clicked.connect( self.generatedTextOnClick) #metoda generujaca text 

                #Setting new width
        # self.buttonGenereted.setMaximumWidth(200)
       


        #label (text)
        self.labelPoint=pq.QLabel("Enter the main point of hand to detect:")
        self.grid.addWidget(self.labelPoint, 1, 0,1,1)
        self.labelPoint.setMaximumHeight(20)
        
        #text line
        self.point_text = pq.QLineEdit()
        self.grid.addWidget(self.point_text, 2, 0,1,1)
        # print(self.point_text.text())
        self.point_text.setMaximumWidth(200)


        #  #label
        # self.ownTextLabel= pq.QLabel("Type your own text.")
        # self.grid.addWidget(self.ownTextLabel, 5, 0,1,1)
        # self.ownTextLabel.setMaximumHeight(20)

       
        # #text line
        # self.ownText = pq.QLineEdit()
        # self.grid.addWidget(self.ownText, 6, 0,1,1)
        # print(self.ownText.text())
        # self.ownText.setMaximumWidth(200)
        
        self.keyboardLabel= pq.QLabel("Choose your keyboard")
        self.grid.addWidget(self.keyboardLabel, 8, 0,1,1)
        self.keyboardLabel.setMaximumHeight(20)

        #camera widget
        self.cameraWidget = pq.QLabel()
        self.cameraWidget.setMaximumWidth(1080)
        self.cameraWidget.setMaximumHeight(768)
        self.grid.addWidget( self.cameraWidget, 0, 0,2,2)


        #Widgety podczas detekcji--------------------

        # self.insertTextLabel= pq.QLabel("Text to insert: "+ self.textToInsert)
        # self.grid.addWidget(self.insertTextLabel, 3, 2,1,1)
        # self.insertTextLabel.setMaximumHeight(20)
        # self.insertTextLabel.hide()

        # self.insertedEPLabel= pq.QLabel("Text inserted in 8Pen: "+ str(self.resultsTableEP))
        # self.grid.addWidget(self.insertedEPLabel, 4, 2,1,1)
        # self.insertedEPLabel.setMaximumHeight(20)


        self.buttonStopDetection = pq.QPushButton("Stop detection")
        self.grid.addWidget(self.buttonStopDetection, 5, 2,1,1)
        self.buttonStopDetection.clicked.connect( self.stop_detection)
        self.buttonStopDetection.setMaximumWidth(200)

        self.buttonHandKeyboardStatic = pq.QPushButton("HAND STATIC triple keyboard ")
        self.grid.addWidget(self.buttonHandKeyboardStatic, 9, 0,1,1)
        self.buttonHandKeyboardStatic.clicked.connect(lambda: self.launch("HandMovingKeyboardStatic"))

        self.buttonHandKeyboardStatic = pq.QPushButton("HAND triple keyboard ")
        self.grid.addWidget(self.buttonHandKeyboardStatic, 9, 0,1,1)
        self.buttonHandKeyboardStatic.clicked.connect(lambda: self.launch("classic_keyboard"))

        # self.buttonHandKeyboard = pq.QPushButton("HAND triple keyboard")
        # self.grid.addWidget(self.buttonHandKeyboard, 10, 0,1,1)
        # self.buttonHandKeyboard.clicked.connect( self.isGeneratedHand)

        # self.buttonHeadKeyboard = pq.QPushButton("HEAD triple keyboard")
        # self.grid.addWidget(self.buttonHeadKeyboard, 11, 0,1,1)
        # self.buttonHeadKeyboard.clicked.connect( self.isGeneratedHead)
        
        # self.button8penKeyboard = pq.QPushButton("HEAD 8PEN keyboard")
        # self.grid.addWidget(self.button8penKeyboard, 12, 0,1,1)
        # self.button8penKeyboard.clicked.connect( self.isGeneratedEP)
        
        #-------------------------------------

        #Setting the layout
        self.window.setLayout(self.grid)

        #Showing and executing the main window
        self.window.show()
        self.app.exec_()
    
    def stop_detection(self):
        self.cameraWidget.hide()
        self.detectionFlag = False
        # self.insertedEPLabel.setText("Text inserted in 8Pen: "+str(self.resultsTableEP))

        self.app.quit()
        ############

    # def getKeyboard(self, keyboard, interface):                               ############ UŻYJ ELSEIFa NIE MA TEGO W PYTHONIE 3.10- 
    #     match keyboard:
    #         case "HandMovingKeyboardStatic":
    #             return static.HandMovingKeyboardStatic(interface,self.point)
    #         case "classic_keyboard":
    #             return HandMovingKeyboard(interface,self.point)

    def hide_components(self):
        # self.text_question.hide()
        # self.buttonGenereted.hide()
        # self.ownText.hide()
        self.point_text.hide()
        # self.ownTextLabel.hide()
        self.labelPoint.hide()

    def isHandNumber(point):
        try:
            if (int(point)<=20 and int(point)>=0):
                return int(point)
            else:
                return 8 
        except ValueError:
            return 8
        
    
    def launch(self, keyboard ,text = ""):
        
        # pass
        self.text_to_write = []
        self.text_written = str(text)
        
        self.hide_components()
       
        # self.textToInsert = text
        # self.insertTextLabel.setText("Text to insert: "+str(text))

        self.insertTextLabel.show()
       
        # #Getting the point of hand
        if (self.point_text.text() != ''):
            self.point = isHandNumber(self.point_text.text())   # tu jest punkt do lms #############????
            
            
        pTime = 0

        cap = cv2.VideoCapture(0)
        detector = htm.handDetector(maxHands=1)
        
        classic_keyboard = Keyboard()

        handMovingKeyboard = self.getKeyboard(keyboard,classic_keyboard)
        
            

        # print("PUNKT: " + str(self.point))

        self.text_written = str(text)


        while (self.detectionFlag == True):
            success, img = cap.read()
            img = cv2.flip(img, 1)
            img = cv2.resize(img, (1080,768 ))  
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

    def convert_cv_qt(self, cv_img):
        """Convert from an opencv image to QPixmap"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = qtgui.QImage(rgb_image.data, w, h, bytes_per_line, qtgui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(1080, 768)
        return QPixmap.fromImage(p)

    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        qt_img = self.convert_cv_qt(cv_img)
        self.cameraWidget.setPixmap(qt_img)
    



def main():

    try :
            M = Menu()
    
    except Exception as e:
        print(e)
        print("Error in main")
        return
    
    
    
    # F = Feedback(M.text_to_write, M.text_written)

    

if __name__ == '__main__':
    main()
	

# %%
