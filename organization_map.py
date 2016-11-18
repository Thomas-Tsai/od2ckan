#!/bin/python
# -*- coding: utf-8 -*-
import unicodecsv
class organization_name():
    def __init__(self):
	self.mapfile = "agencies_name_utf8.csv"

    def search(self, keyword):
	with open(self.mapfile, 'r') as govfile:
	    spamreader = unicodecsv.reader(govfile, encoding='utf-8')
	    for row in spamreader:
		org_data = row[1].encode('utf8')
		if org_data == keyword:
		    en = row[2].lower()
		    en = en.replace(" ", "_")
		    govfile.close()
		    return en

if __name__ == '__main__': 
    org=organization_name()
    print org.search("國家發展委員會")

