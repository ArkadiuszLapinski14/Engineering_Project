from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from components.Navbar import Navbar

class Settings(QWidget):
    def __init__(self):
        super(Settings, self).__init__()
        print("Settings")
        self.UIComponents()

    def UIComponents(self):
        gridLayout = QGridLayout()

        self.setLayout(gridLayout)