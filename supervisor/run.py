import logging
import threading
import time
import queue
from random import randrange

import RPi.GPIO as _gpio

from task.task import Task

#https://realpython.com/python-pep8/
g_lock = threading.Lock()
g_queue = queue.Queue()

def blink(name,pin_nb,init):
	level = init
	while(True):
		g_lock.acquire()
		if(g_queue.empty() == False):
			task  = g_queue.get();
			print("running thread ",name)
			get_level = lambda payload: payload%2
			_gpio.output(pin_nb, get_level(task.get_payload()))
			g_queue.task_done();
		else:
			print("Queue empty just waiting ...")
		g_lock.release()
		time.sleep(1)

def blutooth_listerner(name):
	while(True):
		g_lock.acquire()		
		rand = randrange(1,20,1) 
		print("running thread ",name," ",rand)
		g_queue.put(Task("random task",rand))
		g_lock.release()
		time.sleep(0.1)

def init():
	_gpio.setwarnings(False) 
	_gpio.setmode(_gpio.BCM)
	_gpio.setup(20, _gpio.OUT, initial=_gpio.LOW)
	_gpio.setup(21, _gpio.OUT, initial=_gpio.LOW)
	print("Init done ....")

def main():
	print("Warming up Robot supervisor ....")
	init()

	thread_1 = threading.Thread(target=blink, args=("thread 1",20,_gpio.HIGH))
	thread_2 = threading.Thread(target=blink, args=("thread 2",21,_gpio.HIGH))
	blue_thread = threading.Thread(target=blutooth_listerner, args=("blutooth thread",))

	blue_thread.start()
	thread_1.start()
	thread_2.start()

	g_queue.join()

	thread_1.join()
	thread_2.join()
	blue_thread.join()

if __name__ == '__main__':
    main()