from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from components.Navbar import Navbar

class Statistics(QWidget):
    def __init__(self):
        super(Statistics, self).__init__()
        print("Statistics")
        self.UIComponents()

    def UIComponents(self):
        gridLayout = QGridLayout()

        self.setLayout(gridLayout)