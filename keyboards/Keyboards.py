from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from components.Navbar import Navbar

class Keyboards(QWidget):
    def __init__(self):
        super(Keyboards, self).__init__()
        print("Kboards")
        self.UIComponents()

    def UIComponents(self):
        gridLayout = QGridLayout()

        self.setLayout(gridLayout)