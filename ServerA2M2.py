from PyQt5.QtCore import QThread,QMutex,QWaitCondition
import socket
from ServerSocketWrapper import *
from Linker import *

class ServerA2M2(ServerSocketWrapper,QThread):

    def __init__(self, addr, port, parent=None):
        ServerSocketWrapper.__init__(self,addr,port)
        QThread.__init__(self, parent)
        self.sliderMutex = QMutex()
        self.sliderCondition = QWaitCondition()
        self.thorMutex = QMutex()
        self.thorCondition = QWaitCondition()
        self.linkerThor = LinkerThor(self.thorMutex,self.thorCondition)
        self.linkerSlider = LinkerSlider(self.sliderMutex,self.sliderCondition)

    def doStop(self):
        msg = "SLIDER_STOP:"
        self.linkerSlider.sendAction(msg)

    def doMove(self,velocity,distance,direction):

        msg = "SLIDER_MOVE:%.4f,%.4f,%d"%(velocity,distance,direction)
        print(msg)
        self.linkerSlider.sendAction(msg)

    def doHome(self):
        msg = "SLIDER_HOME:"
        self.linkerSlider.sendAction(msg)

    def startVideo(self,pathDir):
        msg = "THOR_START_VIDEO:" + pathDir
        print (msg)
        self.linkerThor.sendAction(msg)

    def endVideo(self):
        msg = "THOR_END_VIDEO:"
        print(msg)
        self.linkerThor.sendAction(msg)

    def takePhoto(self,pathFile):
        msg = "THOR_CAPTURE:" + pathFile
        print (msg)
        self.linkerThor.sendAction(msg)

    def waitForSlider(self):

        self.sliderMutex.lock()
        print("wait for slider response")
        self.sliderCondition.wait(self.sliderMutex)
        self.sliderMutex.unlock()

        print("slider response has arrived")

    def waitForCameraThor(self):
        self.thorMutex.lock()
        print("wait for thor response")
        self.thorCondition.wait(self.thorMutex)
        self.thorMutex.unlock()
        print("thor response has arrived")

    def endCapture(self):
        msg = "THOR_END\n"
        print (msg)
        self.linkerThor.sendAction(msg)

    def run(self):
        self.listen()
        while True:
            try:
                print ("Waiting for connection")
                connection , addr = self.socket.accept()
                msg = self.receive(connection)
                if len(msg) > 0:
                    print (msg)
                    if msg == 'THOR_CONNECT':
                        print ("Camera Thor connected")
                        self.linkerThor.setConnection(connection)
                        self.linkerThor.start()
                    elif msg == 'SLIDER_CONNECT':
                        print ("Slider connected")
                        self.linkerSlider.setConnection(connection)
                        self.linkerSlider.start()
                    elif msg == 'THERMAL_CONNECT':
                        print ("Camera Termica connected")
                    elif msg == 'RGB_CONNECT':
                        print ("Camera RGB connected")
            except Exception as e:
                print(e)
                #self.closeConnections()
                break
        print("Server Socket termina")