from snogparser import SnogfileParser
from math import sqrt
import logging
import pydot
import sys

logging.basicConfig(level=logging.INFO)
l = logging.getLogger('snog2dot')

try:
	import psyco
	psyco.full()
except ImportError:
	l.info('Psyco not installed')

l.info('Parsing')
web = SnogfileParser().parseFile(sys.stdin)

l.info('Writing to dot')

dot = pydot.Dot()
dot.set_type('graph')
emited = set()

for name, node in web.nodes.iteritems():
	#fontsize = 10 + 2.17 ** (0.5 * len(node.links))
	fontsize = 10 + len(node.links)
	bg = 'white'
	contour = 'black'
	if node.attrs.has_key('m'): bg = 'lightblue'
	if node.attrs.has_key('v'): bg = 'pink'
	if node.attrs.has_key('p'): bg = 'lightgray'
	if node.attrs.has_key('e'):
		contour = bg
		bg = 'white'
	n = pydot.Node(name,
		       fontsize=str(fontsize),
		       style='filled',
		       fillcolor=bg,
		       color=contour)
	dot.add_node(n)

for name, node in web.nodes.iteritems():
	for link in node.links:
		if link in emited: continue
		emited.add(link)
		dot.add_edge(pydot.Edge(link.x.name, link.y.name))

print dot.to_string()

