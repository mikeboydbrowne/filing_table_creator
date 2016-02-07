#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import io
import codecs
from bs4 import BeautifulSoup

def remove_nonascii(text):
	return ''.join([i if ord(i) < 128 else " " for i in text])

soup = BeautifulSoup(open(sys.argv[1]), 'lxml')

i = 0
for table in soup.find_all('table'):
	with codecs.open("AAPL/tables/table" + str(i) + ".htm", 'w', encoding='utf-8') as f:
		table_tag = table.name
		table_attributes = table.attrs
		table_open = "<" + str(table_tag) + " "
		for attr in sorted(table_attributes):
			table_open += str(attr) + '=\"' + str(table[attr]) + '\" '
		table_open = table_open[:-1] + '>'
		table_close = "</" + str(table_tag) + ">"

		table = table.encode_contents(formatter='html')
		table = remove_nonascii(table)

		f.write(table_open)
		f.write(table)
		f.write(table_close)
	i = i + 1

