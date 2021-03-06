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
				command = msg.split(':')[0]
				if not(command in ['SLIDER_HOME','SLIDER_MOVE','SLIDER_STOP']):
					continue
				if self.slider.isRunning():
					self.slider.terminate()
					self.slider.wait(100)
				if command == 'SLIDER_STOP':
					args = msg.split(":")[1]
					print command,args
					self.slider.setAction(command,self,args=args)
				else:
					self.slider.setAction(command,self)
				self.slider.start()

def loadConfiguration(filename):
	with open(filename) as data_file:
		data = json.loads(data_file.read())
	config = data["config"]
	return config

if __name__ == '__main__':
	filename = "config.json"
	app = QApplication(sys.argv)
	config = loadConfiguration(filename)
	device = config['device'] 
	ip = config["ip"]
	port = int(config["port"])
	type = config["type"]

	if type == "serial":
		slider = SerialSlider()
		if(slider.init(device)):
			client = SliderSocket(slider)
			client.connect(ip,port)
			client.start()
		else:
			print("No se puede conectar a %s"%(device))
	
	elif type == "linuxcnc":
		slider = CNCSlider()
		client = SliderSocket(slider)
		client.connect(ip,port)
		client.start()

	sys.exit(app.exec_())