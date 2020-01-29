from utime import sleep
from machine import I2C
from machine import Pin
from utsys01 import TSYS01
from ums5837 import MS5837


# Intialize I2C Bus X
Pin('PULL_SCL', Pin.OUT, value=1)  # enable 5.6kOhm X9/SCL pull-up
Pin('PULL_SDA', Pin.OUT, value=1)  # enable 5.6kOhm X10/SDA pull-up
try:
    i2c = I2C('X', freq=400000)
except Exception as error:
    print(error.__class__.__name__ + ": " + str(error))
    i2c = None


"""
# Intialize I2C Bus Y
y9 = Pin('Y9', Pin.OUT, Pin.PULL_UP)  # enable 5.6kOhm Y9/SCL pull-up
y10 = Pin('Y10', Pin.OUT, Pin.PULL_UP)  # enable 5.6kOhm Y10/SDA pull-up
try:
    i2c = I2C('Y', freq=400000)
    print(i2c.scan())
except Exception as error:
    print(error.__class__.__name__ + ": " + str(error))
    i2c = None
"""

# Instantiate TSYS01 (Temperature Sensor)
try:
    tsys01 = TSYS01(i2c)
except Exception as error:
    print(error.__class__.__name__ + ": " + str(error))
    tsys01 = None

# Instantiate MS5837 (Pressure Sensor)
try:
    ms5837 = MS5837(i2c)
except Exception as error:
    print(error.__class__.__name__ + ": " + str(error))
    ms5837 = None

# Initialize Temperature Sensor for reading
tsys01.init()
# Initialize Pressure Sensor for reading
ms5837.init()
for i in range(10):
    tsys01.read()
    ms5837.read()
    temperature_1 = tsys01.temperature()
    pressure = ms5837.pressure()
    temperature_2 = ms5837.temperature()
    print("Temperature in Centrigrade from TSYS01: {:0.4f} and from MS5837: {:0.4f}".format(temperature_1, temperature_2))
    print("Pressure in mBar from MS5837: {:0.4f}".format(pressure))
    sleep(1.0)


