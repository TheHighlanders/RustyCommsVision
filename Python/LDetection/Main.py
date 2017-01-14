import cv2
import numpy as np
import time
import Line
import math

def nothing(x):
	"""Does nothing. Used for wasting time."""
	pass

def polygonAprox(cnt):
	"""Approximates a contour which is passed as a parameter into a polygon.
	The line of the polygon will not be farther than epsilon away from the original contour edge."""
	epsilon = 0.015*cv2.arcLength(cnt,True)
	approx = cv2.approxPolyDP(cnt,epsilon,True)
	return approx

def longestLines(cnt):
	"""Takes a contour as a parameter.
	This should usually be a contour which has been aproximated as a polygon.
	returns the 6 longest lines in an array."""
	length = len(cnt)
	lines = []
	curPnt = cnt[0][0]
	futPnt = cnt[1][0]
	order = 0
	indexOfLowest = 0
	lowestLength = 0

	# creates a list of the top 6 longest lines.
	for x in range(length):
		curPnt = cnt[(x)%length][0]
		futPnt = cnt[(x+1)%length][0]

		newLine =  Line.Line(curPnt[0],curPnt[1], futPnt[0], futPnt[1], order)
		if order <6:
			lines.append(newLine)
			if newLine.getLength() < lowestLength:
				lowestLength = newline.getLength
				indexOfLowest = order
			order+=1
		elif newLine.getLength() > lowestLength:
			#print (str(newLine.getOrder()) + " order and length" + str(newLine.getLength()) + ", outplaced order, length" +str(lines[indexOfLowest].getOrder()) + ", " + str(lines[indexOfLowest].getLength()))
			lines[indexOfLowest] = newLine
			order +=1

			indexOfNewLow = 0
			newLow = lines[0].getLength()
			for y in range(5):
				if (lines[y+1].getLength()< newLow):
					indexOfNewLow = y+1
					newLow = lines[y+1].getLength()
			indexOfLowest = indexOfNewLow
			lowestLength = newLow
		del newLine
	return lines

def centeredAroundZero(x):
	return ((x+math.pi) % (2 * math.pi) - math.pi)

def isL (plyCnt, frame):
	"""Checks to see if the correct number of opposite interior angles
	sum to Pi and to 0"""
	lines = []
	length = len(plyCnt)
	#print("\n\n\n")

	for x in range(length):
		curPnt = plyCnt[(x)%length][0]
		futPnt = plyCnt[(x+1)%length][0]

		#cv2.circle(frame, (curPnt[0], curPnt[1]), 10, (50,x*40,0), thickness=-1, lineType=8, shift=0)
		#cv2.circle(frame, (0, 0), 10, (255,0,0), thickness=-1, lineType=8, shift=0)

		lines.append(Line.Line(curPnt[0],curPnt[1], futPnt[0], futPnt[1], x))
		#print ("("+str(curPnt[0]) + ", " + str(curPnt[1]) + "), " +"("+str(futPnt[0]) + ", " + str(futPnt[1]) + ") :: " +str(lines[x].getAngle()))
	ttlOne = 0
	ttlZero = 0

	currLine = lines[0]
	nxtLine = lines[1]
	lastAngle = (centeredAroundZero(nxtLine.getAngle() - currLine.getAngle()) / math.pi)
	nxtAngle = (centeredAroundZero(nxtLine.getAngle() - currLine.getAngle()) / math.pi)

	for x in range (length):
		currLine = lines[(x)%length]
		nxtLine = lines[(x+1)%length]

		lastAngle = nxtAngle

		nxtAngle = (centeredAroundZero(nxtLine.getAngle() - currLine.getAngle()) / math.pi)
		#print(str(currLine.getOrder()))
		#print(str(nxtLine.getOrder()))
		#print ("Last: " + str(lastAngle) + " Nxt: " + str(nxtAngle))
		sumang = nxtAngle + lastAngle

		#print ("The sum is: " + str(sumang))
		if (sumang) < 0.2:
			if (sumang) > -0.2:
				ttlZero +=1

		if (sumang) > 0.80:
			if (sumang) < 1.2:
				ttlOne += 1
		if (sumang <-0.8):
			if (sumang) > -1.2:
				ttlOne +=1

	if ttlOne == 4:
		if ttlZero == 2:
			return True
	return False

