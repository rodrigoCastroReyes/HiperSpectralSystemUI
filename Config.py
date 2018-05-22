from PyQt5 import QtWidgets, QtCore
import os

class Config(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        self.initUi()

    def initUi(self):
        self.setWindowTitle('Main Menu')
        self.setFixedSize(200, 200)

    def onClickLoadFileConfig(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(
            None, 'Test Dialog', os.getcwd(), 'All Files(*.*)')
        print(filename)
        QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory')
