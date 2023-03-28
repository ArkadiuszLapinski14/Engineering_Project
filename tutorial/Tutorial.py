from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from components.Navbar import Navbar

class Tutorial(QWidget):
    def __init__(self):
        super(Tutorial, self).__init__()
        print("Tutorial")
        self.UIComponents()

    def UIComponents(self):
        gridLayout = QGridLayout()

        self.setLayout(gridLayout)