from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import requests

class KeyboardsText(QWidget):
    def __init__(self, parent = None):
        super(QWidget, self).__init__()
        self.parent = parent
        self.text = ""
        self.textToCheck = ""
        self.UIComponents()
        self.parent.resultLabel.textChanged.connect(self.updateLabel)
        self.parent.cameraWidget.pixmapChanged.connect(self.updateCamera)

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

        self.myText = QLabel(self.parent.resultLabel, objectName="MyText")
        self.myCamera = QLabel(self, objectName="MyCamera")

        gridLayout.addWidget(self.myCamera, 0, 0, 5, 5)
        gridLayout.addWidget(self.textToWrite, 6, 0, 1 , 3)
        gridLayout.addWidget(self.confirmResetTextBtn, 6, 3, 1, 1)
        gridLayout.addWidget(self.generateTextBtn, 6, 4, 1, 1)
        gridLayout.addWidget(self.myText, 7, 0 , 1, 5)
        self.setLayout(gridLayout)

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
        self.myCamera.setPixmap(self.parent.img)

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