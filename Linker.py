from SocketWrapper import *
from PyQt5.QtCore import QThread

class Linker(QThread):

	def __init__(self,name,parent = None):
		QThread.__init__(self, parent)
		self.name = name
		self.messages = {}
		self.connection = None

	def setConnection(self,connection):
		self.connection = ClientSocket(connection)

	def addMessage(self,msg,action):
		self.messages[msg] = action

	def sendAction(self,msg):
		try:
			if self.connection:
				self.connection.send(msg)
		except Exception as e:
			print (e)

	def doAction(self,msg_recv):
        #se ejecuta una accion segú el mensaje recibido
		if msg_recv in self.messages:
			self.messages[msg_recv]()

	def run(self):
		while True:
			try:
				msg_recv = self.connection.receive()#cuando llega un mensaje
				if len(msg_recv) > 0:
					print(self.name + " SAYS: " + msg_recv)
					self.doAction(msg_recv)
			except Exception as e:
				print(e)
				#self.update(False,lambda : self.offIndicator())
				#self.offConnection()
				break


class LinkerThor(Linker):

	def __init__(self, parent = None):
		Linker.__init__(self, "thor", parent)
		self.configureMessages()

	def printMessage(self):
		print("Thor has responded")


	def configureMessages(self):
		self.addMessage("THOR_CONNECT", lambda: self.printMessage())
		self.addMessage("THOR_CAPTURE_OK",lambda : self.printMessage())


class LinkerSlider(Linker):

	def __init__(self,mutex,condition,parent = None):
		Linker.__init__(self, "slider", parent)
		self.mutex = mutex
		self.condition = condition
		self.configureMessages()

	def printMessage(self):
		print("Slider has responded")

	def homeACK(self,result):
		if result:
			self.notify()

	def moveACK(self,result):
		if result:
			self.notify()

	def notify(self):
		self.mutex.lock()
		self.condition.wakeOne()
		self.mutex.unlock()

	def configureMessages(self):
		self.addMessage("SLIDER_CONNECT", lambda: self.printMessage())
		self.addMessage("SLIDER_HOME_OK",lambda : self.homeACK(True))
		self.addMessage("SLIDER_MOVE_OK",lambda : self.moveACK(True))