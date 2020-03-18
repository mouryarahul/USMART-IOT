import micropython
import pyb
import utime
from machine import UART
from machine import Pin

from unm3driver import MessagePacket
from unm3driver import Nm3

micropython.alloc_emergency_exception_buf(100)

SOUND_SPEED = 320.0  # m/s

# Global Variable
arrival_bflag = False
current_arrival_tick = 0
#previous_arrival_tick = 0


def rxs_callback(line):
    global current_arrival_tick, arrival_bflag
    current_arrival_tick = utime.ticks_us()
    arrival_bflag = True


# Switch ON 3.3V to TTL-RS232 converter
p33V = Pin('EN_3V3', mode=Pin.OUT, pull=Pin.PULL_UP, value=1)

# Initialize UART
uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1, timeout=50, flow=0, timeout_char=0, read_buf_len=64)

# Instantiate Nm3
nm3 = Nm3(uart)

addr = nm3.get_address()
print('Get Address=' + '{:03d}'.format(addr))

voltage = nm3.get_battery_voltage()
print('Battery Voltage=' + '{:.2f}'.format(voltage) + 'V')

# Ping a node
tof = nm3.send_ping(178)
distance = tof*SOUND_SPEED
print('Time of Flight to ' '{:03d}'.format(addr) + ' = ' + '{:.4f}'.format(tof) + 's' + ' distance = ' + '{:.4f}'.format(distance) + 'm')

"""
broadcast_message = 'Hello World Hello World Hello World Hello World!'
sent_bytes_count = nm3.send_broadcast_message(broadcast_message.encode('utf-8'))
print('Sent Broadcast Message of ' + str(sent_bytes_count) + ' bytes')
"""

# Need a pause between transmissions for the modem to finish the last one
utime.sleep(1.0)

# Configure I/O pin "Y3" as an external interrupt connected to RxS pin of Nanomodem
# Rising Edge on RxS pin indicate start of incoming packet on Nanomodem.
extint = pyb.ExtInt('Y3', pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, rxs_callback)
print(extint)

# Global Variable
current_arrival_tick = utime.ticks_us()
previous_arrival_tick = current_arrival_tick

# Receiving unicast and broadcast messages
while True:
    # print("Arrival Flag: ", arrival_bflag)
    # Poll the serial port for bytes if interrupt happen
    if arrival_bflag:
        # Set flag to False for next interrupt to set it True
        arrival_bflag = False

        # Poll UART for data
        nm3.poll_receiver()

        # Periodically process any bytes received
        nm3.process_incoming_buffer()

        # Periodically check for received packets
        if nm3.has_received_packet():
            time_elapsed = utime.ticks_diff(current_arrival_tick, previous_arrival_tick)
            previous_arrival_tick = current_arrival_tick

            message_packet = nm3.get_received_packet()
            payload_as_string = bytes(message_packet.packet_payload).decode('utf-8')

            print('Received a message packet: ' + MessagePacket.PACKETTYPE_NAMES[message_packet.packet_type] +
                  ' src: ' + str(message_packet.source_address) + ' data: ' + payload_as_string)
            print("Time elapsed since previous packet: {:04f}".format(time_elapsed/1E6))



    # Pause for a while before checking for new message
    utime.sleep(0.125)

