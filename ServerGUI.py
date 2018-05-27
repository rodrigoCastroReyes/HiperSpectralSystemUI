import sys
import os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow,QApplication, QDialog
from PyQt5.uic import loadUi
from ServerSocketWrapper import *
from SocketWrapper import *
from PyQt5.QtGui import QIcon
import json
from ServerA2M2 import *

class ModeOperation(QThread):

    def __init__(self,parent=None):
        QThread.__init__(self, parent)

    def doScanner(self,context):
        pass

class StepsModeOperation(ModeOperation):

    def __init__(self,parent=None):
        ModeOperation.__init__(self,parent)

    def doScanner(self,context):
        self.context = context
        self.start()

    def run(self):
        n_images = 100
        self.context.server.doHome()
        self.context.server.waitForSlider()
        while n_images > 0:
            self.context.server.doMove(10,20,1)
            self.context.server.waitForSlider()
            #slider.server.takePhoto()
            #print("wait for camera thor response")
            n_images-=1


class ServerGUI(QMainWindow):

    def __init__(self, *args):
        super(ServerGUI, self).__init__(*args)
        loadUi('interfaz.ui', self)
        self.initUIComponents()
        self.loadConfiguration("config_server.json")
        self.server = ServerA2M2(self.ip,self.port)
        self.server.start()

    def loadConfiguration(self,filename):
        with open(filename) as data_file:
            data = json.loads(data_file.read())
        config = data["config"]
        self.ip = config["ip"]
        self.port = int(config["port"])

    def initUIComponents(self):
        self.setFixedSize(self.size())
        self.directionValue.addItem('izquierda',-1)
        self.directionValue.addItem('derecha',1)
        self.sliderHomeButton.clicked.connect(self.onClickSliderHome)
        self.sliderMoveButton.clicked.connect(self.onClickSliderMove)
        self.sliderStopButton.clicked.connect(self.onClickSliderStop)
        self.cameraCaptureButton.clicked.connect(self.onClickCameraCapture)
        self.startSessionButton.clicked.connect(self.onClickStartSession)

        #self.createSessionButton.setIcon(QIcon('icon/add_session.png'))
        self.createSessionButton.setStyleSheet("background-color: #2ecc71; color:white;")
        self.startSessionButton.setStyleSheet("background-color: #2ecc71; color:white;")
        self.cancelSessionButton.setStyleSheet("background-color: #2ecc71; color:white;")
        self.addFieldButton.setStyleSheet("background-color: #2ecc71; color:white;")
        self.sliderHomeButton.setStyleSheet("background-color: #2ecc71; color:white;")
        self.sliderMoveButton.setStyleSheet("background-color: #2ecc71; color:white;")
        self.sliderStopButton.setStyleSheet("background-color: #2ecc71; color:white;")
        self.cameraCaptureButton.setStyleSheet("background-color: #2ecc71; color:white;")


    def onClickStartSession(self):
        print("algoritmo de adquisión de imágenes")
        self.mode = StepsModeOperation()
        self.mode.doScanner(self)

    def onClickCameraCapture(self):
        fileNameBase = self.cameraThorNameFiles.text()#validar que sea un nombre valido
        nPhotos = self.cameraThorNPhotos.value()
        directory = self.cameraThorDirectory.text()
        
        if(nPhotos < 1):
            return

        for i in range(0,nPhotos):
            fileName = (fileNameBase + "_%d" + ".tif")%i
            pathFile = os.path.join(directory,fileName)
            self.server.takePhoto(pathFile)

    def onClickSliderHome(self):
        print("onHome")
        self.server.doHome()
	
    def onClickSliderMove(self):
        print("onMove")
        velocity = int(self.velocityValue.text())
        distance = int(self.distanceValue.text())
        direction = int(self.directionValue.currentData())
        self.server.doMove(velocity,distance,direction)
        
    def onClickSliderStop(self):
        print("onStop")
        self.server.doStop()
    
app = QApplication(sys.argv)
widget = ServerGUI()
widget.show()
sys.exit(app.exec_())