"""
Max-flow / min-cut utilities built on top of the *graph_theory* ``DiGraph``.

Key features
------------
* **FlowNode** - directed-graph vertex that tracks inflow / outflow totals.
* **Arc**      - edges with capacity & current flow (supports residual view).
* **Network**  - thin DiGraph subclass with an **Edmonds-Karp** ``max_flow``.
  * O(V·E²) - good enough for teaching / medium graphs; zero extra deps.
  * Updates each ``Arc.flow`` in-place and recalculates every node's
    ``inflow`` / ``outflow`` on the fly.

Quick start
-----------
```python
from graph_theory.flow import FlowNode, Network

# vertices
V = [FlowNode("s"), FlowNode("a"), FlowNode("b"), FlowNode("t")]

# arcs: (start, end, capacity)
E = [
    ("s", "a", 10),
    ("s", "b", 5),
    ("a", "b", 15),
    ("a", "t", 10),
    ("b", "t", 10),
]

G = Network(V, E)
print("max-flow =", G.max_flow("s", "t"))         # --> 15
for (u, v), arc in G.arcs.items():
    print(f"{u}->{v}  {arc.flow}/{arc.capacity}")
```
"""

from __future__ import annotations

from collections import deque
from typing import Dict, Iterable, List, Tuple

from graph_theory.directed import Node, DiGraph

__all__ = ["FlowNode", "Arc", "Network"]


# --------------------------------------------------------------------------- #
# Core data objects
# --------------------------------------------------------------------------- #
class FlowNode(Node):
    """Directed-graph node with inflow / outflow accounting."""

    __slots__ = ("inflow", "outflow")

    def __init__(self, name: str) -> None:
        super().__init__(name)
        self.inflow: float = 0.0
        self.outflow: float = 0.0

    def is_source(self) -> bool:
        return self.inflow == 0 and self.outflow > 0

    def is_sink(self) -> bool:
        return self.inflow > 0 and self.outflow == 0


class Arc:
    """Capacity-constrained directed edge."""

    __slots__ = ("start", "end", "capacity", "flow")

    def __init__(self, start: str, end: str, capacity: float, flow: float = 0.0):
        self.start, self.end = start, end
        self.capacity = capacity
        self.flow = flow

    # ------------------------------------------------------------------ #
    # Residual helpers
    # ------------------------------------------------------------------ #
    @property
    def residual_fwd(self) -> float:
        """Remaining capacity to push more flow forward."""
        return self.capacity - self.flow

    @property
    def residual_back(self) -> float:
        """Residual capacity on the *reverse* edge (i.e. retractable flow)."""
        return self.flow

    # Convenience for UI
    def __str__(self) -> str:  # pragma: no cover
        return f"{self.start}->{self.end}  {self.flow}/{self.capacity}"

    __repr__ = __str__


# --------------------------------------------------------------------------- #
# Flow network
# --------------------------------------------------------------------------- #
class Network(DiGraph):
    """Directed graph specialised for :class:`FlowNode` / :class:`Arc`.

    Internally keeps a mapping ``self.arcs[(u, v)] -> Arc`` so that flow
    modifications are O(1).  The superclass still stores raw connectivity
    for generic graph algorithms.
    """

    def __init__(
        self,
        vertices: Iterable[FlowNode] | None = None,
        arcs: Iterable[Tuple[str, str, float]] | None = None,
    ) -> None:
        super().__init__(vertices, None)
        self.arcs: Dict[Tuple[str, str], Arc] = {}
        if arcs:
            self.add_arcs(arcs)

    # ------------------------------------------------------------------ #
    # Adding topology
    # ------------------------------------------------------------------ #
    def add_arc(self, arc: Tuple[str, str, float]) -> None:
        """Add a capacity-constrained arc (u, v, capacity)."""
        u, v, cap = arc
        if u in self and v in self:
            # update connectivity for generic graph ops
            self[u].add_out(self[v])
            self[v].add_in(self[u])

            # create & register Arc
            self.arcs[(u, v)] = Arc(u, v, cap)
        else:
            raise KeyError(f"Unknown vertex in arc {u} -> {v}")

    def add_arcs(self, arcs: Iterable[Tuple[str, str, float]]) -> None:
        for a in arcs:
            self.add_arc(a)

    # ------------------------------------------------------------------ #
    # Edmonds-Karp max-flow
    # ------------------------------------------------------------------ #
    def _bfs_augmenting_path(
        self, s: str, t: str
    ) -> Tuple[float, List[Tuple[str, str, Arc, int]]] | None:
        """Return (path_flow, path) or None if no augmenting path exists.

        *path* is a list of tuples (u, v, arc, dir) where **dir** is
        +1 for forward traversal along (u, v) and -1 for using the
        residual reverse edge (v, u).
        """
        queue: deque[str] = deque([s])
        parent: Dict[str, Tuple[str, str, Arc, int]] = {}  # child -> (u,v,arc,dir)
        visited = {s}

        while queue:
            u = queue.popleft()
            # Explore forward residual edges
            for v in self[u].out_neighbors:
                key = (u, v.id)
                if key in self.arcs:
                    a = self.arcs[key]
                    if a.residual_fwd > 0 and v.id not in visited:
                        visited.add(v.id)
                        parent[v.id] = (u, v.id, a, +1)
                        if v.id == t:
                            break
                        queue.append(v.id)

            # Explore backward residual edges
            for p in self[u].in_neighbors:
                key = (p.id, u)
                if key in self.arcs:
                    a = self.arcs[key]
                    if a.residual_back > 0 and p.id not in visited:
                        visited.add(p.id)
                        parent[p.id] = (u, p.id, a, -1)  # note: child is *p.id*
                        if p.id == t:
                            break
                        queue.append(p.id)
            if t in visited:
                break

        # Reconstruct path
        if t not in visited:
            return None

        path: List[Tuple[str, str, Arc, int]] = []
        v = t
        bottleneck = float("inf")
        while v != s:
            u, x, arc, direction = parent[v]
            # direction +1: arc starts at u, ends at x==v
            # direction -1: arc starts at x==v, ends at u
            residual = arc.residual_fwd if direction == +1 else arc.residual_back
            bottleneck = min(bottleneck, residual)
            path.append((u, x, arc, direction))
            v = u
        path.reverse()
        return bottleneck, path

    def max_flow(self, source: str, sink: str) -> float:
        """Run Edmonds-Karp and return the maximum flow value."""
        if source == sink:
            return 0.0

        # Reset all flows & node stats
        for arc in self.arcs.values():
            arc.flow = 0.0
        for node in self._nodes.values():
            if isinstance(node, FlowNode):
                node.inflow = node.outflow = 0.0

        max_flow_value = 0.0

        while True:
            aug = self._bfs_augmenting_path(source, sink)
            if not aug:
                break
            path_flow, path = aug
            # Augment along the path
            for u, v, arc, direction in path:
                if direction == +1:
                    arc.flow += path_flow
                else:  # reverse edge
                    arc.flow -= path_flow

            max_flow_value += path_flow

        # Update each FlowNode's inflow/outflow
        for (u, v), arc in self.arcs.items():
            self[u].outflow += arc.flow
            self[v].inflow += arc.flow

        return max_flow_value
