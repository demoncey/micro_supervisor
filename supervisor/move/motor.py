import logging
import threading
import time

import RPi.GPIO as _gpio

from task.task import Task
#https://forbot.pl/blog/kurs-raspberry-pi-pwm-wejscia-kamera-w-pythonie-id26930
class Motor(threading.Thread):
	_freq = 0
	_within = 0
	_wait = 0.5
	
	def __init__(self,lock,queue,pinA,pinB):
		self._lock = lock
		self._queue = queue
		self._pinA = pinA
		self._pinB = pinB
		super().__init__(target = self.run, args = ())


	def initialize(self,freq,within):
		self._within = within	
		self._freq =  freq
		_gpio.setup(self._pinA, _gpio.OUT)
		_gpio.setup(self._pinB, _gpio.OUT)

	def run(self):
		motorA = _gpio.PWM(self._pinA, self._freq)
		motorB = _gpio.PWM(self._pinB, self._freq)
		while(True):
			self._lock.acquire()	
			print("running motor thread ")
			motorA.start(self._within)
			self._lock.release()
			time.sleep(self._wait)