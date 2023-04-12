from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from components.Navbar import Navbar
from components.RegisterPanel import RegisterPanel
from keyboards_back.HandMovingKeyboard import HandMovingKeyboard
from keyboards_back.HandMovingKeyboardStatic import HandMovingKeyboardStatic
from keyboards_back.EightPen import EightPen
from components.Launcher import Launcher
from components.LaunchingObject import LaunchingObject
import threading
import queue

class Hand(QWidget):
    def __init__(self, parent = None):
        super(Hand, self).__init__(parent)
        self.parent = parent
        print("Hand")
        self.UIComponents()

    def UIComponents(self):
        gridLayout = QGridLayout()
        self.keyboards = RegisterPanel()
        self.RegisterKeyboards()
        
        self.HandMovingKeyboardSectionBtn = QPushButton("Hand Moving Keyboard", objectName="HandMovingBtn")
        self.HandMovingKeyboardSectionBtn.clicked.connect(self.HandMovingKeyboardSectionBtnOnClick)
        self.HandMovingKeyboardSectionBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.HandMovingStaticKeyboardSectionBtn = QPushButton("Hand Moving Static Keyboard", objectName="HandMovingStaticBtn")
        self.HandMovingStaticKeyboardSectionBtn.clicked.connect(self.HandMovingStaticKeyboardSectionBtnOnClick)
        self.HandMovingStaticKeyboardSectionBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.EightPenSectionBtn = QPushButton("EightPen", objectName="EightPenHandBtn")
        self.EightPenSectionBtn.clicked.connect(self.EightPenSectionBtnOnClick)
        self.EightPenSectionBtn.setCursor(QCursor(Qt.PointingHandCursor))

        gridLayout.addWidget(self.HandMovingKeyboardSectionBtn, 3, 0 , 1, 1)
        gridLayout.addWidget(self.HandMovingStaticKeyboardSectionBtn, 3, 1 , 1, 1)
        gridLayout.addWidget(self.EightPenSectionBtn, 3, 2 , 1, 1)

        self.setLayout(gridLayout)

    def RegisterKeyboards(self):
        self.keyboards.register("HandMoving", lambda:HandMovingKeyboard())
        self.keyboards.register("HandMovingStatic", lambda:HandMovingKeyboardStatic())
        self.keyboards.register("EightPen", lambda:EightPen("palec"))

    def HandMovingKeyboardSectionBtnOnClick(self):
        self.Launcher = Launcher(HandMovingKeyboard())
        self.Launcher.start()
        self.Launcher.started.connect(self.onEnd)
        self.Launcher.finished.connect(self.onEnd)
        self.Launcher.data_ready.connect(self.HandleData)

    def HandleData(self,data):
        self.result = "".join(data)
    
    def onEnd(self):
        print("essa")
        self.parent.SetView(self.parent.views, "KeyboardsText")


    def HandMovingStaticKeyboardSectionBtnOnClick(self):
        Launcher(self.keyboards.getInstance("HandMovingStatic"))

    def EightPenSectionBtnOnClick(self):
        Launcher(self.keyboards.getInstance("EightPen"))

    def ConvertCvToQt(self, img):
        """Convert from an opencv image to QPixmap"""
        h, w, ch = img.shape
        bytes_per_line = ch * w
        converted_img = QImage(img.data, w, h, bytes_per_line, QImage.Format_RGB888).rgbSwapped()
        return QPixmap(converted_img)