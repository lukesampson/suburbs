import wp

cats = wp.subcats('Suburbs in Australia')
print('found {} top-level categories'.format(len(cats)))

for cat, catid in cats:
	pages = wp.catpages(catid)
	print('found {} pages for {}'.format(len(pages), cat))
	for title, pageid in pages:
		if title.startswith('Template:'):
			print("skipping template {}".format(title))
			continue

		text = wp.pagetext(pageid)
		try:
			infotype, data = wp.parseinfo(text)
		except:
			raise Exception("error parsing info for {} ({})".format(title, pageid))

		if infotype:
			name, city, state, postcode = wp.extractdata(data, title)
			print("{},{},{},{}".format(name,city,state,postcode))
		else:
			print('skipped {}'.format(title))