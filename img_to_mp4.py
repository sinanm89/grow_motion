#! /usr/local/bin/python
"""Turn images to mp4 file."""
import cv2

import os
import sys
import shutil
import datetime
from glob import glob  # ohmyglob


def create_the_video(debug_mode=True):
    """Create images into an html5 video."""
    cwd = os.getcwd()
    print "cwd is : " + cwd
    epoch_now = datetime.datetime.now().strftime('%s')
    export_directory = os.path.join(cwd, 'Archive', epoch_now + '-Archived')
    print "exported directory is : " + export_directory
    # create the archive dir if not exists /grow_motion/12345678-Archived/
    if not os.path.exists(export_directory):
        print "creating export directory"
        os.makedirs(export_directory)
    # select every image in the grow_motion/grow_motion/ directory
    files = sorted(glob('{img_path}/{img_regex}'.format(
        img_path=os.path.join(cwd, 'grow_motion'),
        img_regex='*.jpg'
    )))
    print 'found {} files'.format(len(files))
    # 24*60*0.5=720 pictures/day so a bit above 1 day
    leftover_files = None
    # if len(files) > 1000:
    #     # get the last 1000 files
    #     glob_files = files[-1000:]
    #     # get everything until the last thousand files
    #     leftover_files = files[:-1000]

    # Grab the stats from image1 to use for the resultant video
    img = cv2.imread(files[0])
    height, width, layers = img.shape

    # Create the OpenCV VideoWriter
    codec = cv2.cv.CV_FOURCC(*'mp4v')
    # codec = cv2.cv.CV_FOURCC(*'H264') < this is used for web stuff, needs investigation.  # noqa
    filename = "{}-video.mp4".format(epoch_now)
    video = cv2.VideoWriter(
        filename,
        codec,
        15,  # FPS
        (width, height)
    )
    print 'created video'
    error = False
    for f in files:
        # image = Image.open(f)
        try:
            img = cv2.imread(f)
            # Conversion from PIL to OpenCV from: http://blog.extramaster.net/2015/07/python-converting-from-pil-to-opencv-2.html  # noqa
            video.write(img)
            # archive file
        except Exception, e:
            error = e
            print (
                '{error}\nException occurred on file {file},'
                'not moving the rest.'
            ).format(error=error, file=f)

    if not debug_mode and not error:
        for f in files:
            shutil.move(f, export_directory)
        print 'moved files'

    # Release the video for it to be committed to a file
    video.release()
    print 'Created {}'.format(filename)
    return leftover_files

if __name__ == '__main__':
    debug = False if len(sys.argv) > 1 else True
    remaining = create_the_video(debug)
