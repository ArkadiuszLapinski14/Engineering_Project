from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from components.Navbar import Navbar

class HeadHandChoose(QWidget):
    def __init__(self, parent = None):
        super(HeadHandChoose, self).__init__(parent)
        self.parent = parent
        print("HeadHandChoose")
        self.UIComponents()

    def UIComponents(self):
        gridLayout = QGridLayout()

        self.HeadSectionBtn = QPushButton("Head", objectName="HeadBtn")
        self.HeadSectionBtn.clicked.connect(self.HeadSectionBtnOnClick)
        self.HandSectionBtn = QPushButton("Hand", objectName="HandBtn")
        self.HandSectionBtn.clicked.connect(self.HandSectionBtnOnClick)

        gridLayout.addWidget(self.HeadSectionBtn, 3, 0 , 1, 1)
        gridLayout.addWidget(self.HandSectionBtn, 3, 1 , 1, 1)

        self.setLayout(gridLayout)

    def HeadSectionBtnOnClick(self):
        self.parent.SetView(self.parent.views, "Head")

    def HandSectionBtnOnClick(self):
        self.parent.SetView(self.parent.views, "Hand")