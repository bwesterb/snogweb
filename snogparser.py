from pyparsing import *
from snogweb import *
import logging

expression = Forward()

lpar, rpar, lbrack, rbrack, eqe, chash, dquot, excl = \
	map(lambda x: Literal(x).suppress(), 
	('(', ')', '[', ']', '=', '#', '"', '!'))
comma, dash = \
	map(lambda x: Literal(x),
	(',', '-'))

comment = chash + restOfLine

pDirective = excl + restOfLine

identifier = (dquot + Word(printables.replace('"', ' ')) + dquot) | delimitedList(Word(alphanums), delim=' ', combine=True)

attr = Optional(identifier + eqe) + identifier
attrs = lbrack + delimitedList(attr) + rbrack

aExpression = Optional(attrs) + identifier + Optional(attrs)

operator = dash | comma

pExpression = Optional(attrs) + lpar + expression + rpar + Optional(attrs)

nExpression = (pExpression | aExpression)

expression << nExpression + ZeroOrMore(operator + nExpression)

rExpression = pDirective | expression

snogfile = StringStart() + OneOrMore(rExpression).ignore(comment) + StringEnd()

map(lambda x: x[0].setName(x[1]),
    ((attr,		'attribute'),
     (attrs,		'attributes'),
     (aExpression,	'atomic expression'),
     (identifier,	'identifier'),
     (nExpression,	'normal expression'),
     (operator,		'operator'),
     (expression,	'expression'),
     (rExpression,	'root expression'),
     (pDirective,	'parser directive'),
     (pExpression,	'parenthesed expression')))

def on_attr(s, loc, toks):
	if len(toks) == 1: return toks
	return [tuple(toks)]
attr.setParseAction(on_attr)

def on_attrs(s, loc, toks):
	d = dict()
	for tok in toks:
		if type(tok) == tuple:
			d[tok[0]] = tok[1]
		else:
			d[tok] = None
	return [d]
attrs.setParseAction(on_attrs)

class SnogfileParser:
	def __init__(self):
		self.l = logging.getLogger('SnogfileParser')
		self.fileStack = list()
	
	def on_expr(self, s, loc, toks):
		linkingNode = None
		for i in xrange(0, len(toks), 2):
			if linkingNode != None:
				comb = frozenset((linkingNode, toks[i][0]))
				if not self.links.has_key(comb): self.links[comb] = dict()
				if toks[i][1] != None:
					self.links[comb].update(toks[i][1])
			if i != len(toks) - 1 and toks[i+1] == '-':
				linkingNode = toks[i][0]
		
		return [toks[0]]
	
	def on_rexpr(self, s, loc, toks):
		if len(toks) != 0 and toks[0][1] != None:
			self.l.warn("Link attributes %s of %s lost on char %s" % \
				    (toks[0][1], toks[0][0], loc))

	def on_aexpr(self, s, loc, toks):
		pr, po = None, None
		if type(toks[0]) == dict:
			pr = toks[0]
			nm = toks[1]
		else:
			nm = toks[0]
		if type(toks[-1]) == dict:
			po = toks[-1]
		if not self.nodes.has_key(nm):
			self.nodes[nm] = dict()
		if po != None: self.nodes[nm].update(po)
		return [(nm, pr)]
	
	def on_pdir(self, s, loc, toks):
		bits = toks[0].strip().split(' ')
		if bits[0] == 'include':
			self.fileStack.append(bits[1])
		else:
			self.l.warn('No such parser directive: \'%s\'' % bits[0])
		return []

	def openFile(self, fn):
		self.l.info('Parsing %s' % fn)
		return open(fn, 'r')
	
	def _parseFile(self, f):
		global snogfile
		snogfile.parseFile(f)
	
	def _setup(self):
		global snogfile, aExpression, expression, pDirective, \
		       rExpression

		map(lambda x: x[0].setParseAction(x[1]),
		    ((aExpression, self.on_aexpr),
		     (expression,  self.on_expr),
		     (pDirective,  self.on_pdir),
		     (rExpression, self.on_rexpr)))
		
		self.nodes = dict()
		self.links = dict()
	
	def loopOnFileStack(self):
		while len(self.fileStack) > 0:
			f = self.fileStack.pop()
			if type(f) == str:
				f = self.openFile(f)
			self._parseFile(f)
	
	def parseFile(self, s):
		self._setup()
		self.fileStack.append(s)
		self.loopOnFileStack()
		return self.toSnogWeb()
	
	def parseString(self, s):
		global snogfile
		self._setup()
		snogfile.parseString(s)
		self.loopOnFileStack()
		return self.toSnogWeb()
	
	def toSnogWeb(self):
		snodes = []
		lut = {}
		for name, attr in self.nodes.iteritems():
			node = SnogNode(name, attr)
			snodes.append(node)
			lut[name] = node
		web = SnogWeb(snodes)
		for xy, attr in self.links.iteritems():
			x, y = xy
			SnogLink(lut[x], lut[y], attr)
		return web

__names__ = [SnogfileParser]

if __name__ == '__main__':
	logging.basicConfig(level=logging.INFO)
	print SnogfileParser().parseString("""
a - b - c
a - b[a=b,"c"=d,e="f f"]
a [a] - [b] c # hi
a - [pre]b - q
! woo
(a)
#hi 
([1]a - b)
(a - b) - (c - (d - q, e) - a, (f - g - (h, w - i) - (j[2])))

""")

