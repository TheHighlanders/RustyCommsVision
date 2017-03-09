#! /usr/bin/python3

import cv2
cap = cv2.VideoCapture('http://10.62.1.11/mjpg/video.mjpg')


def nothing(x):
    pass

while(1):

    _, frame = cap.read()

    cv2.imshow('frame', cv2.resize(frame,(700,450), interpolation = cv2.INTER_CUBIC))

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()
