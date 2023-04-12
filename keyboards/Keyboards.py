from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from components.Navbar import Navbar
from components.RegisterPanel import RegisterPanel
from keyboards.HeadHandChoose import HeadHandChoose
from keyboards.Head import Head
from keyboards.Hand import Hand
from keyboards.KeyboardsText import KeyboardsText

class Keyboards(QWidget):
    def __init__(self):
        super(Keyboards, self).__init__()
        print("Kboards")
        self.UIComponents()

    def UIComponents(self):
        self.gridLayout = QGridLayout()

        self.views = RegisterPanel()
        self.views = self.ViewsRegister(self.views)
        self.SetView(self.views, "HeadHandChoose")

        self.setLayout(self.gridLayout)


    def ViewsRegister(self, view):
        view.register("HeadHandChoose", lambda:HeadHandChoose(self))
        view.register("Head",lambda:Head(self))
        view.register("Hand",lambda:Hand(self))
        view.register("KeyboardsText",lambda:KeyboardsText())
        return view

    def SetView(self, views, viewName):
        currentView = views.getInstance(viewName)
        
        for i in reversed(range(self.gridLayout.count())): 
            self.gridLayout.itemAt(i).widget().setParent(None)

        self.gridLayout.addWidget(currentView, 3, 0 , 1, 2)
        