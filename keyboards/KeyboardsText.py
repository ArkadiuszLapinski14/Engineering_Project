from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class KeyboardsText(QWidget):
    def __init__(self, parent = None):
        super(QWidget, self).__init__()
        self.parent = parent
        self.UIComponents()
        self.parent.resultLabel.textChanged.connect(self.updateLabel)
        self.parent.cameraWidget.pixmapChanged.connect(self.updateCamera)

    def UIComponents(self):
        gridLayout = QGridLayout()

        self.myText = QLabel(self.parent.resultLabel, objectName="MyText")
        self.myCamera = QLabel(self, objectName="MyCamera")

        gridLayout.addWidget(self.myCamera, 0, 0, 5, 5)
        gridLayout.addWidget(self.myText, 6, 0 , 1, 5)
        self.setLayout(gridLayout)

    def updateLabel(self, text):
        self.myText.setText(text)

    def updateCamera(self):
        self.myCamera.setPixmap(self.parent.img)
