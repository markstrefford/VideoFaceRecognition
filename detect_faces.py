#
# Face recognition from streaming video
#
# Written by Mark Strefford
# Copyright 2015 Timelaps Robotics Limited
#

# The following have been used for inspiration:
#
# https://github.com/slobdell/facebook_face_training_set
# http://docs.opencv.org/modules/contrib/doc/facerec/tutorial/facerec_video_recognition.html
# http://www.pyimagesearch.com
#

# import the necessary packages
import argparse, cv2, os, uuid
import numpy as np
from utils.eyetracker import EyeTracker
from utils import imgutils


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required=True,
                help="path to where the face cascade resides")
ap.add_argument("-e", "--eye", required=True,
                help="path to where the eye cascade resides")
ap.add_argument("-t", "--training", required=True,
                help="path to where the image list csv file resides")
ap.add_argument("-i", "--image", required=True,
                help="path to where the image to recognise resides")
args = vars(ap.parse_args())

# Load csv file
images = []
labels = []
names = []
count = 0
fileList = open(args["training"]).readlines()

# Parse and load the images and the labels
print "Loading training data set..."
for imageInfo in fileList:
    file = imageInfo.split(";")[0]
    face = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
    images.append(np.asarray(imgutils.resize(face, width=225)))
    name = imageInfo.split(";")[1]
    names.append(name)
    labels.append(count)
    count += 1

# Get image size in case its needed later
im_width = images[0].shape[1]
im_height = images[1].shape[0]
print "Done!"

# Call the vision detection algorithm to learn from this data set
print "Training the Fisher Face Recognizer..."
fr = cv2.createFisherFaceRecognizer()
images_array = np.asarray(images)
labels_array = np.asarray(labels)
fr.train(images_array, labels_array)
print "Done!"

# Load the image to "recognise"
image = cv2.imread(args["image"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Convert it to greyscale, resize, etc.
image = cv2.imread(args["image"])
frame = imgutils.resize(image, width=250)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# Recognise the face in it
et = EyeTracker(args["face"], args["eye"])
rects = et.track(gray)
print "I found %d face(s)" % (len(rects))

# loop over the face bounding boxes and draw them
for rect in rects:
    cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (0, 255, 0), 2)


#
#
# --------------------
#
#


# load the image and convert it to grayscale
# image = cv2.imread(args["image"])
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# load the image then resize and convert it to grayscale
# image = cv2.imread(args["image"])
# frame = imgutils.resize(image, width = 250)
# gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# find faces in the image
# et = EyeTracker(args["face"], args["eye"])

# faceRects = fd.detect(gray, scaleFactor = 1.1, minNeighbors = 5,
# 	minSize = (30, 30))
# print "I found %d face(s)" % (len(faceRects))

rects = et.track(gray)
print "I found %d face(s)" % (len(rects))

# loop over the faces and draw a rectangle around each
# for (x, y, w, h) in faceRects:
#     cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#     print "Face at %d %d %d %d" % (x,y,w,h)

# detect faces and eyes in the image
rects = et.track(gray)

# loop over the face bounding boxes and draw them
for rect in rects:
    cv2.rectangle(frame, (rect[0], rect[1]), (rect[2], rect[3]), (0, 255, 0), 2)
    cropped = frame[rect[1]:rect[3], rect[0]:rect[2]]
    print "Rectangle: x1=%d y1=%d x2=%d y2=%d", (rect[0], rect[1], rect[2], rect[3])
    print "Cropped: %d:%d, %d:%d", (rect[1], rect[3], rect[0], rect[2])


# show the detected faces
cv2.imshow("Faces", frame)
cv2.imshow("Cropped", cropped)
cv2.waitKey(0)


