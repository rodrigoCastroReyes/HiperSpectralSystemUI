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
				msg = self.message_received()
				if len(msg) > 0:
					print (msg)
					#response = response.rstrip('\n')
					command = msg.split(':')[0]
					if command == "THOR_CAPTURE":
						t = random.randint(2, 5) 
						time.sleep(t)
						self.connection.send(("THOR_CAPTURE_OK").encode())
					elif command == "THOR_START_VIDEO":
						time.sleep(30)
						self.connection.send(("THOR_CAPTURE_OK").encode())
					elif command == "THOR_END_VIDEO":
						time.sleep(30)
						self.connection.send(("THOR_CAPTURE_OK").encode())
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