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
	_motors = {}

	set_pwm = lambda self,x : _gpio.setup(x, _gpio.OUT)
	set_pin = lambda self,x,y : _gpio.setup(x, _gpio.OUT, initial = y)
	
	def __init__(self,lock,queue):
		self._lock = lock
		self._queue = queue
		super().__init__(target = self.run, args = ())

	def init(self,freq,within):
		self._within = within	
		self._freq =  freq
		return self

	def setup_motor(self,name,cfg):
		self._motors[name] = cfg
		self.set_pwm(cfg[0])
		self.set_pin(cfg[1],_gpio.LOW)
		self.set_pin(cfg[2],_gpio.LOW)
		return self		

	def forward_motor(self,name):
		cfg = self._motors[name]
		self.set_pin(cfg(1),_gpio.HIGH)
		self.set_pin(cfg(1),_gpio.LOW)
		
	def backward_motor(self,name):
		cfg = self._motors[name]
		self.set_pin(cfg(1),_gpio.LOW)
		self.set_pin(cfg(1),_gpio.HIGH)

	def stop_motor(self,name):
		cfg = self._motors[name]
		self.set_pin(cfg(1),_gpio.LOW)
		self.set_pin(cfg(1),_gpio.LOW)

	def run(self):
		motor_A = _gpio.PWM(self._motors["right"][0], self._freq)
		motor_B = _gpio.PWM(self._motors["left"][0], self._freq)
		while(True):
			self._lock.acquire()	
			print("running motor thread ")
			motor_A.start(self._within)
			self._lock.release()
			time.sleep(self._wait)