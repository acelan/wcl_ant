#!/usr/bin/python

import os
import datetime
import shutil
#import cloudscraper
import requests
import json
import time
import re
import pickle
#from requests_toolbelt import MultipartEncoder
from os                                 import path
from subprocess                         import getoutput, getstatusoutput

WCLRanks_path = "../WCLRanks"
WCLRanks_toc = "WCLRanks.toc"
toc = open("%s/%s" % (WCLRanks_path, WCLRanks_toc), "w+")

date_version = datetime.date.today().strftime("%Y%m%d")
version = ""

with open(WCLRanks_toc) as fp:
    line = fp.readline()
    while line:
        if line != line.replace("__DATE__", date_version):
            version = line.replace("__DATE__", date_version)
        line = line.replace("__DATE__", date_version)
        toc.write(line)
        line = fp.readline()
toc.close()

# copy data
getoutput("cp -a Data %s/" % WCLRanks_path)

# ## Version: 1.0.20211009
version = version.replace("## Version: ","")
version = re.sub("[^0-9.]", "", version)

commit_msg = ""
for server_id in [d for d in os.listdir('server') if os.path.isdir(os.path.join('server', d))]:
	added = getoutput("cd %s; git diff Data/%s.lua | grep -- + | grep -v @@ | wc -l" % (WCLRanks_path, server_id))
	deleted = getoutput("cd %s; git diff Data/%s.lua | grep -- - | grep -v @@ | grep -v \"diff --git\" | wc -l" % (WCLRanks_path, server_id))
	server_name = pickle.load(open('server/%s/name.pkl' % server_id, 'rb'))
	commit_msg = commit_msg + "%s:\n\tupdated: %s\n\tnew: %s\n" % (server_name, int(deleted), int(added) - int(deleted))
ret = getoutput("cd %s; git commit -a -s -m \"daily update: %s\n\n%s\"" % (WCLRanks_path, date_version, commit_msg))
print(ret)
ret = getoutput("cd %s; git tag WCLRanks-%s" % (WCLRanks_path, version))
print(ret)
ret = getoutput("cd %s ; git push origin main" % WCLRanks_path)
ret = getoutput("cd %s ; git push origin WCLRanks-%s" % (WCLRanks_path, version))
print(ret)

