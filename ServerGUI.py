import sys
import os
import json
import time
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow,QApplication, QFileDialog,QWidget,QTableWidgetItem
from PyQt5.uic import loadUi
from PyQt5.QtGui import QIcon
from pathlib import Path
from datetime import datetime
from ftplib import FTP
from rx import Observable
from rx.concurrency import NewThreadScheduler
import qtmodern.styles
import qtmodern.windows
import time

import Config, inspect, os, sys, json, time

from ServerA2M2 import *
from communication.ServerSocketWrapper import *
from communication.SocketWrapper import *

UI_PATH = './files/interfaz.ui'
CONFIG_PATH = "./files/config_server.json"


class ModeOperation(QThread):

    def __init__(self,parent=None):
        QThread.__init__(self, parent)

    def doScanner(self,context):
        pass

class ContinuosModeOperation(ModeOperation):

    def __init__(self,parent=None):
        ModeOperation.__init__(self,parent)

    def doScanner(self,context):
        self.context = context
        self.start()

    def run(self):
        pathDir = self.context.getThorDirectory()
        print("Escribiendo datos en %s " % (pathDir))
        #velocity = 10
        #distance = 16
        direction = 1
        self.context.server.doMove(self.context.velocity,self.context.distance, direction)
        self.context.server.startVideo(pathDir)
        self.context.server.waitForSlider()
        self.context.server.endVideo()
        self.context.server.waitForCameraThor()

class StepsModeOperation(ModeOperation):

    def __init__(self,parent=None):
        ModeOperation.__init__(self,parent)

    def doScanner(self,context):
        self.context = context
        self.start()

    def run(self):
        #pathDir = r"C:\Users\BDI\Desktop\exp\prueba_"
        pathDir = self.context.getThorDirectory()
        print ("Escribiendo datos en %s "%(pathDir))
        i = 0
        n_images = 650 #CAMBIAR EN 1 SENTIDO USUARIO INGRE DISTANCIA EN MM 
        #N IMAGENES= DITANCIA EN MM DIVIDIDO PARA PASO
        #self.context.server.doHome()
        #self.context.server.waitForSlider()
        while n_images > 0:
            pathFile = os.path.join(pathDir,str(i) + ".tif")
            self.context.server.doMove(self.context.velocity,self.context.distance,1)#se mueve 0.4mm velocidad,paso,direccion
            self.context.server.waitForSlider()

            time.sleep(1.5)

            self.context.server.takePhoto(pathFile)
            self.context.server.waitForCameraThor()
            n_images-=1
            i+=1

        #self.context.server.endCapture()

