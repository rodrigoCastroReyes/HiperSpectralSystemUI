import sys
import json
from PyQt4 import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class SynchronizedThread(QThread):

	def __init__(self,name,mutex,condition,target,parent = None):
		QThread.__init__(self, parent)
		self.name = name
		self.target = target
		self.mutex = mutex
		self.condition = condition

	def run():
		pass

class Updater(SynchronizedThread):

	def __init__(self,name,mutex,condition,target,parent = None):
		SynchronizedThread.__init__(self,name,mutex,condition,target,parent)

	def update(self,flag,callback):
		self.mutex.lock()#bloque el mutex para actualizar el target
		self.target[self.name] = flag
		#si flag == False quiere decir que una camara se ha desconectado y debe desactivarse el boton
		callback()
		self.condition.wakeOne()#informa al checker que hay un cambio
		self.mutex.unlock()#desbloquea el mutex para que otros hilos puedan revisar el target

	def run():
		pass


class Checker(SynchronizedThread):

	def __init__(self,name,mutex,condition,target,parent = None):
		SynchronizedThread.__init__(self,name,mutex,condition,target,parent)

	def check(self, isSatisfied , callback , callbackTwo ):
		#monitorea el estado del target para realizar una operacion dependiendo del cambio
		self.mutex.lock()
		if isSatisfied() : #si alguna condicion se cumple sobre el target se debe ejecutar el callback
			callback()
		else:#sino se ejecuta callback Two
			callbackTwo()
		self.condition.wait(self.mutex) #espera hasta que un updater cambie el estado de target
		self.mutex.unlock()

	def run():
		pass