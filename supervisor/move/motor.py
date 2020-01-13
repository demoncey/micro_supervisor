import logging
import threading
import time

import RPi.GPIO as _gpio

from task.task import Task

class Motor(threading.Thread):
	
	def __init__(self,lock,queue):
		self._lock = lock
		self._queue = queue
		self._wait = 0.5
		super().__init__(target = self.run, args = ())

	def run(self):
		while(True):
			self._lock.acquire()	
			print("running motor thread ")
			self._lock.release()
			time.sleep(self._wait)