import math
import sys
import os
from SocketWrapper import *
from Slider import *
import json
import random
import time
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication

class SliderSocket(ClientSocket,QThread):

	def __init__(self,slider,parent=None):
		ClientSocket.__init__(self)
		QThread.__init__(self, parent)
		self.slider = slider

	def run(self):
		self.send("SLIDER_CONNECT")
		while True:
			msg = self.receive()
			if len(msg) > 0:
				print(msg)
				command = msg.split(':')[0]
				if not(command in ['SLIDER_HOME','SLIDER_MOVE','SLIDER_STOP']):
					continue
				if command == "SLIDER_HOME":
					#self.slider.setAction(msg)
					#self.slider.start()
					t = random.randint(10, 20) 
					time.sleep(t)
					self.send("SLIDER_HOME_OK")
				elif command == "SLIDER_MOVE":
					t = random.randint(5, 10) 
					time.sleep(t)
					self.send("SLIDER_MOVE_OK")

def loadConfiguration(filename):
	with open(filename) as data_file:
		data = json.loads(data_file.read())
	config = data["config"]
	return config

if __name__ == '__main__':
	filename = sys.argv[1]
	app = QApplication(sys.argv)
	config = loadConfiguration(filename)
	velocity = config["velocity"]
	offset = config["offset"]
	distance = config["distance"]
	device = config['device'] 
	ip = config["ip"]
	port = int(config["port"])

	slider = SerialSlider(velocity,offset,distance)
	#slider.init(device)
	client = SliderSocket(slider)
	client.connect(ip,port)
	client.start()
	sys.exit(app.exec_())
	
	"""
	if(slider.init(device)):
	else:
		print("No se puede conectar a %s"%(device))
	"""