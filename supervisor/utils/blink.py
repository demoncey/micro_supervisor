import logging
import threading

import RPi.GPIO as _gpio


from task.task import Task

class Blink:

	def __init__(self,lock,queue,pin,init_level):
		self._lock = lock
		self._queue = queue
		self._thread = threading.Thread(target = self.run, args = ())
		self._pin = pin
		self._init_level = init_level

	def initialize(self):
		_gpio.setup(self._pin, _gpio.OUT, initial = self._init_level)
		
	def run(self):
		while(True):
			self._lock.acquire()
			if(self._queue.empty() == False):
				task  = self._queue.get(False);
				print("running thread  for pin ",self._pin)
				get_level = lambda x: x%2
				_gpio.output(self._pin, get_level(task.get_payload()))
				self._queue.task_done();
			else:
				print("Queue empty just waiting ",self._pin," ")
			self._lock.release()
		time.sleep(1)

	def start(self):
		self._thread.start()

	def join (self):
		self._thread.join()
		
	def get_thread(self):
		return self._thread