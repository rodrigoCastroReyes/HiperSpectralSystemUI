from Synchronized import *
from Slider import *
from SocketWrapper import *
from observable import Observable
from observer import Observer


class Linker(Updater):

	def __init__(self,name,mutex,condition,target,parent = None):
		Updater.__init__(self,name,mutex,condition,target,parent)
		self.messages = {}
		self.connection = None

	def setConnection(self,connection):
		self.connection = SocketWrapper(connection)

	def addMessage(self,msg,action):
		self.messages[msg] = action

	def run(self):
		while True:
			try:
				msg_recv = self.connection.receive()#cuando llega un mensaje
				if len(msg_recv) > 0:
					print self.name + " SAYS: " + msg_recv
					#se busca el mensaje recibido dentro del conjunto de mensajes configurados
					for  msg, function in self.messages.items() :
						if msg_recv == msg :# si se encuentra se ejecuta la funcion asociada al mensaje
							function()
			except Exception, e:
				print e
				self.update(False,lambda : self.offIndicator())
				self.offConnection()
				break
	
	def notifyNewDirectory(self,folder):
		try:
			if self.connection:
				self.connection.send("CARPETA " + folder)
		except Exception, e:
			print e

	def takePhoto(self):
		try:
			if self.connection:
				self.connection.send("SERVER_TOMAR_FOTO")
		except Exception, e:
			print e

	def notifyDisconnect(self):
		try:
			if self.connection:
				self.connection.send("SERVER_TERMINAR")
		except Exception, e:
			print e

	def offConnection(self):
		try:
			if self.connection:
				self.connection.disconnect()
		except Exception, e:
			print e

	def configureMessages(self):
		pass

	def onIndicator(self):
		pass

	def offIndicator(self):
		pass


class LinkerThor(Linker,Observer):
	
	def __init__(self, mutex, condition, target, parent = None):
		Linker.__init__(self, "thor", mutex, condition, target, parent)
		Observer.__init__(self)
		self.directory = None
		self.configureMessages()

	def printMessage(self):
		print "thor"

	def notifyNewDirectory(self,folder):
		Linker.notifyNewDirectory(self,folder)
		self.setDirectory(folder)

	def setDirectory(self,folder):
		dirFolderShared = "/media/sf_Experimentos/"
		self.directory = dirFolderShared + folder + "/fotoThor/"

	def configureMessages(self):
		self.addMessage("THOR_CARPETA_OK", lambda: self.update(True, lambda : self.onIndicator()) )
		self.addMessage("THOR_INICIAR_VIDEO_OK", lambda: self.printMessage())
		self.addMessage("THOR_TERMINAR_VIDEO_OK", lambda: self.printMessage())
		self.addMessage("THOR_TERMINAR_CAPTURA", lambda: self.showResults())
		self.addMessage("THOR_EXIT",  lambda: self.update(False, lambda : self.offIndicator()))

	def updateState(self, *args, **kwargs):
		state = kwargs['state']
		if state ==  MachineState.READY:
			self.connection.send("SERVER_INICIAR_VIDEO")
		if state == MachineState.DONE:
			self.connection.send("TERMINAR_VIDEO")

	def showResults(self):
		if self.directory:
			self.emit(SIGNAL("showResults(QString)"),self.directory)

	def onIndicator(self):
		self.emit(SIGNAL("updateLed(bool)"),True)

	def offIndicator(self):
		self.emit(SIGNAL("updateLed(bool)"),False)

class LinkerTermica(Linker):

	def __init__(self, mutex, condition, target, parent = None):
		Linker.__init__(self, "termica", mutex, condition, target, parent)
		self.configureMessages()

	def onIndicator(self):
		self.emit(SIGNAL("updateLed(bool)"),True)

	def offIndicator(self):
		self.emit(SIGNAL("updateLed(bool)"),False)

	def printMessage(self):
		print "termica"

	def configureMessages(self):
		self.addMessage("TERMICA_CARPETA_OK", lambda: self.update(True, lambda : self.onIndicator()) )
		self.addMessage("TERMICA_IMAGEN_OK", lambda: self.printMessage())
		self.addMessage("TERMICA_IMAGEN_NK", lambda: self.takePhoto())
		self.addMessage("TERMICA_EXIT", lambda: self.update(False, lambda : self.offIndicator()))


class LinkerFirmewire(Linker):

	def __init__(self, mutex, condition, target, parent = None):
		Linker.__init__(self, "firmewire", mutex, condition, target, parent)
		self.configureMessage()

	def onIndicator(self):
		self.emit(SIGNAL("updateLed(bool)"),True)

	def offIndicator(self):
		self.emit(SIGNAL("updateLed(bool)"),False)

	def printMessage(self):
		print "firmewire"

	def configureMessage(self):
		self.addMessage("FIREWIRE_CARPETA_OK",lambda: self.update(True, lambda : self.onIndicator()) )
		self.addMessage("FIREWIRE_IMAGEN_OK", lambda: self.printMessage())
		self.addMessage("FIREWIRE_EXIT", lambda: self.update(False, lambda : self.offIndicator()))