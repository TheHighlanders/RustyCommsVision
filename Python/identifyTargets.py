import cv2
import numpy as np


#cap = cv2.VideoCapture('http://10.62.1.43/mjpg/video.mjpg')
cap = cv2.VideoCapture(0)

while (True):
	ret, frame = cap.read()


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



## Filter contors for ones with resonable aspect ratios
## match each filtered contour with eachother and find the set that has the highest score
## Score dependent on 
## * ratio of height to horizontal distance between the geometric center of each. 
## * Area of contour
## * distance from the center of field of each contour


	possibleGearTargetContour = []
	possibleGTCBR = []	
# if the conour looks like a possible piece of target tape, add it to the list
	for cnt in hsvContours:
		x, y, w, h = cv2.boundingRect(cnt)
		print (w/h)
		if (w/h >= 1.5/5 and w/h <= 2.5/5):
			possibleGearTargetContour.append(cnt)
			possibleGTCBR.append([x,y,w,h])
	cv2.drawContours(frameContours, possibleGearTargetContour, -1, (0,0,255), 4)
	cv2.imshow("frameContours", frameContours)

# for each contour check if there is another contour an appropiate distance away on the left or right

	for cntA in possibleGTCBR:
		for cntB in possibleGTCBR:
			if cntA[3] * 2.2 >= (abs(cntA[0] - cntB[0])) and  cntA[3] * 1.8 <= (abs(cntA[0] - cntB[0])):
				cv2.line(frame, (cntA[0], cntA[1]), (cntB[0],cntB[1]), (0,0,255), 3)
				cv2.circle(frame, ((int)((cntA[0] + cntB[0])/ 2),(int)((cntA[1] + cntB[1])/ 2)), (10), (0,255,255), -1)

	cv2.imshow('frame', frame)

## Draw a line between the targets, and put a dot at the center
## cv2.line(img, (startX, startY), (endX,endY), (0,0,255), thickness)
## cv2.circle(img, (x,y), (radius), (0,255,255), thickness)



## Graceful shutdown	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

## cleanup on shutdown
cap.release();
cv2.destroyAllWindows();
