import sys
import os
graph=dict()
k=0
resultSetForCliques=list()

#Function to find all the possible combinations of length k recursively.
#when the length k is reached we check if the combination is a clique or not
#if its a clique we save it in resultSetForCliques result
def findCombinations(nodes,resultSet,pos,pointer):
	if(pointer==k):
		isClique=True
		for node in resultSet:
			if not set(resultSet).issubset(set(graph[node])):
				isClique=False
		if isClique:
			print resultSet
			resultSetForCliques.append(list(resultSet))
		return
	#Checking for n clique if it is n clique then only it can be n+1 clique
	#Doing this we won't end up in every possible combination of greater length
	tempResult= [x for x in resultSet if x != None]
	if(len(tempResult)>1):
		for node in tempResult:
			if node!=None and not (set(tempResult).issubset(set(graph[node]))):
				return

	i=pos
	
	while(i<len(nodes)):
		resultSet[pointer]=nodes[i]
		if(pointer<k):
			findCombinations(nodes,resultSet,i+1,pointer+1)
		i=i+1

#Function to generate graph from the dictionary representation 
#converting it to syntax supported by graphviz and running
#the linux command so the output goes to graph_image.png
def generateGraph(keyNodes):
	isTraversed=set()
	graphString="graph{\n"
	for node in keyNodes:
		graphString+=node+" "
	graphString+="\n"
	
	if len(resultSetForCliques)>0:
		for item in resultSetForCliques[0]:
			graphString+=item+" [fillcolor=green,style=filled] \n"
			
	for node in keyNodes:
		for adjusentNode in graph[node]:
			if not(adjusentNode in isTraversed) and node!=adjusentNode:
				graphString+=node +" -- "+adjusentNode+"\n"
		isTraversed.add(node)
	graphString+="}"
	with open("input_graph.dot","w") as graphFile:
		graphFile.write(graphString)
	
	os.system("dot -Tpng input_graph.dot -o graph_image.png")
	#print graphString  	


inputFileName=sys.argv[1]
kFetched=False
k=0

#Reading a file line by line and storing the result in dictionary with node --> self + adjusent nodes form in the variable graph
with open(inputFileName) as inputFile:
    for line in inputFile:
        list_x=line.rstrip().split(" ")
        if(kFetched == False):
            kFetched = True
            k=int(line.rstrip())
        else:
            graph[list_x[0]]=list_x
#Fetching all the nodes of the graph i.e. keys from the dictionary.
keyNodes=graph.keys()
noOfNodes=len(keyNodes)
rSet= [None]*k
findCombinations(keyNodes,rSet,0,0)
if(len(resultSetForCliques)==0):
	print 'No Cliques of size', k,'found'
generateGraph(keyNodes)
