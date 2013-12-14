
import os
import re

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

text = fixture('cannon_hill.txt')
name, data = parseinfo(text)
print(name)
print(data['postcode'])
print(data['name'])