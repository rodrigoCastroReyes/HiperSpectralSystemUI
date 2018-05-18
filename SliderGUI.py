import sys
import os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow,QApplication, QDialog
from PyQt5.uic import loadUi
from ServerSocketWrapper import *
from SocketWrapper import *
from PyQt5.QtGui import QIcon

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

		#self.createSessionButton.setIcon(QIcon('icon/add_session.png'))
		self.createSessionButton.setStyleSheet("background-color: #2ecc71; color:white;")
		self.startSessionButton.setStyleSheet("background-color: #2ecc71; color:white;")
		self.cancelSessionButton.setStyleSheet("background-color: #2ecc71; color:white;")
		self.addFieldButton.setStyleSheet("background-color: #2ecc71; color:white;")
		self.sliderHomeButton.setStyleSheet("background-color: #2ecc71; color:white;")
		self.sliderMoveButton.setStyleSheet("background-color: #2ecc71; color:white;")
		self.sliderStopButton.setStyleSheet("background-color: #2ecc71; color:white;")
		self.cameraCaptureButton.setStyleSheet("background-color: #2ecc71; color:white;")
		self.setDeviceConnections()

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
sys.exit(app.exec_())