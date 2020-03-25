from ucollections import namedtuple

struct_time = namedtuple("struct_time", "tm_year tm_mon tm_mday tm_hour tm_min tm_sec tm_wday tm_yday tm_isdst")


class Test:
    #struct_time = namedtuple("struct_time", "tm_year tm_mon tm_mday tm_hour tm_min tm_sec tm_wday tm_yday tm_isdst")

    def __init__(self, time=struct_time(1970, 1, 1, 0, 0, 0, 0, 1, -1)):
        self.utc_time = time

    @property
    def utc_time(self):
        print("Getting UTC Time...")
        return self._timestamp_utc

    @utc_time.setter
    def utc_time(self, time: struct_time):
        print("Setting UTC time...")
        self._timestamp_utc = time

    def set_utc_time(self, time: tuple):
        print("Setting Time from Tuples")
        self._timestamp_utc = struct_time(time[0], time[1], time[2], time[3], time[4], time[5], time[6], time[0], time[0])


test = Test()
print(test.utc_time)
print(test.utc_time)
print(struct_time)
test.utc_time = struct_time(2020, 2, 10, 13, 39, 15, 0, 41, 0)
print(test.utc_time)
current_time = (2020, 2, 10, 17, 3, 0, 0, 1, -1)
test.set_utc_time(current_time)
print(test.utc_time)

"""
class Celsius:
    def __init__(self, temperature=0):
        self.temperature = temperature

    def to_fahrenheit(self):
        return (self.temperature * 1.8) + 32

    @property
    def temperature(self):
        print("Getting value")
        return self._temperature

    @temperature.setter
    def temperature(self, value):
        if value < -273:
            raise ValueError("Temperature below -273 is not possible")
        print("Setting value to ", value)
        self._temperature = value


test = Celsius(25)
print(test.temperature)
test.temperature = 30
print(test.temperature)
"""