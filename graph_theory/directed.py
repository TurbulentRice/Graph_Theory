"""
Data structures and algorithms for working with **directed graphs**.

Public API
----------
* ``Node``    - vertex with in/out adjacency helpers
* ``DiGraph`` - adjacency-list graph with SCC detection (Kosaraju)
"""

from __future__ import annotations

import logging
from collections import defaultdict, deque
from typing import Iterable, List, Mapping, MutableMapping, Sequence

__all__ = ["Node", "DiGraph"]

logger = logging.getLogger(__name__)


class Node:
    """Vertex in a directed graph."""

    __slots__ = (
        "id",
        "_in",
        "_out",
        "visited",
        "_scc_rep",
        "access_to",
        "accessible_from",
    )

    def __init__(self, name: str) -> None:
        self.id: str = name
        self._in: set[Node] = set()
        self._out: set[Node] = set()
        self.visited: bool = False
        self._scc_rep: Node | None = None

        # Populated lazily by ``expand``
        self.access_to: list[Node] = []
        self.accessible_from: list[Node] = []

    # ------------------------------------------------------------------ #
    # Representations
    # ------------------------------------------------------------------ #

    def __str__(self) -> str:  # pragma: no cover
        return self.id

    __repr__ = __str__

    @property
    def scc_rep(self) -> "Node | None":
        """Representative of this node's strongly-connected component."""
        return self._scc_rep

    # ------------------------------------------------------------------ #
    # Adjacency helpers
    # ------------------------------------------------------------------ #

    def add_in(self, other: "Node") -> None:
        self._in.add(other)

    def add_out(self, other: "Node") -> None:
        self._out.add(other)

    @property
    def in_neighbors(self) -> list["Node"]:
        return list(self._in)

    @property
    def out_neighbors(self) -> list["Node"]:
        return list(self._out)

    @property
    def io_neighbors(self) -> list["Node"]:
        return list(self._in | self._out)

    def is_adjacent(self, other: "Node") -> bool:
        return other in self._out

    # ------------------------------------------------------------------ #
    # Path expansion
    # ------------------------------------------------------------------ #

    def _dfs(
        self,
        current: "Node",
        attr: str,
        next_attr: str,
    ) -> None:
        for nxt in getattr(current, next_attr):
            coll: list[Node] = getattr(self, attr)
            if nxt not in coll:
                coll.append(nxt)
                self._dfs(nxt, attr, next_attr)

    def expand(self) -> None:
        """Populate ``access_to`` and ``accessible_from`` lists."""
        self.reset(clear=True)
        self._dfs(self, "access_to", "_out")
        self._dfs(self, "accessible_from", "_in")

    # ------------------------------------------------------------------ #
    # House-keeping
    # ------------------------------------------------------------------ #

    def reset(self, *, clear: bool = False) -> None:
        self.visited = False
        self._scc_rep = None
        if clear:
            self.access_to.clear()
            self.accessible_from.clear()


class DiGraph:
    """Adjacency-list directed graph."""

    __slots__ = ("_nodes",)

    def __init__(
        self,
        vertices: Iterable[Node] | None = None,
        edges: Iterable[Sequence[str]] | None = None,
    ) -> None:
        self._nodes: dict[str, Node] = {}
        if vertices:
            self.add_vertices(vertices)
        if edges:
            self.add_edges(edges)

    # ------------------------------------------------------------------ #
    # CRUD
    # ------------------------------------------------------------------ #

    def __contains__(self, item: str | Node) -> bool:
        return str(item) in self._nodes

    def __getitem__(self, name: str) -> Node:
        return self._nodes[name]

    def add_vertex(self, v: Node) -> None:
        if v not in self:
            self._nodes[v.id] = v
        else:
            logger.warning("Vertex %s already present - skipping", v.id)

    def add_vertices(self, vertices: Iterable[Node]) -> None:
        for v in vertices:
            self.add_vertex(v)

    def add_edge(self, edge: Sequence[str]) -> None:
        start, end = edge[:2]
        if start in self and end in self:
            self[start].add_out(self[end])
            self[end].add_in(self[start])
        else:
            raise KeyError(f"Unknown vertex in edge {start} -> {end}")

    def add_edges(self, edges: Iterable[Sequence[str]]) -> None:
        for e in edges:
            self.add_edge(e)

    # ------------------------------------------------------------------ #
    # Utilities
    # ------------------------------------------------------------------ #

    def expand_nodes(self) -> None:
        for v in self._nodes.values():
            v.expand()

    # Kosaraju - internal helpers
    def _dfs_visit(self, v: Node, ordering: deque[Node]) -> None:
        if v.visited:
            return
        v.visited = True
        for nxt in v.out_neighbors:
            self._dfs_visit(nxt, ordering)
        ordering.appendleft(v)

    def _assign(self, v: Node, root: Node) -> None:
        if v.scc_rep:
            return
        v._scc_rep = root  # pylint: disable=protected-access
        for nxt in v.in_neighbors:
            self._assign(nxt, root)

    def kosaraju_scc(self) -> Mapping[Node, List[Node]]:
        """Return strongly-connected components."""
        for n in self._nodes.values():
            n.reset()
        ordering: deque[Node] = deque()
        for v in self._nodes.values():
            self._dfs_visit(v, ordering)

        for v in ordering:
            self._assign(v, v)

        groups: MutableMapping[Node, List[Node]] = defaultdict(list)
        for v in self._nodes.values():
            groups[v.scc_rep].append(v)  # type: ignore[arg-type]
        return groups

    # ------------------------------------------------------------------ #
    # Debug helpers
    # ------------------------------------------------------------------ #

    def info(self) -> None:  # pragma: no cover
        for n in sorted(self._nodes.values(), key=lambda x: x.id):
            print(
                f"{n.id}: in={n.in_neighbors}, out={n.out_neighbors}, SCC={n.scc_rep}"
            )
