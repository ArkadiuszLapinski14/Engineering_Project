from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from components.Title import Title
import numpy as np

class Navbar(QWidget):
    def __init__(self, parent = None):
        super(Navbar, self).__init__(parent)
        self.parent = parent
        self.page = "Dashboard"
        self.UIComponents()
    
    def UIComponents(self):
        gridLayout = QGridLayout()
        gridLayout.setSpacing(2)

        background = QLabel(objectName="NavbarBackground")
        
        titleWidget = Title()

        self.dashboardSectionButton = QPushButton("Kamera", objectName="DashboardBtn")
        self.dashboardSectionButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.dashboardSectionButton.clicked.connect(self.DashboardSectionBtnOnClick)

        self.keyboardSectionButton = QPushButton("Klawiatury", objectName="KeyboardsBtn")
        self.keyboardSectionButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.keyboardSectionButton.clicked.connect(self.KeyboardSectionBtnOnClick)

        # self.feedbackSectionButton = QPushButton("Feedback", objectName="FeedbackBtn")
        # self.feedbackSectionButton.setCursor(QCursor(Qt.PointingHandCursor))
        # self.feedbackSectionButton.clicked.connect(self.FeedbackSectionBtnOnClick)

        # self.settingsSectionButton = QPushButton("Settings", objectName="SettingsBtn")
        # self.settingsSectionButton.setCursor(QCursor(Qt.PointingHandCursor))
        # self.settingsSectionButton.clicked.connect(self.SettingsSectionBtnOnClick)

        self.statisticsSectionButton = QPushButton("Statystyki", objectName="StatisticsBtn")
        self.statisticsSectionButton.setCursor(QCursor(Qt.PointingHandCursor))
        self.statisticsSectionButton.clicked.connect(self.StatisticsSectionBtnOnClick)

        # self.tutorialSectionButton = QPushButton("Tutorials", objectName="TutorialsBtn")
        # self.tutorialSectionButton.setCursor(QCursor(Qt.PointingHandCursor))
        # self.tutorialSectionButton.clicked.connect(self.TutorialSectionBtnOnClick)

        self.kBoards = [self.dashboardSectionButton, self.keyboardSectionButton, self.statisticsSectionButton]
        label1 = QLabel("")
        
        gridLayout.addWidget(background, 0, 0, 13, 1)
        gridLayout.addWidget(titleWidget, 0, 0, 1, 1) #1arg - widget, 2arg - row, 3arg - column, 4arg - rowSpan, 5arg - columnSpan
        gridLayout.addWidget(label1, 1, 0, 3, 1)
        gridLayout.addWidget(self.dashboardSectionButton, 4, 0, 1, 1)
        gridLayout.addWidget(self.keyboardSectionButton, 5, 0, 1, 1) 
        # gridLayout.addWidget(self.tutorialSectionButton, 6, 0, 1, 1)
        # gridLayout.addWidget(self.feedbackSectionButton, 7, 0, 1, 1)
        gridLayout.addWidget(self.statisticsSectionButton, 6, 0, 1, 1)
        # gridLayout.addWidget(self.settingsSectionButton, 9, 0, 1, 1)
        self.setLayout(gridLayout)

    
    def KeyboardSectionBtnOnClick(self):
        self.page = "Keyboards"
        self.parent.SetView(self, self.parent.views)

    def DashboardSectionBtnOnClick(self):
        self.page = "Dashboard"
        self.parent.SetView(self, self.parent.views)

    def FeedbackSectionBtnOnClick(self):
        self.page = "Feedback"
        self.parent.SetView(self, self.parent.views)

    def SettingsSectionBtnOnClick(self):
        self.page = "Settings"
        self.parent.SetView(self, self.parent.views)

    def StatisticsSectionBtnOnClick(self):
        self.page = "Statistics"
        self.parent.SetView(self, self.parent.views)

    def TutorialSectionBtnOnClick(self):
        self.page = "Tutorial"
        self.parent.SetView(self, self.parent.views)