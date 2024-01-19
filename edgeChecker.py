


def currentNodeIsReal(currentNodeTuple, edge):
	# Check if the current node is a real node and in the edge
	if isinstance(edge, tuple) and isinstance(edge[0], (tuple, str)):
		return currentNodeTuple == edge[0]
	return False

def currentNodeIsIntermediate(currentNodeTuple, edge):
	# Check if the current node is an intermediate node and within the first tuple of the edge,
	# but compare only with the first or second element of this tuple
	if isinstance(edge, tuple) and isinstance(edge[0], (tuple)):
		return currentNodeTuple in edge[0][:2]
	return False


def edgeChecker(currentNodeTuple, edge):
	# Determine if the edge should be processed based on the given checks
	return currentNodeIsReal(currentNodeTuple, edge) or currentNodeIsIntermediate(currentNodeTuple, edge)


def intermediateToIntermediateEdge(edge):
	# Check if the edge is an edge between two intermediate nodes
	if isinstance(edge, tuple) and isinstance(edge[0], tuple) and isinstance(edge[1], tuple):
		return True
	return False

def originalToIntermediateEdge(edge):
	# Check if the edge is an edge between an original node and an intermediate node
	if isinstance(edge[0], str) and isinstance(edge[1], tuple):
		return True
	return False

def intermediateToOriginalEdge(edge):
	# Check if the edge is an edge between an intermediate node and an original node
	if isinstance(edge[0], tuple) and isinstance(edge[1], str):
		return True
	return False

def backToDepotEdge(edge):
	# Check if the edge is an edge leading back towards the depot
	if isinstance(edge[1], (tuple, str)) and edge[1][-1] == '0':
		return True
	return False

