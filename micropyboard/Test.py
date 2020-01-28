try:
    from machine import I2C
except ImportError as error:
    # Output expected ImportErrors.
    print(error.__class__.__name__ + ": " + str(error))

try:
    from machine import Pin
except ImportError as error:
    # Output expected ImportErrors.
    print(error.__class__.__name__ + ": " + str(error))

try:
    from utsys01 import TSYS01
except ImportError as error:
    # Output expected ImportErrors.
    print(error.__class__.__name__ + ": " + str(error))

try:
    from ums5837 import MS5837
except ImportError as error:
    # Output expected ImportErrors.
    print(error.__class__.__name__ + ": " + str(error))

# Intialize I2C Bus X
Pin('PULL_SCL', Pin.OUT, value=1)  # enable 5.6kOhm X9/SCL pull-up
Pin('PULL_SDA', Pin.OUT, value=1)  # enable 5.6kOhm X10/SDA pull-up
try:
    i2c = I2C('X', freq=400000)
except Exception as error:
    print(error.__class__.__name__ + ": " + str(error))
    i2c = None

# Instantiate TSYS01 (Temperature Sensor)
try:
    tsys01 = TSYS01(i2c)
except Exception as error:
    print(error.__class__.__name__ + ": " + str(error))
    tsys01 = None

# Initialize Sensor for reading
tsys01.init()
tsys01.read()
temp = tsys01.temperature()
print("Temperature from TSYS01: ", temp)

# Instantiate MS5837 (Pressure Sensor)
try:
    ms5837 = MS5837(i2c)
except Exception as error:
    print(error.__class__.__name__ + ": " + str(error))
    ms5837 = None

# Initialize Pressure Sensor for reading
ms5837.init()
ms5837.read()
pressure = ms5837.pressure()
temperature = ms5837.temperature()
print("Temperature from MS5837: ", temperature)
print("Pressure from MS5837: ", pressure)
