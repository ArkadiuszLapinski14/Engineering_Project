from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from components.Navbar import Navbar
from keyboards.Head import Head
from keyboards.Hand import Hand

class HeadHandChoose(QWidget):
    def __init__(self, parent = None):
        super(HeadHandChoose, self).__init__(parent)
        self.parent = parent
        self.pixImgWidth = int(self.frameGeometry().width() * 3)
        self.pixImgHeight = int(self.frameGeometry().height() * 9)
        print("HeadHandChoose")
        self.UIComponents()

    def UIComponents(self):
        gridLayout = QGridLayout()
        gridLayout.setSpacing(0)

        self.HeadSectionBtn = QPushButton("Head", objectName="HeadBtn")
        self.HeadSectionBtn.setCursor(QCursor(Qt.PointingHandCursor))
        self.HeadSectionBtn.clicked.connect(self.HeadSectionBtnOnClick)

        self.HandSectionBtn = QPushButton("Hand", objectName="HandBtn")
        self.HandSectionBtn.clicked.connect(self.HandSectionBtnOnClick)
        self.HandSectionBtn.setCursor(QCursor(Qt.PointingHandCursor))

        pixImgHead = QPixmap("./assets/face_detect.png").scaled(self.pixImgWidth, self.pixImgHeight, transformMode=Qt.SmoothTransformation)
        imgHead = QLabel(objectName="FaceDetectionImg")
        imgHead.setPixmap(pixImgHead)   

        pixImgHand = QPixmap("./assets/hand_detect.png").scaled(self.pixImgWidth, self.pixImgHeight, transformMode=Qt.SmoothTransformation)
        imgHand = QLabel(objectName="HandDetectionImg")
        imgHand.setPixmap(pixImgHand)

        headDescriptionTitle = QLabel(objectName="HeadDescriptionTitle")
        headDescriptionTitle.setText("Details")
        headDescription = QLabel(objectName="HeadDescription")
        headDescription.setText("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus auctor elementum nulla vitae sagittis. In at vehicula nulla. Sed id ex vitae diam vehicula accumsan. Nullam porta quis justo ut faucibus. Donec non mauris tempor urna fermentum rhoncus ut sed felis. Morbi rutrum diam et ante ultricies vehicula. ")
        headDescription.setWordWrap(True)

        handDescriptionTitle = QLabel(objectName="HandDescriptionTitle")
        handDescriptionTitle.setText("Details")
        handDescription = QLabel(objectName="HandDescription")
        handDescription.setText("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Phasellus auctor elementum nulla vitae sagittis. In at vehicula nulla. Sed id ex vitae diam vehicula accumsan. Nullam porta quis justo ut faucibus. Donec non mauris tempor urna fermentum rhoncus ut sed felis. Morbi rutrum diam et ante ultricies vehicula. ")
        handDescription.setWordWrap(True)

        gridLayout.addWidget(self.HeadSectionBtn, 0, 0 , 1, 1)
        gridLayout.addWidget(self.HandSectionBtn, 0, 1 , 1, 1)
        gridLayout.addWidget(imgHead, 1, 0, 1, 1)
        gridLayout.addWidget(imgHand, 1, 1, 1, 1)
        gridLayout.addWidget(headDescriptionTitle, 2, 0, 1, 1)
        gridLayout.addWidget(headDescription, 3, 0, 1, 1)
        gridLayout.addWidget(handDescriptionTitle, 2, 1, 1, 1)
        gridLayout.addWidget(handDescription, 3, 1, 1, 1)

        self.setLayout(gridLayout)

    def HeadSectionBtnOnClick(self):
        self.parent.SetView(Head(self.parent))

    def HandSectionBtnOnClick(self):
        self.parent.SetView(Hand(self.parent))