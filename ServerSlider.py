import math
import sys
import os
from ServerSocketWrapper import *
from Slider import *
import json

class ServerSlider(ServerSocketWrapper):
	"""docstring for ServerSlider"""
	def __init__(self,slider,ip,port):
		super(ServerSlider, self).__init__(ip,port)
		self.slider = slider

	def start(self):#wait for connections
		while True:
			print("Waiting to connect")
			(clientsocket, address) = self.accept()
			self.run(clientsocket)
		
	def run(self,client):
		while True:
			msg = self.receive(client)
			command = msg.split(':')[0]
			if command in ['SLIDER_HOME','SLIDER_MOVE','SLIDER_STOP']:
				self.slider.setAction(msg)
				self.slider.start()
				self.send(client,"SLIDER_ACK")
			else:
				break

def loadConfiguration(filename):
	with open(filename) as data_file:
		data = json.loads(data_file.read())
	config = data["config"]
	return config

if __name__ == '__main__':
	filename = sys.argv[1]
	
	config = loadConfiguration(filename)
	velocity = config["velocity"]
	offset = config["offset"]
	distance = config["distance"]
	device = config['device'] 
	ip = config["ip"]
	port = int(config["port"])

	slider = SerialSlider(velocity,offset,distance)
	if(slider.init(device)):
		server = ServerSlider(slider,ip,port)
		server.listen()
		server.start()
	else:
		print("No se puede conectar a %s"%(device))
