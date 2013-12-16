import wp

cats = wp.subcats('Suburbs in Australia')
print('found {} top-level categories'.format(len(cats)))

for cat, catid in cats:
	pages = wp.catpages(catid)
	print('found {} pages for {}'.format(len(pages), cat))
	for page, pageid in pages:
		print("loading {}...".format(page))
		text = wp.pagetext(pageid)
		infotype, data = wp.parseinfo(text)
		if infotype:
			print("{},{},{}".format(data['name'],data['state'],data['postcode']))