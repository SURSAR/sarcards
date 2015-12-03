#!/usr/bin/python

import sys
import numpy as np
import cv2

def main(file):
    img = cv2.imread(file, 0)
    face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(img, 1.3, 5)
    max = (0, 0, 0, 0)
    for (x, y, w, h) in faces:
        if w + h > max[0] + max[1]:
            max = (w, h, x, y)
    print("%dx%d+%d+%d" % max)

if __name__ == "__main__":
    main(sys.argv[1])
