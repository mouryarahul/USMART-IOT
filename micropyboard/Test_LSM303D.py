from utime import sleep
from machine import I2C
from machine import Pin
from pyb import LED
from lsm303d import LSM303D


def main():
    # Instantiate LEDs
    led_R = LED(1)
    led_G = LED(2)
    led_B = LED(3)
    led_R.off()
    led_G.off()
    led_B.off()

    # Switch ON 3.3V external LDO
    p33v_2 = Pin('Y5', mode=Pin.OPEN_DRAIN, pull=None, value=1)

    # Wait for few seconds to turn on the 3.3V supply
    sleep(3.0)

    # Initialize I2C X bus
    Pin('PULL_SCL', Pin.OUT, value=1)  # enable 5.6kOhm X9/SCL pull-up
    Pin('PULL_SDA', Pin.OUT, value=1)  # enable 5.6kOhm X10/SDA pull-up
    try:
        i2c_bus = I2C('X', freq=400000)
        print(i2c_bus.scan())
    except Exception as error:
        print(error.__class__.__name__ + ": " + str(error))
        i2c_bus = None

    try:
        lsm303 = LSM303D(i2c_bus)
    except Exception as error:
        print(error.__class__.__name__ + ": " + str(error))
        lsm303 = None

    if lsm303:
        x_p, y_p, z_p = lsm303.accelerometer()
        mx_p, my_p, mz_p = lsm303.magnetometer()
        for i in range(20):
            led_R.on()
            x_c, y_c, z_c = lsm303.accelerometer()
            #print("Current Acceleration: {:+06.2f}g : {:+06.2f}g : {:+06.2f}g".format(x_c, y_c, z_c))
            print("Accel Diff. : {:0.4f}g : {:0.4f}g : {:0.4f}g".format(x_c-x_p, y_c-y_p, z_c-z_p))
            (x_p, y_p, z_p) = (x_c, y_c, z_c)
            sleep(0.5)
            led_R.off()
            led_G.on()
            mx_c, my_c, mz_c = lsm303.magnetometer()
            #print("Magnetic Field: {:+06.2f} : {:+06.2f} : {:+06.2f}".format(mx_c, my_c, mz_c))
            print("Magnetic Diff. : {:0.4f} : {:0.4f} : {:0.4f}".format(mx_c - mx_p, my_c - my_p, mz_c - mz_p))
            (mx_p, my_p, mz_p) = (mx_c, my_c, mz_c)
            sleep(0.5)
            led_G.off()
            led_B.on()
            temperature = lsm303.temperature()
            print("Temperature : {:0.4f}".format(temperature))
            sleep(0.5)
            led_B.off()

    # Switch ON 3.3V to TTL-RS232 converter
    p33v_2.value(0)


if __name__ == '__main__':
    main()
