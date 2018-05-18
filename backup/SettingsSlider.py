from PyQt4 import *
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import *

class SettingsSlider(QWidget):

	def __init__(self,*args):
		QtGui.QWidget.__init__(self,*args)
		self.ContenedorVelocity =  QHBoxLayout()
		self.labelVelocity = QLabel("Velocity")
		self.inputText = QLineEdit()
		self.ContenedorVelocity.addWidget(self.labelVelocity)
		self.ContenedorVelocity.addWidget(self.inputText)

		self.contenedorBotones = QHBoxLayout()
		self.acceptBtn = QPushButton("Aceptar")
		self.contenedorBotones.addWidget(self.acceptBtn)

		self.layout = QBoxLayout(QBoxLayout.TopToBottom)
		self.layout.addLayout(self.ContenedorVelocity)
		self.layout.addLayout(self.contenedorBotones)
		self.setLayout(self.layout)
		self.setWindowTitle("Parametros Slider")