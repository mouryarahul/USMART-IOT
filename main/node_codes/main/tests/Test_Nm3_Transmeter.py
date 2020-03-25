import utime
from machine import UART
from machine import Pin
from unm3driver import MessagePacket
from unm3driver import Nm3

# Global Constant
SOUND_SPEED = 320.0  # m/s

# Switch ON 3.3V to TTL-RS232 converter
p33v_1 = Pin('EN_3V3', mode=Pin.OUT, pull=Pin.PULL_UP, value=1)
# Wait until the LDO stabilizes the output voltage
utime.sleep(3.0)

# Initialize UART
uart1 = UART(1, 9600)
uart1.init(9600, bits=8, parity=None, stop=1, timeout=50, flow=0, timeout_char=0, read_buf_len=64)
# Instantiate Nm3
nm3 = Nm3(uart1)

# Get Nanomodem Address and Voltage status
addr = nm3.get_address()
print('Get Address=' + '{:03d}'.format(addr))
voltage = nm3.get_battery_voltage()
print('Battery Voltage=' + '{:0.2f}'.format(voltage) + 'V')

# Ping a node 175
tof = nm3.send_ping(175)
distance = tof*SOUND_SPEED
print('Time of Flight to ' '{:03d}'.format(addr) + ' = ' + '{:.4f}'.format(tof) + 's' + ' distance = ' + '{:.4f}'.format(distance) + 'm')


# Broadcast "hello" msg packet
msg = b'Hello'
for i in range(8):
    tstart = utime.ticks_us()
    nm3.send_broadcast_message(msg)
    tend = utime.ticks_us()
    print("Time Elasped in ms {}".format(utime.ticks_diff(tend, tstart)/1E3))
    utime.sleep_ms(2000)
