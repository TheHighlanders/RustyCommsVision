import cv2
import numpy as np


cap = cv2.VideoCapture('http://10.62.1.43/mjpg/video.mjpg')

while (True):
	ret, frame = cap.read()
#	cv2.imshow('frame', frame)

## Pre-Processing to convert RGB image to a binary image

	blur = cv2.GaussianBlur(frame, (15,15),1)
#	cv2.imshow('blur', blur)

	hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
	
## update these for the green color of our LED
	lower_green = np.array([0,0,156])
	upper_green = np.array([120,209,255])

	hsvMask = cv2.inRange(hsv, lower_green, upper_green)
	cv2.imshow('mask', hsvMask)
	
	kernel = np.ones((5,5), np.uint8)
	maskRemoveNoise = cv2.morphologyEx(hsvMask, cv2.MORPH_OPEN, kernel)
	cv2.imshow('removenoise', maskRemoveNoise)

	maskCloseHoles = cv2.morphologyEx(maskRemoveNoise, cv2.MORPH_CLOSE, kernel)
	cv2.imshow('closeHoles', maskCloseHoles)

#	maskBlur = cv2.GaussianBlur(maskCloseHoles, (15,15),1)
#	cv2.imshow('maskBlur', maskBlur)
## get contours for more abstract analysis

	c1, hsvContours, _ = cv2.findContours(maskCloseHoles, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

## Display all contours found;

	frameContours = np.copy(frame)
	cv2.drawContours(frameContours, hsvContours, -1, (0,0,255), 4)

	cv2.imshow("frameContours", frameContours)


## Filter contors for ones with resonable aspect ratios
## match each filtered contour with eachother and find the set that has the highest score
## Score dependent on 
## * ratio of height to horizontal distance between the geometric center of each. 
## * Area of contour
## * distance from the center of field of each contour



## Graceful shutdown	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

## cleanup on shutdown
cap.release();
cv2.destroyAllWindows();
