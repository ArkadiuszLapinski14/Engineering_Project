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
        self.setStyleSheet("background-color: #e0e0e0;")

        gridLayout = QGridLayout()
        gridLayout.setSpacing(0)

        labelTitle = QLabel("Contactless Keyboards")
        labelTitle.setStyleSheet("font-size: 17pt;"
                                 "font-weight: bold;"
                                 "font-family: Arial, Helvetica, sans-serif;"
                                 "border-top-right-radius: 20px;"
                                 "border-bottom-right-radius: 20px;"
                                 "padding: 7px;"
                                 )
        
        pixImg = QPixmap("./assets/keyboard.png").scaled(self.pixImgWidth, self.pixImgHeight, transformMode=Qt.SmoothTransformation)
        img = QLabel()
        img.setPixmap(pixImg)
        img.setStyleSheet("border-top-left-radius: 20px;"
                          "border-bottom-left-radius: 20px;"
                          "padding: 7px;")

        gridLayout.addWidget(img, 0, 0, 1, 1)
        gridLayout.addWidget(labelTitle, 0, 1, 1, 1)
        self.setLayout(gridLayout)