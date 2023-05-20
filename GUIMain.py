from keyboards_back.HandMovingKeyboard import HandMovingKeyboard
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from screeninfo import get_monitors
from keyboards_back.HeadMovingKeyboard import HeadMovingKeyboard 
import sys

from components.Stylesheet import StyleSheet
from components.Navbar import Navbar
from cameraView.CameraView import CameraView

SCREEN_WIDTH = get_monitors()[0].width
SCREEN_HEIGHT = get_monitors()[0].height

class Menu(QMainWindow):
    def __init__(self):
        ###WINDOW INIT###
        super(Menu, self).__init__()
        self.setWindowTitle("Hand Tracking Program Menu")
        self.width = int(SCREEN_WIDTH - (SCREEN_WIDTH * 0.4))
        self.height = int(SCREEN_HEIGHT - (SCREEN_HEIGHT * 0.4))
        self.setGeometry(int((SCREEN_WIDTH - self.width) / 2), (int((SCREEN_HEIGHT - self.height) / 2)), self.width, self.height)
        self.setFixedSize(self.width, self.height)
        #################

        ####UI INIT######
        self.UIComponents()
        #################

    def UIComponents(self):
        self.page = QWidget()
        self.pageLayout = QGridLayout()

        navbar = Navbar(self)
        cameraView = CameraView(self)

        self.pageLayout.addWidget(navbar, 0, 0, 1, 5)
        self.pageLayout.addWidget(cameraView, 0, 5, 1, 7)

        self.page.setLayout(self.pageLayout)
        self.setCentralWidget(self.page)

################################################################################################################################

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    
    menu = Menu()
    menu.show()
    sys.exit(app.exec())

    

if __name__ == '__main__':
    main()
	
