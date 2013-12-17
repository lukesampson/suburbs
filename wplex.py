test = """hello
{{Use dmy dates|date=October 2012}}
{{Infobox Australian place
| name                = Blakeview
| city                = Adelaide {{Census 2001 AUS |id =SSC41151 |name=Blakeview (State Suburb) |accessdate=20 April 2011 | quick=on}}
| state               = sa}}

'''Blakeview''' is a northern [[Suburbs and localities (Australia)|suburb]] of [[Adelaide]], [[South Australia]].
It is located in the [[City of Playford]]."""

LEFT_DELIM = '{{'
RIGHT_DELIM = '}}'

class Lexer:
	input = ''
	start = 0
	pos = 0
	delim_depth = 0 # depth of template delimiters
	items = []

	def emit(self, type):
		val = self.input[self.start:self.pos]
		self.items.append((type, val))
		self.start = self.pos

	def eof(self):
		return self.pos >= len(self.input)

	def next(self):
		if self.eof():
			return None

		n = self.input[self.pos]
		self.pos += 1
		return n

	# returns true if full value can be accepted at this point
	def can_accept(self, value):
		if self.eof():
			return False

		return self.input.startswith(value, self.pos)


def lex_text(l):
	while True:
		if l.can_accept(LEFT_DELIM):
			if l.pos > l.start:
				l.emit('text')

			return lex_left_tmpl

		if l.next() is None: break

	# reached EOF
	if(l.pos > l.start): l.emit('text')
	return None

def lex_left_tmpl(l):
	l.pos += len(LEFT_DELIM)
	l.delim_depth += 1
	l.emit('left_tmpl')

	return lex_inside_tmpl

def lex_inside_tmpl(l):
	while True:
		if l.can_accept(LEFT_DELIM):
			if l.pos > l.start:
				l.emit('text') # text inside template

			return lex_left_tmpl
		elif l.can_accept(RIGHT_DELIM):
			if l.pos > l.start:
				l.emit('text')
			return lex_right_tmpl

		if l.next() is None: break

	# reached EOF (input is invalid)
	if(l.pos > l.start): l.emit('text')
	return None

def lex_right_tmpl(l):
	l.pos += len(RIGHT_DELIM)
	l.delim_depth -= 1
	l.emit('right_tmpl')

	if l.delim_depth == 0: return lex_text
	return lex_inside_tmpl

def lex(input):
	lexer = Lexer()
	lexer.input = input

	state = lex_text
	while state:
		state = state(lexer)

	return lexer.items

items = lex(test)
for item in items:
	print(item)

	