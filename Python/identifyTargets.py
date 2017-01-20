import cv2
import socket
import numpy as np

#Created by Adriana Massie and David Matthews  

def aspectRatio(w, h):
	''' returns true if the rectangle is of the correct aspect ratio and false if not.'''	
	return (w/h >= 1.5/5 and w/h <= 2.5/5)
def percentFilled(w,h,cnt):
	''' returns if the contour mostly occupies the same area as it's bounding rectangle atleast 70% '''
	return (cv2.contourArea(cnt) >= 0.7 * w * h)

	#cntA and cntB are contour A and B
def correctSize(cntA, cntB):
	'''returns true if the two contours are of similar height and false if not. bbcc testing aspect ratio before, we do not need to compare their widths'''
	error = abs (cntA[3] - cntB[3])
	return (1/(error + 1)) 

def correctSpacingY(cntA, cntB):
	'''returns 1 if the two contours are the expected distance apart in y direction. It gets near zero has the error gets big'''
	# Expected distance
	eDist = 0
	#print ("eDist: ")
	#print (eDist)

	# real distance
	rDist = abs(cntA[1] - cntB[1])
	#print ("rDist: ")
	#print (rDist)
	#print ("")
	error = abs(eDist - rDist)
	return (1/(error + 1))

def mean(a,b):
	'''returns the mean of two numbers'''
	return (0.5 * a + 0.5 * b)

def correctSpacingX(cntA, cntB):
	'''returns 1 if space is correct. returns 0 is space is not correct. This is horizontal direction'''
	# Expected distance
	eDist = (mean(cntA[3], cntB[3]) / 5) * 8.25
	#print ("eDist: ")
	#print (eDist)

	# real distance
	rDist = abs(cntA[0] - cntB[0])
	#print ("rDist: ")
	#print (rDist)
	#print ("")
	error = abs(eDist - rDist)
	return (1/(error + 1))
	
def udpBroadcast (cntA, cntB):
	 #Finds avg by adding x and y 
	 avgY = (cntA[1] + cntB[1] / 2)
	 avgX = (cntA[0] + cntB[0] / 2)
	 #Finds avg by adding height and width
	 avgHeight = (cntA[3] + cntB[3] / 2)   
	 avgWidth = (cntA [2] + cntB[2] / 2)
	 
	 targetX = (avgX + avgWidth)
	 targetY = (avgY +avgHeight) 
	 
	 targetX = (targetX / capWidth)
	 targetY = (targetY / capHeight)
	 
	 avgHeight = (avgHeight / capHeight)
	 avgWidth = (avgWidth / capWidth)
	 bytes = bytes = str.encode((str(targetX)+ ','+str(targetY)+ ','+ str(avgWidth)+',' + str(avgHeight)))
	 socketout.sendto(bytes,(UDP_IP,UDP_PORT)) 

def drawTarget(rectangle1, rectangle2):
	 #Finds avg by adding x and y 
	 avgY = (rectangle1[1] + rectangle2[1] / 2)
	 avgX = (rectangle1[0] + rectangle2[0] / 2)
	 #Finds avg by adding height and width
	 avgHeight = (rectangle1[3] + rectangle2[3] / 2)   
	 avgWidth = (rectangle1 [2] + rectangle2[2] / 2)
	 
	 targetX = (avgX + avgWidth)
	 targetY = (avgY +avgHeight) 
	 
	 targetFrame = np.copy(frame)
	 cv2.rectangle(targetFrame, Point (rectangle1[0],rectangle1[1]),Point (rectangle1[2] + rectangle1[0] ,rectangle1[3] + rectangle1[1]),(255,0,0),10) 
	 cv2.circle(targetFound, (int( targetX), int( targetY)), (10), (0,255,255), -1)

	 cv2.imshow('Target\'s aquired', targetFrame)
	 
UDP_IP = '255.255.255.255' 
UDP_PORT = 5005 

socketout = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
socketout.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
socketout.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)

		
cap = cv2.VideoCapture("http://10.62.1.108/mjpg/video.mjpg")
#cap = cv2.VideoCapture(0)

capWidth = cap.get(3)
print(capWidth) 
capHeight = cap.get(4)
print(capHeight)

while (True):
	ret, frame = cap.read()


## Pre-Processing to convert RGB image to a binary image

	blur = cv2.GaussianBlur(frame, (15,15),1)
#	cv2.imshow('blur', blur)

	hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
	
## update these for the green color of our LED
	lower_green = np.array([0,0,156])
	upper_green = np.array([120,209,255])
	#This is inverted but it works on robot

	hsvMask = cv2.inRange(hsv, lower_green, upper_green)
	cv2.imshow('mask', hsvMask)
	
	kernel = np.ones((5,5), np.uint8)
	maskRemoveNoise = cv2.morphologyEx(hsvMask, cv2.MORPH_OPEN, kernel)
	cv2.imshow('removenoise', maskRemoveNoise)

	maskCloseHoles = cv2.morphologyEx(maskRemoveNoise, cv2.MORPH_CLOSE, kernel)
	cv2.imshow('closeHoles', maskCloseHoles)


## get contours for more abstract analysis

	c1, hsvContours, _ = cv2.findContours(maskCloseHoles, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


## Filter contors for ones with resonable aspect ratios
## match each filtered contour with eachother and find the set that has the highest score
## Score dependent on 
## * ratio of height to horizontal distance between the geometric center of each. 
## * Area of contour
## * distance from the center of field of each contour


	possibleLiftTargetContour = []
	possibleTargetBoundingRect = []	

# if the contour looks like a possible piece of target tape, add it to the list
	for cnt in hsvContours:
		x, y, w, h = cv2.boundingRect(cnt)
		if (aspectRatio(w,h) and percentFilled(w,h,cnt)):
			possibleLiftTargetContour.append(cnt)
			possibleTargetBoundingRect.append([x,y,w,h])

## Display the contours that might be targets.
	frameContours = np.copy(frame)
	cv2.drawContours(frameContours, possibleLiftTargetContour, -1, (0,0,255), 4)
	cv2.imshow("potential target half's", frameContours)

# TODO: possibly update to rate the probability of each set of contours being a target, and then pick the best over a certian threshold. this would help in the case that there are two "targets" being picked up.

# for each contour check if there is another similar contour an appropiate distance away on the left or right
	bestFoundTarget = [0, 0] 
	highestScore = 0 
	
	for cntA in possibleTargetBoundingRect:
		for cntB in possibleTargetBoundingRect:
			currentScore = correctSize(cntA, cntB) * correctSpacingX(cntA, cntB) * correctSpacingY(cntA, cntB)	
			if currentScore > highestScore:
				bestFoundTarget [0] = cntA
				bestFoundTarget [1] = cntB 
				highestScore = currentScore
			
	if (highestScore > 0.05): 	
		print("target found!")
		udpBroadcast(bestFoundTarget[0], bestFoundTarget[1])
		drawTarget(bestFoundTarget[0], bestFoundTarget[1])	
	
## Draw a line between the targets, and put a dot at the center
## cv2.line(img, (startX, startY), (endX,endY), (0,0,255), thickness)
## cv2.circle(img, (x,y), (radius), (0,255,255), thickness)



## Graceful shutdown	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

## cleanup on shutdown
cap.release();
cv2.destroyAllWindows();
