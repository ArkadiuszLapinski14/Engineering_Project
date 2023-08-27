from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from screeninfo import get_monitors
import sys

from components.Stylesheet import StyleSheet
from navbar.Navbar import Navbar
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

        self.navbar = Navbar(self)
        self.cameraView = CameraView(self)

        self.pageLayout.addWidget(self.navbar, 0, 0, 1, 6)
        self.pageLayout.addWidget(self.cameraView, 0, 6, 1, 12)

        self.page.setLayout(self.pageLayout)
        self.setCentralWidget(self.page)

################################################################################################################################

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(StyleSheet)
    app.setWindowIcon(QIcon("./assets/keyboard.png"))
    
    menu = Menu()
    menu.show()
    sys.exit(app.exec())

    

if __name__ == '__main__':
    main()
	
