from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from components.Navbar import Navbar

class Hand(QWidget):
    def __init__(self, parent = None):
        super(Hand, self).__init__(parent)
        self.parent = parent
        print("Hand")
        self.UIComponents()

    def UIComponents(self):
        gridLayout = QGridLayout()

        self.HandMovingKeyboardSectionBtn = QPushButton("Hand Moving Keyboard", objectName="HandMovingBtn")
        self.HandMovingKeyboardSectionBtn.clicked.connect(self.HandMovingKeyboardSectionBtnOnClick)
        self.HandMovingStaticKeyboardSectionBtn = QPushButton("Hand Moving Static Keyboard", objectName="HandMovingStaticBtn")
        self.HandMovingStaticKeyboardSectionBtn.clicked.connect(self.HandMovingStaticKeyboardSectionBtnOnClick)
        self.EightPenSectionBtn = QPushButton("EightPen", objectName="EightPenHandBtn")
        self.EightPenSectionBtn.clicked.connect(self.EightPenSectionBtnOnClick)

        gridLayout.addWidget(self.HandMovingKeyboardSectionBtn, 3, 0 , 1, 1)
        gridLayout.addWidget(self.HandMovingStaticKeyboardSectionBtn, 3, 1 , 1, 1)
        gridLayout.addWidget(self.EightPenSectionBtn, 3, 2 , 1, 1)

        self.setLayout(gridLayout)

    def HandMovingKeyboardSectionBtnOnClick(self):
        pass
        #Tutaj podlaczyc klawiatury
    
    def HandMovingStaticKeyboardSectionBtnOnClick(self):
        pass
        #Tutaj podlaczyc klawiatury

    def EightPenSectionBtnOnClick(self):
        pass
        #Tutaj podlaczyc klawiatury
