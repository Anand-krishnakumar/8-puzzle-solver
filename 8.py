#ANAND KRISHNAKUMAR RAJAGOPALAN
import collections
import queue
import itertools
import math
from queue import PriorityQueue

class Node:

	def __init__(self, puzzle, last=None):
		self.puzzle = puzzle
		self.last = last
	#Order of events to the goal
	@property
	def seq(self): 
		node, seq = self, []
		while node:
			seq.append(node)
			node = node.last
		yield from reversed(seq)
	def __lt__(self, other):
		return (self.manhattan() < other.manhattan())
	

	@property #convert to string so it can be compared in sets
	def state(self):
		return str(self.puzzle.board) 

	@property
	def isSolved(self):
		return self.puzzle.isSolved

	@property
	def getMoves(self):
		return self.puzzle.getMoves
 
	
	def manhattan(self):
		goal = [1,2,3,4,5,6,7,8,0]
		total = 0
		for node in self.puzzle.board:
			if node != 0:
				dist = abs(goal.index(node) - self.puzzle.board.index(node))
				(jumps, steps) = (dist // 3, dist % 9)
				total += jumps + steps
		return total

		
class Puzzle:

	def __init__(self, startBoard):
		self.board = startBoard
	
	@property
	def getMoves(self):

		possibleMoves = []

		# find the blank tile (represented as 0)
		findZero = self.board.index(0) 

		if findZero == 0:
			possibleMoves.append(self.move(0,1))
			possibleMoves.append(self.move(0,3))
		elif findZero == 1:
			possibleMoves.append(self.move(1,0))
			possibleMoves.append(self.move(1,2))
			possibleMoves.append(self.move(1,4))
		elif findZero == 2:
			possibleMoves.append(self.move(2,1))
			possibleMoves.append(self.move(2,5))
		elif findZero == 3:
			possibleMoves.append(self.move(3,0))
			possibleMoves.append(self.move(3,4))
			possibleMoves.append(self.move(3,6))
		elif findZero == 4:
			possibleMoves.append(self.move(4,1))
			possibleMoves.append(self.move(4,3))
			possibleMoves.append(self.move(4,5))
			possibleMoves.append(self.move(4,7))
		elif findZero == 5:
			possibleMoves.append(self.move(5,2))
			possibleMoves.append(self.move(5,4))
			possibleMoves.append(self.move(5,8))
		elif findZero == 6:
			possibleMoves.append(self.move(6,3))
			possibleMoves.append(self.move(6,7))
		elif findZero == 7:
			possibleMoves.append(self.move(7,4))
			possibleMoves.append(self.move(7,6))
			possibleMoves.append(self.move(7,8))
		else:
			possibleMoves.append(self.move(8,7))
			possibleMoves.append(self.move(8,5))

		return possibleMoves

	#for moving the postion of the numbers
	def move(self, current, to):

		changeBoard = self.board[:] 
		changeBoard[to], changeBoard[current] = changeBoard[current], changeBoard[to] 
		return Puzzle(changeBoard) 



	# prints board in matrix form
	def printPuzzle(self): 

		copyBoard = self.board[:]
		for i in range(9):
			if i == 2 or i == 5:
				print((str)(copyBoard[i]))
			else:
				print((str)(copyBoard[i])+" ", end="")
		print('\n')

	
	# goal board	
	@property
	def isSolved(self):
		return self.board == [1, 2, 3, 4, 5, 6, 7, 8, 0] 
	

class Solver:

	def __init__(self, Puzzle, enqueued=0):
		self.puzzle = Puzzle
		self.enqueued = enqueued
	
	def ASTAR(self):
		visited = set()
		pq = queue.PriorityQueue(0)
		pq.put((0, 0, Node(self.puzzle)))
		ctr = 0
		while pq:
			closestChild = pq.get()[2]
			visited.add(closestChild.state)
			for board in closestChild.getMoves:
				newChild = Node(board, closestChild)
				if newChild.state not in visited:
					if newChild.manhattan() == 0:
						return newChild.seq, self.enqueued
					ctr += 1
					pq.put((newChild.manhattan()+ctr, ctr, newChild))	
					self.enqueued = self.enqueued+1	
	
	def DFS(self):
		def DFSvisit(currentNode):
			if currentNode.isSolved:
				return currentNode
			self.enqueued = self.enqueued+len(currentNode.getMoves)
			for board in currentNode.getMoves:	
				nextNode = Node(board, currentNode)
				if nextNode.state not in visited:
					visited.add(nextNode.state)
					goalNode = DFSvisit(nextNode)
					if goalNode != None:
						if goalNode.isSolved:
							return goalNode

		visited = set()
		startNode = Node(self.puzzle)
		goalNode = DFSvisit(startNode)
		if goalNode != None:
				if goalNode.isSolved:
					return goalNode.seq, self.enqueued



	def IDDFS(self):

		def DLS(currentNode, depth):
			if depth == 0:
				return None
			if currentNode.isSolved:
				return currentNode
			elif depth > 0:
				self.enqueued = self.enqueued + len(currentNode.getMoves)
				for board in currentNode.getMoves:
					nextNode = Node(board, currentNode)
					if nextNode.state not in visited:
						visited.add(nextNode.state)
						goalNode = DLS(nextNode, depth - 1)
						if goalNode != None: 
							if goalNode.isSolved:
								return goalNode

		for depth in itertools.count():
			visited = set()
			startNode = Node(self.puzzle)
			goalNode = DLS(startNode, depth)
			if goalNode != None:
				if goalNode.isSolved:
					return goalNode.seq, self.enqueued

print ("8-PUZZLE SOLVER")
print (" **********************************************************************")
n = -1
while (n != 0): 
	print("Solve using:")
	print ("1. Depth First search")
	print("2.Iterative Deepening search")
	print("3.A* search")
	print("0.Exit Program")
	n = int(input("Enter the option:  "))
	if (n == 0) or (n<1) or (n>3):
		print("END")
		print("********************************************************")
		exit(0)	
	print(" Enter the 8-puzzle input in the following format")
	print(" Example: 1 2 3 4 5 6 7 0 8")
	k = input()
	l = k.split(" ")
	l = list(map(int, l))
	myPuzzle = Puzzle(l)
	if (n == 1):
		mySolver1 = Solver(myPuzzle)
		Ans1, e = mySolver1.DFS()

		counter = -1
		for node in Ans1:
			counter = counter + 1
			node.puzzle.printPuzzle()
		print("Total number of moves: " + str(counter))
		print("Total number enqueued: " +str(e))

	elif (n == 2):
		mySolver2 = Solver(myPuzzle)
		Ans2, e = mySolver2.IDDFS()

		counter = -1
		for node in Ans2:
			counter = counter + 1
			node.puzzle.printPuzzle()
		print("Total number of moves: " + str(counter))
		print("Total number enqueued: " +str(e))
	
	elif (n == 3):
		mySolver3 = Solver(myPuzzle)
		Ans3, e = mySolver3.ASTAR()

		counter = -1
		for node in Ans3:
			counter = counter + 1
			node.puzzle.printPuzzle()
		print("Total number of moves: " + str(counter))
		print("Total number enqueued: " +str(e))

	












