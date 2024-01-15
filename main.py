import arcClass, network, parameterfreeNetwork, theAlgorithm, label, CSVreader
import pprint

distanceMatrix = 'DistanceMatrix.csv'
timeMatrix = 'TimeMatrix.csv'

testingInstanceFilename = 'smallerInstanceTest.txt'

distanceData = CSVreader.CSVreader(distanceMatrix)
timeData = CSVreader.CSVreader(timeMatrix)

# Populate arcs with city data
citiesArcs = arcClass.cityArcs.createArcs(distanceData, timeData)


testNetwork = network.Network(testingInstanceFilename, citiesArcs)
testNetwork.parse()
# Print network nodes
nodes = testNetwork.getNodes()
#pprint.pprint(nodes)

paraNetwork = parameterfreeNetwork.parameterfreeNetwork(testNetwork)
interNodes = paraNetwork._getIntermediateNodes()
# Print intermediate nodes
#pprint.pprint(interNodes)
# Print all edges in parameterfree network
#pprint.pprint(paraNetwork._getEdges())

# Run the algortihm
algo = theAlgorithm.algorithm(paraNetwork)


#Finding the label with the lowest timecc
bestLabel = label.Label(paraNetwork._getDepot(), len(paraNetwork.originalNetwork.nodes))
bestLabel.time = float('inf')   #Setting the cost to infinity to compare the cost with the created labels

for l in algo:
	if (l.path[len(l.path)-1] == 3 and l.time < bestLabel.time):
		bestLabel = label

print(f"BEST LABEL: {bestLabel}")


# Network and parameterfree network verification check
"""

for edge in list(paraNetwork.edges.keys())[:20]:  # Checking first 5 edges for example
	from_node, _, to_node = edge if len(edge) == 3 else (edge[0], edge[0], edge[1])
	print(f"Distance from {from_node} to {to_node} is {paraNetwork.originalNetwork.getDistance(from_node, to_node)}")

# Verify Node ID Consistency
original_node_ids = list(paraNetwork.originalNetwork.nodes.keys())
edge_node_ids = [edge for edge in paraNetwork.edges.keys()]

# Print to compare manually or write logic to compare programmatically
print("Original Node IDs:", original_node_ids)
print("Edge Node IDs:", edge_node_ids)

# Verify Correct Data Mapping in Original Network
for node_id in original_node_ids[:5]:  # Checking first 5 nodes for example
    print(f"Node {node_id} data: {paraNetwork.originalNetwork.nodes[node_id]}")


# Test Edge Data
for edge in list(paraNetwork.edges.keys())[:5]:  # Checking first 5 edges for example
    from_node, _, to_node = edge if len(edge) == 3 else (edge[0], edge[0], edge[1])
    print(f"Edge from {from_node} to {to_node}")
    print("From Node Data:", paraNetwork.originalNetwork.nodes.get(from_node))
    print("To Node Data:", paraNetwork.originalNetwork.nodes.get(to_node))
"""
