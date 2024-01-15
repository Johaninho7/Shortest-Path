
class Label():

	#Initializing the label
	def __init__(self, startNode, nNodes):
		startingNode = startNode	# This gets the starting city node ID
		self.path = [startingNode]		# Initialize path as a list with the starting city node ID
		self.detailedPath = [startingNode] # Path including intermediate nodes
		self.elem = [0]*nNodes
		self.elem[0] = 1
		self.time = 0
		self.timeToNext = 0
		self.distance = 0
		self.distanceToNext = 0
		self.drive_R = 0
		self.drive_B = 0
		self.rest = 11
		self.lBreak = 0.75
		self.elapsed_R = 0
		self.latest_R = float('inf')
		self.done = False


	def __str__(self):
		return (f"Label(DetailedPath = {self.detailedPath}, Path = {self.path}, time = {self.time}, timeToNext = {self.timeToNext}, "
			f"distance = {self.distance}, distanceToNext = {self.distanceToNext}, "
			f"drive_R = {self.drive_R}, drive_B = {self.drive_B}, rest = {self.rest}, "
			f"lBreak = {self.lBreak}, elapsed_R = {self.elapsed_R}, latest_R = {self.latest_R}, "
			f"done = {self.done})")

	def __repr__(self):
		return self.__str__()

