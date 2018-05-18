from PyQt4 import *
from CubeGenerator import *


class DisplayImage(QWidget):

	def __init__(self, inputDirectory, filename ,*args):
		QtGui.QWidget.__init__(self,*args)
		self.contenedorImagen = QVBoxLayout()
		self.labelImage = QLabel()
		#cube = CubeGenerator(inputDirectory,filename,1,2)
		#rgb_img = cube.generateRGB()
		#qimage = cube.getQImage(rgb_img)
		#self.labelImage.setPixmap(QPixmap(qimage))
		self.contenedorImagen.addWidget(self.labelImage)
		       
		self.acceptBtn = QPushButton("Aceptar")
		self.cancelBtn = QPushButton("Cancelar")
		self.contenedorBotones =  QHBoxLayout()
		self.contenedorBotones.addWidget(self.acceptBtn)
		self.contenedorBotones.addWidget(self.cancelBtn)
	
		self.layout = QBoxLayout(QBoxLayout.TopToBottom)
		self.layout.addLayout(self.contenedorImagen)
		self.layout.addLayout(self.contenedorBotones)
		self.setLayout(self.layout)
		self.setWindowTitle("Resultados del Experimento")