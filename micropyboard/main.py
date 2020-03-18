# Your code goes here

import utime
from pyb import LED


# list of leds (1:red, 2:green, 3:blue)
leds = [LED(i) for i in range(1,4)]
# switch off all
for led in leds:
	led.off()

# Toggle the leds in sequence
for i in range(100):
	leds[i%3].on()
	utime.sleep(1.)
	led[i%3].off()
	utime.sleep(1.)


