LEFT_DELIM = '{{'
RIGHT_DELIM = '}}'
PARAM_DELIM = '|'

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

	# get the next character
	def next(self):
		if self.eof():
			return None

		n = self.input[self.pos]
		self.pos += 1
		return n

	# checks whether <value> is ahead
	def ahead(self, value):
		if self.eof():
			return False

		return self.input.startswith(value, self.pos)

	def which_ahead(self, *values):
		for value in values:
			if self.ahead(value): return value
		return None


def lex_text(l):
	while True:
		if l.ahead(LEFT_DELIM):
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
		which = l.which_ahead(LEFT_DELIM, RIGHT_DELIM, PARAM_DELIM)
		if which:
			if l.pos > l.start:
				l.emit('param')

			if which == LEFT_DELIM:  return lex_left_tmpl
			if which == RIGHT_DELIM: return lex_right_tmpl
			if which == PARAM_DELIM: return lex_param_delim

		if l.next() is None: break

	# reached EOF (input is invalid)
	if(l.pos > l.start): l.emit('text')
	return None

def lex_param_delim(l):
	l.pos += len(PARAM_DELIM)
	l.emit('param_delim')
	return lex_inside_tmpl

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
	