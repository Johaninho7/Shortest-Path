import numpy as np



def dominate(labelList):
	# List to save the iterators of dominated labels
	dominatedLabels = []

	# Compare the last added label to the existing labels
	lastLabel = len(labelList)-1
	lastInPathLastLabel = len(labelList[lastLabel].detailedPath)-1
	for i in range(len(labelList)-1):
		lastInPath = len(labelList[i].detailedPath)-1
		# Can only dominate a label if the two compared labels have visited the same node as their last visit
		if (labelList[lastLabel].detailedPath[lastInPathLastLabel] == labelList[i].detailedPath[lastInPath]):
			# If both labels are equal we dominate the latest added label
			if (labelList[lastLabel].time == labelList[i].time and labelList[lastLabel].drive_R == labelList[i].drive_R and labelList[lastLabel].drive_B == labelList[i].drive_B and labelList[lastLabel].elapsed_R == labelList[i].elapsed_R and np.all(np.asarray(labelList[lastLabel].elem) == np.asarray(labelList[i].elem))):
				labelList[lastLabel].done = True
				dominatedLabels.append(lastLabel)
				# If latest added label is dominated we can abort
				break
			elif (labelList[lastLabel].time <= labelList[i].time and labelList[lastLabel].drive_R <= labelList[i].drive_R and labelList[lastLabel].drive_B <= labelList[i].drive_B and labelList[lastLabel].elapsed_R <= labelList[i].elapsed_R and np.all(np.asarray(labelList[lastLabel].elem) <= np.asarray(labelList[i].elem))):
				# Only register dominance if the label has not already been dominated or completed processing
				if (labelList[i].done == False):
					labelList[i].done = True
					dominatedLabels.append(i)
			elif (labelList[lastLabel].time >= labelList[i].time and labelList[lastLabel].drive_R >= labelList[i].drive_R and labelList[lastLabel].drive_B >= labelList[i].drive_B and labelList[lastLabel].elapsed_R >= labelList[i].elapsed_R and np.all(np.asarray(labelList[lastLabel].elem) >= np.asarray(labelList[i].elem))):
					labelList[lastLabel].done = True
					dominatedLabels.append(lastLabel)
					break
	return dominatedLabels
