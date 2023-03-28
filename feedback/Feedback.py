from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from components.Navbar import Navbar

class Feedback(QWidget):
    def __init__(self):
        super(Feedback, self).__init__()
        print("Feedback")
        self.UIComponents()

    def UIComponents(self):
        gridLayout = QGridLayout()

        self.setLayout(gridLayout)