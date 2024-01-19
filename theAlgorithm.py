import label, copy, arcClass, time, parameterfreeNetwork, copy, isFeasible, dominate, pprint, edgeChecker


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

def algorithm(paraNetwork):
	numIntermediateNodes = len(paraNetwork.intermediate_nodes)
	numNormalNodes = len(paraNetwork.originalNetwork.nodes)
	numNodes = numIntermediateNodes + numNormalNodes
	
	# Initialise list of labels with the first label, the depot, having index 0
	labels = [label.Label(paraNetwork._getDepot(), numNormalNodes)]
	# Initialise an iterator to keep track of which label is currently being processed
	iterator = 0
	# Intrduce a counter which counts the number of dominated labels for stats
	numDominated = 0


	while iterator < len(labels):
		currentLabel = labels[iterator]
		currentNodeTuple = currentLabel.path[-1]
		print(f"\nITERATION {iterator}: Processing label {currentLabel}")
		print(f"\nCURRENTLY IN: {currentNodeTuple}")
		print(f"\nCURRENT DETAILED PATH: {currentLabel.detailedPath}")
		print(f"\nCURRENT PATH: {currentLabel.path}")

		# Processing label if the current one is not done
		if (labels[iterator].done == False):
			# Iterate over edges starting from the current node
			for edge, edgeData in paraNetwork.edges.items():
				# Check if currentNodeTuple is in the edge
				if edgeChecker.edgeChecker(currentNodeTuple, edge):

					if edgeChecker.backToDepotEdge(edge):
						continue
					
					# Edge from an original node to an intermediate node
					if edgeChecker.originalToIntermediateEdge(edge):
						print(f"Edge from customer: {edge[0]} to fit intermediate node: {edge[1]}")
						resourceExtension = edgeData['REF']
						if 'fit' in edge[1] and resourceExtension == paraNetwork._fstart_nm:
							nextTuple = edge[1]
							if callable(resourceExtension):
								# fstart_nm
								time_nm = float(paraNetwork.originalNetwork.getTime(currentNodeTuple, nextTuple))
								dist_nm = float(paraNetwork.originalNetwork.getDistance(currentNodeTuple, nextTuple))
								newLabel = copy.deepcopy(currentLabel)
								newLabel.detailedPath.append(nextTuple)
								resourceExtension(newLabel, time_nm, dist_nm)

						elif 'dull' in edge[1] and resourceExtension == paraNetwork._fstart_nm:
							print(f"Edge from customer: {edge[0]} to dull intermediate node: {edge[1]}")
							nextTuple = edge[1]
							resourceExtension = edgeData['REF']
							if callable(resourceExtension):
								# fstart_nm
								time_nm = float(paraNetwork.originalNetwork.getTime(currentNodeTuple, nextTuple))
								dist_nm = float(paraNetwork.originalNetwork.getDistance(currentNodeTuple, nextTuple))
								newLabel = copy.deepcopy(currentLabel)
								newLabel.detailedPath.append(nextTuple)
								resourceExtension(newLabel, time_nm, dist_nm)
						# Calculate delta after fstart sets timeToNext and distanceToNext
						delta = paraNetwork.delta_l(newLabel, maxTimeDrive_R, maxTimeDrive_B, timeDay, minTimeRest)
					# Edge from an intermediate node to another intermediate node
					elif edgeChecker.intermediateToIntermediateEdge(edge):
						print(f"Edge from intermediate node: {edge[0]} to intermediate node: {edge[1]}")
						nextTuple = edge[1]
						resourceExtension = edgeData['REF']
						while newLabel.timeToNext > 0:
							delta = paraNetwork.delta_l(newLabel, maxTimeDrive_R, maxTimeDrive_B, timeDay, minTimeRest)
							if 'fit' in edge[0] and resourceExtension == paraNetwork._fdrive_delta:
								if callable(resourceExtension):
									# fdrive_delta)
									resourceExtension(newLabel, delta)
									if newLabel.timeToNext == 0 or newLabel.drive_B >= minTimeBreak or newLabel.drive_R >= minTimeRest:
										break
							# In a dull intermedaite node, checking fbreak_delta REF
							elif 'dull' in edge[0] and resourceExtension == paraNetwork._fbreak_delta:
								if callable(resourceExtension):
									# fbreak_delta
									resourceExtension == paraNetwork._fbreak_delta
									resourceExtension(newLabel, delta)
									break

							elif 'dull'	in edge[0] and resourceExtension == paraNetwork._frest_delta:
								if callable(resourceExtension):
									# frest_delta
									resourceExtension == paraNetwork._frest_delta
									resourceExtension(newLabel, delta)
									break
							else:
								if callable(resourceExtension):
									# If unsure, rest
									resourceExtension == paraNetwork._frest_delta
									resourceExtension(newLabel, delta)
									break
					
					# Edge from an intermediate node to an original node
					elif edgeChecker.intermediateToOriginalEdge(edge):
						print(f"Edge from intermediate node: {edge[0]} to customer node: {edge[1]}")
						resourceExtension = edgeData['REF']
						if 'fit' in edge[0] and resourceExtension == paraNetwork._fvisit_nm and newLabel.timeToNext == 0:
							# Access and call the REF method
							if callable(resourceExtension):
								# fvisit_nm
								nextTuple = edge[1]
								TWS_m, TWE_m = paraNetwork.originalNetwork.getTimeWindows(nextTuple)
								ST_m = paraNetwork.originalNetwork.getServiceTime(nextTuple)
								dist_nm = float(paraNetwork.originalNetwork.getDistance(currentNodeTuple, nextTuple))
								resourceExtension(newLabel, TWS_m, TWE_m, ST_m, nextTuple, dist_nm)
								newLabel.elem[int(nextTuple)] += 1
								newLabel = copy.deepcopy(newLabel)

						elif 'dull' in edge[0] and resourceExtension == paraNetwork._fvisit_nm and newLabel.timeToNext == 0:
							if callable(resourceExtension):
								# fvisit_nm
								nextTuple = edge[1]
								TWS_m, TWE_m = paraNetwork.originalNetwork.getTimeWindows(nextTuple)
								ST_m = paraNetwork.originalNetwork.getServiceTime(nextTuple)
								dist_nm = float(paraNetwork.originalNetwork.getDistance(currentNodeTuple, nextTuple))
								resourceExtension(newLabel, TWS_m, TWE_m, ST_m, nextTuple, dist_nm)
								newLabel.elem[int(nextTuple)] += 1
								newLabel = copy.deepcopy(newLabel)
					
					# Add next node to detailed path
					newLabel.detailedPath.append(nextTuple)
					print(f"\nnextTuple: {nextTuple}")

					print(f'\nNEWEST LABEL: {newLabel}')
					print(f"\nNEW DETAILED PATH: {newLabel.detailedPath}")
					print(f"\nNEW PATH: {newLabel.path}")



					# Check feasiblity of new label and if it can be dominated
					if (isFeasible.isFeasible(newLabel)):
						labels.append(newLabel)
						print(f'\n ADDED NEW LABEL: {newLabel}')
						# Check dominance
						dominated = dominate.dominate(labels)


						numDominated += len(dominated)

						# Setting done = True for all dominated labels to avoid expanding these again
						for i in dominated:
							labels[i].done = True

		currentLabel.done = True
		iterator += 1
	print(f"\nNumber of dominated labels: {numDominated}")
	print(f"\nNumber of labels: {len(labels)}")
	#print(f"Label list: {labels}")


	return labels

