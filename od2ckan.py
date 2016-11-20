#!/bin/python
# -*- coding: utf-8 -*-
import odtw
import map2ckan
import os
from ckanapi import RemoteCKAN, NotAuthorized

class import2ckan():
    def __init__(self):
	url = "http://140.110.240.59"
	ckan_key = "a6d44b37-7407-4ad1-b457-aa4b6c611d29"
	ua = 'ckanapiexample/1.0 (+http://example.com/my/website)'
	self.ckan = RemoteCKAN(url, apikey=ckan_key, user_agent=ua)
	self.package = {}
	self.package_exist = 0

    def check_package(self):
	pkgs = self.ckan.action.package_autocomplete(q=self.package['name'].lower())
	for pkg in pkgs: 
	    if self.package['name'].lower() == pkg['name']:
		return True
	return False

    def check_resource(self, testresid):
	package_resources = self.ckan.action.package_show(id=self.package['name'].lower())
	for res in package_resources['resources']:
	    if res['name'] == testresid:
		return True
	return False

    def check_organization(self):
	org = self.ckan.action.organization_list(organizations=[self.package['owner_org']])
	if len(org) == 0:
	    return False
	else:
	    return True

    def check_tag(self):
	return

    def add_package(self):
        self.ckan.action.package_create(
	    name = self.package['name'].lower(),
	    title = self.package['title'],
	    owner_org = self.package['owner_org'],
	    notes = self.package['notes'],
	    type = self.package['type'],
	    last_modified = self.package['last_modified'],
	    #license_id = self.package['license_id'],
	    author = self.package['author'],
	    author_email = self.package['author_email'],
	    tags = self.package['tag'],
	    extras = self.package['extras']
        )

	return

    def add_resource(self):

	for res in self.package['resources']:
	    rfile = self.package['basepath']+'/'+res['resourceid']+'.'+res['format'].lower()
	    if self.check_resource(res['resourceid'].lower()) == True:
		print "res exist %s" % res['resourceid']
	    else:
	        self.ckan.action.resource_create(
	            package_id=self.package['name'].lower(),
	            url=res['resourceid'].lower(),
	            description=res['resourcedescription'],
	            format=res['format'].lower(),
	            name=res['resourceid'].lower(),
	            last_modified=res['resourcemodified'],
		    upload=open(rfile, 'rb'),
	        )
	return

    def add_organization(self):
	self.ckan.action.organization_create(
		name=self.package['owner_org'],
		title=self.package['org']['title'],
		extras=self.package['org']['extras']
		)
	return

    def add_tag(self):
	return

    def update_organization(self):
	self.ckan.action.organization_update(
		id=self.package['owner_org'],
		name=self.package['owner_org'],
		title=self.package['org']['title'],
		extras=self.package['org']['extras']
		)
	return

    def update_package(self):
        self.ckan.action.package_update(
	    name = self.package['name'].lower(),
	    title = self.package['title'],
	    owner_org = self.package['owner_org'],
	    notes = self.package['notes'],
	    type = self.package['type'],
	    last_modified = self.package['last_modified'],
	    #license_id = self.package['license_id'],
	    author = self.package['author'],
	    author_email = self.package['author_email'],
	    tags = self.package['tag'],
	    extras = self.package['extras']
        )

	return

    def commit(self, data):
	self.package = data
	if self.check_organization() == False:
	    print "add organization"
	    self.add_organization()
	else:
	    print "update organization"
	    self.update_organization()
	
	if self.check_package() == True:
	    print "update package"
	    self.update_package()
	    self.add_resource()
	else:
	    print "add package and resource"
	    self.add_package()
	    self.add_resource()
	return

if __name__ == '__main__': 
    jsonfile = 'testdata/data.txt'
    odtw = odtw.od()
    data = odtw.read(jsonfile)

    ckmap = map2ckan.mapod2ckan()
    package = ckmap.map(data)
    od_data_path = os.path.dirname(os.path.realpath(jsonfile))
    package['basepath'] = od_data_path
    put2ckan = import2ckan()
    res = put2ckan.commit(package)

