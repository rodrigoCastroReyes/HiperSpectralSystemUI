from Synchronized import *

class ControlButton(Checker):

	def __init__(self,mutex,condition,target,parent = None):
		Checker.__init__(self,"button",mutex,condition,target,parent)
	
	def areCamerasConnected(self):
		#return self.target["thor"] and self.target["termica"] and self.target["firmewire"]
		return self.target["thor"]

	def on(self):
		self.emit(SIGNAL("updateButton(bool)"),False)#activa el boton

	def off(self):
		self.emit(SIGNAL("updateButton(bool)"),True)#desactiva el boton

	def run(self):
		while True:
			self.check(lambda: self.areCamerasConnected(), lambda: self.on() , lambda: self.off())
