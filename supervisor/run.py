import logging
import threading
import time
import queue
from random import randrange

import RPi.GPIO as _gpio


from  utils.blink import Blink
from task.task import Task
from comm.communication import Bluetooth


#https://realpython.com/python-pep8/
lock = threading.Lock()
queue = queue.Queue()

def init():
	_gpio.setwarnings(False) 
	_gpio.setmode(_gpio.BCM)
	#_gpio.setup(20, _gpio.OUT, initial =_gpio.LOW)
	#_gpio.setup(21, _gpio.OUT, initial =_gpio.LOW)
	print("Init done ....")

def main():
	print("Warming up Robot supervisor ....")
	init()

	bluetooth = Bluetooth(lock,queue)
	blink_20 = Blink(lock,queue,20,_gpio.HIGH)
	blink_21 = Blink(lock,queue,21,_gpio.HIGH)

	blink_20.initialize()
	blink_21.initialize()

	bluetooth.start()
	blink_20.start()
	blink_21.start()

	queue.join()

	bluetooth.join()
	blink_20.join()
	blink_21.join()

if __name__ == '__main__':
    main()