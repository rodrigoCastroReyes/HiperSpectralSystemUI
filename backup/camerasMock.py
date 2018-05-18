import socket
import threading
import time
import random

class ClientMock(threading.Thread):

	def __init__(self,threadName):
		threading.Thread.__init__(self,name=threadName)
		self.name = threadName
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect(('200.126.20.61', 7777))

	def message_received(self):
		return self.connection.recv(1024)

	def run(self):
		#inpt = raw_input('type anything and click enter... ')
		self.connection.send(self.name + "_CONECTAR")
		while True:
			response = self.message_received()
			if len(response) > 0:
				print response
				if response == "CARPETA":
					print "entro"
					t = random.randint(10, 20) 
					time.sleep(t)
					self.connection.send(self.name + "_CARPETA_OK")
					time.sleep(60)
					self.connection.send(self.name + "_EXIT")
					self.connection.close()
					break
					print "conexion cerrada"

if __name__ == '__main__':
	thor = ClientMock("THOR")
	thor.start()

	termica = ClientMock("TERMICA")
	termica.start()

	firmewire = ClientMock("FIRMEWIRE")
	firmewire.start()
