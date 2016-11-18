#!/bin/python
# -*- coding: utf-8 -*-
import json
import io

class od():
    def __init__(self):
	self.data={'distribution':[]}

    def restruct(self, data):
	for k,v in data.items():
	    if k == "distribution":
		for desc in v:
		    desc_data = {}
		    for dk,dv in desc.items():
			desc_data[dk] = dv
		    self.data['distribution'].append(desc_data)
	    elif k == "keyword":
		for keyword in v:
		    self.data['keyword']=v
	    elif k == 'Comments':
		continue
	    else:
		self.data[k]=v
	return self.data

    def loadfile(self, odfile):
	with io.open(odfile, 'r', encoding='utf-8') as datafd:
	    data = datafd.read()
	x=json.loads(data)
	rs = self.restruct(x['result'])
	return rs

    def display(self, odfile):
	rs = self.loadfile(odfile)
	for k,v in rs.items():
	    if k == "distribution":
		for desc in v:
		    for dk,dv in desc.items():
			print "%30s : %s" % (dk, dv)
	    elif k == "keyword":
		for keyword in v:
		    print "%30s : %s" % ("keyword", keyword)
	    else:
		print "%30s : %s" % (k, v)

    def read(self, odfile):
	rs = self.loadfile(odfile)
	return rs

if __name__ == '__main__': 
    jsonfile = 'data.txt'
    odtw=od()
    odtw.display(jsonfile)
    data = odtw.read(jsonfile)
    print data