class ServerGUI(QMainWindow):

    def __init__(self, *args):
        super(ServerGUI, self).__init__(*args)
        loadUi(UI_PATH, self)
        self.experiment_directory = ""
        self.initUIComponents()
        self.loadConfiguration(CONFIG_PATH)
        self.server = ServerA2M2(self.ip,self.port)
        self.server.start()

    def loadConfiguration(self,filename):
        with open(filename) as data_file:
            data = json.loads(data_file.read())
        config = data["config"]
        self.ip = config["ip"]
        self.port = int(config["port"])
        self.velocity = float(config["velocity"])
        self.distance = float(config["distance"])
        print (config)

    def onClickSelectPath(self):
        #QFileDialog.getExistingDirectory(self, 'Select directory')
        options = QFileDialog.DontResolveSymlinks | QFileDialog.ShowDirsOnly
        directory = QFileDialog.getExistingDirectory(self,"Open Folder",options=options)
        if directory:
            self.lineEdit.setText(directory)

    def getThorDirectory(self):
        return self.thor_directory

    def onClickCreate(self):
        t = time.time()
        t_str = time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(t))
        t_str = self.lineEdit.text()+"/"+"Experimento-" + t_str
        self.experiment_directory = os.path.abspath(t_str)
        self.thor_directory = os.path.abspath(t_str + "/fotoThor/")
        self.calibration_directory = os.path.abspath(t_str + "/imagenesCalibracion/")
        if not os.path.exists(t_str):
            os.makedirs(self.experiment_directory)
            os.makedirs(self.thor_directory)
            os.makedirs(self.calibration_directory)
            self.cameraThorDirectory.setText(self.calibration_directory)
            file_config = open(t_str+"/Data_Experimento.txt", 'w', encoding='utf-8')
            for row in range(self.tableWidget.rowCount()):
                item1 = self.tableWidget.item(row, 0)
                item2 = self.tableWidget.item(row, 1)
                file_config.write(str(item1.text())+":"+str(item2.text())+"\n")
            file_config.close()
            self.lineEdit.setText(t_str)

    def onClickLoadFileConfig(self):
        #filename = QtWidgets.QFileDialog.getOpenFileName(None, 'Test Dialog', os.getcwd(), 'All Files(*.*)')
        #print(filename)
        print(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) ) # script directory
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
        self.createSessionButton.clicked.connect(self.onClickCreate)
        self.pathButton.clicked.connect(self.onClickSelectPath)
        self.uploadSessionButton.clicked.connect(self.onClickUploadSession)

        default_file = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        connection_file = open(default_file + "/files/parametros.json", 'r')
        conn_string = json.load(connection_file)
        connection_file.close()
        self.tableWidget.setRowCount(len(conn_string["parametros"]))
        self.tableWidget.setColumnCount(2)
        # self.tableWidget.setRowCount(len(conn_string["parametros"])+1)
        # num_row = len(conn_string["parametros"])
        num_row = 0
        for parametro in conn_string["parametros"]:
            # self.tableWidget.inserRow(num_row)
            item = QTableWidgetItem(parametro)
            item.setFlags(Qt.ItemIsEnabled)
            self.tableWidget.setItem(num_row, 0, QTableWidgetItem(item))
            self.tableWidget.setItem(num_row, 1, QTableWidgetItem(""))
            num_row = num_row + 1

    def upload_files(self,parent_path,server_path,my_ftp):
        print("directorio actual %s"%my_ftp.pwd())
        #print(server_path)
        files = os.listdir(parent_path)
        for file in files:
            full_path = os.path.join(parent_path,file)
            if os.path.isfile(full_path):
                fh = open(full_path, 'rb')
                my_ftp.storbinary('STOR %s' % file, fh)
                fh.close()
            elif os.path.isdir(full_path):
                my_ftp.mkd(file)
                my_ftp.cwd(file)
                self.upload_files(full_path,file,my_ftp)
        my_ftp.cwd('..')

    def launch_upload_thread(self,my_ftp):
        local_parent_path = self.experiment_directory
        parts = os.path.split(local_parent_path)
        folder_name = parts[1]
        server_path = "/home/obayona/Cacao_Experimentos/"+folder_name
        print ("server path",server_path)
        my_ftp.mkd(server_path)
        my_ftp.cwd(server_path)
        scheduler = NewThreadScheduler()
        #scheduler.schedule(lambda sch,state : self.upload_files(local_parent_path,server_path,my_ftp))

        Observable.from_([local_parent_path]) \
            .subscribe_on(scheduler) \
            .map(lambda x: self.upload_files(x,server_path,my_ftp)) \
            .subscribe(on_error=lambda e: print(e),
                       on_completed=lambda: my_ftp.close())

    def onClickUploadSession(self):
        server = '200.126.1.152'
        username = 'obayona'
        password = 'EloyEcuador93'
        print("inicio de subida")
        my_ftp = FTP(server, username, password)
        self.launch_upload_thread(my_ftp)
        print("fin de subida")

    def onClickStartSession(self):
        print("algoritmo de adquisión de imágenes")
        self.mode = StepsModeOperation()
        #self.mode = ContinuosModeOperation()
        self.mode.doScanner(self)
        #self.mode.join()
        #join hasta que mode termine

    def onClickCameraCapture(self):
        fileNameBase = self.cameraThorNameFiles.text()#validar que sea un nombre valido
        nPhotos = self.cameraThorNPhotos.value()
        directory = self.cameraThorDirectory.text()
        
        if(nPhotos < 1):
            return

        for i in range(0,nPhotos):
            fileName = (fileNameBase + "_%d" + ".tif")%i
            pathFile = os.path.join(directory,fileName)
            pathFile = os.path.abspath(pathFile)
            self.server.takePhoto(pathFile)
            self.server.waitForCameraThor()

    def onClickSliderHome(self):
        print("onHome")
        self.server.doHome()
	
    def onClickSliderMove(self):
        print("onMove")
        velocity = float(self.velocityValue.text())
        distance = float(self.distanceValue.text())
        direction = int(self.directionValue.currentData())
        self.server.doMove(velocity,distance,direction)
        
    def onClickSliderStop(self):
        print("onStop")
        self.server.doStop()
    
app = QApplication(sys.argv)
qtmodern.styles.dark(app)
widget = ServerGUI()
mw = qtmodern.windows.ModernWindow(widget)
mw.show()
sys.exit(app.exec_())