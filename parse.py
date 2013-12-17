import lex

def parse(input):
	output = []
	
	items = lex.lex(input)
	
	


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