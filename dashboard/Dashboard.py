from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from components.Navbar import Navbar

class Dashboard(QWidget):
    def __init__(self):
        super(Dashboard, self).__init__()
        self.UIComponents()

    def UIComponents(self):
        gridLayout = QGridLayout()
        
        navbar = Navbar()
        navbar.findChild(QPushButton, "DashboardBtn").setStyleSheet("color: #720e9e;" "font-weight: bold")

        gridLayout.addWidget(navbar, 0, 0, 1, 1)
        self.setLayout(gridLayout)
