import logging
import threading
import time

import RPi.GPIO as _gpio
#https://realpython.com/python-pep8/

g_lock = threading.Lock()



def blink(name,pin_nb,init):
	level = init
	while(1):
		g_lock.acquire()
		print("running thread ",name)
		_gpio.output(pin_nb, level)
		if(level == _gpio.LOW):
			level = _gpio.HIGH
		else :
			level = _gpio.LOW
		g_lock.release()
		time.sleep(1)

def init():
	_gpio.setwarnings(False) # Ignore warning for now
	_gpio.setmode(_gpio.BCM) # Use physical pin numbering
	_gpio.setup(20, _gpio.OUT, initial=_gpio.LOW)
	_gpio.setup(21, _gpio.OUT, initial=_gpio.LOW)

def main():
	print("Warming up Robot supervisor ....")
	init()
	thread_1 = threading.Thread(target=blink, args=("thread 1",20,_gpio.LOW))
	thread_2 = threading.Thread(target=blink, args=("thread 2",21,_gpio.HIGH))

	thread_1.start()
	thread_2.start()

	thread_1.join()
	thread_2.join()

if __name__ == '__main__':
    main()