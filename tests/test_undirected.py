import unittest
from graph_theory import Vertex, Edge, UndiGraph

class UndirectedGraphTests(unittest.TestCase):
    def test_edge_weight_and_retrieval(self):
        verts = [Vertex("X"), Vertex("Y")]
        edges = [Edge("X", "Y", 42)]
        g = UndiGraph(verts, edges)
        # Test edge weight
        self.assertEqual(g.edge("X", "Y"), 42)
        self.assertEqual(g.edge("Y", "X"), 42)

    def test_bfs_order(self):
        verts = [Vertex(n) for n in ("A", "B", "C")]
        edges = [Edge("A", "B", 1), Edge("B", "C", 1)]
        g = UndiGraph(verts, edges)

        order = g.bfs("A", record=True)
        self.assertEqual(order, ["A", "B", "C"])
