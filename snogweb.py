class SnogWeb:
	def __init__(self, nodes=None):
		if nodes == None: nodes = list()
		self.nodes = dict()
		for node in nodes:
			self.nodes[node.name] = node

class SnogNode:
	def __init__(self, name, attrs=None, links=None):
		if attrs == None: attrs = dict()
		if links == None: links = set()
		self.attrs = attrs
		self.links = links
		self.name = name

class SnogLink:
	def __init__(self, x, y, attrs=None):
		self.x, self.y = x, y
		if attrs == None: attrs = dict()
		self.attrs = attrs
		x.links.add(self)
		y.links.add(self)
	def __del__(self):
		self.x.links.remove(self)
		self.y.links.remove(self)
