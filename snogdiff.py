from __future__ import with_statement

from snogparser import SnogfileParser
import logging
import pydot
import sys

logging.basicConfig(level=logging.INFO)

if len(sys.argv) != 3:
	print "Expecting exactly two arguments"
	sys.exit(-1)

with open(sys.argv[1]) as f:
	weba = SnogfileParser().parseFile(f)
with open(sys.argv[2]) as f:
	webb = SnogfileParser().parseFile(f)

def linksOf(web):
	for link in reduce(lambda x, y: x.union(y.links),
			web.nodes.itervalues(), set()):
		yield "%s-%s" % tuple(sorted((link.x.name, link.y.name)))

la, lb = frozenset(linksOf(weba)), frozenset(linksOf(webb))

for link in lb - la:
	x, y = link.split('-')
	print '+ %s%s -- %s%s' % (x, '' if x in weba.nodes else '*',
				  y, '' if y in weba.nodes else '*')
for link in la - lb:
	x, y = link.split('-')
	print '- %s%s -- %s%s' % (x, '' if x in webb.nodes else '*',
				  y, '' if y in webb.nodes else '*')

for n in weba.nodes:
	if not n in webb.nodes:
		print '- %s' % n
for n in webb.nodes:
	if not n in weba.nodes:
		print '+ %s' % n


