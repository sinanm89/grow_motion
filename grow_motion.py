#! /usr/bin/python -u
"""
Garden health measurement system.

Reads humidity, temperature around a plant and in the soil, writes to db and
takes the picture of the plant.
"""
import time
import os
from datetime import datetime
# Import SPI library (for hardware SPI) and MCP3008 library.
# import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

import picamera
from dht11.dht11 import DHT11
import RPi.GPIO as GPIO

# for dht11 ambient setup
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.cleanup()

DHT11_PIN = 17

# Software SPI configuration #pin:
CLK = 18
MISO = 23
MOSI = 24
CS = 25
mcp = Adafruit_MCP3008.MCP3008(clk=CLK, cs=CS, miso=MISO, mosi=MOSI)

# Hardware SPI configuration:
# SPI_PORT   = 0
# SPI_DEVICE = 0
# mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))


print('Reading MCP3008 values, press Ctrl-C to quit...')
# Print nice channel column headers.
# Main program loop.
DIR_NAME = 'grow_motion'
if not os.path.exists(DIR_NAME):
    print 'creating {} directory...'.format(DIR_NAME)
    os.makedirs(DIR_NAME)
dry = 1023
wet = normalize_wet = 600
delta_wet = dry - wet

average_frequency = 3


def take_ambient_values():
    """
    Read the dht11 module.

    The custom dht11 module is on git@github.com:sinanm89/DHT11_Python.git
    """
    instance = DHT11(pin=DHT11_PIN)
    result = instance.read()
    if result.is_valid():
        print("Last valid input: " + str(datetime.datetime.now()))
        print("Temperature: %d C" % result.temperature)
        print("Humidity: %d %%" % result.humidity)
        return result.temperature, result.humidity


def take_soil_values():
    """
    Read the moisture sensor connected to the MCP3008.

    The important part is mcp.read_adc(channel_number), you can read up to 8
    which is the number of inputs the physical chip has.
    """
    avg_humid = 0
    for i in range(average_frequency):
        # Read all the ADC channel values in a list
        # The read_adc function will get the value of the channel (0-7)
        temp_humid = mcp.read_adc(0)
        avg_humid += temp_humid
        time.sleep(0.5)
    # (960 + 962 + 961) / 3
    avg_humid = avg_humid / average_frequency
    # 961 - (600)
    avg_humid = avg_humid - normalize_wet
    # 361 / 423 = 0.8, so its pretty moist.
    avg_humid_percentage = float(avg_humid) / delta_wet
    time.sleep(0.5)
    now = datetime.now().strftime('%s')
    pic_name = '{time}_0{humidity}.jpg'.format(
        time=now, humidity=int(avg_humid_percentage * 100))
    trial = 'took'
    try:
        with picamera.PiCamera() as camera:
            camera.vflip = True
            camera.capture('{0}/{1}'.format(DIR_NAME, pic_name))
    except picamera.exc.PiCameraError:
        print 'camera borked, moving on.'
    except Exception, e:
        print 'WOW FATAL EXCEPTION'
        trial = 'tried'
        print e
    print '{0} {1}'.format(trial, pic_name)

# main
while True:
    take_soil_values()
    take_ambient_values()
    print 'Sleeping for 2 minutes, see you soon ;)'
    time.sleep(2 * 60)
