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