import math

class Line:

	def __init__(self, x1, y1, x2, y2, order):
		self.x1 = x1
		self.x2 = x2
		self.y1 = y1
		self.y2 = y2
		self.order = order
		self.length = ((x2-x1)**2 + (y2-y1)**2)**0.5


		tmp1 = (self.x2-self.x1)
		tmp2 = (self.y2-self.y1)
		self.angle = math.atan2(tmp2, tmp1)

	def getLength (self):
		return self.length

	def getOrder (self):
		return self.order

	def getAngle (self):
		return self.angle
