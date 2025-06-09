import unittest
from graph_theory import Node, DiGraph

class DirectedGraphTests(unittest.TestCase):
    def test_simple_cycle_scc(self):
        # Create a cycle A -> B -> C -> A
        nodes = [Node(name) for name in ("A", "B", "C")]
        edges = [("A", "B"), ("B", "C"), ("C", "A")]
        g = DiGraph(nodes, edges)

        # Expand paths (not necessary for SCC but ensures no errors)
        g.expand_nodes()

        sccs = g.kosaraju_scc()
        # All three nodes should be in one strongly connected component
        reps = list(sccs.keys())
        self.assertEqual(len(reps), 1)
        comp = sccs[reps[0]]
        self.assertCountEqual([n.id for n in comp], ["A", "B", "C"])

    def test_disconnected_scc(self):
        # Two separate pairs: A->B and C->D
        nodes = [Node(name) for name in ("A", "B", "C", "D")]
        edges = [("A", "B"), ("C", "D")]
        g = DiGraph(nodes, edges)
        sccs = g.kosaraju_scc()

        # Expect 4 SCCs: each individual node not strongly connected back
        self.assertEqual(len(sccs), 4)
        all_ids = sorted(n.id for comp in sccs.values() for n in comp)
        self.assertCountEqual(all_ids, ["A", "B", "C", "D"])

    def test_adjacency(self):
        # Test adjacency helpers
        a, b = Node("A"), Node("B")
        g = DiGraph([a, b], [("A", "B")])
        self.assertTrue(a.is_adjacent(b))
        self.assertFalse(b.is_adjacent(a))
