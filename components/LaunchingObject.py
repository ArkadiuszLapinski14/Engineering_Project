from PyQt5.QtCore import *
from components.Launcher import Launcher
from keyboards_back.HandMovingKeyboard import HandMovingKeyboard

class LaunchingObject(QObject):
    def __init__(self):
        super().__init__()
        self.thread = QThread()
        self.worker = Launcher()
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.launch(HandMovingKeyboard()))
        self.worker.data_ready.connect(self.HandleData)
        self.worker.finished.connect(self.worker.deleteLater)
        self.worker.finished.connect(self.thread.quit)
        self.thread.finished.connect(self.thread.deleteLater)
        print('Connection made:', self.worker.data_ready.connect(self.HandleData))

    def start(self):
        self.thread.start()

    @pyqtSlot(object)   
    def HandleData(self, data):
        print(data)