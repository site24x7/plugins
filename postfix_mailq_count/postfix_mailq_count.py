#!/usr/bin/python

import subprocess
import json

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

def get_data():
	data = {}
	data["plugin_version"]=PLUGIN_VERSION
	data['heartbeat_required']=HEARTBEAT
	try:
		cmd = 'mailq | grep -c "^[A-F0-9]"'
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		p_status = p.wait()
		
		data['mailq_count'] = int(output)
		
		qshape_metrics={"deferred":"deferred_count","active":"active_count","hold":"hold_count","incoming":"incoming_count","bounce":"bounce_count","corrupt":"corrupt_count"}
		
		for i in qshape_metrics:
			cmd='qshape '+i+' | head'
			p=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True)
			(output,err)=p.communicate()
			p_status=p.wait()
			if err==None:
				output=output.strip().decode("utf-8")
				output=output.split()
				index=output.index('TOTAL')+1
				data[qshape_metrics[i]]=int(output[index])
			
	except Exception as e:
		data["status"]=0
		data["msg"]=str(e)
	return data
     
    
if __name__ == '__main__':
	data=get_data()
	print(json.dumps(data, indent=2, sort_keys=False))
