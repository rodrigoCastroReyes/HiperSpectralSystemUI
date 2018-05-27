import socket
import threading
import time
import random

class ClientMock(threading.Thread):

	def __init__(self,threadName):
		threading.Thread.__init__(self,name=threadName)
		self.name = threadName
		self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.connection.connect(('localhost', 9090))

	def message_received(self):
		return self.connection.recv(1024).decode()

	def run(self):
		self.connection.send((self.name + "_CONNECT").encode())
		print("Waiting for commands")
		try:
			while True:
				response = self.message_received()
				if len(response) > 0:
					response = response.rstrip('\n')
					tokens = response.split(":")
					print(tokens)
					t = random.randint(10, 20) 
					time.sleep(t)
					self.connection.send(self.name + "_CAPTURE_OK")
					"""
					device = tokens[0]
					params = tokens[1]
					action = device.split("_")[1]
					print(device,params,action)
					
					if action == "CAPTURE":
						print("Capturing photos in %s "%(params))
					"""
		except KeyboardInterrupt:
   			print('interrupted!')

if __name__ == '__main__':
	thor = ClientMock("THOR")
	thor.start()

	"""
	termica = ClientMock("TERMICA")
	termica.start()

	firmewire = ClientMock("FIRMEWIRE")
	firmewire.start()
	"""