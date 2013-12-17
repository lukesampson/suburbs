import lex

class Parser:
	input = []
	pos = 0
	items = []

	def next(self):
		if self.pos >= len(self.input):
			return None

		n = self.input[self.pos]
		self.pos += 1
		return n

	def backup(self):
		self.pos -= 1

	def peek(self):
		n = self.next()
		self.backup()
		return n

def parse_token(t, p):
	type = t[0]
	if type == 'text':
		p.items.append(parse_text(t))
	elif type == 'left_tmpl':
		p.items.append(parse_tmpl(p))

def parse_text(t):
	return t

def parse_tmpl(p):
	name = ''
	params = []

	tok = p.next()
	while tok:
		#print(tok)
		if tok[0] == 'param':
			if not name:
				name = tok[1].strip() # first param is name
			else:
				params.append(tok[1]) # subsequent params (don't strip yet)
		elif tok[0] == 'param_delim':
			pass
		elif tok[0] == 'right_tmpl':
			break
		elif tok[0] == 'left_tmpl':
			p.backup()
			params[-1] += serialize_tmpl(p) # add to last param
		else:
			raise Exception("unexpected token {} ({})".format(tok[0], p.pos))

		tok = p.next()

	# convert params list to data dict
	data = {}
	for param in params:
		clean = param.strip()
		if clean == '': continue
		eq = clean.find('=')
		if eq > -1:
			name = clean[:eq].strip()
			val = clean[eq+1:].strip()
			data[name] = val
		else:
			data[clean] = None

	return ('template', name, data)

# for nested templates, just serialize them back to text to
def serialize_tmpl(p):
	tok = p.next()
	nest_level = 1
	str = ''
	while tok:
		str += tok[1]
		if tok[0] == 'left_tmpl':
			nest_level += 1
		elif tok[0] == 'right_tmpl':
			nest_level -= 1
			if nest_level == 1: break

		tok = p.next()

	return str


def parse(input):
	parser = Parser()
	parser.input = lex.lex(input)

	tok = parser.next()
	while tok:
		parse_token(tok, parser)
		tok = parser.next()

	return parser.items

example = """
('text', 'hello\n')
('left_tmpl', '{{')
('param', 'Use dmy dates')
('param_delim', '|')
('param', 'date=October 2012')
('right_tmpl', '}}')
('text', '\n')
('left_tmpl', '{{')
('param', 'Infobox Australian place\n')
('param_delim', '|')
('param', ' name                = Blakeview\n')
('param_delim', '|')
('param', ' city                = Adelaide ')
('left_tmpl', '{{')
('param', 'Census 2001 AUS ')
('param_delim', '|')
('param', 'id =SSC41151 ')
('param_delim', '|')
('param', 'name=Blakeview (State Suburb) ')
('param_delim', '|')
('param', 'accessdate=20 April 2011 ')
('param_delim', '|')
('param', ' quick=on')
('right_tmpl', '}}')
('param', '\n')
('param_delim', '|')
('param', ' state               = sa')
('right_tmpl', '}}')
('text', "\n\n'''Blakeview''' is a northern [[Suburbs and localities (Australia)|suburb]] of [[Adelaide]], [[South Australia]].\nIt is located in the [[City of Playford]].")
"""


test = """hello
{{Use dmy dates|date=October 2012}}
{{Infobox Australian place
| name                = Blakeview
| city                = Adelaide {{Census 2001 AUS |id =SSC41151 |name=Blakeview (State Suburb) |accessdate=20 April 2011 | quick=on}}
| state               = sa}}

'''Blakeview''' is a northern [[Suburbs and localities (Australia)|suburb]] of [[Adelaide]], [[South Australia]].
It is located in the [[City of Playford]]."""


for item in parse(test):
	print(item)


