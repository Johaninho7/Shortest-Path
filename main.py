from dataframing import CSVreader
import arcClass, solutionClass, network, parameterfreeNetwork, theAlgorithm, label
import pandas as pd
import pprint

distanceMatrix = 'DistanceMatrix.csv'
timeMatrix = 'TimeMatrix.csv'
timeMatrixCSV = pd.read_csv('/Users/johan/Desktop/solutionDictionary Approach/Dataset/TimeMatrix.csv')
path = ('/Users/johan/Desktop/solutionDictionary Approach/Dataset')
#solutionFilename = ('/Users/johan/Desktop/solutionDictionary Approach/Dataset/Results_PDPTW_with_driver_scheduling/BP output/Output Routes 10 with updated Subproblem.txt')
#taskFilename = ('/Users/johan/Desktop/solutionDictionary Approach/Dataset/1D/1D10R1V48-144T10-20W.txt')
testingInstanceFilename = ('/Users/johan/Desktop/class Approach/smallerInstanceTest.txt')

distanceData = CSVreader(distanceMatrix, path)
timeData = CSVreader(timeMatrix, path)

citiesArcs = arcClass.cityArcs.createArcs(distanceData, timeData)

#print(f"Distance from Oslo to Drammen: {cities['OsloO'].distances['Drammen']} and time: {cities['OsloO'].times['Drammen']}")

#solutions = solutionClass.solutionDataDict(solutionFilename)

#print(f"Solution from testcase 3D10R3V24-48T10-20W.txt: Vehicles: {solutions['3D10R3V24-48T10-20W.txt'].vehicles} with solutions: {solutions['3D10R3V24-48T10-20W.txt'].solutions}")

testNetwork = network.Network(testingInstanceFilename, citiesArcs)
testNetwork.parse()
nodes = testNetwork.getNodes()
#pprint.pprint(nodes)




#pprint.pprint(nodes)

paraNetwork = parameterfreeNetwork.parameterfreeNetwork(testNetwork)
interNodes = paraNetwork._getIntermediateNodes()
#pprint.pprint(interNodes)
#pprint.pprint(paraNetwork._getEdges())

algo = theAlgorithm.algorithm(paraNetwork)


#Finding the label with the lowest timecc
bestLabel = label.Label(paraNetwork._getDepot(), len(paraNetwork.originalNetwork.nodes))
bestLabel.time = float('inf')   #Setting the cost to infinity to compare the cost with the created labels

for l in algo:
	if (l.path[len(l.path)-1] == 3 and l.time < bestLabel.time):
		bestLabel = label

print(f"BEST LABEL: {bestLabel}")
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