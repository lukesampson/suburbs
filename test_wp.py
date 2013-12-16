import wp, os

def fixture(name):
	basedir = os.path.dirname(os.path.abspath(__file__))
	f = open(os.path.join(basedir, 'fixtures', name))
	return f.read()

def test_normal_infobox():
	name, data = wp.parseinfo(fixture('cannon_hill.txt'))
	assert data['name'] == 'Cannon Hill'

def test_infobox_with_data_on_first_line():
	name, data = wp.parseinfo(fixture('bulimba.txt'))
	assert name == 'Australian place'
	assert data['type'] == 'suburb'
	assert data['name'] == 'Bulimba'

def test_infobox_without_padding_after_bars():
	name, data = wp.parseinfo(fixture('craigmore.txt'))
	assert name == 'Australian place'
	assert 'name' in data
	assert data['name'] == 'Craigmore'
	assert data['city'] == 'Adelaide'
'''
def test_infobox_endtag_without_newline():
	name, data = wp.parseinfo(fixture('seaford_heights.txt'))
	assert name'''


def test_strip_tags():
	orig = 'hello<there>mate</there>'
	assert wp.striptags(orig) == 'hello'

	unclosed_tag = '5114<ref name=Postcodes>{{cite web |url=http://www.postcodes-australia.com/areas/sa/adelaide/blakeview'
	assert wp.striptags(unclosed_tag) == '5114'

def test_postcode_with_ref():
	text = wp.parsetext(fixture('beverley.json'), 24011354)
	_, data = wp.parseinfo(text)
	_,_,_,postcode = wp.extractdata(data)
	assert postcode == '5009'

	'''
	text = wp.parsetext(fixture('blakeview.json'), 31548825)
	_, data = wp.parseinfo(text)
	_,_,_,postcode = wp.extractdata(data)

	assert postcode == '5114'
	'''