from directed_graph import *
from undirected_graph import *
from flow_network import *
from data import *
###############################
#	GENERAL FUNCTIONS
###############################

# UI Format
def f():
    print("-" * 40)

# Show iterable line by line
def show_it(iterable):
    for thing in iterable:
        print(thing)

###############################
f()#	DIRECTED MAIN
print("Directed Graph Test:")
f()
###############################

####################################################
f() # Test airport dataset
print("Airport Data Set:")
f()
####################################################

# Make Nodes
node_list = [Node(n) for n in airports]

# Initialize directed graph
my_graph = DiGraph(node_list, routes)

# Initial DFS traversal, establish "paths" to and from each Node
my_graph.expand_Nodes()

# Perform Kosaraju's algorithm, grouping together strongly connected components
f()
my_graph.kosaraju_algo()
f()

# Print a dict of strongly connected components
print("Strongly Connected Components:")
f()
for k, v in my_graph.get_SCCs().items():
    print(k, v)
f()

my_graph.show_nodes()

####################################################
#	UNDIRECTED Program Functions
####################################################

# Return Vertex list from list of strings
# Since edge data is stored in Graph key: dict, Vertex objects may be unecessary
def make_vertices(vertices):
	return [Vertex(v) for v in vertices]
# Return Edge list from list of [str,str,str]
def make_edges(edges):
	return [Edge(s, e, w) for s, e, w in edges]

#####################################
f()#	UNDIRECTED GRAPH MAIN
print("Undirected Graph Test:")
f()
#####################################

####################################################
f() # Test undirected airport dataset
print("Airport Data Set:")
f()
####################################################
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
my_graph.bfs('LGA')
my_graph.show_matrix()

####################################################
f() # Test a randomly populated A-Z graph with x vertices
print("A-Z Matrix:")
f()
####################################################
# A-Z edge graph with rand connections and rand weights (1-100)

show_it(alpha_e)

abc_graph = UndiGraph(make_vertices(alpha_v), make_edges(alpha_e))

abc_graph.show_matrix()

abc_graph.bfs('A')

#abc_graph.bfs_all()

#abc_graph.traverse()

# print("Check edge between:")
# s, e = input('Start = '), input('End = ')
# print(f'Edge between {s} and {e}: {abc_graph.edge_at(s, e)}')

