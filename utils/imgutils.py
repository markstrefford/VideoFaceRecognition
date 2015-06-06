# Import the necessary packages
import numpy as np
import cv2


def translate(image, x, y):
    # Define the translation matrix and perform the translation
    M = np.float32([[1, 0, x], [0, 1, y]])
    shifted = cv2.warpAffine(image, M, (image.shape[1], image.shape[0]))

    # Return the translated image
    return shifted


def rotate(image, angle, center=None, scale=1.0):
    # Grab the dimensions of the image
    (h, w) = image.shape[:2]

    # If the center is None, initialize it as the center of
    # the image
    if center is None:
        center = (w / 2, h / 2)

    # Perform the rotation
    M = cv2.getRotationMatrix2D(center, angle, scale)
    rotated = cv2.warpAffine(image, M, (w, h))

    # Return the rotated image
    return rotated


def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # resize the image
    resized = cv2.resize(image, dim, interpolation=inter)

    # return the resized image
    return resized


def cropface(image, (x1, y1), (x2, y2), width=75):
    # Get face aspect ratio
    face_width = x2 - x1
    face_height = y2 - y1
    face_aspect = face_width / face_height
    print "image size ", image.shape[1], image.shape[0]
    print "Initial dimensions:"  , face_width, face_height, " aspect: " , face_aspect

    # Reshape the face is we don't have a perfect aspect ratio of 1:1 (this is highly unlikely!!)
    if face_aspect != 1:

        # Face width < face height
        if face_aspect < 1:
            # Reduce height to be 1:1 ratio
            new_height = face_height * face_aspect
            y1 += (face_height - new_height) / 2
            y2 -= (face_height - new_height) / 2

        # Face height < face width
        elif face_aspect > 1:
            # Reduce width to be 1:1 ratio
            new_width = face_width / face_aspect
            x1 += (face_width - new_width) / 2
            x2 -= (face_width - new_width) / 2

    new_aspect = (x2 - x1) / (y2 - y1)
    print "Cropping to ", x2 ,x1, y2 , y1, new_aspect
    cv2.imshow('Original', image)
    face = image[y1 : y2, x1 : x2]
    cv2.imshow('Cropped', face)
    cv2.waitKey(0)
    print "Cropped face size ", face.shape[1], face.shape[0]
    print "Resizing face to width=", width
    resized_face = resize(face, width=width)
    return resized_face



# left = 2407
# top = 804
# width = 300
# height = 200
# box = (left, top, left+width, top+height)
# area = img.crop(box)