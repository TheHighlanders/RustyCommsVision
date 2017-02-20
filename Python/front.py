import cv2
import numpy as np

cap = cv2.VideoCapture('http://10.62.1.11/mjpg/video.mjpg')


def nothing(x):
    pass

while(1):

    _, frame = cap.read()

    cv2.imshow('frame', frame)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        break

cap.release()

cv2.destroyAllWindows()
