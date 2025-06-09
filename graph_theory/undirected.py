"""
Light-weight **undirected** graph data structures.

Public API
----------
* ``Vertex``   - labelled graph vertex
* ``Edge``     - weighted undirected connection
* ``UndiGraph``- adjacency-matrix implementation
"""

from __future__ import annotations

from collections import deque
from typing import Iterable, List, Sequence

__all__ = ["Vertex", "Edge", "UndiGraph"]


class Vertex:
    """Graph vertex identified by a unique label."""

    __slots__ = ("id",)

    def __init__(self, name: str) -> None:
        self.id: str = name

    def __str__(self) -> str:  # pragma: no cover
        return self.id

    __repr__ = __str__


class Edge:
    """Weighted undirected connection."""

    __slots__ = ("start", "end", "weight")

    def __init__(self, start: str, end: str, weight: int | float = 0) -> None:
        self.start, self.end, self.weight = start, end, weight


class UndiGraph:
    """Adjacency-matrix undirected graph."""

    __slots__ = ("_key", "_size", "_matrix")

    def __init__(self, vertices: Iterable[Vertex], edges: Iterable[Edge] | None = None):
        self._key: dict[str, int] = {v.id: i for i, v in enumerate(vertices)}
        self._size: int = len(self._key)
        self._matrix: List[List[int | float]] = [
            [0] * self._size for _ in range(self._size)
        ]
        if edges:
            self.add_edges(edges)

    # ------------------------------------------------------------------ #
    # Matrix helpers
    # ------------------------------------------------------------------ #

    def _idx(self, label: str | int) -> int:
        return label if isinstance(label, int) else self._key[label]

    def add_edge(self, edge: Edge) -> None:
        i, j = self._idx(edge.start), self._idx(edge.end)
        self._matrix[i][j] = self._matrix[j][i] = edge.weight

    def add_edges(self, edges: Iterable[Edge]) -> None:
        for e in edges:
            self.add_edge(e)

    def edge(self, a: str | int, b: str | int) -> int | float:
        return self._matrix[self._idx(a)][self._idx(b)]

    # ------------------------------------------------------------------ #
    # Traversal
    # ------------------------------------------------------------------ #

    def bfs(self, source: str | int, *, record: bool = False) -> None:  # pragma: no cover
        root = self._idx(source)
        visited = [False] * self._size
        q: deque[int] = deque([root])
        visited[root] = True
        # Keep list of order if returning record
        order: list[str] = []
        while q:
            cur = q.popleft()
            if record:
                order.append(self._label(cur))
            for i, w in enumerate(self._matrix[cur]):
                if w and not visited[i]:
                    visited[i] = True
                    q.append(i)
        if record:
            return order

    # ------------------------------------------------------------------ #
    # Debug
    # ------------------------------------------------------------------ #

    def _label(self, idx: int) -> str:
        for lab, i in self._key.items():
            if i == idx:
                return lab
        raise KeyError(idx)

    def show_matrix(self) -> None:  # pragma: no cover
        labels = list(self._key)
        print("\t" + "\t".join(labels))
        for r, row in enumerate(self._matrix):
            print(self._label(r), *row, sep="\t")
