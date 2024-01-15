
# Parameters
maxTimeDrive_B = 4.5
maxTimeDrive_R = 9
minTimeBreak = 0.75
minTimeBreakFirst = 0.25
minTimeBreakSecond = 0.5
minTimeRest = 11
minTimeRestFirst = 3
minTimeRestSecond = 9
timeDay = 24

timeDrive_B = 4.5 
timeDrive_R = 9 
timeBreak = 0.75 
timeBreakFirst = 0.25
timeBreakSecond = 0.5 
timeRest = 11 
timeRestFirst = 3
timeRestSecond = 9



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


def delta_l(label, timeDrive_R, timeDrive_B, timeDay, timeRest):
	"""
	print("Checking numeric attributes:")
	print(f"label.timeToNext: {label.timeToNext}, type: {type(label.timeToNext)}")
	print(f"label.drive_R: {label.drive_R}, type: {type(label.drive_R)}")
	print(f"label.elapsed_R: {label.elapsed_R}, type: {type(label.elapsed_R)}")
	print(f"timeDrive_R: {timeDrive_R}, type: {type(timeDrive_R)}")
	print(f"timeDrive_B: {timeDrive_B}, type: {type(timeDrive_B)}")
	print(f"timeDay: {timeDay}, type: {type(timeDay)}")
	print(f"timeRest: {timeRest}, type: {type(timeRest)}")
	"""
	# Ensure all attributes and parameters are numeric
	numeric_attributes = [label.timeToNext, label.drive_R, label.elapsed_R, timeDrive_R, timeDrive_B, timeDay, timeRest]
	
	if all(isinstance(attr, (int, float)) for attr in numeric_attributes):
		# Proceed with calculations
		return min(
			label.timeToNext, 
			timeDrive_R - label.drive_R, 
			timeDrive_B - label.drive_B, 
			timeDay - (label.elapsed_R + timeRest)
		)
	else:
		raise ValueError("All attributes and parameters must be numeric.")

# Define the resource extension functions (REFs)
def fstart_nm(label, time_nm, dist_nm):
	label.timeToNext = time_nm
	label.distanceToNext = dist_nm


def fdrive_delta(label, delta, dist_nm):
	label.time += delta
	label.timeToNext -= delta
	label.drive_B += delta
	label.drive_R += delta
	label.elapsed_R += delta
	label.distance += dist_nm

def fbreak_delta(label, delta):
	label.time += delta
	label.elapsed_R += delta
	label.drive_B = 0
	label.lBreak = timeBreak

def frest_delta(label, delta):
	label.time += delta
	label.drive_R = 0
	label.elapsed_R = 0
	label.drive_B = 0
	label.lBreak = timeBreak
	label.rest = timeRest

def fvisit_nm(label, t_min_m, t_max_m, serviceTime_m, nextNodeId):
	label.time = max(label.time, t_min_m) + serviceTime_m
	label.elapsed_R = max(label.elapsed_R, t_min_m - label.latest_R) + serviceTime_m
	label.latest_R = min(label.latest_R, t_max_m + serviceTime_m - label.elapsed_R)
	label.path.append(nextNodeId)
	label.timeToNext = 0

def fbreak_first(label, delta, timeBreakSecond):
	label.lBreak = timeBreakSecond
	label.time += delta
	label.elapsed_R += delta


def frest_first(label, delta, timeRestSecond):
	label.time += delta
	label.drive_B = 0
	label.drive_R = timeRestSecond
	label.lBreak = timeBreak