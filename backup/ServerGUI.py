from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *
#from Server import *
#from display import *
from experiment import *
import json
#from SettingsSlider import *
import sys
import shutil

# Cargar nuestro archivo .ui
form_class = uic.loadUiType("interfaz.ui")[0]
 
class ServerGUI(QtGui.QMainWindow, form_class):

    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)
        self.loadConfiguration("config.json")
        #self.server = Server(self.name,self.ip,self.port)
        #self.server.start()
        """
        self.server.initSlider(self.velocity,self.distance,self.offset)
        self.homeBtn.clicked.connect(self.homeAction)
        self.goOnBtn.pressed.connect(self.goOnAction)
        self.goOnBtn.released.connect(self.stopAction)
        self.goBackBtn.pressed.connect(self.goBackAction)
        self.goBackBtn.released.connect(self.stopAction)
        self.stopBtn.clicked.connect(self.stopAction)
        self.settingsBtn.clicked.connect(self.settingsAction)
        self.blancasBtn.clicked.connect(self.takeWhitesImageAction)
        self.negrasBtn.clicked.connect(self.takeBlackImageAction)
        
        self.startBtn.clicked.connect(self.startCaptureAction)
        self.cancelBtn.clicked.connect(self.cancelCaptureAction)
        self.updateButton(True)

        self.thorLed.setColor(QColor(255,0,0,255))
        self.termicaLed.setColor(QColor(255,0,0,255))
        self.firmewireLed.setColor(QColor(255,0,0,255))
        self.connect(self.server.slider,SIGNAL("started()"),self.notifyStartCapture)
        self.connect(self.server.slider,SIGNAL("finished()"),self.notifyEndCapture)
        self.connect(self.server.controlButton,SIGNAL("updateButton(bool)"),self.updateButton)
        self.connect(self.server.linkerThor,SIGNAL("updateLed(bool)"),self.updateThorLed)
        self.connect(self.server.linkerThor,SIGNAL("showResults(QString)"),self.showResults)
        self.connect(self.server.linkerTermica,SIGNAL("updateLed(bool)"),self.updateTermicaLed)
        self.connect(self.server.linkerFirewire,SIGNAL("updateLed(bool)"),self.updateFirmewireLed)
        """

    def takeBlackImageAction(self):
        self.server.linkerThor.connection.send("SERVER_NEGRAS")

    def takeWhitesImageAction(self):
        self.server.linkerThor.connection.send("SERVER_BLANCAS")

    def settingsAction(self):
        self.settings = SettingsSlider()
        self.settings.acceptBtn.clicked.connect(self.changeSliderParameters)
        self.settings.show()

    def changeSliderParameters(self):
        velocity = float(self.settings.inputText.text())
        self.server.slider.setVelocity(velocity)
        self.settings.close()

    def notifyStartCapture(self):
        print "empieza captura"
        self.updateButton(True)
        self.homeBtn.setDisabled(True)
        self.goOnBtn.setDisabled(True)
        self.goBackBtn.setDisabled(True)

    def notifyEndCapture(self):
        print "finalizar captura"
        self.updateButton(False)
        self.homeBtn.setDisabled(False)
        self.goOnBtn.setDisabled(False)
        self.goBackBtn.setDisabled(False)

    def updateButton(self,flag):
        self.startBtn.setDisabled(flag)

    def updateThorLed(self,flag):
        if flag:
            self.thorLed.setColor(QColor(0,255,0,255))
            self.thorLed.on()
        else:
            self.thorLed.setColor(QColor(255,0,0,255))
            self.thorLed.off()

    def updateTermicaLed(self,flag):
        if flag:
            self.termicaLed.setColor(QColor(0,255,0,255))
            self.termicaLed.on()
        else:
            self.termicaLed.setColor(QColor(255,0,0,255))
            self.termicaLed.off()

    def updateFirmewireLed(self,flag):
        if flag:
            self.firmewireLed.setColor(QColor(0,255,0,255))
            self.firmewireLed.on()
        else:
            self.firmewireLed.setColor(QColor(255,0,0,255))
            self.firmewireLed.off()

    def loadConfiguration(self,filename):
        with open(filename) as data_file:
            data = json.loads(data_file.read())
        config = data["config"]
        self.name = config["name"]
        self.ip = config["ip"]
        self.port = int(config["port"])
        self.velocity = config["velocity"]
        self.distance = config["distance"]
        self.offset = config["offset"]
        print "Parameter configured"

    def isDataExperimentCorrect(self):
        if (len(self.lineEditPlanta.text()) > 0 and len(self.lineEditHoja.text())):
            return True
        else:
            return False 

    def startCaptureAction(self):
        if self.isDataExperimentCorrect():
            idPlanta = self.lineEditPlanta.text()
            idHoja = self.lineEditHoja.text()
            self.dataExperiment = DataExperiment(idPlanta,idHoja,self.server.dataDirectory)
            self.server.startCapture()

    def cancelCaptureAction(self):
        print "cancelar captura"


    def homeAction(self):
        slider = self.server.getSlider()
        slider.doHome(waitComplete=False)

    def goOnAction(self):
        slider = self.server.getSlider()
        slider.goOn()

    def goBackAction(self):
        slider = self.server.getSlider()
        slider.goBack()

    def stopAction(self):
        slider = self.server.getSlider()
        slider.stopMoving()
        print "stop action"

    def reset(self):
        self.server.dataDirectory = {}
        self.server.setDataDirectory()
        self.lineEditPlanta.setText("")
        self.lineEditHoja.setText("")
        folder = self.server.getFolder()
        #notificar a las camaras sobre el nuevo directorio
        self.server.linkerThor.notifyNewDirectory(folder)
        self.server.linkerFirewire.notifyNewDirectory(folder)
        self.server.linkerTermica.notifyNewDirectory(folder)

    def deleteDataExperiment(self):
        folder = self.server.getFolder()
        if len(folder)> 0: 
            fileDirectory = self.server.dirFolderShared + folder
            for root, dirs, files in os.walk(fileDirectory, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))
            os.rmdir(fileDirectory)
        self.reset()
        self.display.close() 
        
    def saveDataExperiment(self):
        if self.dataExperiment :
            line = "idPlanta:%s \nidHoja:%s \nDate:%s %s \nFolder:%s \n"%(self.dataExperiment.idPlanta, 
                self.dataExperiment.idHoja, self.dataExperiment.dataDirectory["date"], 
                self.dataExperiment.dataDirectory["hour"], self.dataExperiment.dataDirectory["folder"])
            fileDirectory = self.server.dirFolderShared + self.dataExperiment.dataDirectory["folder"] + "/Data_Experimento.txt"
            fileWorker = open(fileDirectory, 'w')
            fileWorker.write(line)
            fileWorker.close()
            self.dataExperiment = None
            self.reset()
            self.display.close()

    def showResults(self,directory):
        self.display = DisplayImage(str(directory),"nombres.txt")
        self.display.acceptBtn.clicked.connect(self.saveDataExperiment)
        self.display.cancelBtn.clicked.connect(self.deleteDataExperiment)
        self.display.show()

    #override
    def closeEvent(self,event):
        result = QtGui.QMessageBox.question(self, "Confirmar Salida", "Estas seguro que deseas salir?",
            QtGui.QMessageBox.Yes| QtGui.QMessageBox.No)
        event.ignore()
        if result == QtGui.QMessageBox.Yes:
            event.accept()
            self.end()

    def end(self):
        self.server.closeConnections()
        self.close()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    MyWindow = ServerGUI()
    MyWindow.show()
    app.exec_()