# boot.py -- run on boot-up
# can run arbitrary Python, but best to keep it minimal

import pyb
from machine import Pin
# Switch OFF the Main 3.3V LDO
Pin('Y5', mode=Pin.OPEN_DRAIN, pull=None, value=0)
# Switch OFF 3.3V to TTL-RS232 converter
Pin('EN_3V3', mode=Pin.OUT, pull=Pin.PULL_UP, value=0)

pyb.country('GB')  # ISO 3166-1 Alpha-2 code, eg US, GB, DE, AU
#pyb.main('main.py') # main script to run after this one
#pyb.usb_mode('VCP+MSC') # act as a serial and a storage device
#pyb.usb_mode('VCP+HID') # act as a serial device and a mouse
