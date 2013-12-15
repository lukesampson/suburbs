import json, os, re, requests

def fixture(name):
	basedir = os.path.dirname(os.path.abspath(__file__))
	f = open(os.path.join(basedir, 'fixtures', name))
	return f.read()

def parseinfo(text):
	match = re.search('(?:^|\n){{Infobox *([^\n]*)(\n *\|[^\n]*)*\n}}', text)
	if not match:
		return None

	name = match.group(1)
	infotext = match.group(0)
	lines = re.findall('(?m)^ *\|[^\n]*$', infotext)

	data = {}
	for line in lines:
		linematch = re.match('\| ([^ ]+) *= *(.*)', line)
		if linematch:
			data[linematch.group(1)] = linematch.group(2)

	return name, data

def parsesubcats(text):
	j = json.loads(text)
	if 'error' in j:
		raise Exception(j['error']['info'])
	cm = j['query']['categorymembers']#
	return [(p['title'], p['pageid']) for p in cm]

def geturl(url):
	headers = { 'User-Agent': 'PostcodeBot/0.1 (+https://github.com/lukesampson/postcodes)' }
	return requests.get(url, headers=headers).text

def qs(vars):
	return '?' + '&'.join(['{0}={1}'.format(key, value) for key, value in vars.items()])

def apiurl(vars):
	return 'http://en.wikipedia.org/w/api.php' + qs(vars)

def subcats(name):
	vars = { 'cmtitle': 'Category:' + name.replace(' ', '_'), 'action': 'query', 'list': 'categorymembers', 'cmlimit': 500, 'cmtype': 'subcat', 'format': 'json'}
	url = apiurl(vars)
	try:
		return parsesubcats(geturl(url))
	except Exception as err:
		raise Exception("error loading {}".format(url))

def catpages(pageid):
	vars = { 'cmpageid': pageid, 'action': 'query', 'list': 'categorymembers', 'cmlimit': 500, 'cmtype': 'page', 'format': 'json'}
	url = apiurl(vars)
	return parsesubcats(geturl(url))

cats = subcats('Suburbs in Australia')
print('found {} top-level categories'.format(len(cats)))

for cat, pageid in cats:
	p = catpages(pageid)
	print('found {} pages for {}'.format(len(p), cat))


