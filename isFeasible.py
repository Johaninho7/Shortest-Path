
# Parameters
maxElapsed_R = 13
maxTimeDrive_B = 4.5
maxTimeDrive_R = 9
minTimeBreak = 0.75
minTimeBreakFirst = 0.25
minTimeBreakSecond = 0.5
minTimeRest = 11
minTimeRestFirst = 3
minTimeRestSecond = 9
timeDay = 24


def isFeasible(label):
	if (label.drive_R <= maxTimeDrive_R and label.drive_B <= maxTimeDrive_B and label.elapsed_R <= maxElapsed_R and max(label.elem) <= 1):
		return True
	else:
		return False
