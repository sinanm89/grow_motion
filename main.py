#! /usr/local/bin/python
"""
Garden health measurement system.

Reads humidity, temperature around a plant and in the soil, writes to db and
takes the picture of the plant.
"""
import time
import os
from datetime import datetime

import sqlalchemy
from sqlalchemy.engine.url import URL
from sqlalchemy.orm import sessionmaker

import Adafruit_MCP3008

import picamera
from DHT11_Python.dht11 import DHT11
import RPi.GPIO as GPIO

from plants.models import Plant
from generic_models import Base
from local_settings import DATABASE


class LivingPlantView(object):
    """Plant information processor Factory."""

    DHT11_PIN = 17

    # Software SPI configuration #pin:
    CLK = 18
    MISO = 23
    MOSI = 24
    CS = 25

    DIR_NAME = 'grow_motion'

    dry = 1023
    wet = 600
    normalize_wet = 600
    delta_wet = dry - wet

    average_frequency = 3

    def __init__(self):
        """Create the LivingPlantView."""
        engine = sqlalchemy.create_engine(URL(**DATABASE))
        self.session = sessionmaker(bind=engine)
        # Create table if it doesnt exist.
        Base.metadata.create_all(engine)

        self.model = Plant()

        # Hardware SPI configuration:
        # SPI_PORT   = 0
        # SPI_DEVICE = 0
        # mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

        if not os.path.exists(self.DIR_NAME):
            print 'creating {} directory...'.format(self.DIR_NAME)
            os.makedirs(self.DIR_NAME)

    def process_item(self, data):
        """Save deals in the database.

        This method is called for every item pipeline component.

        """
        session = self.session()
        obj = Plant(**data)

        try:
            session.add(obj)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()
        return obj

    def read_values(self):
        """Read all values from every sensor."""
        avg_humid_percentage, time = self.take_soil_values()
        temperature, humidity = self.take_ambient_values()
        data = dict(
            measured_at=datetime.fromtimestamp(float(time)),
            name=time,
            ambient_temperature=float(temperature) if temperature else None,
            ambient_humidity=float(humidity) if humidity else None,
            soil_humidity=float(avg_humid_percentage)
        )
        self.process_item(data)

    def take_ambient_values(self):
        """
        Read the dht11 module.

        The custom dht11 module is on git@github.com:sinanm89/DHT11_Python.git
        """
        instance = DHT11(pin=self.DHT11_PIN)
        result = instance.read()
        if result.is_valid():
            print("Last valid input: " + str(datetime.now()))
            print("Temperature: %d C" % result.temperature)
            print("Humidity: %d %%" % result.humidity)
            return result.temperature, result.humidity
        return None, None

    def take_soil_values(self):
        """
        Read the moisture sensor connected to the MCP3008.

        The important part is mcp.read_adc(channel_number), you can read up to
        8 which is the number of inputs the physical chip has.
        """
        avg_humid = 0
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BCM)
        GPIO.cleanup()

        self.mcp = Adafruit_MCP3008.MCP3008(
            clk=self.CLK, cs=self.CS, miso=self.MISO, mosi=self.MOSI)

        for i in range(self.average_frequency):
            # Read all the ADC channel values in a list
            # The read_adc function will get the value of the channel (0-7)
            temp_humid = self.mcp.read_adc(0)
            avg_humid += temp_humid
            time.sleep(0.5)
        # (960 + 962 + 961) / 3
        avg_humid = avg_humid / self.average_frequency
        # 961 - (600)
        avg_humid = avg_humid - self.normalize_wet
        # 361 / 423 = 0.8, so its pretty moist.
        avg_humid_percentage = float(avg_humid) / self.delta_wet
        time.sleep(0.5)
        now = datetime.now().strftime('%s')
        pic_name = '{time}_0{humidity}.jpg'.format(
            time=now, humidity=int(avg_humid_percentage * 100))
        try:
            with picamera.PiCamera(resolution=(1920, 1080)) as camera:
                camera.vflip = True
                camera.awb_mode = 'sunlight'
                camera.contrast = 30
                camera.sharpness = 100
                time.sleep(2)
                camera.capture('{0}/{1}'.format(self.DIR_NAME, pic_name))
        except picamera.exc.PiCameraError:
            print 'camera borked, moving on.'
        except Exception, e:
            print 'WOW FATAL EXCEPTION'
            print e
        print 'Took {0}'.format(pic_name)

        return avg_humid_percentage, now


def main():
    """Main program."""
    plant = LivingPlantView()
    while True:
        hour_now = datetime.now().hour
        minutes_now = datetime.now().minute
        # plant sleeps 6 hrs
        if 4 < hour_now < 22:
            plant.read_values()
            sleeptime = 2 * 60
            print 'Sleeping for 2 minutes, see you soon ;)'
        else:
            sleeptime = abs(4 - (hour_now - 24)) % 6  # hours to minutes
            sleeptime = (sleeptime * 60) - minutes_now  # minutes total
        time.sleep(sleeptime)

if __name__ == '__main__':
    main()
