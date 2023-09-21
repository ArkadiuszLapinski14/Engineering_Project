from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from front.components.Title import Title
import numpy as np
from back.EightPen import EightPen
from back.HandMovingKeyboard import HandMovingKeyboard
from back.HandMovingKeyboardStatic import HandMovingKeyboardStatic
from back.Keyboard import Keyboard
from back.EPKeyboard import EPKeyboard
from back.Hover import Hover
from back.QWERTY import QWERTY
from back.QwertyKeyboard import QwertyKeyboard
from back.HeadMovingKeyboard import HeadMovingKeyboard
from back.HeadMovingKeyboardStatic import HeadMovingKeyboardStatic

class Navbar(QWidget):
    def __init__(self, parent = None):
        super(Navbar, self).__init__(parent)
        self.parent = parent
        self.page = "Dashboard"
        self.keyboardDisplayMethod = ""
        self.keyboardType = "default"
        self.headHand = ""
        self.UIComponents()
    
    def UIComponents(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(2)

        background = QLabel(objectName="NavbarBackground")
        
        titleWidget = Title()

        # self.cameraButton = self.ButtonInit(self.CameraBtnOnClick, "Camera")
        self.headHandButton = self.ButtonInit(self.HeadHandBtnOnClick, "Select Head or Hand")
        self.keyboardDisplayButton = self.ButtonInit(self.KeyboardDisplayBtnOnClick, "Select Display Method")
        self.keyboardTypeButton = self.ButtonInit(self.KeyboardTypeBtnOnClick, "Select Keyboard Type")
        
        label1 = QLabel("")
        
        self.gridLayout.addWidget(background, 0, 0, 13, 2)
        self.gridLayout.addWidget(titleWidget, 0, 0, 1, 2)
        self.gridLayout.addWidget(label1, 1, 0, 3, 2)
        # self.gridLayout.addWidget(self.cameraButton, 4, 0, 1, 2)
        self.gridLayout.addWidget(self.headHandButton, 5, 0, 1, 2)
        
        self.setLayout(self.gridLayout)

    def ButtonInit(self, btnOnClick, title):
        btn = QPushButton(title, objectName="HeadHandBtn")
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.clicked.connect(btnOnClick)
        return btn

    def ButtonReplace(self, toDelete, toReplace, place):
        for btn in toDelete:
            self.gridLayout.removeWidget(btn)

        for btn in toDelete:
            btn.deleteLater()

        self.gridLayout.addWidget(toReplace, place, 0, 1, 2)

    def CameraBtnOnClick(self):
        print("Camera Choose")

    def StatisticsBtnOnClick(self):
        print("Statistics")
        
    def HeadHandBtnOnClick(self):
        self.headHand = ""
        self.keyboardDisplayButton.setEnabled(False)
        self.keyboardTypeButton.setEnabled(False)
        self.headButton = self.ButtonInit(lambda: self.HeadHandOnChange("Head"), "Head")
        self.headButton.setObjectName("MultiBtn")
        self.handButton = self.ButtonInit(lambda: self.HeadHandOnChange("Hand"), "Hand")
        self.handButton.setObjectName("MultiBtn")

        self.gridLayout.removeWidget(self.headHandButton)
        self.headHandButton.deleteLater()

        self.gridLayout.addWidget(self.headButton, 5, 0, 1, 1)
        self.gridLayout.addWidget(self.handButton, 5, 1, 1, 1)

    def HeadHandOnChange(self, title):
        self.headHand = title
        self.keyboardType = ""
        self.keyboardDisplayButton.setEnabled(True)
        self.keyboardTypeButton.setEnabled(True)

        self.keyboardTypeButton.setText("Select Keyboard Type")

        self.headHandButton = self.ButtonInit(self.HeadHandBtnOnClick, title)
        self.ButtonReplace([self.headButton, self.handButton], self.headHandButton, 5)
        self.parent.cameraView.Launcher.keyboardType.emit(None)
        self.gridLayout.addWidget(self.keyboardDisplayButton, 6, 0, 1, 2)
        self.gridLayout.addWidget(self.keyboardTypeButton, 7, 0, 1, 2)


    def KeyboardDisplayBtnOnClick(self):
        self.keyboardDisplayMethod = ""
        self.keyboardTypeButton.setEnabled(False)
        self.headHandButton.setEnabled(False)
        self.circleKboardButton = self.ButtonInit(lambda: self.KeyboardDisplayOnChange(EPKeyboard(), "Circle"), "Circle")
        self.circleKboardButton.setObjectName("MultiBtn")
        self.lineKboardButton = self.ButtonInit(lambda: self.KeyboardDisplayOnChange(Keyboard(), "Line"), "Line")
        self.lineKboardButton.setObjectName("MultiBtn")
        self.QWERTYMethodKboardButton = self.ButtonInit(lambda: self.KeyboardDisplayOnChange(QwertyKeyboard(), "QWERTY"), "QWERTY")
        self.QWERTYMethodKboardButton.setObjectName("MultiBtn")

        self.gridLayout.removeWidget(self.keyboardDisplayButton)
        self.keyboardDisplayButton.deleteLater()

        if self.headHand == "Head":
            self.gridLayout.addWidget(self.circleKboardButton, 6, 0, 1, 1)
            self.gridLayout.addWidget(self.lineKboardButton, 6, 1, 1, 1)
            self.gridLayout.addWidget(self.keyboardTypeButton, 7, 0, 1, 2)
        elif self.headHand == "Hand":
            self.gridLayout.addWidget(self.circleKboardButton, 6, 0, 1, 1)
            self.gridLayout.addWidget(self.lineKboardButton, 6, 1, 1, 1)
            self.gridLayout.addWidget(self.QWERTYMethodKboardButton, 7, 0, 1, 1)
            self.gridLayout.addWidget(self.keyboardTypeButton, 8, 0, 1, 2)


    def KeyboardDisplayOnChange(self, method, title):
        self.keyboardDisplayMethod = title
        self.keyboardType = ""
        self.keyboardDisplayButton = self.ButtonInit(self.KeyboardDisplayBtnOnClick, title)
        self.keyboardTypeButton.setEnabled(True)
        self.headHandButton.setEnabled(True)

        self.keyboardTypeButton.setText("Select Keyboard Type")

        self.parent.cameraView.Launcher.keyboardType.emit(None)
        self.parent.cameraView.Launcher.keyboard.emit(method)
        self.gridLayout.addWidget(self.keyboardTypeButton, 7, 0, 1, 2)
        self.ButtonReplace([self.circleKboardButton, self.lineKboardButton, self.QWERTYMethodKboardButton], self.keyboardDisplayButton, 6)

    def KeyboardTypeBtnOnClick(self):
        self.keyboardType = ""
        self.keyboardDisplayButton.setEnabled(False)
        self.headHandButton.setEnabled(False)
        self.swipeKboardButton = self.ButtonInit(lambda: self.KeyboardTypeOnChange(HandMovingKeyboard(), Keyboard(), "Swipe Dynamic"), "Swipe Dynamic")
        self.swipeKboardButton.setObjectName("MultiBtn")
        self.swipeKboardStaticButton = self.ButtonInit(lambda: self.KeyboardTypeOnChange(HandMovingKeyboardStatic(), Keyboard(), "Swipe Static"), "Swipe Static")
        self.swipeKboardStaticButton.setObjectName("MultiBtn")
        self.eightpenKboardButton = self.ButtonInit(lambda: self.KeyboardTypeOnChange(EightPen(), EPKeyboard(), "EightPen"), "EightPen")
        self.eightpenKboardButton.setObjectName("MultiBtn")
        self.QWERTYHoverKboardButton = self.ButtonInit(lambda: self.KeyboardTypeOnChange(Hover(), Keyboard(), "QWERTY Hover"), "QWERTY Hover")
        self.QWERTYHoverKboardButton.setObjectName("MultiBtn")
        self.QWERTYKboardButton = self.ButtonInit(lambda: self.KeyboardTypeOnChange(QWERTY(), QwertyKeyboard(), "Pinch"), "Pinch")
        self.QWERTYKboardButton.setObjectName("MultiBtn")
        self.headSwipeKboardButton = self.ButtonInit(lambda: self.KeyboardTypeOnChange(HeadMovingKeyboard(), Keyboard(), "Head Swipe Dynamic"), "Swipe Dynamic")
        self.headSwipeKboardButton.setObjectName("MultiBtn")
        self.headSwipeKboardStaticButton = self.ButtonInit(lambda: self.KeyboardTypeOnChange(HeadMovingKeyboardStatic(), Keyboard(), "Head Swipe Static"), "Swipe Static")
        self.headSwipeKboardStaticButton.setObjectName("MultiBtn")
        self.headEightpenKboardButton = self.ButtonInit(lambda: self.KeyboardTypeOnChange(EightPen(methode="head"), EPKeyboard(), "EightPen"), "EightPen")
        self.headEightpenKboardButton.setObjectName("MultiBtn")
        
        self.gridLayout.removeWidget(self.keyboardTypeButton)
        self.keyboardTypeButton.deleteLater()

        if self.headHand == "Hand":
            if self.keyboardDisplayMethod == "Line":
                self.gridLayout.addWidget(self.swipeKboardButton, 7, 0, 1, 1)
                self.gridLayout.addWidget(self.swipeKboardStaticButton, 7, 1, 1, 1)
                self.gridLayout.addWidget(self.QWERTYHoverKboardButton, 8, 0, 1, 1)
            elif self.keyboardDisplayMethod == "Circle":
                self.gridLayout.addWidget(self.eightpenKboardButton, 7, 0, 1, 1)
            elif self.keyboardDisplayMethod == "QWERTY":
                self.gridLayout.addWidget(self.QWERTYKboardButton, 7, 0, 1, 1)
            else:
                self.gridLayout.addWidget(self.swipeKboardButton, 7, 0, 1, 1)
                self.gridLayout.addWidget(self.swipeKboardStaticButton, 8, 0, 1, 1)
                self.gridLayout.addWidget(self.eightpenKboardButton, 7, 1, 1, 1)
                self.gridLayout.addWidget(self.QWERTYHoverKboardButton, 8, 1, 1, 1)
                self.gridLayout.addWidget(self.QWERTYKboardButton, 9, 0, 1, 1)
        elif self.headHand == "Head":
            if self.keyboardDisplayMethod == "Line":
                self.gridLayout.addWidget(self.headSwipeKboardButton, 7, 0, 1, 1)
                self.gridLayout.addWidget(self.headSwipeKboardStaticButton, 7, 1, 1, 1)
            elif self.keyboardDisplayMethod == "Circle":
                self.gridLayout.addWidget(self.headEightpenKboardButton, 7, 0, 1, 1)
            else:
                self.gridLayout.addWidget(self.headSwipeKboardButton, 7, 0, 1, 1)
                self.gridLayout.addWidget(self.headSwipeKboardStaticButton, 7, 1, 1, 1)
                self.gridLayout.addWidget(self.headEightpenKboardButton, 8, 0, 1, 1)

    def KeyboardTypeOnChange(self, type, method, title):
        self.keyboardType = title
        self.keyboardDisplayButton.setEnabled(True)
        self.headHandButton.setEnabled(True)
        self.keyboardTypeButton = self.ButtonInit(self.KeyboardTypeBtnOnClick, title)

        if isinstance(method, Keyboard):
            self.keyboardDisplayButton.setText("Line")
            self.keyboardDisplayMethod = "Line"
        elif isinstance(method, EPKeyboard):
            self.keyboardDisplayButton.setText("Circle")
            self.keyboardDisplayMethod = "Circle"
        elif isinstance(method, QwertyKeyboard):
            self.keyboardDisplayButton.setText("QWERTY")
            self.keyboardDisplayMethod = "QWERTY"

        self.parent.cameraView.Launcher.keyboardType.emit(type)
        self.parent.cameraView.Launcher.keyboard.emit(method)
        self.ButtonReplace([self.headSwipeKboardButton, self.headSwipeKboardStaticButton, self.headEightpenKboardButton, self.swipeKboardButton, self.swipeKboardStaticButton, self.eightpenKboardButton, self.QWERTYHoverKboardButton, self.QWERTYKboardButton], self.keyboardTypeButton, 7)
        
