import sys,os
from time import sleep
import math
import serial
from observable import Observable
from PyQt5.QtCore import *
import io
import time
from LinuxCNCMachine import *

class SliderStates:
	HOMED,READY,DONE = range(3)

class Slider(Observable, QThread):

	def __init__(self, parent=None):
		QThread.__init__(self, parent)
		Observable.__init__(self)
		self.velocity = 0
		self.distance = 0
		self.state = SliderStates.READY
		self.name = name

	def getState(self):
		return self.state

	def setState(self,state):
		if self.state != state: # set logical state machine
			self.state = state
			print("States %d "%(self.state))

	def setHome(self):
		self.setState(SliderStates.HOMED)

	def setReady(self):
		self.setState(SliderStates.READY)

	def setDone(self):
		self.setState(SliderStates.DONE)

	def isDone(self):
		return self.state == SliderStates.DONE

	def isReady(self):
		return self.state == SliderStates.READY

	def setVelocity(self,vel):
		self.velocity = vel

	def setAction(self,msg,context,args=None):
		self.action = msg
		self.context = context
		self.args = args


class CNCSlider(Slider):

	def __init__(self):
		super(CNCSlider, self).__init__()
		self.controller = LinuxCNCMachine()

	def do(self,action,args):
		sleep(1)

		if action == 'SLIDER_HOME':
			print action

		elif action == 'SLIDER_MOVE':
			attr = args.split(',')
			velocity = attr[0]
			direction = attr[1]
			step = attr[2]
			self.controller.move(velocity,direction,step)

		elif action == 'SLIDER_STOP':
			self.controller.stopMoving()

	def run(self):
		self.do(self.action)
		self.context.send("SLIDER_MOVE_OK")#notifica al servidor que ha terminado de efectuar la accion

	def terminate(self):
		pass

	def wait(self,time):
		sleep(time)

class SerialSlider(Slider):

	def __init__(self):
		super(SerialSlider, self).__init__()
		self.position = 0

	def init(self,device):
		try:
			self.channel = serial.Serial(device,9600,timeout=1)#open serial port
			self.sio = io.TextIOWrapper(io.BufferedRWPair(self.channel, self.channel))
			return True
		except Exception as e:
			print (e)
			return False

	def run(self):
		start_time = time.time()
		self.send(self.action)
		while (True):
			self.channel.reset_input_buffer()
			line = self.channel.readline()
			line = line.decode()
			line = line.rstrip('\n')
			line = line.replace('\r','')
			print("enviado por slider",line)
			if line == "SLIDER_MOVE_OK" or line=="SLIDER_STOP_OK":
				break
		self.context.send(line)
		print("--- %s seconds ---" % (time.time() - start_time))

		
	def send(self,msg):
		msg = msg + "\n"
		self.channel.reset_output_buffer()
		self.channel.write(msg.encode())
		self.channel.flush()#wait until all data is written.


	def getCurrentPosition(self):
		return self.position