# Directed Graph Data Structures
# Node:		Directional vertex object
# 			Recursive Depth First Search method
#           connects i/o paths
# DiGraph:	Directed graph object
# 			Recursive Kosaraju Algorithm method
#           assigns Strongly Connected Component representatives
from collections import defaultdict, deque


# Directional vertex object with expanded adjacency lists
class Node:
    def __init__(self, name: str):
        # ID:			"AAA"
        # Adjacency Lists:
        # prev:	 		in-neighbors
        # next:	 		out-neighbors
        # access_to:	 	all Nodes accessible via fwd path
        # accessible_from:	all Nodes weakly connected to self via back path
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

    # Adders for in/out neighbors
    # Takes a Node, adds
    def add_i(self, n):
        self.prev.append(n)
    def add_o(self, n):
        self.next.append(n)

    # Getters for in/out neighbors
    # if no neighbors, returns empty list (evaluates to false)
    # thus, can be used in conjunction with boolean and len() operations
    # ex; if in_neighbors:;     in_degree(x) = len(x.in_neihgbors)
    def in_neighbors(self):
        return self.prev
    def out_neighbors(self):
        return self.next
    def io_neighbors(self):
        return (self.in_neighbors + self.out_neighbors)

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

    # Reset marker attributes (visited, scc_rep)
    # clear=True:	Also clear access_to and accessible_from lists
    def vreset(self, clear=False):
        self.visited = False
        self.scc_rep = None
        if clear:
            self.access_to.clear()
            self.accessible_from.clear()

    # Test if there is an edge self->y
    def is_adj(self, y):
        return (y in self.next)


# Directed Graph base class
# Use with Node
# Can be initialized with list of Nodes 
class DiGraph:
    def __init__(self, vertex_list=None, edge_list=None):
        # {'ID': Node}
        self.Graph = {}

        # If Nodes/edges provided, add
        if vertex_list:
            self.add_vertices(vertex_list)
        if edge_list:
            self.add_edges(edge_list)

    # Check if an ID (or Node) exists in Graph
    def is_node(self, name: str):
        return (str(name) in self.Graph.keys())

    # Takes a Node and adds to Graph
    def add_vertex(self, v):
        # Check type and exclusion in Graph
        _good = isinstance(v, Node) and not self.is_node(v)

        if _good:
            self.Graph[v.ID] = v
        else: print("Couldn't add vertex...")

    # Takes an edge [start, end] and adds to Nodes
    def add_edge(self, e):
        # Check type and inclusion in Graph
        _good = isinstance(e, list) and (all(self.is_node(x) for x in e[:2]))

        if _good:
            self.Graph[e[0]].add_o(self.Graph[e[1]])
            self.Graph[e[1]].add_i(self.Graph[e[0]])
        else: print ("Couldn't add edge...")

    # Takes a list of Nodes and adds to Graph
    def add_vertices(self, vertices):
        for vertex in vertices:
            self.add_vertex(vertex)

    # Takes a list of [str, str] and adds Node edges
    def add_edges(self, edges):
        for edge in edges:
            self.add_edge(edge)

    # Perform DFS fwd/back on each Node in Graph, adding paths
    def expand_Nodes(self):
        for v in self.Graph.values():
            v.expand()

    def reset_Nodes(self):
        for v in self.Graph.values():
            v.vreset()

    def get_SCCs(self):
        # Get a dict of SCCs
        # {scc_rep: [MemberNodes]}
        strong_components = defaultdict(list)
        for v in self.Graph.values():
            strong_components[v.scc_rep].append(v)
        return strong_components

    # Kosaraju's algorithm to determine Strongly Connected Components
    # Ascribes each Node a representative Node denoting membership in Component
    # rep is an arbitrary member of the Components
    def kosaraju_algo(self):
        # Visit all out
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

        # Visit all in
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
        # Visit nodes, prepend
        for v in self.Graph.values():
            visit(v)
        # Assign nodes to a rep, opposite order of visited
        for v in tree:
            assign(v, v)
        # Return a dict(list) of Srongly Connected Components
        return self.get_SCCs()

    # Print a generic info screen
    def show_nodes(self):
        for name, node in sorted(self.Graph.items()):
            print(f'''
ID: {name}
Connects from: {node.prev}
Connects to: {node.next}
Access to: {node.access_to}
Accessible from: {node.accessible_from}
Group: {node.scc_rep}''')
