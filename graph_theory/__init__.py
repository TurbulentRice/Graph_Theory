"""
graph_theory package

Core graph data structures and algorithms.

Provides:
  - Directed graphs with SCC detection
  - Undirected adjacency-matrix graphs
  - Flow networks with max-flow (Edmonds-Karp)

Usage:
    from graph_theory import DiGraph, Node, UndiGraph, Vertex, Network, FlowNode
"""

from .directed import Node, DiGraph
from .undirected import Vertex, Edge, UndiGraph
from .flow import FlowNode, Arc, Network

__all__ = [
    "Node",
    "DiGraph",
    "Vertex",
    "Edge",
    "UndiGraph",
    "FlowNode",
    "Arc",
    "Network",
]
