import logging
import threading
import time
import queue
from random import randrange

import RPi.GPIO as _gpio

from task.task import Task
from comm.communication import Bluetooth

#https://realpython.com/python-pep8/
lock = threading.Lock()
queue = queue.Queue()

def blink(name,pin_nb,init):
	level = init
	while(True):
		lock.acquire()
		if(queue.empty() == False):
			task  = queue.get();
			print("running thread ",name)
			get_level = lambda x: x%2
			_gpio.output(pin_nb, get_level(task.get_payload()))
			queue.task_done();
		else:
			print("Queue empty just waiting ...")
		lock.release()
		time.sleep(1)

def init():
	_gpio.setwarnings(False) 
	_gpio.setmode(_gpio.BCM)
	_gpio.setup(20, _gpio.OUT, initial =_gpio.LOW)
	_gpio.setup(21, _gpio.OUT, initial =_gpio.LOW)
	print("Init done ....")

def main():
	print("Warming up Robot supervisor ....")
	init()

	bluetooth = Bluetooth(lock,queue)
	thread_1 = threading.Thread(target = blink, args = ("thread 1",20,_gpio.HIGH))
	thread_2 = threading.Thread(target = blink, args = ("thread 2",21,_gpio.HIGH))

	bluetooth.start()
	thread_1.start()
	thread_2.start()

	queue.join()

	bluetooth.join()
	thread_1.join()
	thread_2.join()


if __name__ == '__main__':
    main()