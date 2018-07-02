import sys,os
from time import sleep
import math
import serial
from observable import Observable
from PyQt5.QtCore import *
import io
import time

class SliderStates:
	HOMED,READY,DONE = range(3)

class Slider(Observable, QThread):
	
	def __init__(self, velocity, offset, distance, name ="Slider", parent=None):
		QThread.__init__(self, parent)
		Observable.__init__(self)
		self.velocity = velocity
		self.offset = offset
		self.distance = distance
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

	def checkCurrentPosition(self):
		pass
		"""
		currentPosition = self.getCurrentPosition()
		firstStop = currentPosition + offset 
		finalStop = currentPosition + offset + distance
		while currentPosition <= finalStop:
			print("slider serial checkin position")
			currentPosition = self.getCurrentPosition()
			if currentPosition == 0 :
				self.setHome()#do home
			if currentPosition >= firstStop:
				if not(context.isReady()):
					context.setReady() #do ready
					#self.update_observers(state = MachineState.READY)
			if currentPosition >= (finalStop - 1):
				if not(context.isDone()):
					context.setDone() #do done
					#self.update_observers(state = MachineState.DONE)
					break
			self.position += 1
		"""

class SerialSlider(Slider):

	def __init__(self, velocity, offset, distance):
		super(SerialSlider, self).__init__(velocity, offset, distance)
		self.position = 0

	def init(self,device):
		try:
			self.channel = serial.Serial(device,9600,timeout=1)#open serial port
			self.sio = io.TextIOWrapper(io.BufferedRWPair(self.channel, self.channel))
			return True
		except Exception as e:
			print (e)
			return False
	
	def setAction(self,msg,context):
		self.action = msg
		self.context = context

	def run(self):
		self.send(self.action)
		print(self.action)
		print("waiting for serial")
		#tdata = self.channel.read()
		#print("waiting for serial 2")
		while (True):
			self.channel.reset_input_buffer()
			line = self.channel.readline()
			line = line.decode()
			line = line.rstrip('\n')
			line = line.replace('\r','')
			print("enviado por slider",line)
			if line == "SLIDER_MOVE_OK" or line=="SLIDER_STOP_OK":
				break
		print("sending message")
		self.context.send(line)
		print("message sent")
		#wait for response
		
	def send(self,msg):
		msg = msg + "\n"
		self.channel.reset_output_buffer()
		self.channel.write(msg.encode())
		self.channel.flush()#wait until all data is written.


	def getCurrentPosition(self):
		return self.position