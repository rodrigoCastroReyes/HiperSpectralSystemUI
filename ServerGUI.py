import sys
import os
import Config
import json
import time
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow,QApplication, QFileDialog,QWidget,QTableWidgetItem
from PyQt5.uic import loadUi
from ServerSocketWrapper import *
from SocketWrapper import *
from PyQt5.QtGui import QIcon
from ServerA2M2 import *
from pathlib import Path
from datetime import datetime

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
        pathDir = r"C:\Users\BDI\Desktop\exp\prueba_"
        i = 0
        n_images = 10
        #self.context.server.doHome()
        #self.context.server.waitForSlider()
        while n_images > 0:
            pathFile = pathDir + str(i) + ".tif"
            self.context.server.doMove(10,20,1)
            self.context.server.waitForSlider()
            self.context.server.takePhoto(pathFile)
            self.context.server.waitForCameraThor()
            n_images-=1
            i+=1
        self.context.server.endCapture()

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

    def onClickSelectPath(self):
        #QFileDialog.getExistingDirectory(self, 'Select directory')
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,"Open Folder",options=options)
        print(directory)
        if directory:
            self.lineEdit.setText(directory)

    def onClickCrear(self):
        #print('Experimento-%Y-%m-%d %H-%M-%S}'.format(datetime(2001, 2, 3, 4, 5)))
        t = time.time()
        t_str = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(t))
        t_str=self.lineEdit.text()+"/"+"Experimiento-" + t_str
        print(t_str)
        if not os.path.exists(t_str):
            os.makedirs(t_str)
            os.makedirs(t_str+"/fotoThor")
            os.makedirs(t_str+"/imagenesCalibracion")
            file_config = open(t_str+"/Data_Experimento.txt", 'w', encoding='utf-8')
            for row in range(self.tableWidget.rowCount()):
                item1 = self.tableWidget.item(row, 0)
                item2 = self.tableWidget.item(row, 1)
                file_config.write(str(item1.text())+":"+str(item2.text())+"\n")
            file_config.close()

    def onClickLoadFileConfig(self):
        #filename = QtWidgets.QFileDialog.getOpenFileName(None, 'Test Dialog', os.getcwd(), 'All Files(*.*)')
        #print(filename)
        #
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        print(fileName)
        if fileName:
            my_file = Path(fileName)
            if my_file.exists():
                print(fileName)
                connection_file = open(fileName, 'r')
                conn_string = json.load(connection_file)
                connection_file.close()
                print(conn_string["parametros"])

                self.tableWidget.setRowCount(len(conn_string["parametros"]) )
                self.tableWidget.setColumnCount(2)
                '''
                self.tableWidget.setItem(0, 0, QTableWidgetItem("Cell (1,1)"))
                self.tableWidget.setItem(0, 1, QTableWidgetItem("Cell (1,2)"))
                self.tableWidget.setItem(1, 0, QTableWidgetItem("Cell (2,1)"))
                self.tableWidget.setItem(1, 1, QTableWidgetItem("Cell (2,2)"))
                self.tableWidget.setItem(2, 0, QTableWidgetItem("Cell (3,1)"))
                self.tableWidget.setItem(2, 1, QTableWidgetItem("Cell (3,2)"))
                self.tableWidget.setItem(3, 0, QTableWidgetItem("Cell (4,1)"))
                self.tableWidget.setItem(3, 1, QTableWidgetItem("Cell (4,2)"))
                #self.tableWidget.move(0, 0)'''
                #self.tableWidget.setRowCount(len(conn_string["parametros"])+1)
                #num_row = len(conn_string["parametros"])
                num_row = 0
                for parametro in conn_string["parametros"]:
                    #self.tableWidget.inserRow(num_row)
                    print(str(num_row))
                    item = QTableWidgetItem(parametro)
                    item.setFlags(Qt.ItemIsEnabled)
                    self.tableWidget.setItem(num_row, 0, QTableWidgetItem(item))
                    self.tableWidget.setItem(num_row, 1, QTableWidgetItem(""))
                    num_row = num_row+1

    def onClickConfig(self):
        print("Permission granted!")
        mw = Config.Config(self)
        mw.show()

    def initUIComponents(self):
        self.setFixedSize(self.size())
        self.directionValue.addItem('izquierda',-1)
        self.directionValue.addItem('derecha',1)
        self.sliderHomeButton.clicked.connect(self.onClickSliderHome)
        self.sliderMoveButton.clicked.connect(self.onClickSliderMove)
        self.sliderStopButton.clicked.connect(self.onClickSliderStop)
        self.cameraCaptureButton.clicked.connect(self.onClickCameraCapture)
        self.startSessionButton.clicked.connect(self.onClickStartSession)
        
        self.configButton.clicked.connect(self.onClickConfig)
        self.addFieldButton.clicked.connect(self.onClickLoadFileConfig)
        self.createSessionButton.clicked.connect(self.onClickCrear)
        self.pathButton.clicked.connect(self.onClickSelectPath)

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