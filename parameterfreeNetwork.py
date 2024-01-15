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

class parameterfreeNetwork:
	def __init__(self, originalNetwork):
		self.originalNetwork = originalNetwork
		self.intermediate_nodes = self._create_intermediate_nodes()
		self.edges = self._create_edges()

	def _create_intermediate_nodes(self):
		intermediate_nodes = {}
		# For every arc in the original network, create corresponding fit and dull nodes
		for (n, m) in self.originalNetwork.arcs:
			if (n!=m):
				intermediate_nodes['fit', n, m] = self._create_node('fit', n, m)
				intermediate_nodes['dull', n, m] = self._create_node('dull', n, m)
		return intermediate_nodes

	def _create_edges(self):
		edges = {}
		# Connect original nodes to intermediate nodes and intermediate nodes to each other
		for (state, n, m) in self.intermediate_nodes:
			if state == 'fit':
				# Adding edges from original node to fit node
				edges[n, (n, 'fit', m)] = {'REF': self._determine_REF('start', n, m)}
				# Adding edges from fit node to end node
				edges[('fit', n, m), m] = {'REF': self._determine_REF('visit', n, m)}
				# Adding edges from fit node to dull node
				edges[('fit', n, m), ('dull', n, m)] = {'REF': self._determine_REF('drive', n, m)}
			elif state == 'dull':
				# Adding edges from original node to dull node
				edges[n, (n, 'dull', m)] = {'REF': self._determine_REF('start', n, m)}
				# Adding edges from dull node to fit node invoking rest
				edges[('dull', n, m), ('fit', n, m)] = {'REF': self._determine_REF('rest', n, m)}
				# Adding edges from dull node to fit node invoking break
				edges[('dull', n, m), ('fit', n, m)] = {'REF': self._determine_REF('break', n, m)}
				# Adding edges from dull node to end node
				edges[('dull', n, m), m] = {'REF': self._determine_REF('visit', n, m)}
		return edges


	# Create a single, specific intermediate node
	def _create_node(self, state, n, m):
		return {
			'state': state,
			'original_arc': (n, m),
			'attributes': self._define_node_attributes(state, n, m)
		}

	def _getIntermediateNodes(self):
		return self.intermediate_nodes

	def _getEdges(self):
		return self.edges

	def _getDepot(self):
		return (next(iter(self.originalNetwork.getNodes().keys())))



	def _define_node_attributes(self, state, n, m):
		# Define the attributes based on whether it's a fit or dull node
		attributes = {}
		if state == 'fit':
			# Attributes for a fit node (driver can drive)
			attributes = {
				'can_drive': True,
				'needs_rest': False,
				# other attributes...
			}
		elif state == 'dull':
			# Attributes for a dull node (driver needs rest or a break)
			attributes = {
				'can_drive': False,
				'needs_rest': True,
				# other attributes...
			}
		return attributes

	def _determine_REF(self, transition_type, n, m):
		# Define the REFs for different types of transitions
		if transition_type == 'start':
			# REF when starting from an original node to a fit node
			return self._fstart_nm
		elif transition_type == 'drive':
			# REF when driving, transitioning from fit to dull
			return self._fdrive_delta
		elif transition_type == 'rest_or_break':
			# REF when resting or taking a break, transitioning from dull to fit
			return self._frest_delta or self._fbreak_delta
		elif transition_type == 'rest':
			# REF when resting or taking a break, transitioning from dull to fit
			return self._frest_delta
		elif transition_type == 'break':
			# REF when taking a break, transitioning from dull to fit
			return self._fbreak_delta
		elif transition_type == 'visit':
			# REF when transitioning from an intermediate node to the end node
			return self._fvisit_nm

	def delta_l(self, label, maxTimeDrive_R, maxTimeDrive_B, timeDay, minTimeRest):
		
		print("Checking numeric attributes:")
		print(f"label.timeToNext: {label.timeToNext}, type: {type(label.timeToNext)}")
		print(f"label.drive_R: {label.drive_R}, type: {type(label.drive_R)}")
		print(f"label.elapsed_R: {label.elapsed_R}, type: {type(label.elapsed_R)}")
		print(f"maxTimeDrive_R: {maxTimeDrive_R}, type: {type(maxTimeDrive_R)}")
		print(f"maxTimeDrive_B: {maxTimeDrive_B}, type: {type(maxTimeDrive_B)}")
		print(f"timeDay: {timeDay}, type: {type(timeDay)}")
		print(f"minTimeRest: {minTimeRest}, type: {type(minTimeRest)}")
		
		# Ensure all attributes and parameters are numeric
		numeric_attributes = [label.timeToNext, label.drive_R, label.elapsed_R, maxTimeDrive_R, maxTimeDrive_B, timeDay, minTimeRest]
		
		if all(isinstance(attr, (int, float)) for attr in numeric_attributes):
			# Proceed with calculations
			return min(
				label.timeToNext, 
				maxTimeDrive_R - label.drive_R, 
				maxTimeDrive_B - label.drive_B, 
				timeDay - (label.elapsed_R + minTimeRest)
			)
		else:
			raise ValueError("All attributes and parameters must be numeric.")

	# Define REF methods here
	def _fstart_nm(self, label, time_nm, dist_nm): 
		label.timeToNext = time_nm
		label.distanceToNext = dist_nm
		print(f"\nSTARTING after leaving: {label.detailedPath[-1]}.")

	def _fdrive_delta(self, label, delta_l):
		label.time += delta_l
		label.timeToNext -= delta_l
		label.drive_B += delta_l
		label.drive_R += delta_l
		label.elapsed_R += delta_l
		print(f"\nDRIVING for {delta_l} after leaving: {label.detailedPath[-1]}.")

	def _fbreak_delta(self, label, delta_l):
		label.time += delta_l
		label.elapsed_R += delta_l
		label.drive_B = 0
		label.lBreak = minTimeBreak
		print(f"\nBREAKING for {delta_l} after leaving: {label.detailedPath[-1]}.")

	def _frest_delta(self, label, delta_l):
		label.time += delta_l
		label.drive_R = 0
		label.elapsed_R = 0
		label.drive_B = 0
		label.lBreak = minTimeBreak
		label.rest = minTimeRest
		print(f"\nRESTING for {delta_l} after leaving: {label.detailedPath[-1]}.")

	def _fvisit_nm(self, label, t_min_m, t_max_m, serviceTime_m, nextNodeId, dist_nm):
		label.time = max(label.time, t_min_m) + serviceTime_m
		label.elapsed_R = max(label.elapsed_R, t_min_m - label.latest_R) + serviceTime_m
		label.latest_R = min(label.latest_R, t_max_m + serviceTime_m - label.elapsed_R)
		label.path.append(nextNodeId)
		label.timeToNext = 0
		label.distance += dist_nm
		label.distanceToNext = 0
		print(f"\nVISITING {nextNodeId[-1]} after leaving: {label.detailedPath[-1]}.")

