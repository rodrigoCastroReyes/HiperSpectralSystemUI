import Config, inspect, os, sys, json, time
from PyQt5.QtWidgets import QMainWindow,QApplication, QFileDialog,QWidget,QTableWidgetItem
from PyQt5.uic import loadUi
from ServerSocketWrapper import *
from SocketWrapper import *
from pathlib import Path
from datetime import datetime
from PyQt5.QtCore import Qt
import aioftpclient
from ftp import FtpClient
import asyncio
import MyThread

class SliderUI(QMainWindow):
    def __init__(self, *args):
        super(SliderUI, self).__init__(*args)
        loadUi('interfaz.ui', self)
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
        self.pushButton.clicked.connect(self.onClickPushButton)

        #self.createSessionButton.setIcon(QIcon('icon/add_session.png'))
        self.createSessionButton.setStyleSheet("background-color: #2ecc71; color:white;")
        self.startSessionButton.setStyleSheet("background-color: #2ecc71; color:white;")
        self.cancelSessionButton.setStyleSheet("background-color: #2ecc71; color:white;")
        self.addFieldButton.setStyleSheet("background-color: #2ecc71; color:white;")
        self.sliderHomeButton.setStyleSheet("background-color: #2ecc71; color:white;")
        self.sliderMoveButton.setStyleSheet("background-color: #2ecc71; color:white;")
        self.sliderStopButton.setStyleSheet("background-color: #2ecc71; color:white;")
        self.cameraCaptureButton.setStyleSheet("background-color: #2ecc71; color:white;")

        default_file = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        connection_file = open(default_file + "/parametros.json", 'r')
        conn_string = json.load(connection_file)
        connection_file.close()
        self.tableWidget.setRowCount(len(conn_string["parametros"]))
        self.tableWidget.setColumnCount(2)
        # self.tableWidget.setRowCount(len(conn_string["parametros"])+1)
        # num_row = len(conn_string["parametros"])
        num_row = 0
        for parametro in conn_string["parametros"]:
            # self.tableWidget.inserRow(num_row)
            print(str(num_row))
            item = QTableWidgetItem(parametro)
            item.setFlags(Qt.ItemIsEnabled)
            self.tableWidget.setItem(num_row, 0, QTableWidgetItem(item))
            self.tableWidget.setItem(num_row, 1, QTableWidgetItem(""))
            num_row = num_row + 1
        #self.setDeviceConnections()

    def worker(self, inval):
        print("in worker, received '%s'" % inval)
        #time.sleep(5)
        aioftpclient.prueba2()
        #asyncio.wait(aioftpclient.subir_datos())
        #loop = asyncio.get_event_loop()
        #tasks = (aioftpclient.subir_datos(),)

        #ftp = aioftp.Aioftp()
        #loop.run_until_complete(asyncio.wait(tasks))
        #asyncio.wait(tasks)
        return "%s worked" % inval

    def end_send(self, cmd):
        print("send returned '%s'" % cmd)

    def onClickPushButton(self):
        #ftp = FtpClient()
        #ftp.rx_ython()
        #loop = asyncio.get_event_loop()
        #tasks = (aioftp.subir_datos(),)

        # ftp = Aioftp()
        #loop.run_until_complete(asyncio.wait(tasks))
        print("Kicked off thread")
        #loop = asyncio.new_event_loop()
        #asyncio.set_event_loop(loop)
        #future = asyncio.ensure_future(aioftpclient.subir_datos())  # tasks to do
        #loop.run_until_complete(future)  # loop until done
        #t = MyThread.MyThread(self, self.worker, "some val")
        t = MyThread.MyThread2( "sdfg")
        t.start()
        print("Kicked off thread")

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
            self.cameraThorDirectory.setText(t_str+"/imagenesCalibracion")
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
        #
        #print(inspect.getfile(inspect.currentframe()) ) # script filename (usually with path)
        print(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) ) # script directory
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                  "All Files (*);;Python Files (*.py)", options=options)
        print(fileName)
        if fileName:
            my_file = Path(fileName)
            if my_file.exists():
                connection_file = open(fileName, 'r')
                conn_string = json.load(connection_file)
                connection_file.close()
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
        #self.close()
        mw = Config.Config(self)
        mw.show()

    def setDeviceConnections(self):
        if(not(self.connectToSlider())):
            raise ConnectionError("Slider connection error")
        if(not(self.connectToCameraThor())):
            raise ConnectionError("Camera Thor connection error")

    def onClickStartSession(self):
        """
        establecer parámetros
        d: longitud del objeto a captuarar
        X: número de pasos por cada parada
        enviar mensaje a cámara y slider sobre el inicio de sesion
        esperar por mensaje de los dispositivos, los cuales deben notificar que estan listos para empezar
        mientras que slider no alcance la distancia d
            hacer que slider avance X pasos
            esperar por confirmación
            capturar foto
            esperar por confirmación de foto
        mostrar resultados
        """
        print("algoritmo de adquisión de imágenes")

    def onClickSliderHome(self):
        print("onHome")
        self.sliderChannel.send("SLIDER_HOME:\n")

    def onClickCameraCapture(self):
        fileNameBase = self.cameraThorNameFiles.text()#validar que sea un nombre valido
        nPhotos = self.cameraThorNPhotos.value()
        directory = self.cameraThorDirectory.text()
        if(nPhotos < 1):
            return

        for i in range(0,nPhotos):
            fileName = (fileNameBase + "_%d" + ".tif")%i
            pathFile = os.path.join(directory,fileName)
            msg = "CAMERATHOR_CAPTURE:" + pathFile
            print (msg)
            self.cameraChannel.send(msg)

    def onClickSliderMove(self):
        print("onMove")
        velocity = int(self.velocityValue.text())
        distance = int(self.distanceValue.text())
        direction = int(self.directionValue.currentData())
        msg = "SLIDER_MOVE:%d,%d,%d\n"%(velocity,distance,direction)
        self.sliderChannel.send(msg)

    def onClickSliderStop(self):
        print("onStop")
        self.sliderChannel.send("SLIDER_STOP:\n")

    def connectToCameraThor(self):
        self.cameraChannel = ClientSocket()
        if (self.cameraChannel.connect('localhost',8000)):
            return True
        else:
            return False

    def connectToSlider(self):
        self.sliderChannel = ClientSocket()
        if (self.sliderChannel.connect('localhost',7778)):
            return True
        else:
            return False

app = QApplication(sys.argv)
widget = SliderUI()
widget.show()
#mw = MainWindow.MainWindow()
#mw.show()
#window = QWidget()
#indow.setWindowTitle("Hello World")
#window.show()
sys.exit(app.exec_())