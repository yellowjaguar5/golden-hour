# -*- coding: utf-8 -*-

from board import SCL, SDA, G0
from busio import I2C
from digitalio import DigitalInOut, Direction, Pull
from adafruit_pm25 import PM25_I2C

reset_pin = None
# If you have a GPIO, its not a bad idea to connect it to the RESET pin
# reset_pin = DigitalInOut(board.G0)
# reset_pin.direction = Direction.OUTPUT
# reset_pin.value = False


def read():
    # Create library object, use 'slow' 100KHz frequency!
    i2c = I2C(SCL, SDA, frequency=100000)
    # Connect to a PM2.5 sensor over I2C
    sensor = PM25_I2C(i2c, reset_pin)
    print("Found PM2.5 sensor, reading data...")

    try:
        aq_data = sensor.read()
        # print(aq_data)
        return [  # aq_data["pm10 standard"],
                aq_data["pm25 standard"],
                aq_data["pm100 standard"]]
    except RuntimeError:
        print("Unable to read from sensor, retrying...")
        return None


"""
Sample module for Adafruit 4632 (PMSA003I) sensor
More details & credit to: 
    https://github.com/adafruit/Adafruit_CircuitPython_PM25
"""

if __name__ == '__main__':
    from time import sleep

    # Create library object, use 'slow' 100KHz frequency!
    i2c_test = I2C(SCL, SDA, frequency=100000)
    # Connect to a PM2.5 sensor over I2C
    pm25 = PM25_I2C(i2c_test, reset_pin)
    print("Found PM2.5 sensor, reading data...")

    while True:
        sleep(1)
        try:
            aqdata = pm25.read()
            # print(aqdata)
        except RuntimeError:
            print("Unable to read from sensor, retrying...")
            continue

        print("Concentration Units (standard)")
        print("---------------------------------------")
        print(
            "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
            % (aqdata["pm10 standard"], aqdata["pm25 standard"],
               aqdata["pm100 standard"])
        )
        print("Concentration Units (environmental)")
        print("---------------------------------------")
        print(
            "PM 1.0: %d\tPM2.5: %d\tPM10: %d"
            % (aqdata["pm10 env"], aqdata["pm25 env"], aqdata["pm100 env"])
        )
        print("---------------------------------------")
        print("Particles > 0.3um / 0.1L air:", aqdata["particles 03um"])
        print("Particles > 0.5um / 0.1L air:", aqdata["particles 05um"])
        print("Particles > 1.0um / 0.1L air:", aqdata["particles 10um"])
        print("Particles > 2.5um / 0.1L air:", aqdata["particles 25um"])
        print("Particles > 5.0um / 0.1L air:", aqdata["particles 50um"])
        print("Particles > 10 um / 0.1L air:", aqdata["particles 100um"])
        print("---------------------------------------\n")
