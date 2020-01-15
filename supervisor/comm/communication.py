import logging
import threading
#import bluetooth
import time
from random import randrange



from task.task import Task

class Bluetooth(threading.Thread):
	_wait = 0.2
	def __init__(self,lock,queue):
		self._lock = lock
		self._queue = queue
		
		super().__init__(target = self.run, args = ())

	def run(self):
		while(True):
			self._lock.acquire()	
			rand = randrange(1,20,1) 
			print("running bluetooth thread ",rand)
			self._queue.put(Task("random task",rand))
			self._lock.release()
			time.sleep(self._wait)
