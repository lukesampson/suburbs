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
	cm = json.loads(text)['query']['categorymembers']
	return [(p['title'], p['pageid']) for p in cm]

def getapi(query):
	url = 'http://en.wikipedia.org/w/api.php?' + query
	headers = { 'User-Agent': 'PostcodeBot/0.1 (+https://github.com/lukesampson/postcodes)' }
	return requests.get(url, headers=headers).text

text = getapi('action=query&list=categorymembers&cmtitle=Category:Suburbs_in_Australia&cmlimit=500&format=json')
print(text)