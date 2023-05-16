from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class Title(QWidget):
    def __init__(self):
        super(Title, self).__init__()
        self.pixImgWidth = int(self.frameGeometry().width() * 0.10)
        self.pixImgHeight = int(self.frameGeometry().height() * 0.13)
        self.UIComponents()

    def UIComponents(self):
        self.setStyleSheet("background-color: #F8F8F8;")

        gridLayout = QGridLayout()
        gridLayout.setSpacing(0)

        labelTitle = QLabel("CLess KBoards", objectName="LabelTitle")

        pixImg = QPixmap("./assets/keyboard.png").scaled(self.pixImgWidth, self.pixImgHeight, transformMode=Qt.SmoothTransformation)
        img = QLabel(objectName="Logo")
        img.setPixmap(pixImg)

        gridLayout.addWidget(img, 0, 0, 1, 1)
        gridLayout.addWidget(labelTitle, 0, 1, 1, 1)
        self.setLayout(gridLayout)