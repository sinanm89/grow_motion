from time import sleep
import picamera

with picamera.PiCamera(resolution=(1920, 1080)) as camera:
    # Set ISO to the desired value
    # camera.iso = 100
    # Wait for the automatic gain control to settle
    # camera.meter_mode = 'backlit'
    # Now fix the values
    # camera.shutter_speed = camera.exposure_speed
    # camera.exposure_mode = 'spotlight'
    # g = camera.awb_gains
    camera.awb_mode = 'auto'
    camera.vflip = True
    sleep(1)
    # camera.awb_gains = g
    # Finally, take several photos with the fixed settings
    camera.capture('harambe.jpg')
