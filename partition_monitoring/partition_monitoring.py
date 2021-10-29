#!/usr/bin/python

import subprocess
import json

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

mount_name = ""

def get_data():
	data = {}
	data["plugin_version"]=PLUGIN_VERSION
	data['heartbeat_required']=HEARTBEAT
	try:
		cmd = 'df'
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		p_status = p.wait()
		final_output = output.decode('utf-8')
		
		final_output_list = final_output.split('\n')
		l=[]
		
		for i in final_output_list:
			val = i.split()
			l.append(val)
		
		disk_found = False
		for i in l:
			if len(i)!=0 and i[-1]==mount_name:
				data["file_system"]=i[0]
				data["size"]=i[1]
				data["used_size"]=i[2]
				data["available_size"]=i[3]
				data["used_percentage"]=float(i[4].replace('%',''))
				data["mounted_on"]=i[5]
				data["units"]={"size":"KB","used_size":"KB","available_size":"KB","used_percentage":"%"}
				disk_found = True
				
		if disk_found == False:
			data["status"]=0
			data["msg"]="Disk Partition not found"
			
	except Exception as e:
		data["status"]=0
		data["msg"]=str(e)
	return data
     
    
if __name__ == '__main__':
	import argparse
	parser=argparse.ArgumentParser()
	parser.add_argument('--mount_name',help="Mount name in which the disk is mounted on",type=str)
	args=parser.parse_args()
	
	if args.mount_name:
		mount_name=args.mount_name
	data=get_data()
	print(json.dumps(data, indent=2, sort_keys=False))
