from __future__ import with_statement

from pydot import *

import logging
import sys

logging.basicConfig(level=logging.INFO)

def anonymize_dot(dot):
	for node in dot.get_nodes():
		node.set_label('')
		node.set_fillcolor('white')
		node.set_color('black')

if __name__ == '__main__':
	if len(sys.argv) != 3:
		print "usage: python anonymize-dot.py <in.dot> <out.dot>"
		sys.exit(-1)
	dot = graph_from_dot_file(sys.argv[1])
	anonymize_dot(dot)
	with open(sys.argv[2], 'w') as fo:
		fo.write(dot.to_string())
