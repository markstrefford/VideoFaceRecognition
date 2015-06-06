# USAGE
# python detect_faces.py --face cascades/haarcascade_frontalface_default.xml --image images/obama.png

# import the necessary packages
import argparse, cv2, os, uuid
from utils.eyetracker import EyeTracker
from utils import imgutils


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required = True,
	help = "path to where the face cascade resides")
ap.add_argument("-e", "--eye", required = True,
	help = "path to where the eye cascade resides")
ap.add_argument("-i", "--images", required = True,
	help = "path to where the image file resides")
ap.add_argument("-i", "--image", required = True,
	help = "path to where the image file resides")
args = vars(ap.parse_args())

# load the image and convert it to grayscale
# image = cv2.imread(args["image"])
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# load the image then resize and convert it to grayscale
image = cv2.imread(args["image"])
frame = imgutils.resize(image, width = 250)
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

# find faces in the image
# fd = FaceDetector(args["face"])
et = EyeTracker(args["face"], args["eye"])

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
    cropped = frame[rect[1]:rect[3] , rect[0]:rect[2]]
    print "Rectangle: x1=%d y1=%d x2=%d y2=%d", (rect[0], rect[1], rect[2], rect[3])
    print "Cropped: %d:%d, %d:%d", (rect[1], rect[3], rect[0], rect[2])

# Write the cropped image
dirname, filename = os.path.split(os.path.relpath(args["image"]))
newfile = dirname + "/face-" + str(uuid.uuid4()) + ".jpg"
print "Writing " + filename + " to " + newfile
cv2.imwrite(newfile, cropped)

# show the detected faces
cv2.imshow("Faces", frame)
cv2.imshow("Cropped", cropped)
cv2.waitKey(0)


