# Flow Network
# A Digraph where each Edge has a capacity and receives a flow:
# (flow <= capacity)
# maxflow = largest possible flow from source-> sink
# Transportation Problem (Monge–Kantorovich transportation problem)
# cheapest/most efficient distrubution of resources to meet demand
from directed_graph import Node, DiGraph
from undirected_graph import Edge


# Flow Object
# Represents a total outward flow, determined by total inward flow
# inflow = sum of all outflows of all in-neighbors
# sum([fn.flow for fn in self.in_neighbors()]
# outflow = inflow
class Flow(Node):
	def __init__(self, name: str, i=0, o=0):
		super().__init__(name)
		self.inflow = i
		self.outflow = o

	def set_inflow():
		self.inflow = sum([fn.outflow for fn in self.prev])

	def set_outflow():
		self.outflow = self.inflow

	# source if inflow=0, outflow>0
	# sink if inflow>0 and outflow=0
	def is_source(self):
		return (self.outflow and not self.inflow)
	def is_sink(self):
		return (self.inflow and not self.outflow)


# Arc Object
# Use with FlowNode
# Represents total outflow from one FlowNode to another
# capacity denotes total possible flow from x->y
# flow represents current flow x->
class Arc(Edge):
	def __init__(self, start, end, cap=1, flow=0):
		super().__init__()
		self.capacity = cap
		self.flow = flow

	# Residual Capacity = capacity - flow
	@property
	def res_cap(self):
		return self.capacity - self.flow


# DiGraph Object
# P\ush-relabel algorithm considers 
class Network(DiGraph):
	# add_edge Will have a super() in Network child class that accepts weights
	def __init__(self, v_list=None, e_list=None):
		super().__init__(vlist, elist)
