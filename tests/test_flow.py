import unittest
from graph_theory import FlowNode, Network

class FlowNetworkTests(unittest.TestCase):
    def test_max_flow_simple_direct(self):
        # Single direct edge s->t
        V = [FlowNode("s"), FlowNode("t")]
        E = [("s", "t", 5)]
        net = Network(V, E)
        result = net.max_flow("s", "t")
        self.assertEqual(result, 5)

    def test_max_flow_via_intermediate(self):
        # s->a->t with bottleneck at a->t
        V = [FlowNode("s"), FlowNode("a"), FlowNode("t")]
        E = [("s", "a", 10), ("a", "t", 3)]
        net = Network(V, E)
        result = net.max_flow("s", "t")
        self.assertEqual(result, 3)

    def test_flow_values_and_residuals(self):
        V = [FlowNode("s"), FlowNode("t")]
        E = [("s", "t", 7)]
        net = Network(V, E)
        _ = net.max_flow("s", "t")
        arc = net.arcs[("s", "t")]
        self.assertEqual(arc.flow, 7)
        # residual forward should be zero, backward equal to flow
        self.assertEqual(arc.residual_fwd, 0)
        self.assertEqual(arc.residual_back, 7)
