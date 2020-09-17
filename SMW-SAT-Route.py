import pycosat
stages = ["Yoshi's House","Yoshi's Island 1","Yellow Switch Palace","Yoshi's Island 2","Yoshi's Island 3","Yoshi's Island 4","#1 Iggy's Castle","Donut Plains 1","Donut Secret 1","Donut Secret House","Donut Secret 2","Donut Plains 2","Green Switch Palace","Donut Ghost House","Top Secret Area","Donut Plains 3","Donut Plains 4","#2 Morton's Castle","Vanilla Dome 1","Vanilla Secret 1","Vanilla Secret 2","Vanilla Secret 3","Vanilla Fortress","Butter Bridge 1","Butter Bridge 2","Vanilla Dome 2","Red Switch Palace","Vanilla Ghost House","Vanilla Dome 3","Vanilla Dome 4","#3 Lemmy's Castle","Cheese Bridge Area","Soda Lake","Cookie Mountain","#4 Ludwig's Castle","Forest of Illusion 1","Forest of Illusion 2","Blue Switch Palace","Forest of Illusion 3","Forest Ghost House","Forest of Illusion 4","Forest Secret Area","Forest Fortress","#5 Roy's Castle","Chocolate Island 1","Choco-Ghost House","Chocolate Island 2","Chocolate Secret","Chocolate Island 3","Chocolate Fortress","Chocolate Island 4","Chocolate Island 5","#6 Wendy's Castle","Sunken Ghost Ship","Valley of Bowser 1","Valley of Bowser 2","Valley Fortress","Back Door","Valley Ghost House","Valley of Bowser 3","Valley of Bowser 4","#7 Larry's Castle","Front Door","Star World 1","Star World 2","Star World 3","Star World 4","Star World 5","Gnarly","Tubular","Way Cool","Awesome","Groovy","Mondo","Outrageous","Funky"]
exits = [(0,1),(1,2),(0,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(7,11),(11,12),(11,13),(8,13),(13,14),(13,15),(10,15),(15,16),(16,17),(17,18),(18,19),(19,20),(20,21),(21,22),(22,23),(23,24),(18,25),(25,26),(25,27),(27,28),(28,29),(29,30),(30,31),(31,32),(31,33),(33,34),(34,35),(35,39),(39,40),(40,41),(41,42),(39,35),(35,36),(36,38),(38,39),(40,36),(36,37),(38,43),(43,44),(44,45),(45,46),(46,47),(46,48),(48,48),(48,49),(49,50),(50,51),(51,52),(47,52),(52,53),(53,54),(54,55),(55,56),(56,57),(55,58),(58,59),(58,61),(59,60),(60,61),(61,62),(9,63),(19,64),(42,66),(60,68),(63,64),(64,65),(65,66),(66,67),(67,63),(67,68),(68,69),(69,70),(70,71),(71,72),(72,73),(73,74),(74,75),(75,0),(32,65),(63,63),(64,64),(65,65),(66,66)]
rev   = [(1,0),(2,1),(3,0),(4,3),(5,4),(6,5),(7,6),(8,7),(9,8),(10,9),(11,7),(12,11),(13,11),(13,8),(14,13),(15,13),(15,10),(16,15),(17,16),(17,18),(19,18),(20,19),(21,20),(22,21),(23,22),(24,23),(25,18),(26,25),(27,25),(28,27),(29,28),(30,29),(31,30),(32,31),(33,31),(34,33),(35,34),(39,35),(40,39),(41,40),(42,41),(35,39),(36,35),(38,36),(39,38),(36,40),(37,36),(43,38),(44,43),(45,44),(46,54),(47,46),(48,46),(48,48),(49,48),(50,49),(51,50),(52,51),(52,47),(53,52),(54,53),(55,54),(56,55),(57,56),(55,58),(59,58),(61,58),(60,59),(61,60),(62,61),(63,9),(64,19),(66,42),(68,60),(64,63),(65,64),(66,65),(67,66),(67,63),(68,67),(69,68),(70,69),(71,70),(72,71),(73,72),(74,73),(75,74),(75,75),(65,32),(63,63),(64,64),(65,65),(66,66)]
allPath = exits+rev
E = len(allPath) # number of paths total
N = 100                 # number of moves to test for solution

cnf = []
#Constraints:
#Each turn contains at least one edge
for n in range (0,N): # for each turn
	curTurn = []
	for e in range(0,E): # for each edge
		curTurn.append(n*E+e+1)
	cnf.append(curTurn)

#Each turn contains no more than one edge
for n in range (0,N): # for each turn
	for e1 in range (0,E-1): # for each edge
		for e2 in range (e1+1,E): # subsequent edge
			cnf.append([-(n*E+e1+1),-(n*E+e2+1)])

#Every edge in E must be visited at least once
for e in range(0,len(exits)):
	curExit = []
	for n in range (0,N): # for each turn
		curExit.append(n*E+e+1)
	cnf.append(curExit)
	
#Each turn begins where previous turn has ended
#Turn 0
curTurn = []
for p in range(0,len(allPath)):
	path = allPath[p]
	if (path[0]==0):
		curTurn.append(p+1)
cnf.append(curTurn)
# Subsequent turns
for n in range(1,N):
	for p in range(0,len(allPath)):
		path = allPath[p]
		begin = path[0]
		curPath = [-(n*E+p+1)]
		for q in range(0,len(allPath)):
			qath = allPath[q]
			qend = qath[1]
			if (qend==begin):
				curPath.append((n-1)*E+q+1)
		cnf.append(curPath)

#Reverse paths must be preceded by their corresponding forward path
for n in range(1,N):
	for r in range(0,len(rev)):
		curPath = [-(n*E+len(exits)+r+1)]
		for n2 in range(0,n):
			curPath.append((n2)*E+r+1)
		#print(curPath)
		cnf.append(curPath)

import sys
with open('test.cnf','w') as f:
	sys.stdout = f
	print("c test.cnf")
	print("c")
	num_clauses = len(cnf)
	num_variables = 0
	for clause in cnf:
		for val in clause:
			if (abs(val)>num_variables):
				num_variables = abs(val)
	print(f"p cnf {num_variables} {num_clauses}")
	for clause in cnf:
		clause.append(0)
		print(*clause)
