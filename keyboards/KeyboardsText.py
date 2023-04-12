from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class KeyboardsText(QWidget):
    def __init__(self, parent = None):
        super(QWidget, self).__init__()
        self.parent = parent
        self.UIComponents()
        self.parent.resultLabel.textChanged.connect(self.updateLabel)

    def UIComponents(self):
        gridLayout = QGridLayout()

        self.myText = QLabel(self.parent.resultLabel, objectName="MyText")

        gridLayout.addWidget(self.myText, 0, 0 , 1, 1)
        
        self.setLayout(gridLayout)

    def updateLabel(self, text):
        self.myText.setText(text)