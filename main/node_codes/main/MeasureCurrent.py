import utime
from pyb import LED
from machine import Pin
from machine import UART
from unm3driver import MessagePacket
from unm3driver import Nm3


# Wait for few seconds to turn on the 3.3V supply
utime.sleep(3.0)

# Switch ON 3.3V to TTL-RS232 converter
p33v_1 = Pin('EN_3V3', mode=Pin.OUT, pull=Pin.PULL_UP, value=1)

utime.sleep(2.0)

# Initialize UART
uart1 = UART(1, 9600)
uart1.init(9600, bits=8, parity=None, stop=1, timeout=50, flow=0, timeout_char=0, read_buf_len=64)

# Instantiate Nm3
nm3 = Nm3(uart1)

# Instantiate LEDs
led_R = LED(1)
led_G = LED(2)

led_R.off()
led_G.off()

#utime.sleep(6.0)
# Repeated Broadcast of "Hello World"
for i in range(5):
    led_R.on()
    byte_count = nm3.send_broadcast_message(b'Hello World')
    print("{:d} bytes where broadcasted.".format(byte_count))
    led_R.off()
    utime.sleep(3.0)

# Switch Off 3.3V to TTL-RS232 converter
p33v_1.value(0)
