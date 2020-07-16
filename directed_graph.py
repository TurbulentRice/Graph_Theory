from collections import defaultdict, deque
from data import *


# Directed Graph Data Structures
# Node:		Directional vertex object
# 			Recursive Depth First Search method
# DiGraph:	Directed graph object
# 			Recursive Kosaraju Algorithm method


# Directional vertex object with expanded adjacency lists
class Node:
    def __init__(self, name: str):
        # ID:			"AAA"
        # Adjacency Lists:
        # prev:	 		in-neighbors
        # next:	 		out-neighbors
        # access_to:	 	all nodes accessible to self
        # accessible_from:	all Nodes weakly connected to self via undirected path
        # scc_rep:			Node representing this Node's strongly connected group
        self.ID = name
        self.prev = []
        self.next = []
        self.access_to = []
        self.accessible_from = []
        self.visited = False
        self.scc_rep = None

    # Map ID str to object reference
    # Allows us to reference Node ID directly
    def __str__(self):
        return self.ID

    def __repr__(self):
        return self.ID

    # dfs_fwd():	Recursively connect all accessible out-neighbors
    # dfs_back():	Recursively connect all accessible in-neighbors
    # expand():		Wrapper for dual-DFS, defines root as self.
    # 				Calls DFS fwd and back, appends access_to adjacency list
    def expand(self):
        def dfs_fwd(u):
            for v in u.next:
                if v not in self.access_to:
                    self.access_to.append(v)
                    print(f"Parsing... {self} -> {v}")
                    dfs_fwd(v)

        def dfs_back(u):
            for v in u.prev:
                if v not in self.accessible_from:
                    self.accessible_from.append(v)
                    print(f"Parsing... {self} <- {v}")
                    dfs_back(v)

        # Clear exising paths and visit all neighbors
        self.vreset(clear=True)
        dfs_fwd(self)
        dfs_back(self)

    # Reset temporary Node markers
    # clear=True:	Also clear access_to and accessible_from attributes
    def vreset(self, clear=False):
        self.visited = False
        self.scc_rep = None
        if clear:
            self.access_to.clear()
            self.accessible_from.clear()

    # Get in/out degrees
    def in_degree(self):
        return len(self.prev)

    def out_degree(self):
        return len(self.next)

    def io_degree(self):
        return (self.in_degree + self.out_degree)


class DiGraph:
    def __init__(self, vertex_list, edge_list):
        # Dict map of Nodes {ID: Node}
        self.Graph = {}
        self.add_vertices(vertex_list)
        self.add_edges(edge_list)

    def add_vertices(self, vertices):
        # Add vertices (Nodes) from list of strings
        for vertex in vertices:
            self.Graph[vertex] = Node(vertex)

    def add_edges(self, edges):
        # Add edges to vertices (Node's next/prev attributes)
        for edge in edges:
            self.Graph[edge[0]].next.append(self.Graph[edge[1]])
            self.Graph[edge[1]].prev.append(self.Graph[edge[0]])

    def expand_Nodes(self):
        for v in self.Graph.values():
            v.expand()

    def reset_Nodes(self):
        for v in self.Graph.values():
            v.vreset()

    def get_SCCs(self):
        # Get a dict of SCCs
        strong_components = defaultdict(list)
        for v in self.Graph.values():
            strong_components[v.scc_rep].append(v)
        return strong_components

    # Kosaraju's algorithm to determine Strongly Connected Components
    # Ascribes each Node a "rep" property, which default=None
    def kosaraju_algo(self):
        def visit(v):
            # If v already visited, do nothing
            if v.visited:
                return
            # Otherwise, visit v and successors of v
            v.visited = True
            print(f"Visiting {v}")
            for w in v.next:
                print(f"{v} -> {w}")
                visit(w)
            # Depth reached, add v to tree
            tree.appendleft(v)

        def assign(v, root):
            if v.scc_rep:
                return
            v.scc_rep = root
            print(f"Assigning {v} to {root}")
            for w in v.prev:
                assign(w, root)

        # Implementation
        self.reset_Nodes()
        tree = deque()
        # Visit nodes
        for v in self.Graph.values():
            visit(v)
        # Assign nodes to a rep
        for v in tree:
            assign(v, v)
        # Return a dict(list) of Srongly Connected Components
        return self.get_SCCs()

    def show_nodes(self):
        for name, node in sorted(self.Graph.items()):
            print(f'''
ID: {name}
Connects from: {node.prev}
Connects to: {node.next}
Access to: {node.access_to}
Accessible from: {node.accessible_from}
Group: {node.scc_rep}''')


###########
#	MAIN
###########

# Initialize directed graph
f()
my_graph = DiGraph(airports, routes)
f()

# Initial DFS traversal, establish "paths" to and from each Node
f()
my_graph.expand_Nodes()
f()

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
