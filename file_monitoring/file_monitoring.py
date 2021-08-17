#!/usr/bin/python

'''
Created on 18-Nov-2020

This Plugin is to monitor server file checks

metrics monitored are 

1. file_size                              ->      Size of the File in kb
2. file_index                             ->      Inode Number of the File 
3. file_owner_id                          ->      User Identifier of the File
4. hash_value_changed                     ->      Boolean value that returns 1 when the hash value of the file changes else 0
5. content_match                          ->      If search_text value is None, it will skip content searching, else will return True if there is a match and false if there is no match
6. content_occurrence_count               ->      Count of number of times the content occurred
7. read_access                            ->      Read Access Enabled
8. write_access                           ->      Write Access Enabled
9. execution_access                       ->      Execution Access Enabled
10.last_access_time                       ->      Last File Accessed Time
11.last_modified_time                     ->      Last File Modified Time
12.time_since_last_accessed               ->      hours before the file was accessed
13.time_since_last_modified               ->      hours before the file was modified
  
  @author: anita-1372
  
  '''
import json
import os
import hashlib
import time
import datetime

plugin_version="1"
heartbeat="true"

file_name = ""
hash_type="md5"
search_text=""
case_sensitive="False"

metric_units={"file_size":"kb","time_since_last_accessed":"hours","time_since_last_modified":"hours"}

def get_hash_value_changed():
	previous_hash_value=""
	hash_storage_path="./hash_value_storage_unit_file_monitoring.txt"
	hash_value_changed=0
	if hash_type=="md5":
		hashing=hashlib.md5(open(file_name,'rb').read()).hexdigest()
	elif hash_type=="sha256":
		hashing=hashlib.sha256(open(file_name,'rb').read()).hexdigest()
	else:
		raise Exception("hash_type is not valid")
	if(os.path.exists(hash_storage_path)):
		file_object = open(hash_storage_path)
		previous_hash_reference = file_object.readlines()
		previous_hash_value = ""
		line_number = -1
		for i in previous_hash_reference:
			name,value = i.split(":")
			name = name.strip()
			if name==file_name:
				previous_hash_value = value.strip()
				line_number = previous_hash_reference.index(i)
		file_object.close()
	if(previous_hash_value != "" and previous_hash_value != hashing.strip()):
		hash_value_changed = 1
	if(previous_hash_value == ""):
		file_object = open(hash_storage_path,'a+')
		file_object.write(file_name+":"+hashing)
		file_object.write("\n")
		file_object.close()
	if previous_hash_value != "" and previous_hash_value != hashing.strip():
		file_object = open(hash_storage_path,'w')
		previous_hash_reference[line_number]=file_name+":"+hashing
		file_object.writelines(previous_hash_reference)
		file_object.write('\n')
		file_object.close()
	return hash_value_changed
	
	

def get_data():
    data={}
    data['plugin_version']=plugin_version
    data['heartbeat_required']=heartbeat
    data['units']=metric_units
    try:
    	if (file_name==""):
    		raise Exception("File not given")
    	
    	
    	#Size Check: When the specified file's size exceeds the given threshold
    	data["file_size"]=os.path.getsize(file_name)
    	
    	#Hash Value Changed Check: Checks whether the hash value of the file is changed or not.
    	hash_value_changed = get_hash_value_changed()
    	data["hash_value_changed"]=hash_value_changed
    	
    	
    	now=time.time()
    	date_format="%a %b %d %H:%M:%S %Y"
    	
    	#File Index Check: When there is a change in the file index.
    	data["file_index"]=os.stat(file_name).st_ino
    		
    	data["file_owner_id"]=os.stat(file_name).st_uid
    	
    	#Access Check: When the configured file is accessed
    	access_time=time.ctime(os.path.getatime(file_name))
    	data["last_access_time"]=access_time
    	
    	last_access_time=time.mktime(datetime.datetime.strptime(access_time,date_format).timetuple())
    	accessed_minute_difference=int((now-last_access_time)/3600)
    	data["time_since_last_accessed"]=accessed_minute_difference
    	
    	#Last Modified Check: When there is a change in the file status
    	modified_time=time.ctime(os.path.getmtime(file_name))
    	data['last_modified_time']=modified_time
    	
    	last_modified_time=time.mktime(datetime.datetime.strptime(modified_time,date_format).timetuple())
    	modified_minute_difference=int((now-last_modified_time)/3600)
    	data["time_since_last_modified"]=modified_minute_difference
    	
    	#Permission Checks
    	data["read_access"]=1 if os.access(file_name,os.R_OK) else 0
    	data["write_access"]=1 if os.access(file_name,os.W_OK) else 0
    	data["execution_access"]=1 if os.access(file_name,os.X_OK) else 0
    	
    	#Content Checks
    	if search_text!="" and search_text is not None:
    		data["content_match"]="False"
    		file_object=open(file_name,"r")
    		file_contents=file_object.readlines()
    		content_count=0
    		if case_sensitive=="False":
    			for i in file_contents:
    				content=i.lower()
    				content=content.replace('\n',"")
    				content=content.split(" ")
    				for j in content:
    					if search_text.lower() in j:
    						data["content_match"]="True"
    						content_count+=1
    		else:
    			for i in file_contents:
    				content=i.replace('\n',"")
    				content=content.split(" ")
    				for j in content:
    					if search_text in j:
    						data["content_match"]="True"
    						content_count+=1
    		file_object.close()
    		data["content_occurance_count"]=content_count
    	else:
    		data["content_match"]="no Search Key"
    		data["content_occurance_count"]=0
    		
    	
    except Exception as e:
    	data["msg"]=str(e)
    	data["status"]=0
    return data
if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--filename',help="file to monitor",type=str,nargs='?')
    parser.add_argument('--hashtype',help="type of the hash",type=str,default="md5")
    parser.add_argument('--search_text',help="Text to check whether the content is present",type=str,default="")
    parser.add_argument('--case_sensitive',help="Give True When Searching Content needs to be case sensitive",type=str,default="False")
    parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=1)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=True)
    args=parser.parse_args()
    
    if args.filename:
    	file_name=args.filename
    if args.hashtype:
    	hash_type=args.hashtype
    if args.search_text:
    	search_text=args.search_text
    if args.case_sensitive:
    	case_sensitive=args.case_sensitive
    if args.plugin_version:
    	plugin_version=args.plugin_version
    if args.heartbeat:
    	heartbeat=args.heartbeat
    hash_type=hash_type.lower()

    data=get_data()
    print(json.dumps(data,indent=4))

