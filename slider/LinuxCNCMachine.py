
import linuxcnc
"""
User interfaces control LinuxCNC activity by sendind NML messages to the LinuxCNC task controller
and monitor results by observing the LinuxCNC status structure

"""
class LinuxCNCMachine():	

	def __init__(self):
		self.emc = linuxcnc
		self.status = self.emc.stat()
		self.command = self.emc.command()
		self.error = self.emc.error_channel()
	
		self.maxVelocity = 8.0
		self.axis = 2

		self.startCommand()
		self.setModeCommand(linuxcnc.MODE_MANUAL)
		self.doUnhome()

	def resetCommand(self):
		self.status.poll()
		if self.status.task_state==linuxcnc.STATE_ON:
			self.setStateCommand(linuxcnc.STATE_ESTOP)
			sleep(0.25)
			self.setStateCommand(linuxcnc.STATE_ESTOP_RESET)
			sleep(0.25)
		if self.status.task_state==linuxcnc.STATE_ESTOP:
			self.setStateCommand(linuxcnc.STATE_ESTOP_RESET)
			sleep(0.25)
		self.setStateCommand(linuxcnc.STATE_ON)
		sleep(0.25)

	def startCommand(self):
		self.status.poll()
		if self.status.task_state == linuxcnc.STATE_ESTOP:
			self.setStateCommand(linuxcnc.STATE_ESTOP_RESET)
			sleep(0.25)
			self.setStateCommand(linuxcnc.STATE_ON)
			sleep(0.25)
		if self.status.task_state == linuxcnc.STATE_ESTOP_RESET:
			self.setStateCommand(linuxcnc.STATE_ON)
			sleep(0.25)

	def setStateCommand(self,state):
		self.status.poll()#method to update current status attributes.
		if self.status.task_state != state:
			self.command.state(state)       

	def getStateCommand(self):
		return self.status.task_state

	def setModeCommand(self,mode):
		self.status.poll()
		if self.status.task_mode != mode:
			self.command.mode(mode)

	def isHome(self,axismask):
		self.status.poll()
		return self.status.axis[axismask]['homed']

	def waitToComplete(self,velocity,delay=1):
		distance = abs(self.getCurrentPosition())
		timeout = distance/velocity + delay
		sleep(timeout)
		self.resetCommand()

	def doHome(self,waitComplete=True,axismask=2):
		self.status.poll()
		if self.isHome(axismask):
			self.resetCommand()
		self.command.home(axismask)
		self.setStateMachine(MachineState.HOMED)
		if waitComplete:
			self.waitToComplete()

	def doUnhome(self,axismask=2):
		self.status.poll()
		if self.isHome(axismask):
			self.command.unhome(axismask)
			self.resetCommand()

	def getCurrentPosition(self, axismask = 2):
		self.status.poll()
		return self.status.position[axismask]

	def move(self,velocity, direction, step, axismask = 2, delay = 1):
		self.status.poll()
		self.setStateCommand(linuxcnc. STATE_ON)
		self.command.jog(linuxcnc.JOG_INCREMENT,axismask,direction*velocity,step)
		self.waitToComplete()

	def moveContinuous(self,direction,axismask=2):
		self.status.poll()
		self.setStateCommand(linuxcnc. STATE_ON)
		self.command.jog(linuxcnc.JOG_CONTINUOUS,axismask,direction*self.maxVelocity)
		self.waitToComplete()

	def goOn(self):
		self.moveContinuous(1)

	def goBack(self):
		self.moveContinuous(-1)

	def stopMoving(self, axismask = 2):
		self.command.jog(linuxcnc.JOG_STOP,axismask)

	def printHomeState(self, axismask):
		print "HOMED: "+ str(self.isHome(axismask))



		






