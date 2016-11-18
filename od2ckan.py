#!/bin/python
# -*- coding: utf-8 -*-
import odtw
import map2ckan
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
	pkgs = self.ckan.action.package_autocomplete(q=self.package['name']) 
	for pkg in pkgs: 
	    if self.package['name'] == pkg['name']:
		print "package exist %s %s" % (pkg['name'], pkg['title'])
		return True
	return False

    def check_resource(self, testresid):
	package_resources = self.ckan.action.package_show(id=self.package['name'])
	for res in package_resources['resources']:
	    print "test resname %s" % res['name']
	    if res['name'] == testresid:
		return True
	return False

    def check_organization(self):
	org = self.ckan.action.organization_list(organizations=[self.package['owner_org']])
	if org == '':
	    return False
	return True

    def check_tag(self):
	return

    def add_package(self):
        self.ckan.action.package_create(
	    name = self.package['name'],
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
	    rfile = res['resourceid']+'.'+res['format']
	    if self.check_resource(res['resourceid']) == True:
		print "res exist %s" % res['resourceid']
	    else:
	        ckan.action.resource_create(
	            package_id=self.package['name'],
	            url=res['resourceid'],
	            description=res['resourcedescription'],
	            format=res['format'],
	            name=res['resourceid'],
	            last_modified=res['resourcemodified'],
		    upload=open(rfile, 'rb')
	        #    revision_id=resourceID,
	        #    hash='',
	        #    resource_type='',
	        #    mimetype='',
	        #    mimetype_inner='',
	        #    cache_url='',
	        #    size='',
	        #    created='',
	        #    cache_last_updated='',
	        )
	return

    def add_organization(self):
	self.ckan.action.organization_create(name=self.package['owner_org'])
	return

    def add_tag(self):
	return

    def upload(self, data):
	self.package = data
	if self.check_organization() == False:
	    self.add_organization()
	
	if self.check_package() == True:
	    #update later
	    self.add_resource()
	else:
	    self.add_package()
	    self.add_resource()
	return

if __name__ == '__main__': 
    jsonfile = 'data.txt'
    odtw = odtw.od()
    data = odtw.read(jsonfile)

    ckmap = map2ckan.mapod2ckan()
    package = ckmap.map(data)
    print package
    put2ckan = import2ckan()
    res = put2ckan.upload(package)

