#! /usr/bin/python3
import cv2
import socket
import numpy as np
import math
import time
import subprocess
#Created by Adriana Massie and David Matthews


def uptime():
    ms = time.time()*1000.0 
    return ms

def aspectRatio(w, h):
	''' returns true if the rectangle is of the correct aspect ratio and false if not.'''	
	return (w/h >= 1/5 and w/h <= 3/5)
def percentFilled(w,h,cnt):
	''' returns if the contour mostly occupies the same area as it's bounding rectangle atleast 70% '''
	return (cv2.contourArea(cnt) >= 0.3 * w * h)

	#cntA and cntB are contour A and B
def correctSize(cntA, cntB):
	'''returns true if the two contours are of similar height and false if not. bbcc testing aspect ratio before, we do not need to compare their widths'''
	avgHeight = (cntA[3] + cntB[3]) / 2
	rawError = abs (cntA[3] - cntB[3])
	scaledError = int (rawError / avgHeight) 
	returnError =  int((100 / (1 + math.e** (-20*(2*scaledError - 0.7)))) + 100*scaledError)
#	print ("correctSize: " + str(returnError))
	return (returnError) 

def correctSpacingY(cntA, cntB):
	'''returns 1 if the two contours are the expected distance apart in y direction. It gets near zero has the error gets big'''
	# Expected distance
	eDist = 0

	# real distance
	rDist = abs(cntA[1] - cntB[1])
	
	avgHeight = ((cntA[3] + cntB[3]) / 2)
   
	rawError = abs(eDist - rDist)
	scaledError = rawError / avgHeight
	returnError = ((100 / (1 + math.e** (-20*(2*scaledError - 0.7)))) + 100*scaledError)
#	print ("correctYSpacing: " + str(returnError))
	return (returnError)

def mean(a,b):
	'''returns the mean of two numbers'''
	return (0.5 * a + 0.5 * b)

def correctSpacingX(cntA, cntB):
	'''returns 1 if space is correct. returns 0 is space is not correct. This is horizontal direction'''
	# Expected distance
	eDist = (mean(cntA[3], cntB[3]) / 5) * 8.25
	
	# real distance
	rDist = abs(cntA[0] - cntB[0])
	
	rawError = abs(eDist - rDist)
	scaledError = rawError / eDist
	returnError = ((100 / (1 + math.e** (-20*(2*scaledError - 0.7)))) + 100*scaledError)
#	print ("correctXSpacing: " + str(returnError))
	return (returnError)
	
def udpBroadcast (cntA, cntB):
	 #Finds avg by adding x and y 
	 avgY = (cntA[1] + cntB[1]) / 2
	 avgX = (cntA[0] + cntB[0]) / 2
	 #Finds avg by adding height and width
	 avgHeight = (cntA[3] + cntB[3]) / 2   
	 avgWidth = (cntA [2] + cntB[2] )/ 2
	 
	 targetX = (avgX + avgWidth)
	 targetY = (avgY +avgHeight) 
	 
	 targetX = (targetX / capWidth)
	 targetY = (targetY / capHeight)
	 
	 avgHeight = (avgHeight / capHeight)
	 print(avgHeight)
	 if (avgHeight >= 0.29):
		 print('\n\n\n\n\n\n\n\n\n')
	 avgWidth = (avgWidth / capWidth)
	 bytes = bytes = str.encode((str(targetX)+ ','+str(targetY)+ ','+ str(avgWidth)+',' + str(avgHeight)))
	 socketout.sendto(bytes,(UDP_IP,UDP_PORT)) 

def drawTarget(rectangle1: list, rectangle2: list):
	 #Finds avg by adding x and y 
	 avgY = (rectangle1[1] + rectangle2[1]) / 2
	 avgX = (rectangle1[0] + rectangle2[0]) / 2

	 #Finds avg by adding height and width
	 avgHeight = (rectangle1[3] + rectangle2[3] )/ 2   
	 avgWidth = (rectangle1 [2] + rectangle2[2] )/ 2
	 
	 targetX = (avgX + avgWidth / 2)
	 targetY = (avgY + avgHeight / 2) 
	 
	 targetFrame = np.copy(frame)

	 cv2.rectangle(targetFrame, (rectangle1[0],rectangle1[1]),(rectangle1[0] + rectangle1[2], rectangle1[1] + rectangle1[3]), (255,0,0),-1) 
	 cv2.rectangle(targetFrame, (rectangle2[0],rectangle2[1]),(rectangle2[0] + rectangle2[2], rectangle2[1] + rectangle1[3]), (255,0,0),-1) 
	 cv2.circle(targetFrame, (int( targetX), int( targetY)), (10), (0,255,255), -1)

