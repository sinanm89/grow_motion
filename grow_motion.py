# Simple example of reading the MCP3008 analog input channels and printing
# them all out.
# Author: Tony DiCola
# License: Public Domain
import time
import os
from datetime import datetime
# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

import picamera

# Software SPI configuration #pin:
CLK  = 18
MISO = 23
MOSI = 24
CS   = 25
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

while True:
	avg_humid = 0
	for i in range(average_frequency):
	    # Read all the ADC channel values in a list
	        # The read_adc function will get the value of the specified channel (0-7).
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
        try:
            camera = picamera.PiCamera()
        except picamera.exc.PiCameraError:
            print 'camera borked, moving on.'
            continue
        except Exception, e:
            print 'WOW FATAL EXCEPTION'
            print e
            continue
        now = datetime.now().strftime('%s')
	pic_name = '{time}_{humidity}.jpg'.format(time=now, humidity=humidity)
	camera.capture('{}/{}'.format(DIR_NAME, pic_name))
	print 'took {}'.format(pic_name)
	time.sleep(2*60)
