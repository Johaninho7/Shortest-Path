import label, copy, arcClass, time, parameterfreeNetwork, copy, isFeasible, dominate, pprint


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
		currentNodeTuple = currentLabel.detailedPath[-1]
		print(f"\nITERATION {iterator}: Processing label {currentLabel}")
		print(f"\nCURRENTLY IN: {currentNodeTuple}")
		print(f"\nCURRENT DETAILED PATH: {currentLabel.detailedPath}")
		print(f"\nCURRENT PATH: {currentLabel.path}")

		# Processing label if the current one is not done
		if (labels[iterator].done == False):
			# Iterate over edges starting from the current node
			for edge, edgeData in paraNetwork.edges.items():
				if isinstance(edge, tuple) and (edge[0] == currentNodeTuple or 
					(isinstance(edge[0], tuple) and currentNodeTuple in edge[0] and currentNodeTuple != edge[0][-1]) or
					(isinstance(currentNodeTuple, str) and edge[0] == currentNodeTuple)):
					
					# Initialise new label
					newLabel = copy.deepcopy(currentLabel)
					currentNodeTuple = newLabel.detailedPath[-1]
					
					# Edge from an original node to an intermediate node
					if isinstance(edge[0], str) and isinstance(edge[1], tuple):
						print(f"Edge from customer: {edge[0]} to fit intermediate node: {edge[1]}")
						resourceExtension = edgeData['REF']
						if 'fit' in edge[1] and resourceExtension == paraNetwork._fstart_nm:
							nextTuple = edge[1]
							if callable(resourceExtension):
								# fstart_nm
								time_nm = float(paraNetwork.originalNetwork.getTime(currentNodeTuple, nextTuple))
								dist_nm = float(paraNetwork.originalNetwork.getDistance(currentNodeTuple, nextTuple))
								resourceExtension(newLabel, time_nm, dist_nm)

						elif 'dull' in edge[1] and resourceExtension == paraNetwork._fstart_nm:
							print(f"Edge from customer: {edge[0]} to dull intermediate node: {edge[1]}")
							nextTuple = edge[1]
							resourceExtension = edgeData['REF']
							if callable(resourceExtension):
								# fstart_nm
								time_nm = float(paraNetwork.originalNetwork.getTime(currentNodeTuple, nextTuple))
								dist_nm = float(paraNetwork.originalNetwork.getDistance(currentNodeTuple, nextTuple))
								resourceExtension(newLabel, time_nm, dist_nm)

						delta = paraNetwork.delta_l(newLabel, maxTimeDrive_R, maxTimeDrive_B, timeDay, minTimeRest)
					# Edge from an intermediate node to another intermediate node
					elif isinstance(edge[0], tuple) and isinstance(edge[1], tuple):
						print(f"Edge from intermediate node: {edge[0]} to intermediate node: {edge[1]}")
						nextTuple = edge[1]
						resourceExtension = edgeData['REF']
						while newLabel.timeToNext > 0:
							if 'fit' in edge[0] and resourceExtension == paraNetwork._fdrive_delta:
								if callable(resourceExtension):
									# fdrive_delta
									print(f'\n delta before drive: {delta}')
									resourceExtension(newLabel, delta)
									print(f'\n delta after drive: {delta}')
							
							# In a dull intermedaite node, checking fbreak_delta REF
							elif 'dull' in edge[0] and resourceExtension == paraNetwork._fbreak_delta:
								if callable(resourceExtension):
									# fbreak_delta
									#if currentLabel.drive_B <= maxTimeDrive_B:
									resourceExtension == paraNetwork._fbreak_delta
									resourceExtension(newLabel, delta)
									print(f'\n NEW LABEL: {newLabel}')

							elif 'dull'	in edge[0] and resourceExtension == paraNetwork._frest_delta:
								if callable(resourceExtension):
									# frest_delta
									 #if currentLabel.drive_R <= maxTimeDrive_R:
									resourceExtension == paraNetwork._frest_delta
									resourceExtension(newLabel, delta)
							else:
								if callable(resourceExtension):
									# If unsure, rest
									resourceExtension == paraNetwork._frest_delta
									delta = paraNetwork.delta_l(newLabel, maxTimeDrive_R, maxTimeDrive_B, timeDay, minTimeRest)
									resourceExtension(newLabel, delta)
					
					# Edge from an intermediate node to an original node
					elif isinstance(edge[0], tuple) and isinstance(edge[1], str):
						print(f"Edge from intermediate node: {edge[0]} to customer node: {edge[1]}")
						nextNodeId = edge[1]
						nextTuple = edge[1]
						resourceExtension = edgeData['REF']
						if 'fit' in edge[0] and resourceExtension == paraNetwork._fvisit_nm and newLabel.timeToNext == 0:
							# Access and call the REF method
							if callable(resourceExtension):
								# fvisit_nm
								TWS_m, TWE_m = paraNetwork.originalNetwork.getTimeWindows(nextNodeId)
								ST_m = paraNetwork.originalNetwork.getServiceTime(nextTuple)
								dist_nm = float(paraNetwork.originalNetwork.getDistance(currentNodeTuple, nextNodeId))
								resourceExtension(newLabel, TWS_m, TWE_m, ST_m, nextNodeId, dist_nm)
								newLabel.elem[int(nextNodeId)] += 1

						elif 'dull' in edge[0] and resourceExtension == paraNetwork._fvisit_nm and newLabel.timeToNext == 0:
							if callable(resourceExtension):
								# fvisit_nm
								TWS_m, TWE_m = paraNetwork.originalNetwork.getTimeWindows(nextTuple)
								ST_m = paraNetwork.originalNetwork.getServiceTime(nextTuple)
								dist_nm = float(paraNetwork.originalNetwork.getDistance(currentNodeTuple, nextTuple))
								resourceExtension(newLabel, TWS_m, TWE_m, ST_m, nextNodeId, dist_nm)
								newLabel.elem[int(nextNodeId)] += 1
					
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


