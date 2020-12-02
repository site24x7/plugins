#!/usr/bin/python

'''
Created on 18-Nov-2020

This Plugin is to monitor server file checks

metrics monitored are

1. size                       : size of the file in KB
2. read access enabled        : read_access
3. write access enabled       : write_access
4. execution access enabled   : execution_access
5. last_access_time           : last file accessed time
6. last file modified time    : last file modified time
7. hours before the file was accessed last    : time_since_last_accessed
8. hours before the file was modified last    : time_since_last_modified

@author: anita-1372

'''

import os.path
import time
import json
import argparse
import datetime
import mmap

parser = argparse.ArgumentParser()
parser.add_argument('--file', help='file to be monitored', nargs='?', default = __file__)
parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=1)
parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=True)
args = parser.parse_args() 


file = args.file 
heartbeat = args.heartbeat
version = args.plugin_version

now = time.time()
date_format = "%a %b %d %H:%M:%S %Y"
data = {}
data['units'] = {}

data['heartbeat_required'] = heartbeat
data['plugin_version'] = version

### Size Check: When the specified file's size exceeds the given threshold
data['size'] = os.path.getsize(file) 
data['units']['size'] = 'kb'
 
### Access Check: When the configured file is accessed
access_time = time.ctime(os.path.getatime(file))
data['last_access_time'] =  access_time

last_access_time = time.mktime(datetime.datetime.strptime(access_time, date_format).timetuple())
accessed_minute_diff = int((now - last_access_time) / 60 / 60)
data['time_since_last_accessed'] = accessed_minute_diff
data['units']['last_accessed'] = 'hours'


### Last Modified Check: When there is a change in the file status
modified_time = time.ctime(os.path.getmtime(file))
data['last_modified_time'] = modified_time  

last_modified_time = time.mktime(datetime.datetime.strptime(modified_time, date_format).timetuple())
modified_minute_diff = int((now - last_modified_time)/ 60 / 60)
data['time_since_last_modified'] = modified_minute_diff
data['units']['last_modified'] = 'hours'


### Permission checks
data['read_access'] = 1 if os.access(file, os.R_OK) else 0# Check for read access
data['write_access'] = 1 if os.access(file, os.W_OK) else 0# Check for read access
data['execution_access'] = 1 if os.access(file, os.X_OK) else 0# Check for read access


### Content checks
if search_text is not None :
	f = open(file, 'r')
	s = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
	if s.find(search_text) != -1: data['content_match'] = "True"
	else : data['content_match'] = "False"
else :
	data['content_match'] = "no search key"

 
# Print the data for monitoring
print(json.dumps(data, indent=2, sort_keys=True))

