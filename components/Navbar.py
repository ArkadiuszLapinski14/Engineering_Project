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