"""
def algorithm(paraNetwork):



	# Use a list to save all labels. Initialise the list with the first label having index 0
	labels = [None]*1
	labels[0] = label.Label(paraNetwork._getDepot())	# The depot node

	depotNodeID = paraNetwork._getDepot()
	nextNodeID = '1'
	print("Depot nodeID:", depotNodeID)

	startNode = ('fit', depotNodeID, nextNodeID)
	labels = [label.Label(startNode)]
	print("Initial label:", labels[0])


	# Introduce an iteration counter to keep track of which label is currenly being processed
	iterator = 0

	# Intrduce a counter which counts the number of dominated labels for stats
	numDominated = 0

	print("Starting Algorithm")
	print(f"Depot Node ID: {depotNodeID}")
	print(f"Initial Label: {labels[0]}")

	# Start the algorithm
	while(iterator < len(labels)):
		currentLabel = labels[iterator]

		print(f"Iteration {iterator}: Processing label {currentLabel}")

		if (not currentLabel.done):
			currentNodeID = currentLabel.path[-1]
			print(f"Current Node ID: {currentNodeID}")
			#nextNodeID = None

			# Iterate over edges starting from the current node
			for edge, edgeData in paraNetwork.edges.items():
				print(f"Checking edge: {edge} for node {currentNodeID}")
				if currentNodeID == edge[0]:
					nextNodeID = edge[1]
				elif currentNodeID == edge[1]:
					nextNodeID = edge[0]
				else:
					continue  # Skip if the edge does not involve the current node

				print(f"nextNodeID set to {nextNodeID}")

				# Skip if the edge does not start from the current node

				# Apply the appropriate REF
				resourceExtension = edgeData['REF']
				
				# Determine necessary arguments for the REF method
				
				if resourceExtension == paraNetwork._fstart_nm:
					time_nm = paraNetwork.originalNetwork.getTime(currentNodeID, nextNodeID)
					dist_nm = paraNetwork.originalNetwork.getDistance(currentNodeID, nextNodeID)
					resourceExtension(currentLabel, time_nm, dist_nm)

				elif resourceExtension == paraNetwork._fdrive_delta:
					delta = paraNetwork.delta_l(currentLabel, maxTimeDrive_R, maxTimeDrive_B, timeDay, minTimeRest)
					resourceExtension(currentLabel, delta)

				elif resourceExtension == paraNetwork._fbreak_delta:
					delta = paraNetwork.delta_l(currentLabel, maxTimeDrive_R, maxTimeDrive_B, timeDay, minTimeRest)
					resourceExtension(currentLabel, delta)
				
				elif resourceExtension == paraNetwork._frest_delta:
					delta = paraNetwork.delta_l(currentLabel, maxTimeDrive_R, maxTimeDrive_B, timeDay, minTimeRest)
					resourceExtension(currentLabel, delta_l)
				
				elif resourceExtension == paraNetwork._fvisit_nm:
					TWS_m, TWE_m = paraNetwork.originalNetwork.getTimeWindows(nextNodeID)
					ST_m = paraNetwork.originalNetwork.getServiceTime(nextNodeID)
					dist_nm = paraNetwork.originalNetwork.getDistance(currentNodeID, nextNodeID)
					resourceExtension(currentLabel, TWS_m, TWE_m, ST_m, nextNodeID, dist_nm)


				# Create a new label and update the path
				newLabel = copy.deepcopy(currentLabel)
				newLabel.path.append(nextNodeID)

				print(f"Created new label: {newLabel}")
				print(f"Appending new label to the list.")

				# Add new label to the list of labels, apply dominance checks if necessary
				labels.append(newLabel)
				print(f'Added new label: {newLabel}')

				break

		# Mark the current label as processed
		currentLabel.done = True
		print(f"Completed processing label: {currentLabel}")
		iterator += 1
		print(f"Moving to the next label.")

	print(f"Final set of labels after algorithm completion: {labels}")



"""







