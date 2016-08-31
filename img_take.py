from time import sleep
from datetime import datetime
import picamera

with picamera.PiCamera(resolution=(1920, 1080)) as camera:
    camera.vflip = True
    camera.awb_mode = 'sunlight'
    camera.contrast = 30
    camera.sharpness = 100
    new_file ='one_shot_{}.jpg'.format(datetime.now().strftime('%s'))
    sleep(2)
    camera.capture(new_file)