"""
	def _create_edges(self):
		edges = {}

		# Iterate over each original arc and its corresponding intermediate nodes
		for (n, m) in self.originalNetwork.arcs:
			# Skip self-loops
			if n == m:
				continue

			# Intermediate nodes for the arc
			fit_node = ('fit', n, m)
			dull_node = ('dull', n, m)

			# Connect original node to intermediate nodes
			edges[(n, fit_node)] = {'REF': self._determine_REF('start', n, m)}
			edges[(n, dull_node)] = {'REF': self._determine_REF('start', n, m)}

			# Connect intermediate nodes to each other
			edges[(fit_node, dull_node)] = {'REF': self._determine_REF('drive', n, m)}
			edges[(dull_node, fit_node)] = {'REF': self._determine_REF('rest_or_break', n, m)}
			#edges[(dull_node, fit_node)] = {'REF': self._determine_REF('rest', n, m)}
			#edges[(dull_node, fit_node)] = {'REF': self._determine_REF('break', n, m)}

			# Connect intermediate nodes back to original end node
			edges[(fit_node, m)] = {'REF': self._determine_REF('visit', n, m)}
			edges[(dull_node, m)] = {'REF': self._determine_REF('visit', n, m)}

		return edges
"""
"""
	def _create_edges(self):
		edges = {}
		# Iterate through each node in the original network
		for node_id in self.originalNetwork.nodes:
			# Create edges for 'fit' and 'dull' states
			for state in ['fit', 'dull']:
				# Adding edges from original node to intermediate node
				edges[(node_id, state)] = {'REF': self._determine_REF('start', node_id)}

				# Assuming you have a method to find connected nodes
				connected_nodes = self.originalNetwork.cityArcs(node_id)  # Implement this method
				for connected_node in connected_nodes:
					# Adding edges from intermediate node to end node and other intermediate node
					edges[(state, node_id, connected_node)] = {'REF': self._determine_REF('drive', node_id, connected_node)}
					edges[(state, connected_node, node_id)] = {'REF': self._determine_REF('rest_or_break', connected_node)}

		return edges
"""

"""
def _create_edges(self):
	edges = {}
	# Connect original nodes to intermediate nodes and intermediate nodes to each other
	for node_id in self.originalNetwork.nodes:
		for state in ['fit', 'dull']:
			intermediate_node_id = (state, node_id)
			# Adding edges from original node to intermediate nodes (fit and dull)
			edges[(node_id, intermediate_node_id)] = {'REF': self._determine_REF('start', node_id, intermediate_node_id)}

			# Iterate over connected nodes to create edges to and from intermediate nodes
			for connected_node_id in self.originalNetwork.arcs:
				if node_id in connected_node_id:
					# Determine the other node in the arc
					other_node_id = connected_node_id[1] if connected_node_id[0] == node_id else connected_node_id[0]

					# Adding edges from fit intermediate node to connected nodes and dull intermediate node
					if state == 'fit':
						edges[(intermediate_node_id, other_node_id)] = {'REF': self._determine_REF('visit', node_id, other_node_id)}
						edges[(intermediate_node_id, ('dull', node_id))] = {'REF': self._determine_REF('drive', node_id, other_node_id)}

					# Adding edges from dull intermediate node to fit intermediate node and connected nodes
					elif state == 'dull':
						edges[(intermediate_node_id, ('fit', node_id))] = {'REF': self._determine_REF('rest_or_break', node_id, other_node_id)}
						edges[(intermediate_node_id, other_node_id)] = {'REF': self._determine_REF('visit', node_id, other_node_id)}

	return edges

	"""

"""

	def _getTime(self, edge):
		# Handle intermediate nodes by extracting original node Ids
		if isinstance(edge, tuple):
			toNode = self.intermediate_nodes[edge]['original_arc'][0]
			fromNode = self.intermediate_nodes[edge]['original_arc'][1]
			toCity = self.originalNetwork.nodes.get(toNode, {}).get('location')
			fromCity = self.originalNetwork.nodes.get(fromNode, {}).get('location')
			return self.originalNetwork.cityArcs[fromCity]._getTime(toCity)
		# Handle regular nodes by extracting original node Ids
		else:
			toNode = self.originalNetwork.nodes.get(edge[1], {}).get('location')
			fromNode = self.originalNetwork.nodes.get(edge[0], {}).get('location')
			return self.originalNetwork.cityArcs[fromNode]._getTime(toNode)


"""