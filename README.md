# Graph_Theory
Data structures and algorithms useful in graph theory-related problems, including:
* Finding shortest paths between nodes.
* Determining strongly connected components of a system.
* Calculating maximum and minimunm flow in a network.

# Directed Graphs
Node:	        Directional vertex object
               Contains lists of in/out-neighbors, representing edges.
 	          Implements recursive depth-first search through neighbors
        
DiGraph:        Directed graph object
                Uses an adjacency list (dict) to "map" edges.
                Kosaraju Algorithm method determines strongly connected components by performing DFS from each Node.
          
# Undirected Graphs
Vertex:         Wrapper object for a string identifier, potentially superfluous.

Edge:           Weighted edge object, represents connection between two vertices. In/out neighbors can be either directional or undirectional (start/end may be arbitrary).
                Holds weight info for connections between vertecies.
                Can be used in Flow Network implementations as well, since it is weighted and possibly directional.
        
UndiGraph:      Undirected graph object
                Uses adjacency matrix (n x n dimensional array) in conjunciton with ID map (dict) for traversal
                Implements bread-first search through matrix.
            
# Flow Networks (work in progress!)
Directed graph, nodes, and weighted edges
Uses Node, DiGraph, and Edge objects.

Flow:           Subclass of Node. Inherits all from parent, adds inflow and outflow attributes.

Arc:            Subclass of Edge. Inherits all from parent, adds capacity, flow, and residual capacity attributes.

Network:        Subclass of DiGraph. Inherits all from parent, added algorithms for determining sinks, sources, and max and min flow.
