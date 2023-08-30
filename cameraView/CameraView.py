from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import requests
import os
import numpy as np
import pandas as pd
import time
import Levenshtein
from scipy.spatial import distance
import textdistance
from components.Launcher import Launcher
from keyboards_back.HandMovingKeyboard import HandMovingKeyboard
from screeninfo import get_monitors


class PixmapLabel(QLabel):
    pixmapChanged = pyqtSignal()

    def setPixmap(self, pixmap):
        super().setPixmap(pixmap)
        self.pixmapChanged.emit()

class CameraView(QWidget):
    def __init__(self, parent = None):
        super(QWidget, self).__init__()
        self.parent = parent
        self.textToWrite = ""
        self.textToCheck = ""
        self.reset = False
        self.pixImgWidth = int(self.frameGeometry().width() * 1.1)
        self.pixImgHeight = int(self.frameGeometry().height() * 1.1)
        self.result = ""
        self.imgData = np.array([])
        self.img = QPixmap()
        self.cameraInit()
        self.UIComponents()

    def UIComponents(self):
        gridLayout = QGridLayout()

        self.testText = QLineEdit(self.textToCheck, objectName="TextToWrite")
        self.testText.textChanged.connect(self.handleTextChange)
        self.testText.returnPressed.connect(self.handleReturn)

        self.confirmResetTextBtn = QToolButton(objectName="ConfirmResetTextBtn")
        self.confirmResetTextBtn.setIcon(QIcon('./assets/acceptIC.png'))
        self.confirmResetTextBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.confirmResetTextBtn.setEnabled(False)
        self.confirmResetTextBtn.clicked.connect(self.handleConfirmClick)

        self.generateTextBtn = QToolButton(objectName="ConfirmResetTextBtn")        
        self.generateTextBtn.setIcon(QIcon('./assets/generateIC.png'))
        self.generateTextBtn.setCursor(QCursor(Qt.PointingHandCursor))  
        self.generateTextBtn.clicked.connect(self.handleGenerateClick)

        self.confirmBtn = QToolButton(objectName="ConfirmResetTextBtn")
        self.confirmBtn.setIcon(QIcon('./assets/acceptIC.png'))
        self.confirmBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.confirmBtn.setEnabled(False)
        self.confirmBtn.clicked.connect(self.handleConfirmAllClick)
        
        self.cameraWidget = PixmapLabel(self)
        self.cameraWidget.pixmapChanged.connect(self.updateCamera)
        self.cameraWidget.hide()
        
        self.resultLabel = QLineEdit(self.result)
        self.resultLabel.textChanged.connect(self.updateLabel)

        self.myText = QLabel(self.resultLabel, objectName="MyText")
        self.myCamera = QLabel(self, objectName="MyCamera")
        self.myCamera.setAlignment(Qt.AlignCenter)
        print(self.myCamera.width())
        movie = QMovie("./assets/loadingXD.gif")
        movie.setScaledSize(QSize(self.pixImgWidth * 0.3, self.pixImgHeight * 0.35))
        self.myCamera.setMovie(movie)
        movie.start()

        gridLayout.addWidget(self.myCamera, 0, 0, 14, 5)
        gridLayout.addWidget(self.testText, 15, 0, 1, 3)
        gridLayout.addWidget(self.confirmResetTextBtn, 15, 3, 1, 1)
        gridLayout.addWidget(self.generateTextBtn, 15, 4, 1, 1)
        gridLayout.addWidget(self.myText, 16, 0 , 1, 4)
        gridLayout.addWidget(self.confirmBtn, 16, 4, 1, 1)
        self.setLayout(gridLayout)

    def cameraInit(self):
        self.Launcher = Launcher()
        self.Launcher.start()
        self.Launcher.started.connect(self.onStart)
        self.Launcher.finished.connect(self.onEnd)
        self.Launcher.data_ready.connect(self.HandleData)
        self.Launcher.keyboardType.connect(self.HandleKeyboardType)
        
    def onStart(self):
        print("Started")

    def onEnd(self):
        print("Finished")

    def HandleData(self, res, img):
        self.result = "".join(res)
        self.textToCheck = "".join(res)
        self.img = self.ConvertCvToQt(img)
        self.cameraWidget.setPixmap(self.img)
        self.resultLabel.setText(self.result)

    def ConvertCvToQt(self, img):
        """Convert from an opencv image to QPixmap"""
        h, w, ch = img.shape
        bytes_per_line = ch * w
        converted_img = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        return QPixmap(converted_img).scaled(self.myCamera.width(), self.myCamera.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)

    def updateLabel(self, text):
        if len(self.textToWrite) < len(self.textToCheck):
            self.myText.setText(text)
            self.myText.setStyleSheet("QLabel { border: 1.5px solid red; }")
        elif self.textToWrite.startswith(self.textToCheck):
            self.myText.setText(text)
            self.myText.setStyleSheet("QLabel { border: 1.5px solid black; }")
        else:
            self.myText.setText(text)
            self.myText.setStyleSheet("QLabel { border: 1.5px solid red; }")

    def updateCamera(self):
        self.myCamera.setPixmap(self.img)

    def handleTextChange(self, text):
        self.textToWrite = text.upper()
        if len(text) > 0:
            self.confirmResetTextBtn.setEnabled(True)
        else:
            self.confirmResetTextBtn.setEnabled(False)   
        self.testText.setText(text.upper())

    def handleReturn(self):
        self.testText.setEnabled(False)
        self.confirmResetTextBtn.setIcon(QIcon('./assets/changeIC.png'))
        self.check(self.textToWrite)

    def handleConfirmClick(self):
        if self.testText.isEnabled() == True:
            self.startTime = time.time()
            self.confirmBtn.setEnabled(True)
            self.reset = True
            self.confirmResetTextBtn.setIcon(QIcon('./assets/changeIC.png'))
        elif self.testText.isEnabled() == False:
            self.confirmBtn.setEnabled(False)
            self.confirmResetTextBtn.setIcon(QIcon('./assets/acceptIC.png'))
        self.testText.setEnabled(not self.testText.isEnabled())
        self.check(self.textToWrite)

    def HandleKeyboardType(self, type):
        if type != None:
            self.type = type
            if self.reset == True:
                self.type.res = []
                self.reset = False

        
    def handleGenerateClick(self):
        paragraphs = '1'
        max_length = '20'
        start_with_lorem_ipsum = "false"
        random = "true"
        api_url = 'https://api.api-ninjas.com/v1/loremipsum?paragraphs='+ paragraphs + '&max_length=' + max_length + '&start_with_lorem_ipsum=' + start_with_lorem_ipsum
        response = requests.get(api_url, headers={'X-Api-Key': 'nAAMyBvCSyh5TiwddgibaQ==92rFNYzdpiywgLD2'})
        if response.status_code == requests.codes.ok:
            data = response.json()
            text = data.get('text')
            if text:
                self.testText.setText(text.upper())
            else:
                print("No 'text' found in the response.")
        else:
            print("Error:", response.status_code, response.text)

    def check(self, text):
        if text.startswith(self.textToCheck):
            self.myText.setStyleSheet("QLabel { border: 1.5px solid black; }")
        else:
            self.myText.setStyleSheet("QLabel { border: 1.5px solid red; }")

    def handleConfirmAllClick(self):
        self.endTime = time.time()
        self.elapsedTime = np.round(self.endTime - self.startTime)
        
        err, rat_ob, jaro_wr = self.getSimilarity(self.textToCheck, self.textToWrite)

        data = {
            "Text": [self.textToWrite], 
            "User Text": [self.textToCheck], 
            "Elapsed Time (seconds)": [self.elapsedTime],
            "Mistakes": [err], 
            "Ratcliff": [rat_ob], 
            "Jaro Winkler": [jaro_wr]
        }

        df = pd.DataFrame(data)

        if os.path.exists("stats.csv"):
            df.to_csv("stats.csv", mode='a', index=False, header=False )
        else:
            df.to_csv("stats.csv", index=False)

        self.reset = True
        self.confirmResetTextBtn.setEnabled(True)
        self.testText.setEnabled(True)
        self.confirmResetTextBtn.setIcon(QIcon('./assets/acceptIC.png'))

    def getSimilarity(self, str1, str2):
        leven = Levenshtein.distance(str1, str2)  #ile transformacji , -
        rat_ob = textdistance.ratcliff_obershelp(str1, str2) #Ratcliff-Obershelp similarity - sekwencja, +
        jaro_wr = textdistance.jaro_winkler(str1, str2)   #jaro winkler - kolejnosc+te same, +
        return leven, rat_ob, jaro_wr


