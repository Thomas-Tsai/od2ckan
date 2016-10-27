#!/bin/python
# -*- coding: utf-8 -*-
import odtw
import map2ckan
import os
import logging
import psycopg2
import time
from datetime import datetime

LOGGING_FILE = 'ipgod-od2ckan.log'
logging.basicConfig(filename=LOGGING_FILE,
                    level=logging.INFO,
                    format='%(asctime)s [%(levelname)s] %(filename)s_%(lineno)d  : %(message)s')
logger = logging.getLogger('root') 

class ipgoddb():
    def __init__(self)
        try:
            self.conn = psycopg2.connect("dbname='ipgod' user='thomas' host='localhost' password='okok7480'")
            self.cur = conn.cursor()
        except:
            print "connect db error"

    def get_pkgs(self):
        try:
            self.cur.execute("SELECT package_name, status, datetime from import where  datetime > CURRENT_TIMESTAMP - INTERVAL '60 secs' and status == 0")
            rows = self.cur.fetchall()
        except:
            print "select error"
        pkgs = []
        for row in rows:
                pkgs.append(row['package_name'])
        return pkgs

    def update_pkg(self, package, status):
        try:
            self.cur.execute("UPDATE import SET status = %s where package_name = %s", (statue, package))
            self.conn.commit()
        except:
            print "update error"

    def log_package(self, package, log):
        try:
            self.cur.execute("UPDATE import SET comment = %s where package_name = %s", (log, package))
            self.conn.commit()
        except:
            print "log comment error"

    def remove_pkg(self):
        try:
            self.cur.execute("DELETE from import  where package_name = %s", package)
            self.conn.commit()
        except:
            print "remove error"

if __name__ == '__main__':
    idb = ipgoddb()
    while True:
        pkgs = idb.get_pkgs()
        for pkg in pkgs:

            jsonfile = pkg['package_name']
            odtw = odtw.od()
            data = odtw.read(jsonfile)

            ckmap = map2ckan.mapod2ckan()
            package = ckmap.map(data) 
            od_data_path = os.path.dirname(os.path.realpath(jsonfile))
            package['basepath'] = od_data_path
            put2ckan = import2ckan()
            res = put2ckan.commit(package)
            if res == True:
                idb.update_pkg(pkg, res)
                idb.remove_pkg(pkg)
            else:
                idb.update_pkg(pkg, res)
                idb.log_package(pkg, error_log)
    time.sleep(10)

