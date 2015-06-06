#!/usr/bin/env python
__author__ = 'markstrefford'
__org__ = 'Timelaps Robotics'

import argparse, sys
import os.path

# This is a tiny script to help you creating a CSV file from a face
# database with a similar hierarchie:
#
# philipp@mango:~/facerec/data/at$ tree
#  .
#  |-- README
#  |-- s1
#  |   |-- 1.pgm
#  |   |-- ...
#  |   |-- 10.pgm
#  |-- s2
#  |   |-- 1.pgm
#  |   |-- ...
#  |   |-- 10.pgm
#  ...
#  |-- s40
#  |   |-- 1.pgm
#  |   |-- ...
#  |   |-- 10.pgm
#
# Based on http://docs.opencv.org/modules/contrib/doc/facerec/facerec_tutorial.html#

if __name__ == "__main__":

    #Parse arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--images", required=True,
                    help="path to the directory containing the images")
    ap.add_argument("-c", "--csv", required=True,
                    help="path to use for creating the csv file")
    ap.add_argument("-p", "--prefix", required=False,
                    help="Optional prefix for images to be indexed")
    ap.add_argument("-e", "--exclude", required=False,
                    help="Optional prefix for images to be excluded")
    args = vars(ap.parse_args())

    # BASE_PATH=sys.argv[1]
    # CSV_PATH=sys.argv[2]
    BASE_PATH = args["images"]
    CSV_PATH = args["csv"]
    PREFIX = str(args["prefix"])
    EXCLUDE = str(args["exclude"])
    SEPARATOR = ";"

    print "Creating csv for files with prefix " + PREFIX

    # TODO: Label should be the last directory name (so ideally the name of the person!)
    label = "n/a"
    csvfile = open(CSV_PATH, "w")

    for dirname, dirnames, filenames in os.walk(BASE_PATH):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname, subdirname)
            for filename in os.listdir(subject_path):
                # Check we haven't processed this file already!

                # If we have a prefix check that
                if EXCLUDE != "" and filename.find(EXCLUDE) != 0:
                    if (PREFIX != "None" and filename.find(PREFIX) == 0 ) or PREFIX == "None":
                        label = os.path.basename(subject_path)
                        abs_path = "%s/%s" % (subject_path, filename)
                        #print "%s%s%s" % (abs_path, SEPARATOR, label)
                        csvfile.write(abs_path + SEPARATOR + label + "\n")

    csvfile.close()

