import lex

def assert_tokens(tokens, *expect):
	assert len(tokens) == len(expect)

	for i, tok in enumerate(expect):
		assert tokens[i][1] == tok


def test_template_with_link():
	test = "{{test|[[link]]}}"
	items = lex.lex(test)

	assert_tokens(items, '{{', 'test', '|', '[[link]]', '}}')
	assert items[3][0] == 'param'

def test_template_with_link_among_param_text():
	test = "{{test|one [[link]]}}"
	items = lex.lex(test)

	assert_tokens(items, '{{', 'test', '|', 'one [[link]]', '}}')
	assert items[3][0] == 'param'

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