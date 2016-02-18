#!/usr/bin/env python
import sys
import io
import os
import codecs
import requests
from bs4 import BeautifulSoup
from urlparse import urlparse

# Function
def remove_nonascii(text):
	return ''.join([i if ord(i) < 128 else " " for i in text])

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

# Getting URL Info
link = raw_input("Please paste url to scrape: ")
url = urlparse(link)
r = requests.get(url.geturl())
soup = BeautifulSoup(r.text, 'lxml')

# Getting path to folder and making directories
output_dest = raw_input("Type path to tables folder: ")
if not os.path.exists(output_dest):
	os.makedirs(output_dest)

# Min number of rows
num_rows = int(raw_input("Min number of rows in your tables: "))

# Percentage of table that is #s
percent_num = long(raw_input("Percentage of table that is numbers: "))/100

# Parsing tables
i = 0
for table in soup.find_all('table'):
	
	# Checking table size
	rows = table.findChildren(['th', 'tr'])
	if len(rows) > int(num_rows):
		# print rows
		
		# Checking table contains a majority of numbers
		entries = len(rows)
		# print(type(entries))
		numerical = 0
		# print(type(numerical))
		for row in rows:
			columns = row.findChildren(['td'])
			entry_strings = (entry for entry in columns if entry.string != None)
			for entry in entry_strings:
				if RepresentsInt(entry.string):
					# print entry
					numerical += 1
		entries = entries * len(columns)
		if numerical/entries > percent_num:
			with codecs.open(output_dest + "table" + str(i) + ".htm", 'w', encoding='utf-8') as f:
				
				# Get opening/closing table tags
				table_tag = table.name
				table_attributes = table.attrs
				table_open = "<" + str(table_tag) + " "
				for attr in sorted(table_attributes):
					table_open += str(attr) + '=\"' + str(table[attr]) + '\" '
				table_open = table_open[:-1] + '>'
				table_close = "</" + str(table_tag) + ">"

				# Format table content
				table = table.encode_contents(formatter='html')
				table = remove_nonascii(table)

				# Write to file
				f.write(table_open)
				f.write(table)
				f.write(table_close)

		i = i + 1

