import logging
import threading
import time
import queue
from random import randrange

import RPi.GPIO as _gpio

from  utils.blink import Blink
from task.task import Task
from comm.communication import Bluetooth
from move.motor import Motor


#https://realpython.com/python-pep8/
lock = threading.Lock()
queue = queue.Queue()

def init():
	_gpio.setwarnings(False) 
	_gpio.setmode(_gpio.BCM)
	print("Init done ....")

def main():
	print("Warming up Robot supervisor ....")
	init()

	threads = []

	bluetooth = Bluetooth(lock,queue)
	motor = Motor(lock,queue)
	blink_20 = Blink(lock,queue,20,_gpio.HIGH)
	blink_21 = Blink(lock,queue,21,_gpio.HIGH)

	blink_20.init()
	blink_21.init()
	motor.init(5,50)
	motor.setup_motor("right",(16,0,0))
	motor.setup_motor("left",(0,0,0))

	bluetooth.start()
	motor.start()
	blink_20.start()
	blink_21.start()

	queue.join()

	bluetooth.join()
	motor.join()
	blink_20.join()
	blink_21.join()

if __name__ == '__main__':
    main()