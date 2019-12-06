#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class CscAlgo:
	def __init__(self, V,S,G):
		self.V	=	V
		self.S	=	S
		self.G	=	G
		self.R	=	[]		#list of lists
		self.U	=	None	#list

		self.doAlgorithm()



	def get_neighbors(self, S):
		"""
		Returns (a deep copy of) the list of neighbors of vertex S in G
		"""
		return list(self.G[S][1:])


	def find_shortest_path(self, R, T):
		"""
		Finds the shortest R->T path, from any node in R to T.
		Returns a list of nodes P, where:
			. P[0] is a node in R
			. P[-1] is T
			. Every other node in not in R
		"""

		# Take neighbors of T
		T_neighbors = self.get_neighbors(T)

		to_explore = list(T_neighbors)	#nodes to explore via the BFS
		explored = set([T])				#nodes already explored via the BFS
		next_nodes = dict({n: T for n in T_neighbors})	#maps a node to its successor in the R->T path
		starting_node = None 			#first node of the R->T path
		
		# Do the BFS on the graph in "reverse": starting from node T and breaking when arriving to the first node in R
		while len(to_explore) > 0:
			node, to_explore = to_explore[0], to_explore[1:]

			if node in R:
				# This is the nearest node in R. I set it as the first node of the path and exit the BFS
				starting_node = node
				break
			
			for neighbor in self.get_neighbors(node):
				# Append neighbors of `node` to the list of nodes to be explored
				if not neighbor in explored:
					next_nodes[neighbor] = node
					to_explore.append(neighbor)

			explored.add(node)

		else:
			raise Exception("starting_node not found")

		# Use next_nodes to contruct path P
		P = []	#path to be returned
		node = starting_node
		while node != T:
			P.append(node)
			node = next_nodes[node]
		P.append(T)  #append last node T to path

		return P


	def graphAdjacent(self, S1, S2, G):
		for elems1 in S1:

			for setsS2 in S2:
				for elsubsS2 in setsS2:

					if elems1 in G[elsubsS2-1]:
						return True

		return False



#remodule coverAdjacent with S1 and S2  
	def coverAdjacent(self, S1, S2):
		setS1	=	set(S1)
		for lS2	in	S2:
			setS2	=	set(lS2)

			if setS1.intersection(setS2)	==	set():
				return	False
		
		return	True


	def choseMaxS(self,S):
		#1 Chose S_0 € S_corsivo s.t. |S_0| is the maximum, and let R={S_0} and U = S_0
		#return a list inside the first maximum |S_0|
		return max(S, key=len)

	def getElemS1notS2(self,S1,S2):
		#where is a list of lists MORE ATTENTION HERE!
		tempS1	=	[]

		for lsS1 in S1:
			setS1	=	set(lsS1)
			for lsS2 in S2:
				setS2	=	set(lsS2)

				# S1 \ S2
				if setS1.difference(setS2) != set():
					tempS1.append(list(setS1))
					continue
		return tempS1

	def doAlgorithm(self):
		#######################################################################
		## In this program there are only lists							  	  #
		## but in every fuction  we manipulate them through set and subset	  #
		##																	  #
		#######################################################################

		################	FIRST STEP	###################################
		#Choose S0 ∈ S such that |S0| is the maximum
		S_0		=	self.choseMaxS(self.S)
		
		#let R = {S0} and U = S0
		self.R.append(S_0)
		self.U	=	S_0
		

		#################	SECOND STEP	################
		# create a set of V and U

		setV	=	set(self.V)
		setU	=	set(self.U)

		# While V \ U != ∅ DO
		while setV.difference(setU) != set():

			# For each S ∈ S \ R which is cover-adjacent or graph-adjacent 
			# with a set in R

			elemNotR	=	self.getElemS1notS2(self.S,self.R)

			for Sx	in	elemNotR:
				resultCovAdj	= self.coverAdjacent(Sx,self.R)
				resultGraphAdj	= self.graphAdjacent(Sx,self.R,self.G)
				
				
				if resultCovAdj or resultGraphAdj:
					#Try It
					shortest_Path = self.find_shortest_path(self.R,Sx)
					
					"""
					lenghtPs = len(shortest_Path)

					setShortPs = set(shortest_Path)

					tempElemR = []
					for sx in self.R:
						for sxx in sx:
							tempElemR.append(sxx)
					
					setElemR = set(tempElemR)

					diff = setShortPs.difference(setElemR)

					e_Ps = lenghtPs / len(diff)

					"""
				

			break








