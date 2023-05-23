from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import requests
import numpy as np
from components.Launcher import Launcher
from keyboards_back.HandMovingKeyboard import HandMovingKeyboard

class PixmapLabel(QLabel):
    pixmapChanged = pyqtSignal()

    def setPixmap(self, pixmap):
        super().setPixmap(pixmap)
        self.pixmapChanged.emit()

class CameraView(QWidget):
    def __init__(self, parent = None):
        super(QWidget, self).__init__()
        self.parent = parent
        self.text = ""
        self.textToCheck = ""
        self.pixImgWidth = int(self.frameGeometry().width() * 1.13)
        self.pixImgHeight = int(self.frameGeometry().height() * 1.08)
        self.result = ""
        self.imgData = np.array([])
        self.img = QPixmap()
        self.cameraInit()
        self.UIComponents()

    def UIComponents(self):
        gridLayout = QGridLayout()

        self.textToWrite = QLineEdit(self.textToCheck, objectName="TextToWrite")
        self.textToWrite.textChanged.connect(self.handleTextChange)
        self.textToWrite.returnPressed.connect(self.handleReturn)

        self.confirmResetTextBtn = QToolButton(objectName="ConfirmResetTextBtn")
        self.confirmResetTextBtn.setIcon(QIcon('./assets/acceptIC.png'))
        self.confirmResetTextBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.confirmResetTextBtn.clicked.connect(self.handleConfirmClick)

        self.generateTextBtn = QToolButton(objectName="ConfirmResetTextBtn")        
        self.generateTextBtn.setIcon(QIcon('./assets/generateIC.png'))
        self.generateTextBtn.setCursor(QCursor(Qt.PointingHandCursor))  
        self.generateTextBtn.clicked.connect(self.handleGenerateClick)
        
        self.cameraWidget = PixmapLabel(self)
        self.cameraWidget.pixmapChanged.connect(self.updateCamera)
        self.cameraWidget.hide()
        
        self.resultLabel = QLineEdit(self.result)
        self.resultLabel.textChanged.connect(self.updateLabel)

        self.myText = QLabel(self.resultLabel, objectName="MyText")
        self.myCamera = QLabel(self, objectName="MyCamera")
        self.myCamera.setAlignment(Qt.AlignCenter)
        movie = QMovie("./assets/loadingXD.gif")
        movie.setScaledSize(QSize(self.pixImgWidth * 0.3, self.pixImgHeight * 0.35))
        self.myCamera.setMovie(movie)
        movie.start()

        gridLayout.addWidget(self.myCamera, 0, 0, 14, 5)
        gridLayout.addWidget(self.textToWrite, 15, 0, 1, 3)
        gridLayout.addWidget(self.confirmResetTextBtn, 15, 3, 1, 1)
        gridLayout.addWidget(self.generateTextBtn, 15, 4, 1, 1)
        gridLayout.addWidget(self.myText, 16, 0 , 1, 5)
        self.setLayout(gridLayout)

    def cameraInit(self):
        self.Launcher = Launcher()
        self.Launcher.start()
        self.Launcher.started.connect(self.onStart)
        self.Launcher.finished.connect(self.onEnd)
        self.Launcher.data_ready.connect(self.HandleData)
        
    def onStart(self):
        print("Started")

    def onEnd(self):
        print("Finished")

    def HandleData(self, res, img):
        self.result = "".join(res)
        self.img = self.ConvertCvToQt(img)
        self.cameraWidget.setPixmap(self.img)
        self.resultLabel.setText(self.result)

    def ConvertCvToQt(self, img):
        """Convert from an opencv image to QPixmap"""
        h, w, ch = img.shape
        bytes_per_line = ch * w
        converted_img = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        return QPixmap(converted_img).scaled(self.pixImgWidth, self.pixImgHeight, transformMode=Qt.SmoothTransformation)

    def updateLabel(self, text):
        if self.textToCheck.startswith(text):
            self.textToCheck = text
            self.myText.setText(text)
            self.myText.setStyleSheet("QLabel { border: 1.5px solid black; }")
        else:
            self.textToCheck = text
            self.myText.setText(text)
            self.myText.setStyleSheet("QLabel { border: 1.5px solid red; }")

    def updateCamera(self):
        self.myCamera.setPixmap(self.img)

    def handleTextChange(self, text):   
        self.text = text.upper()
        self.textToWrite.setText(text.upper())

    def handleReturn(self):
        self.textToWrite.setEnabled(False)
        self.confirmResetTextBtn.setIcon(QIcon('./assets/changeIC.png'))
        self.check(self.text)

    def handleConfirmClick(self):
        if self.textToWrite.isEnabled() == True:
            self.confirmResetTextBtn.setIcon(QIcon('./assets/changeIC.png'))
        elif self.textToWrite.isEnabled() == False:
            self.confirmResetTextBtn.setIcon(QIcon('./assets/acceptIC.png'))
        self.textToWrite.setEnabled(not self.textToWrite.isEnabled())
        self.check(self.text)

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
                self.textToWrite.setText(text.upper())
            else:
                print("No 'text' found in the response.")
        else:
            print("Error:", response.status_code, response.text)

    def check(self, text):
        if text.startswith(self.textToCheck):
            self.myText.setStyleSheet("QLabel { border: 1.5px solid black; }")
        else:
            self.myText.setStyleSheet("QLabel { border: 1.5px solid red; }")