import micropython
import pyb
import utime
from machine import UART
from machine import Pin

from unm3driver import MessagePacket
from unm3driver import Nm3

micropython.alloc_emergency_exception_buf(100)

# ==================== Global Variable ========================== #
packet_arrival_bflag = False
packet_arrival_time = 0


def rxs_callback(line):
    """
    Callback for ExtInt on pin 'Y3': An indication of reception of a packet at Nanomodem
    :param line:
    :return: None
    """
    global packet_arrival_time, packet_arrival_bflag
    packet_arrival_time = utime.ticks_us()
    packet_arrival_bflag = True


# Pins to control LDOs on the board:
# ldo1 controls the 3.3V ldo on the micropython board
# ldo2 controls the 3.3V ldo on daughter board
ldo1 = Pin('EN_3V3', mode=Pin.OUT, pull=Pin.PULL_UP)
ldo2 = Pin('Y5', mode=Pin.OPEN_DRAIN, pull=None)

# =================== Initialize different modules =================== #
# Configure I/O pin "Y3" as an external interrupt connected to RxS pin of Nanomodem
# Rising Edge on RxS pin indicate start of incoming packet on Nanomodem.
extint = pyb.ExtInt('Y3', pyb.ExtInt.IRQ_RISING, pyb.Pin.PULL_DOWN, rxs_callback)

# Initialize UART1 for Nanomodem
uart1 = UART(1, 9600)
uart1.init(9600, bits=8, parity=None, stop=1, timeout=50, flow=0, timeout_char=0, read_buf_len=64)
# Instantiate Nm3
nm3 = Nm3(uart1)


# Main Infinite Loop, where all data are processed and decision are taken
while True:
    # Check an arrival of data packet
    if packet_arrival_bflag:
        packet_arrival_bflag = False

        # Poll UART for data
        nm3.poll_receiver()

        # Periodically process any bytes received
        nm3.process_incoming_buffer()

        if nm3.has_received_packet():
            # record the packet arrival time and get the data payload
            message_packet = nm3.get_received_packet()
            payload_as_string = bytes(message_packet.packet_payload).decode('utf-8')