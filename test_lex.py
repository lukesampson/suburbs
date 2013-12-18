import lex

def test_template_with_link():
	test = "{{test|[[link]]}}"
	items = lex.lex(test)

	assert len(items) == 7

'''
def test_template_param():
	test = "{{test|a=b}}"
	items = lex.lex(test)

	assert len(items) == 7
'''

'''
def test_link_with_pipe():
	test = "{{test|param=[[link|]]}}"
	items = lex.lex(test)'''