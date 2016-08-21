"""Turn images to mp4 file."""
from PIL import Image
import numpy
import cv2

import os
import shutil as files
import datetime
from glob import glob  # ohmyglob


image_files = glob('./grow_motion/*.jpg')
image_files[:-50]
cwd = os.getcwd()
epoch_now = datetime.datetime.now().strftime('%s')
export_directory = os.path.join(cwd, epoch_now + '-Archived')
# create the archive dir if not exists /grow_motion/12345678-Archived/
if not os.path.exists(export_directory):
    os.makedirs(export_directory)
# select every image in the grow_motion/grow_motion/ directory
glob_files = sorted(glob('{img_path}/{img_regex}'.format(
    img_path=os.path.join(cwd, 'grow_motion'),
    img_regex='*.jpg'
)))

# while glob_files:
    # 24*60*0.5=720 pictures/day so a bit above 1 day
if len(glob_files) > 1000:
    # get the last 1000 files
    glob_files = glob_files[-1000:]
    # get everything until the last thousand files
    leftover_glob_files = glob_files[:-1000]


# Grab the stats from image1 to use for the resultant video
height, width, layers = numpy.array(Image.open(glob_files[0])).shape

# Create the OpenCV VideoWriter
video = cv2.VideoWriter(
    "{}-kifh.avi".format(epoch_now),  # Filename
    -1,  # Negative 1 denotes manual codec selection. You can make this automatic by defining the "fourcc codec" with "cv2.VideoWriter_fourcc"
    30,  # 30 frames per second is chosen as a demo, 30FPS and 60FPS is more typical for a YouTube video
    (width, height)  # The width and height come from the stats of image1
)
for f in glob_files:
    # process file onto variable
    image = Image.open(f)
    # Conversion from PIL to OpenCV from: http://blog.extramaster.net/2015/07/python-converting-from-pil-to-opencv-2.html
    video.write(cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR))
    # archive file
    files.move(f, export_directory)

# Release the video for it to be committed to a file
video.release()

# Load up the first and second demo images, assumed is that image1 and image2 both share the same height and width
# image2 = Image.open("demo3_2.jpg")


# # We'll have 30 frames be the animated transition from image1 to image2. At 10FPS, this is a whole 3 seconds
# for i in xrange(0, 30):
#     image = Image.open(f)
#     # Conversion from PIL to OpenCV from: http://blog.extramaster.net/2015/07/python-converting-from-pil-to-opencv-2.html
#     video.write(cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR))

# # Release the video for it to be committed to a file
# video.release()
