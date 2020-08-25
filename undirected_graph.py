# Undirected Graph Data Structures
# Vertices are IDs
# Edges are most important, hold weighted connections between IDs
from collections import deque


# Non-directional vertex, essentially just a string ID
class Vertex:
	def __init__(self, name: str):
		# Potential attributes: Rank, IO degree
		self.ID = name
	# Map ID str to object reference
	def __str__(self):
		return self.ID
	def __repr__(self):
		return self.ID


# Weighted edge shared between two vertices
# Not necessarily undirectional (we'll use this in a directed flow network)
# In UndiGraph, start and end distinction is arbitrary
# However, in a DiGraph, start/end can indicate direction of travel
class Edge:
	def __init__(self, start, end, weight=0):
		self.start = start
		self.end = end
		self.W = weight


# Undirected Graph Object using Adjacency Matrix
class UndiGraph:
	def __init__(self, vertex_list, edge_list=None):
		# key:		dict {"ID": Index}, map Vertex IDs to Matrix index
		# size:		number of vertices
		# Matrix:	Adjacency matrix, plot of edge weights
		self.key = {name.ID: num for num, name in enumerate(vertex_list)}
		self.size = len(vertex_list)
		self.Matrix = [[0 for col in range(self.size)]for row in range(self.size)]

		if edge_list:
			self.add_edges(edge_list)

	# Takes an Edge, adds to Matrix
	# Add s->e to Matrix[key[s]][key[e]]
	# Add e->s to Matrix[key[e]][key[s]]
	def add_edge(self, e):
		# s->e
		self.Matrix[self.key[e.start]][self.key[e.end]] = e.W
		# e->s
		self.Matrix[self.key[e.end]][self.key[e.start]] = e.W

	# Takes list of Edges, adds each to Matrix
	def add_edges(self, edges):
		for edge in edges:
			self.add_edge(edge)

	# Check if something is a vertex in self.key
	def is_v(self, s):
		return s in self.key.keys()

	# Takes a number and gives the ID with corresponding index
	def get_ID(self, s):
		for k, v in self.key.items():
			if v == s:
				return k
		print("Could not find index...")

	def show_matrix(self):
		print('\n')
		
		# Column names
		for t in self.key.keys():
			print(f'\t{t}', end='')
		# Row
		for k, v in self.key.items():
			# Column
			print(f'\n{k}', end='\t')
			for k2, v2 in self.key.items():
				print(self.Matrix[v][v2], end='\t')

		print('\n')

	# Return edge between (start,end) in Matrix
	# Accepts either string of int
	def edge_at(self, s, e):
		# If string IDs, convert and return
		if isinstance(s, str) and isinstance(e, str):
			return self.Matrix[self.key[s]][self.key[e]]
		# Otherwise, if num, simply return
		return self.Matrix[s][e]

	# Breadth-first search from given source (int or str)
	# Depth=0, 1, 2, 3, until no edges left, next vertex
	# Unlike traverse(), we will be checking every cell in every row
	# Completeness counts, we want to explore all vertices and edges, even dups
	def bfs(self, source):
		# If source is str ID, convert to int
		if isinstance(source, str):
			if not self.is_v(source):
			 	print("No corresponding start point...")
			 	return
			root = self.key[source]
		# Otherwise, use int(source) as root
		elif isinstance(source, int):
			root = source

		# Data structures
		# Visited list with len() of matrix, initialize all to False
		visited = [False]*self.size
		# Depth queue
		q = deque()
		q.appendleft(root)
		# Visit source
		visited[root] = True
		# BFS path expansion
		while q:
			current = q.popleft()
			print(f'Current Node: {self.get_ID(current)}')
			
			# For every non-visited adj vertex to current
			for i in range(self.size):
				if ((self.edge_at(current, i)) and (not visited[i])):
					q.appendleft(i)
					visited[i] = True

	# Perform BFS on all vertices
	def bfs_all(self):
		c = 0
		for i in range(self.size):
			print(f'Search #{i+1}')
			self.bfs(i)

	# Query the Matrix
	# Since edges are two-way, we only need to check ((size^2)/2) cells
	# Also, we do not need to check a vertex against itself (ex.A->A)
	def traverse(self):
		counter = 0
		# Row
		for i in range(self.size):
			# Col
			# Ignore vertices before and including this one
			for j in range(i+1, self.size):
				# Get current cell value (index = [i][j])
				cell = self.edge_at(i, j)
				counter+=1

				# Do something if there's an edge
				if cell:
					print(f'Edge between {self.get_ID(i)} and {self.get_ID(j)}: {cell}')
				else:
					print(f'No edge between {self.get_ID(i)} and {self.get_ID(j)}')


		print(f'Number of cells in Matrix:\t{self.size**2}')
		print(f'Number of cells searched:\t{counter}')
