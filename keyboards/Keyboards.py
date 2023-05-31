from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from components.Navbar import Navbar
from components.RegisterPanel import RegisterPanel
from keyboards.HeadHandChoose import HeadHandChoose
from keyboards.Head import Head
from keyboards.Hand import Hand
from cameraView.CameraView import KeyboardsText

class Keyboards(QWidget):
    def __init__(self):
        super(Keyboards, self).__init__()
        print("Kboards")
        self.UIComponents()

    def UIComponents(self):
        self.gridLayout = QGridLayout()

        self.SetView(HeadHandChoose(self))

        self.setLayout(self.gridLayout)


    def SetView(self, viewName):
        currentView = viewName
        
        for i in reversed(range(self.gridLayout.count())): 
            self.gridLayout.itemAt(i).widget().setParent(None)

        self.gridLayout.addWidget(currentView, 3, 0 , 1, 2)
        