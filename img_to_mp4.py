"""Turn images to mp4 file."""
from PIL import Image
import numpy
import cv2

import os
import shutil as files
import datetime
from glob import glob  # ohmyglob

cwd = os.getcwd()
print "cwd is : " + cwd
epoch_now = datetime.datetime.now().strftime('%s')
export_directory = os.path.join(cwd, epoch_now + '-Archived')
print "export directory is : " + export_directory
# create the archive dir if not exists /grow_motion/12345678-Archived/
if not os.path.exists(export_directory):
    print "creating export directory"
    os.makedirs(export_directory)
# select every image in the grow_motion/grow_motion/ directory
glob_files = sorted(glob('{img_path}/{img_regex}'.format(
    img_path=os.path.join(cwd, 'grow_motion'),
    img_regex='*.jpg'
)))
print 'found {} files'.format(len(glob_files))
# while glob_files:
# 24*60*0.5=720 pictures/day so a bit above 1 day
if len(glob_files) > 1000:
    # get the last 1000 files
    glob_files = glob_files[-1000:]
    # get everything until the last thousand files
    leftover_glob_files = glob_files[:-1000]

# Grab the stats from image1 to use for the resultant video
# height, width, layers = numpy.array(Image.open(glob_files[0].split(cwd)[-1][1:])).shape
# img = Image.open(glob_files[0])
img = cv2.imread(glob_files[0])
height, width, layers = img.shape

# Create the OpenCV VideoWriter
# codec = cv2.cv.CV_FOURCC(*'mp4v')
codec = cv2.cv.CV_FOURCC(*'H264')

video = cv2.VideoWriter(
    "{}-video.mp4".format(epoch_now),  # Filename
    codec,  # Negative 1 denotes manual codec selection. You can make this automatic by defining the "fourcc codec" with "cv2.VideoWriter_fourcc"
    25,  # 30 frames per second is chosen as a demo, 30FPS and 60FPS is more typical for a YouTube video
    (width, height)  # The width and height come from the stats of image1
)
print 'created video'
for f in glob_files:
    # process file onto variable
    # image = Image.open(f)
    img = cv2.imread(f)
    # Conversion from PIL to OpenCV from: http://blog.extramaster.net/2015/07/python-converting-from-pil-to-opencv-2.html
    video.write(img)
    # archive file
    files.move(f, export_directory)
print 'files processed'

# Release the video for it to be committed to a file
video.release()
print 'video processed'

# Load up the first and second demo images, assumed is that image1 and image2 both share the same height and width
# image2 = Image.open("demo3_2.jpg")


# # We'll have 30 frames be the animated transition from image1 to image2. At 10FPS, this is a whole 3 seconds
# for i in xrange(0, 30):
#     image = Image.open(f)
#     # Conversion from PIL to OpenCV from: http://blog.extramaster.net/2015/07/python-converting-from-pil-to-opencv-2.html
#     video.write(cv2.cvtColor(numpy.array(image), cv2.COLOR_RGB2BGR))

# # Release the video for it to be committed to a file
# video.release()
