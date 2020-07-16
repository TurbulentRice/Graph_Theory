from data import *

# Undirected Graph Data Structures
# Vertices are IDs
# Edges are most important, hold weighted connections between IDs

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
class Edge:
	def __init__(self, start, end, weight=None):
		self.start = start
		self.end = end
		self.W = weight


# Undirected Graph Object
# Wrapper for Adjacency Matrix
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

	# Loop through Edges, adding to Matrix
	# Add s->e to Matrix[key[s]][key[e]]
	# Add e->s to Matrix[key[e]][key[s]]
	def add_edges(self, edges):
		for e in edges:
			# s->e
			self.Matrix[self.key[e.start]][self.key[e.end]] = e.W
			# e->s
			self.Matrix[self.key[e.end]][self.key[e.start]] = e.W

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

	def bfs(self):
		pass

	# Getting around The Matrix
	# Since this is undirected graph, we only need to check n/2 rows
	# When we find a pair, we can mark its partner as checked as well
	def traverse_matrix(self):
		self.Matrix[self.key[]]


##########################
#	Program Functions
##########################

# Return Vertex list from list of strings
# Since edge data is stored in Graph key: dict, Vertex objects may be unecessary
def make_vertices(vertices):
	return [Vertex(v) for v in vertices]
# Return Edge list from list of [str,str,str]
def make_edges(edges):
	return [Edge(s, e, w) for s, e, w in edges]

###########
#	MAIN
###########
#Airports
# Make Vertices and Edges
vertex_list = make_vertices(airports)
edge_list = make_edges(weighted_routes)

# Show edge list
show_it([(e.start, e.end, e.W) for e in edge_list])

# Init undirected graph with Vertecies
my_graph = UndiGraph(vertex_list)

# Add edges
# Edge(start: str, end: str, weight: int)
my_graph.add_edges(edge_list)
my_graph.show_matrix()

####################################################
f() # Test a randomly populated A-Z graph
####################################################
# A-Z edge graph with rand connections and rand weights (1-100)

show_it(alpha_e)

abc_graph = UndiGraph(make_vertices(alpha_v), make_edges(alpha_e))

abc_graph.show_matrix()

# Find vertices with io degree of 0
# 1) check each element in each row until non 0 found
#for every k, v in key, 







