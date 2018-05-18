from LinkerCameras import *
from ControlButton import *
from Slider import *
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import socket
import json
import time
import sys
import signal
import datetime
import time
import os
from os import getpid


class Server(ServerSocketWrapper,QThread):
    dirFolderShared = "/media/sf_Experimentos/"

    def __init__(self, name, addr, port, parent=None):
        ServerSocketWrapper.__init__(self,addr,port)
        QThread.__init__(self, parent)
        self.mutex = QMutex()
        self.condition = QWaitCondition()
        self.target = { 'thor': False , 'termica': False , 'firmewire': False , 'button': False }
        self.controlButton = ControlButton(self.mutex,self.condition,self.target)
        self.controlButton.start()
        self.slider = None
        self.linkerThor = LinkerThor(self.mutex,self.condition,self.target)
        self.linkerTermica = LinkerTermica(self.mutex,self.condition,self.target)
        self.linkerFirewire = LinkerFirmewire(self.mutex,self.condition,self.target)
        self.dataDirectory = {}
        self.setDataDirectory()
   
    def initSlider(self, velocity, distance, offset):
        self.slider = Slider("SLIDER",velocity,distance,offset)
        self.slider.register(self.linkerThor)

    def getSlider(self):
        return self.slider

    def startCapture(self):#si el boton de activar captura esta activo se puede empezar
        self.slider.start()
        self.linkerTermica.takePhoto()
        self.linkerFirewire.takePhoto()

    def getTimeStamp(self):
        ts = time.time()
        st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H-%M-%S')
        return st

    def isThereDirectory(self,path):
        return not os.path.isdir(path)

    def createFolder(self,pathFull):
        if self.isThereDirectory(pathFull):
            os.mkdir(pathFull)
            return True
        else:
            print "Error directorio ya existente"
            return False

    def getFolder(self):
        return self.dataDirectory['folder']

    def setDataDirectory(self):
        st = self.getTimeStamp()
        data = st.split(' ')
        self.dataDirectory['date'] = data[0]
        self.dataDirectory['hour'] = data[1]
        #guarda fecha y hora
        path = "Experimento-" + st
        pathFull = Server.dirFolderShared + path
        try:
            #crea una carpeta y guarda ese nombre en 'folder'
            if self.createFolder(pathFull):
                self.dataDirectory['folder'] = path
            else:
                self.dataDirectory = {}
                return ""
        except Exception, e:
            print e
            return ""


    def run(self):
        while True:
            try:
                print "Waiting for connection"
                connection , addr = self.socket.accept()
                msg = self.receive(connection)
                if len(msg) > 0:
                    print msg
                    if msg == 'THOR_CONECTAR':
                        print "Camera Thor connected"
                        folder = self.getFolder()
                        if len(folder) > 0:
                            self.linkerThor.setConnection(connection)
                            self.linkerThor.notifyNewDirectory(folder)
                            self.linkerThor.start()
                        else:
                            connection.send("ERROR DIRECTORIO")
                    elif msg == 'TERMICA_CONECTAR':
                        print "Termica connected"
                        folder = self.getFolder()
                        if len(folder) > 0:
                            self.linkerTermica.setConnection(connection)
                            self.linkerTermica.notifyNewDirectory(folder)
                            self.linkerTermica.start()
                        else:
                            connection.send("ERROR DIRECTORIO")
                    elif msg == 'FIREWIRE_CONECTAR':
                        print "firewire connected"
                        folder = self.getFolder()
                        if len(folder) > 0:
                            self.linkerFirewire.setConnection(connection)
                            self.linkerFirewire.notifyNewDirectory(folder)
                            self.linkerFirewire.start()
                        else:
                            connection.send("ERROR DIRECTORIO")
            except Exception, e:
                print(e)
                self.closeConnections()
                break
        print("Server Socket termina")

    def closeConnections(self):
        self.linkerThor.notifyDisconnect()
        self.linkerTermica.notifyDisconnect()
        self.linkerFirewire.notifyDisconnect()
        self.linkerThor.offConnection()
        self.linkerTermica.offConnection()
        self.linkerFirewire.offConnection()
        pid = getpid()
        os.kill(pid, signal.SIGTERM) #or signal.SIGKILL 

