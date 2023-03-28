from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from components.Title import Title
import numpy as np

class Navbar(QWidget):
    def __init__(self):
        super(Navbar, self).__init__()
        self.page = "Dashboard"
        self.UIComponents()
    
    def UIComponents(self):
        gridLayout = QGridLayout()
        gridLayout.setSpacing(2)

        background = QLabel(objectName="NavbarBackground")
        
        titleWidget = Title()

        self.dashboardSectionButton = QPushButton("Dashboard", objectName="DashboardBtn")
        self.dashboardSectionButton.clicked.connect(self.DashboardSectionBtnOnClick)
        self.keyboardSectionButton = QPushButton("Keyboards", objectName="KeyboardsBtn")
        self.keyboardSectionButton.clicked.connect(self.KeyboardSectionBtnOnClick)
        self.feedbackSectionButton = QPushButton("Feedback", objectName="FeedbackBtn")
        self.feedbackSectionButton.clicked.connect(self.FeedbackSectionBtnOnClick)
        self.settingsSectionButton = QPushButton("Settings", objectName="SettingsBtn")
        self.settingsSectionButton.clicked.connect(self.SettingsSectionBtnOnClick)
        self.statisticsSectionButton = QPushButton("Statistics", objectName="StatisticsBtn")
        self.statisticsSectionButton.clicked.connect(self.StatisticsSectionBtnOnClick)
        self.tutorialSectionButton = QPushButton("Tutorials", objectName="TutorialsBtn")
        self.tutorialSectionButton.clicked.connect(self.TutorialSectionBtnOnClick)

        self.kBoards = [self.dashboardSectionButton, self.keyboardSectionButton, self.feedbackSectionButton, self.settingsSectionButton, self.statisticsSectionButton, self.tutorialSectionButton]
        label = QLabel("")
        label1 = QLabel("")
        
        gridLayout.addWidget(background, 0, 0, 13, 1)
        gridLayout.addWidget(titleWidget, 0, 0, 1, 1) #1arg - widget, 2arg - row, 3arg - column, 4arg - rowSpan, 5arg - columnSpan
        gridLayout.addWidget(label1, 1, 0, 3, 1)
        gridLayout.addWidget(self.dashboardSectionButton, 4, 0, 1, 1)
        gridLayout.addWidget(self.keyboardSectionButton, 5, 0, 1, 1) 
        gridLayout.addWidget(self.tutorialSectionButton, 6, 0, 1, 1)
        gridLayout.addWidget(self.feedbackSectionButton, 7, 0, 1, 1)
        gridLayout.addWidget(self.statisticsSectionButton, 8, 0, 1, 1)
        gridLayout.addWidget(self.settingsSectionButton, 9, 0, 1, 1)
        gridLayout.addWidget(label, 0, 1, 3, 3)
        self.setLayout(gridLayout)

    
    def KeyboardSectionBtnOnClick(self):
        # [kBoard.setStyleSheet("color: black;" "font-weight: normal") for kBoard in self.kBoards]
        # self.keyboardSectionButton.setStyleSheet("color: #720e9e;" "font-weight: bold")
        self.page = "Keyboards"

    def DashboardSectionBtnOnClick(self):
        # [kBoard.setStyleSheet("color: black;" "font-weight: normal") for kBoard in self.kBoards]
        # self.dashboardSectionButton.setStyleSheet("color: #720e9e;" "font-weight: bold")
        self.page = "Dashboard"

    def FeedbackSectionBtnOnClick(self):
        [kBoard.setStyleSheet("color: black;" "font-weight: normal") for kBoard in self.kBoards]
        self.feedbackSectionButton.setStyleSheet("color: #720e9e;" "font-weight: bold")
        self.page = "Feedback"

    def SettingsSectionBtnOnClick(self):
        [kBoard.setStyleSheet("color: black;" "font-weight: normal") for kBoard in self.kBoards]
        self.settingsSectionButton.setStyleSheet("color: #720e9e;" "font-weight: bold")
        self.page = "Settings"

    def StatisticsSectionBtnOnClick(self):
        [kBoard.setStyleSheet("color: black;" "font-weight: normal") for kBoard in self.kBoards]
        self.statisticsSectionButton.setStyleSheet("color: #720e9e;" "font-weight: bold")
        self.page = "Statistics"

    def TutorialSectionBtnOnClick(self):
        [kBoard.setStyleSheet("color: black;" "font-weight: normal") for kBoard in self.kBoards]
        self.tutorialSectionButton.setStyleSheet("color: #720e9e;" "font-weight: bold")
        self.page = "Tutorial"