"""


		# Processing label if the current one is not done
		if (labels[iterator].done == False):
			# Iterate over edges starting from the current node
			for edge, edgeData in paraNetwork.edges.items():
				# Check if the edge is a tuple (Tuple Edge)
				if isinstance(edge, tuple) and len(edge) == 3:
					
					edgeType, node1, node2 = edge

					# Determine the next node
					if currentNodeID == node1:
						nextTuple = node2
						print(f'\nNexT TuPlE: {nextTuple}')
						break  # Exit the loop if a match is found

				# Check if the edge is a shorter tuple
				elif isinstance(edge, tuple) and len(edge) == 2:
					if currentNodeID == edge[0]:
						nextTuple = edge[1]
						print(f'\nEDGE: {edge}')

				# Check if the edge is a single node
				else:
					nextTuple = edge
					print(f'\nEDGE FAILURE')
				
				#print(f"\nNEXT TUPLE: {nextTuple}")

				if nextTuple != currentNodeID:
					# Create and add new label
					newLabel = copy.deepcopy(currentLabel)
					newLabel.path.append(nextTuple[-1] if len(nextTuple) == 3 else nextTuple)
					print(f"\nCreated new label: {newLabel}")
					
					# Access and call the REF method
					resourceExtension = edgeData['REF']
					if callable(resourceExtension):
						# fstart_nm
						if resourceExtension == paraNetwork._fstart_nm:
							time_nm = float(paraNetwork.originalNetwork.getTime(currentNodeID, nextTuple))
							dist_nm = float(paraNetwork.originalNetwork.getDistance(currentNodeID, nextTuple))
							resourceExtension(currentLabel, time_nm, dist_nm)
						# fdrive_delta, fbreak_delta, frest_delta
						elif resourceExtension in [paraNetwork._fdrive_delta, paraNetwork._fbreak_delta, paraNetwork._frest_delta]:
							delta = paraNetwork.delta_l(currentLabel, maxTimeDrive_R, maxTimeDrive_B, timeDay, minTimeRest)
							print(f'\n delta: {delta}')
							print(f'\n currentLabel: {currentLabel}')
							resourceExtension(currentLabel, delta)
						# fvisit_nm
						elif resourceExtension == paraNetwork._fvisit_nm:
							TWS_m, TWE_m = paraNetwork.originalNetwork.getTimeWindows(nextTuple)
							ST_m = paraNetwork.originalNetwork.getServiceTime(nextTuple)
							dist_nm = float(paraNetwork.originalNetwork.getDistance(currentNodeID, nextTuple))
							resourceExtension(currentLabel, TWS_m, TWE_m, ST_m, nextTuple[1] if len(nextTuple) == 2 else nextTuple, dist_nm)
"""


"""
if isinstance(edge, tuple) and (edge[0] == currentNodeTuple or (isinstance(edge[0], tuple) and
					currentNodeTuple in edge[0] and 
					currentNodeTuple != edge[0][-1])):


"""




"""
		if (not currentLabel.done):		# Processing the label if the current label is not yet processedopå
			# Current node is the last node in the path of the current label
			currentNodeID = currentLabel.path[-1]
			print(f'Checking connections for nodeID: {currentNodeID}')

			# Iterate over edges starting from the current node
			for edge, edgeData in paraNetwork.edges.items():


				# Skip if the next node is the same as the current node
				if (edge == currentNodeID):
					continue

				# Expand the label from nodes that start from the last in labels[iterator].path, i.e the last visited node in the current label
				if(edge[0] == currentNodeID):
					nextNodeID = edge[1]

					
					resourceExtension = edgeData['REF']

					# If REF requires delta, calculate it
					if (resourceExtension in [self._fdrive_delta, self._fbreak_delta, self._frest_delta]):
						delta = paraNetwork.delta_l(newLabel, maxTimeDrive_R, maxTimeDrive_B, timeDay, minTimeRest)

						# Apply REF with delta
						resourceExtension(currentLabel, delta)
					else:
						# Apply REF without delta
						resourceExtension(currentLabel)

					# Initialise a new label based on the current label and the REF
					newLabel = deepcopy(currentLabel)
					resourceExtension

					

					# Add new label to the list of labels
					newLabel.path.append(nextNodeID)
					labels.append(newLabel)


		break


"""

#for edge, edgeData in paraNetwork.edges.items():
		#	if isinstance(currentNodeID, tuple):
		#		# When the current node is intermediate
		#		if currentNodeID == edge[1]:
		#			nextNodeID = edge[2] if isinstance(edge[1], tuple) else edge[1]
		#		elif currentNodeID == edge[1]:
		#			nextNodeID = edge[2] if isinstance(edge[0], tuple) else edge[0]
		#	else:
		#		# When the current node is direct
		#		if currentNodeID == edge[0]:
		#			nextNodeID = edge[1] if isinstance(edge[1], tuple) else edge[1]
		#		elif currentNodeID == edge[1]:
		#			nextNodeID = edge[0] if isinstance(edge[0], tuple) else edge[0]
		#	print(f"Next Node ID: {nextNodeID}")
