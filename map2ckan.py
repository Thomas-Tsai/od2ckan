#!/bin/python
# -*- coding: utf-8 -*-
import organization_map

class mapod2ckan():
    def __init__(self):
	self.package={'extras':[], 'tag':[], 'resources':[], 'org':{'extras':[]}}
	self.license_id='1'
	self.license_url='http'

    def map_package_params(self, key, value):
	self.package[key] = value

    def map_tag_params(self, key, value):
	for keyword in value:
	    testkeyword = keyword.encode('utf-8')
	    if testkeyword.isalpha() == True:
		testkeyword = testkeyword.lower()
		testkeyword = testkeyword.replace(" ", "_")
		tagdata={'name':testkeyword.lower()}
		self.package['tag'].append(tagdata)
	    #else:
		#map_package_extras(k, v)

    def map_organization_params(self, key, value):
	if key == 'organization':
	    org = organization_map.organization_name()
	    owner_org = org.search(value.encode('utf8'))
	    self.package['owner_org'] = owner_org
	    self.package['org']['name'] = owner_org
	    self.package['org']['title'] = value.encode('utf-8')
	else:
	    org_extra={}
	    org_extra['key'] = key.encode('utf-8')
	    org_extra['value'] = value.encode('utf-8')
	    self.package['org']['extras'].append(org_extra)
	

    def map_package_extras(self, key, value):
        if key == 'notes':
	   key="extra note"
        if type(value) is int:
	   data=value
        else:
	    data = value.encode('utf-8')
	    extra={}
	    extra['key']=key.encode('utf-8')
	    extra['value']=data
	    self.package['extras'].append(extra)
    
    def map_resources_params(self, key, value):
        for data in value:
	    resource={'resourceid':'', 'resourcedescription':'', 'format':'', 'resourcemodified':'', 'extras':{}}
	    for rk, rv in data.items():
		if rk == 'resourceID':
		    resource['resourceid'] = rv
		elif rk == 'resourceDescription':
		    resource['resourcedescription'] = rv
		elif rk == 'format':
		    resource['format'] = rv
		elif rk == 'resourceModified':
		    resource['resourcemodified'] = rv
		else:
		    resource['extras'][rk] = rv
	    self.package['resources'].append(resource)

    def map(self, data):
	rs = data
	for k,v in rs.items():
	    if k == 'title':
		self.map_package_params('title', v)
	    elif k == 'identifier':
		self.map_package_params('name', v)
	    elif k == 'description':
		self.map_package_params('notes', v)
	    elif k == 'type':
		self.map_package_params('type', v)
	    elif k == 'publisher':
		self.map_package_params('owner_org', v)
	    elif k == 'modified':
		self.map_package_params('last_modified', v)
	    elif k == 'license':
		self.map_package_params('license_id', self.license_id)
	    elif k == 'license_URL':
		self.map_package_params('license_url', self.license_url)
	    elif k == 'organization':
		self.map_organization_params(k, v)
	    elif k == 'organizationContactName':
		self.map_organization_params(k, v)
	    elif k == 'organizationContactPhone':
		self.map_organization_params(k, v)
	    elif k == 'organizationContactEmail':
		self.map_organization_params(k, v)
	    elif k == 'contactName':
		self.map_package_params('author', v)
	    elif k == 'publisherContactName':
		self.map_package_params('author', v)
	    elif k == 'contactEmail':
		self.map_package_params('author_email', v)
	    elif k == 'publisherContactEmail':
		self.map_package_params('author_email', v)
	    elif k == 'landingPage':
		self.map_organization_params(k, v)
	    elif k == 'keyword':
		self.map_tag_params(k, v)
	    elif k == 'distribution':
		self.map_resources_params(k, v)
	    elif k == 'Comments':
		continue
	    else:
		self.map_package_extras(k, v)
	return self.package