lastLW = 0
lastLH = 0
lastSlide = 0
firstLFound = False

def slideWhichWay(x, y, w, h):

	aspect_ratio = w/h

	if ( aspect_ratio >= 1/2.5* 0.95):
		print("Move foward.")
	elif (not(firstLFound)):
		lastSlide = -1
		firstLFound = True
		print ("slide:")
		print (lastSlide);
	else:
		if (aspect_ratio < lastLW/ lastLH):
			lastSlide *= -1
			print ("Slide:")
			print (lastSlide)

	lastLH = h
	lastLW = w

def rotate (x,y,w,h):
	if (x + w/2 > 410):
		print("Turn right")
	elif (x + w/2< 360):
		print ("turn left")
	else:
		print("don't rotate")
		slideWhichWay(x,y,w,h)

# used for the mask to isloate the Letters
lower_blue = np.array([55,10,100])
upper_blue = np.array([150,255,200])

# start the video stream
#cap = cv2.VideoCapture('http://axis-00408cb18f11.local/mjpg/video.mjpg')

cap = cv2.VideoCapture (0)

# Calculate the contour of an 'L' for use with compairision against candidate L's
m = cv2.imread('L.tif')
#mHSV = cv2.cvtColor(m, cv2.COLOR_BGR2HSV)
#mMask = cv2.inRange(m, lower_blue, upper_blue)
medge = cv2.Canny(m, 100, 250, True)
_, mContours, _ = cv2.findContours(medge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
mPoly = polygonAprox(mContours[0])

#print (len(mContours))
cv2.drawContours(m,[mPoly],-1, (0,0,255), 1)
#cv2.imshow('M',m)
#cv2.imshow('edgem', medge)

allowed = True
# Process the video feed.
while(allowed):

	# get the new frame
	ret, frame = cap.read()
	#print(frame)
	#print(ret)

	blur = cv2.GaussianBlur(frame, (15,15), 1)
	# Make a mask of the blue part of the image.
	hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)


	cv



	erode = cv2.erode(blur, (np.ones((3,3), np.uint8)), iterations = 1)
	cv2.imshow('erode',erode)

	edges = cv2.Canny(erode, 1, 254)
	#cv2.imshow('edges', edges)
	cv2.imshow('mask',mask)
	# find the coutours
	c1, contours_canny, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	polyContour = []
	lContour = []
	for cnt in contours_canny:
		polyAprox = polygonAprox(cnt)
		#print (polyAprox)
		polyContour.append(polyAprox)
		if (len(polyAprox) == 6 ):
			ret = cv2.matchShapes(polyAprox,mPoly,3,0.0)
			if isL(polyAprox, frame):
				lContour.append(polyAprox)
				M = cv2.moments(polyAprox)
				cx = int(M['m10']/M['m00'])
				cy = int(M['m01']/M['m00'])
				x,y,w,h = cv2.boundingRect(cnt)
				print (x)
				print (y)
				print (w)
				print (h)
				rotate(x,y,w,h);
				aspect_ratio = float(w)/h
				#print("("+str(cx/640) + ", " + str(cy/400)+")")
				#print("Apect Ratio: " + str(aspect_ratio))
			#	if h < 500:
				#	print ("Move Foward")
					#print (cy/640 - 0.5)
					#print (cx/400 - 0.5)


				print ("\n")
		#
	#		if (ret <= .35):
	#			if (cv2.contourArea(cnt) >= 100):

#					print (str(isL(polyAprox, frame)))


	frame2 = np.copy(frame)

	cv2.drawContours(blur,polyContour,-1, (0,0,255), 2)
	cv2.drawContours(frame2,lContour,-1, (255,0,255), 4)
	cv2.drawContours(frame,contours_canny,-1, (255,0,255), 4)

# Mix the res with the blue and the
	cv2.imshow('L', frame2)
	cv2.imshow('p', blur)



#	retval2, graythresh = cv2.threshold (grayblur, r, 255, cv2.THRESH_BINARY)


	if cv2.waitKey(1) & 0xFF == ord('q'):
		break
cap.release()
cv2.destroyAllWindows()
