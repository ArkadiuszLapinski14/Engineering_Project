from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from components.Title import Title

class Navbar(QWidget):
    def __init__(self):
        super(Navbar, self).__init__()
        self.UIComponents()
    
    def UIComponents(self):
        gridLayout = QGridLayout()

        titleWidget = Title()

        dashboardSectionButton = QPushButton("Dashboard")
        keyboardSectionButton = QPushButton("Keyboards")
        feedbackSectionButton = QPushButton("Feedback")
        settingsSectionButton = QPushButton("Settings")
        statisticsSectionButton = QPushButton("Statistics")
        tutorialSectionButton = QPushButton("Tutorials")
        label = QLabel("")
        label1 = QLabel("")
        
        gridLayout.addWidget(titleWidget, 0, 0, 1, 1) #1arg - widget, 2arg - row, 3arg - column, 4arg - rowSpan, 5arg - columnSpan
        gridLayout.addWidget(label1, 1, 0, 3, 1)
        gridLayout.addWidget(dashboardSectionButton, 4, 0, 1, 1)
        gridLayout.addWidget(keyboardSectionButton, 5, 0, 1, 1) 
        gridLayout.addWidget(tutorialSectionButton, 6, 0, 1, 1)
        gridLayout.addWidget(feedbackSectionButton, 7, 0, 1, 1)
        gridLayout.addWidget(statisticsSectionButton, 8, 0, 1, 1)
        gridLayout.addWidget(settingsSectionButton, 9, 0, 1, 1)
        gridLayout.addWidget(label, 0, 1, 3, 3)
        self.setLayout(gridLayout)
