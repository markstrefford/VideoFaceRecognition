# USAGE
# python detect_faces.py --face cascades/haarcascade_frontalface_default.xml --image images/obama.png

# import the necessary packages
import argparse, cv2, os, uuid, imgutils
from eyetracker import EyeTracker

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-f", "--face", required=True,
                help="path to where the face cascade resides")
ap.add_argument("-e", "--eye", required=True,
                help="path to where the eye cascade resides")
ap.add_argument("-i", "--images", required=True,
                help="path to file containing list of images to process")
ap.add_argument("-a", "--aspect", required=False,
                help="Define aspect ratio (note this doesn't squash or stretch the image)")
args = vars(ap.parse_args())

# Aspect ratio
target_aspect = args["aspect"]

# Setup face finder and eye tracker
# TODO - Rework to just use Face Detection?
et = EyeTracker(args["face"], args["eye"])

# Get list of images
fileList = open(args["images"]).readlines()
for imageInfo in fileList:
    file = imageInfo.split(";")[0]
    label = imageInfo.split(";")[1]

    # Filename processing
    print "Processing file:" + file
    dirname, filename = os.path.split(os.path.relpath(file))

    # load the image then resize and convert it to grayscale
    image = cv2.imread(file)
    frame = imgutils.resize(image, width=300)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # detect faces and eyes in the image
    rects = et.track(gray)
    print "I found %d face(s)" % (len(rects))

    # loop over the face bounding boxes and draw them
    for rect in rects:
        # Ensure that all images are the same size and within the bounds of the image
        face = imgutils.cropface(frame, (rect[0], rect[1]), (rect[2], rect[3]))

        # Write the cropped image
        newfile = dirname + "/face-" + str(uuid.uuid4()) + ".jpg"
        print "Writing " + filename + " to " + newfile
        cv2.imwrite(newfile, face)

# show the detected faces
# cv2.imshow("Faces", frame)
# cv2.imshow("Cropped", cropped)
# cv2.waitKey(0)


