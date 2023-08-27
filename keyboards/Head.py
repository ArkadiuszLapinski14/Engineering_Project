from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from navbar.Navbar import Navbar

class Head(QWidget):
    def __init__(self, parent = None):
        super(Head, self).__init__(parent)
        self.parent = parent
        print("Head")
        self.UIComponents()

    def UIComponents(self):
        gridLayout = QGridLayout()

        self.EightPenKeyboardSectionBtn = QPushButton("Eight Pen", objectName="EightPenHeadBtn")
        self.EightPenKeyboardSectionBtn.clicked.connect(self.EightPenKeyboardSectionBtnOnClick)
        self.HeadMovingKeyboardSectionBtn = QPushButton("Head Moving Keyboard", objectName="HeadMovingBtn")
        self.HeadMovingKeyboardSectionBtn.clicked.connect(self.HeadMovingKeyboardSectionBtnOnClick)

        gridLayout.addWidget(self.EightPenKeyboardSectionBtn, 3, 0 , 1, 1)
        gridLayout.addWidget(self.HeadMovingKeyboardSectionBtn, 3, 1 , 1, 1)

        self.setLayout(gridLayout)

    def EightPenKeyboardSectionBtnOnClick(self):
        pass
        #Tutaj podlaczyc klawiatury

    def HeadMovingKeyboardSectionBtnOnClick(self):
        pass
        #Tutaj podlaczyc klawiatury
