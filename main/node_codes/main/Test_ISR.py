import pyb, micropython

micropython.alloc_emergency_exception_buf(100)


class Foo(object):
    def __init__(self, timer, led):
        self.led = led
        timer.callback(None)

    def cb(self, tim):
        self.led.toggle()


pyb.LED(1).on()
pyb.LED(2).off()
red = Foo(pyb.Timer(4, freq=1), pyb.LED(1))
green = Foo(pyb.Timer(2, freq=1), pyb.LED(2))
pyb.LED(1).off()
pyb.LED(2).off()
