import ply.lex as lex

tokens = (
	'TEXT',
	'TEMPLATE',
)

states = (
	('template','exclusive'),
)

def t_template(t):
	r'{{'
	t.lexer.template_start = t.lexer.lexpos
	t.lexer.level = 1
	t.lexer.begin('template')

def t_template_lbraces(t):
	r'{{'
	t.lexer.level += 1

def t_template_rbraces(t):
	r'}}'
	t.lexer.level -= 1
	if t.lexer.level == 0:
		t.value = t.lexer.lexdata[t.lexer.template_start:t.lexer.lexpos-2]
		t.type = 'TEMPLATE'
		t.lexer.lineno += t.value.count('\n')
		t.lexer.begin('INITIAL')
		return t

def t_template_error(t):
	t.lexer.skip(1)

t_TEXT = r'.+'
def t_error(t):
	return t

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

wplexer = lex.lex()

test = """{{Use dmy dates|date=October 2012}}
{{Infobox Australian place
| name                = Blakeview
| city                = Adelaide {{Census 2001 AUS |id =SSC41151 |name=Blakeview (State Suburb) |accessdate=20 April 2011 | quick=on}}
| state               = sa}}

'''Blakeview''' is a northern [[Suburbs and localities (Australia)|suburb]] of [[Adelaide]], [[South Australia]].
It is located in the [[City of Playford]]."""

wplexer.input(test)
while True:
	tok = wplexer.token()
	if not tok: break
	print(tok)
