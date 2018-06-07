import sys
import time

from qtasync import CallbackEvent  # No need for the coroutine stuff
from PyQt5 import QtGui
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow,QApplication, QFileDialog,QWidget,QPushButton

import MyThread


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self):
        self.cmd_button = QPushButton("Push", self)
        self.cmd_button.clicked.connect(self.send)
        self.statusBar()
        self.show()

    def customEvent(self, event):
        event.callback()

    def worker(self, inval):
        print("in worker, received '%s'" % inval)
        time.sleep(5)
        return "%s worked" % inval

    def end_send(self, cmd):
        print("send returned '%s'" % cmd)

    def send(self, arg):
        t = MyThread.MyThread(self, self.worker, "some val")
        print("Kicked off thread")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = MainWindow()
    sys.exit(app.exec_())