#	 cv2.imshow('Target\'s aquired', targetFrame)
	 
highestTargetScoreYet = 0;
UDP_IP = '255.255.255.255' 
UDP_PORT = 5801

socketout = socket.socket (socket.AF_INET, socket.SOCK_DGRAM)
socketout.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
socketout.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST,1)
oimg = 0
img = 0
oinit = 0
oread = 0
oblur = 0
ohsv = 0
omask = 0
odenoise = 0
otape = 0
init = 0
read = 0
blur = 0
hsv = 0
mask = 0
denoise = 0
tape = 0
cnt = 0
ocnt = 0
oinit = uptime ()

print ('beginning pinging')
p = subprocess.Popen(['ping', '-c', '2', '10.62.1.11'])
p.wait()
print ('pinging completed')

cap = cv2.VideoCapture("http://10.62.1.11/mjpg/video.mjpg?resolution=640x360&compression=0&color=1&mirror=0&fps=30&videocodec=jpeg&rotation=0")

#cap = cv2.VideoCapture(1)
print ('capture obtained')

capWidth = cap.get(3)
print(capWidth) 
capHeight = cap.get(4)
print(capHeight)

meow = 0

while (True):
	try:

		ret, frame = cap.read()
	except Exception as e:
		continue

	if (meow % 3 != 0 ):
		continue

## Pre-Processing to convert RGB image to a binary image
#	oblur = uptime()
#	bluri = cv2.GaussianBlur(frame, (15,15),1)
#	cv2.imshow('blur', blur)
#	blur = uptime()
#	print( 'Blur:\t\t' + str( blur - oblur))


# HSV
	hsvi = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	

## update these for the green color of our LED
	
	lower_green = np.array([8,0,200])
	upper_green = np.array([180,255,255])

	#This is inverted but it works on robot
	hsvMask = cv2.inRange(hsvi, lower_green, upper_green)
#	cv2.imshow('mask', hsvMask)

#	odenoise = uptime()
	
#	kernel = np.ones((5,5), np.uint8)
#	maskRemoveNoise = cv2.morphologyEx(hsvMask, cv2.MORPH_OPEN, kernel)
#	cv2.imshow('removenoise', maskRemoveNoise)

#	maskCloseHoles = cv2.morphologyEx(maskRemoveNoise, cv2.MORPH_CLOSE, kernel)
#	cv2.imshow('closeHoles', maskCloseHoles)
	#denoise = uptime()
#	print( 'denoise:\t' + str(denoise - odenoise))
#
## get contours for more abstract analysis

	c1, hsvContours, _ = cv2.findContours(hsvMask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


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
	if (int(len(possibleTargetBoundingRect)) >= 1):
		print (len(possibleTargetBoundingRect))

## Display the contours that might be targets.
#	frameContours = np.copy(frame)
#	cv2.drawContours(frameContours, possibleLiftTargetContour, -1, (0,0,255), 4)
#	cv2.imshow("potential target half's", frameContours)

# TODO: possibly update to rate the probability of each set of contours being a target, and then pick the best over a certian threshold. this would help in the case that there are two "targets" being picked up.

# for each contour check if there is another similar contour an appropiate distance away on the left or right
	bestFoundTarget = [0, 0] 
	highestScore = 100000
	
	for cntA in possibleTargetBoundingRect:
		for cntB in possibleTargetBoundingRect:
			currentScore = correctSize(cntA, cntB) + correctSpacingX(cntA, cntB) + correctSpacingY(cntA, cntB)
#			print ("Score: " + str(currentScore))	
			if currentScore < highestScore:
				bestFoundTarget [0] = cntA
				bestFoundTarget [1] = cntB 
				highestScore = currentScore
			
	if (highestScore < 50): 	
		print("target found. Score: \n\n\n\n\n " + str(highestScore))
		udpBroadcast(bestFoundTarget[0], bestFoundTarget[1])
#		drawTarget(bestFoundTarget[0], bestFoundTarget[1])
		if (highestScore > highestTargetScoreYet):
			highestTargetScoreYet = highestScore
#			print("HighestScore: " +str(highestTargetScoreYet))	
#			print( 'target:\t'+ str(uptime()))
	
## Draw a line between the targets, and put a dot at the center
## cv2.line(img, (startX, startY), (endX,endY), (0,0,255), thickness)
## cv2.circle(img, (x,y), (radius), (0,255,255), thickness)

#
#	img = uptime()
#	print ('img:\t\t' + str(img - oimg))
#	print ('\n\n\n')
## Graceful shutdown	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

## cleanup on shutdown
cap.release();
cv2.destroyAllWindows();
print ("Shuting down Vision\n\n\n")
