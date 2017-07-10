import sys
import time
import threading 

class progressor:
	def __init__(self, ptype):
		self.type = ptype

	def start(self):
		if self.type == 'rotor':
			self.counter = rotor()
		elif self.type == 'linear':
			self.counter = linear()
		self.t = threading.Thread(target=self.counter.start)
		self.t.start()

	def stop(self):
		self.counter.stop()

	def update(self, value, eta='-'):
		self.counter.progress = value
		self.counter.eta = eta

class rotor:
	def __init__(self):
		self.running = False
		self.elements = ['/','-','\\']

	def start(self):
		self.running = True
		i=0
		while self.running:
			if(i > 100):
				i = 0
			print '   {}\r'.format(self.elements[i%3]),
			sys.stdout.flush()
			i+=1
			time.sleep(.2)
		return True

	def stop(self):
		self.running = False

class linear:
	def __init__(self):
		self.progress = 0
		self.elements = ['#','#','-']
		self.eta = '-'

	def start(self):
		while self.progress <= 100:
			print '   [{}{}{}]  {}%\t\t{} sec\r'.format(self.elements[0]*(self.progress/5), self.elements[1],self.elements[2]*(20-(self.progress/5)), self.progress, self.eta),
			sys.stdout.flush()
		return True

	def stop(self):
		self.progress = 101

