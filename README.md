# Graph_Theory
Data structures and implementations useful in graph-related problems.

# Directed Graph Data Structures
Node:		Directional vertex object
        Contains lists of in/out-neighbors, representing edges.
 			  Implements recursive depth-first search through neighbors
        
DiGraph:	Directed graph object
          Uses an adjacency list (dict) to "map" edges.
          Kosaraju Algorithm method determines strongly connected components by performing DFS from each Node.
          
# Undirected Graph Data Structures
Vertex: Wrapper for a string identifier, potentially superfluous.

Edge:   Weighted edge between two vertices. In/out neighbors are undirectional (start/end is arbitrary)
        Holds weight info for connections between vertecies.
        Can be used in Flow Network implementations as well, as it is both undirected and weighted.
        
UndiGraph:  Undirected graph object
            Uses adjacency matrix (n x n dimensional array) in conjunciton with ID map (dict) for traversal
            Implements bread-first search through matrix.
