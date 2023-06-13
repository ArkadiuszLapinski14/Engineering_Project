from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from components.Title import Title
import numpy as np
from keyboards_back.EightPen import EightPen
from keyboards_back.HandMovingKeyboard import HandMovingKeyboard
from keyboards_back.HandMovingKeyboardStatic import HandMovingKeyboardStatic
from keyboards_back.Keyboard import Keyboard
from keyboards_back.EPKeyboard import EPKeyboard
from keyboards_back.Hover import Hover
from keyboards_back.QWERTY import QWERTY
from keyboards_back.QwertyKeyboard import QwertyKeyboard

class Navbar(QWidget):
    def __init__(self, parent = None):
        super(Navbar, self).__init__(parent)
        self.parent = parent
        self.page = "Dashboard"
        self.UIComponents()
    
    def UIComponents(self):
        self.gridLayout = QGridLayout()
        self.gridLayout.setSpacing(2)

        background = QLabel(objectName="NavbarBackground")
        
        titleWidget = Title()

        self.cameraButton = QPushButton("Camera", objectName="CameraBtn")
        self.cameraButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.cameraButton.clicked.connect(self.CameraBtnOnClick)

        self.HeadHandButtonInit("Head")
        self.KeyboardDisplayButtonInit("Keyboard Type")
        self.KeyboardTypeButtonInit("Selection Type")

        self.statisticsButton = QPushButton("Statistics", objectName="StatisticsBtn")
        self.statisticsButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.statisticsButton.clicked.connect(self.StatisticsBtnOnClick)
        label1 = QLabel("")
        
        self.gridLayout.addWidget(background, 0, 0, 13, 2)
        self.gridLayout.addWidget(titleWidget, 0, 0, 1, 2)
        self.gridLayout.addWidget(label1, 1, 0, 3, 2)
        self.gridLayout.addWidget(self.cameraButton, 4, 0, 1, 2)
        self.gridLayout.addWidget(self.headHandButton, 5, 0, 1, 2)
        self.gridLayout.addWidget(self.keyboardDisplayButton, 6, 0, 1, 2)
        self.gridLayout.addWidget(self.keyboardTypeButton, 7, 0, 3, 2)
        self.gridLayout.addWidget(self.statisticsButton, 10, 0, 1, 2)
        
        self.setLayout(self.gridLayout)

    def CameraBtnOnClick(self):
        print("Camera Choose")

    def StatisticsBtnOnClick(self):
        print("Statistics")
        
    def HeadHandBtnOnClick(self):
        self.headButton = QPushButton("Head", objectName="HeadHandBtn")
        self.headButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.headButton.clicked.connect(self.HeadOnClick) #######TO WAZNE
        self.handButton = QPushButton("Hand", objectName="HeadHandBtn")
        self.handButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.handButton.clicked.connect(self.HandOnClick)

        self.gridLayout.removeWidget(self.headHandButton)
        self.headHandButton.deleteLater()

        self.gridLayout.addWidget(self.headButton, 5, 0, 1, 1)
        self.gridLayout.addWidget(self.handButton, 5, 1, 1, 1)

    def HeadOnClick(self):
        self.HeadHandButtonInit("Head")
        self.HeadHandReplace()

    def HandOnClick(self):
        self.HeadHandButtonInit("Hand")
        self.HeadHandReplace()
        
    def HeadHandReplace(self):
        self.gridLayout.removeWidget(self.headButton)
        self.gridLayout.removeWidget(self.handButton)
        self.headButton.deleteLater()
        self.handButton.deleteLater()

        self.gridLayout.addWidget(self.headHandButton, 5, 0, 1, 2)

    def HeadHandButtonInit(self, title):
        self.headHandButton = QPushButton(title, objectName="HeadHandBtn")
        self.headHandButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.headHandButton.clicked.connect(self.HeadHandBtnOnClick)

    def KeyboardDisplayBtnOnClick(self):
        self.circleKboardButton = QPushButton("Circle Keyboard", objectName="HeadHandBtn")
        self.circleKboardButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.circleKboardButton.clicked.connect(self.CircleKboardOnClick)
        self.circleKboardButton.setEnabled(False)

        self.lineKboardButton = QPushButton("Line Keyboard", objectName="HeadHandBtn")
        self.lineKboardButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.lineKboardButton.clicked.connect(self.LineKboardOnClick)
        self.lineKboardButton.setEnabled(False)

        self.gridLayout.removeWidget(self.keyboardDisplayButton)
        self.keyboardDisplayButton.deleteLater()

        self.gridLayout.addWidget(self.circleKboardButton, 6, 0, 1, 1)
        self.gridLayout.addWidget(self.lineKboardButton, 6, 1, 1, 1)

    def CircleKboardOnClick(self):
        self.KeyboardDisplayButtonInit("Circle Keyboard")
        self.parent.cameraView.Launcher.keyboard.emit(EPKeyboard())
        self.KeyboardReplace()


    def LineKboardOnClick(self):
        self.KeyboardDisplayButtonInit("Line Keyboard")
        self.parent.cameraView.Launcher.keyboard.emit(Keyboard())
        self.KeyboardReplace()

    def KeyboardDisplayButtonInit(self, title):
        self.keyboardDisplayButton = QPushButton(title, objectName="KboardDisplayBtn")
        self.keyboardDisplayButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.keyboardDisplayButton.clicked.connect(self.KeyboardDisplayBtnOnClick)
        self.keyboardDisplayButton.setEnabled(False)

    def KeyboardReplace(self):
        self.gridLayout.removeWidget(self.circleKboardButton)
        self.gridLayout.removeWidget(self.lineKboardButton)
        self.circleKboardButton.deleteLater()
        self.lineKboardButton.deleteLater()

        self.gridLayout.addWidget(self.keyboardDisplayButton, 6, 0, 1, 2)

    def KeyboardTypeButtonInit(self, title):
        self.keyboardTypeButton = QPushButton(title, objectName="KboardDisplayBtn")
        self.keyboardTypeButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.keyboardTypeButton.clicked.connect(self.KeyboardTypeBtnOnClick)

    def KeyboardTypeBtnOnClick(self):
        self.swipeKboardButton = QPushButton("Swipe Dynamic", objectName="HeadHandBtn")
        self.swipeKboardButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.swipeKboardButton.clicked.connect(self.SwipeKboardOnClick)

        self.swipeKboardStaticButton = QPushButton("Swipe Static", objectName="HeadHandBtn")
        self.swipeKboardStaticButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.swipeKboardStaticButton.clicked.connect(self.SwipeKboardStaticOnClick)

        self.eightpenKboardButton = QPushButton("EightPen", objectName="HeadHandBtn")
        self.eightpenKboardButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.eightpenKboardButton.clicked.connect(self.EightPenKboardOnClick)

        self.QWERTYHoverKboardButton = QPushButton("QWERTY Hover", objectName="HeadHandBtn")
        self.QWERTYHoverKboardButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.QWERTYHoverKboardButton.clicked.connect(self.QWERTYHoverKboardOnClick)

        self.QWERTYKboardButton = QPushButton("QWERTY", objectName="HeadHandBtn")
        self.QWERTYKboardButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.QWERTYKboardButton.clicked.connect(self.QWERTYKboardOnClick)

        self.gridLayout.removeWidget(self.keyboardTypeButton)
        self.keyboardTypeButton.deleteLater()

        self.gridLayout.addWidget(self.swipeKboardButton, 7, 0, 1, 1)
        self.gridLayout.addWidget(self.swipeKboardStaticButton, 8, 0, 1, 1)
        self.gridLayout.addWidget(self.eightpenKboardButton, 7, 1, 1, 1)
        self.gridLayout.addWidget(self.QWERTYHoverKboardButton, 8, 1, 1, 1)
        self.gridLayout.addWidget(self.QWERTYKboardButton, 9, 0, 1, 1)
        

    def SwipeKboardOnClick(self):
        self.KeyboardTypeButtonInit("Swipe Dynamic")
        self.parent.cameraView.Launcher.keyboardType.emit(HandMovingKeyboard())
        self.parent.cameraView.Launcher.keyboard.emit(Keyboard())
        self.KeyboardTypeReplace()

    def SwipeKboardStaticOnClick(self):
        self.KeyboardTypeButtonInit("Swipe Static")
        self.parent.cameraView.Launcher.keyboardType.emit(HandMovingKeyboardStatic())
        self.parent.cameraView.Launcher.keyboard.emit(Keyboard())
        self.KeyboardTypeReplace()

    def EightPenKboardOnClick(self):
        self.KeyboardTypeButtonInit("EightPen")
        self.parent.cameraView.Launcher.keyboardType.emit(EightPen())
        self.parent.cameraView.Launcher.keyboard.emit(EPKeyboard())
        self.KeyboardTypeReplace()

    def QWERTYHoverKboardOnClick(self):
        self.KeyboardTypeButtonInit("QWERTY Hover")
        self.parent.cameraView.Launcher.keyboardType.emit(Hover())
        self.parent.cameraView.Launcher.keyboard.emit(Keyboard())
        self.KeyboardTypeReplace()

    def QWERTYKboardOnClick(self):
        self.KeyboardTypeButtonInit("QWERTY")
        self.parent.cameraView.Launcher.keyboardType.emit(QWERTY())
        self.parent.cameraView.Launcher.keyboard.emit(QwertyKeyboard())
        self.KeyboardTypeReplace()
        
    def KeyboardTypeReplace(self):
        self.gridLayout.removeWidget(self.swipeKboardButton)
        self.gridLayout.removeWidget(self.swipeKboardStaticButton)
        self.gridLayout.removeWidget(self.eightpenKboardButton)
        self.gridLayout.removeWidget(self.QWERTYHoverKboardButton)
        self.gridLayout.removeWidget(self.QWERTYKboardButton)
        self.swipeKboardButton.deleteLater()
        self.swipeKboardStaticButton.deleteLater()
        self.eightpenKboardButton.deleteLater()
        self.QWERTYHoverKboardButton.deleteLater()
        self.QWERTYKboardButton.deleteLater()

        self.gridLayout.addWidget(self.keyboardTypeButton, 7, 0, 3, 2)
