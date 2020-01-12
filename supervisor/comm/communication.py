import logging
import threading
#import bluetooth
import time
from random import randrange



from task.task import Task

class Bluetooth(threading.Thread):
	
	def __init__(self,lock,queue):
		self._lock = lock
		self._queue = queue
		self._wait = 0.1
		super().__init__(target = self.run, args = ())

	def run(self):
		while(True):
			self._lock.acquire()	
			rand = randrange(1,20,1) 
			print("running bluetooth thread ",rand)
			self._queue.put(Task("random task",rand))
			self._lock.release()
			time.sleep(0.2)
