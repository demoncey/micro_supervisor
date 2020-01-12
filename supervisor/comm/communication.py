import logging
import threading
#import bluetooth
import time
from random import randrange



from task.task import Task

class Bluetooth:
	def __init__(self,lock,queue):
		self._lock = lock
		self._queue = queue
		self._thread = threading.Thread(target = self.run, args = ())

	def run(self):
		while(True):
			self._lock.acquire()	
			rand = randrange(1,20,1) 
			print("running bluetooth thread ",rand)
			self._queue.put(Task("random task",rand))
			self._lock.release()
			time.sleep(0.1)

	def start(self):
		self._thread.start()

	def join (self):
		self._thread.join()
		
	def get_thread(self):
		return self._thread
