# Package Path: examples/main.py
"""
Example usage of the *graph-theory* package.

Run with:
    python -m examples.main
"""

from graph_theory.directed import Node, DiGraph
from graph_theory.undirected import Vertex, Edge, UndiGraph
from graph_theory.flow import FlowNode, Network 

from examples.data import airports, routes, weighted_routes, alpha_v, alpha_e  # type: ignore

# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #


def hr() -> None:  # horizontal rule
    print("-" * 40)


def show(items):
    for x in items:
        print(x)


# ------------------------------------------------------------------ #
# Directed graph demo
# ------------------------------------------------------------------ #

hr()
print("Directed Graph")
hr()

g = DiGraph([Node(a) for a in airports], routes)
g.expand_nodes()
for rep, members in g.kosaraju_scc().items():
    print(f"SCC rooted at {rep}: {members}")

# ------------------------------------------------------------------ #
# Undirected graph demo
# ------------------------------------------------------------------ #

hr()
print("Undirected Graph")
hr()

ug = UndiGraph([Vertex(v) for v in airports], [Edge(s, e, w) for s, e, w in weighted_routes])
ug.bfs("LGA")
ug.show_matrix()

# ------------------------------------------------------------------ #
# A-Z demo
# ------------------------------------------------------------------ #

hr()
print("A-Z matrix")
hr()


az = UndiGraph([Vertex(v) for v in alpha_v], [Edge(s, e, w) for s, e, w in alpha_e])
az.show_matrix()

# ------------------------------------------------------------------ #
# Flow-network demo (Edmonds-Karp)
# ------------------------------------------------------------------ #

hr()
print("Flow network (max-flow)")
hr()

# vertices
flow_vertices = [FlowNode("s"), FlowNode("a"), FlowNode("b"), FlowNode("t")]

# arcs: (start, end, capacity)
flow_arcs = [
    ("s", "a", 10),
    ("s", "b", 5),
    ("a", "b", 15),
    ("a", "t", 10),
    ("b", "t", 10),
]

net = Network(flow_vertices, flow_arcs)
print("max-flow =", net.max_flow("s", "t"))

for (u, v), arc in net.arcs.items():
    print(f"{u}->{v}\t{arc.flow}/{arc.capacity}")
