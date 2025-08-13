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
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True, stderr=subprocess.PIPE)
		(output, err) = p.communicate()
		p_status = p.wait()
		error=err.decode('utf-8')
		if p_status != 0:
			raise Exception("Command failed with exit code {}: {}".format(p_status,error))
		
		data['mailq_count'] = int(output)
		
		qshape_metrics={"deferred":"deferred_count","active":"active_count","hold":"hold_count","incoming":"incoming_count","bounce":"bounce_count","corrupt":"corrupt_count"}
		
		for i in qshape_metrics:
			cmd='qshape '+i+' | head'
			p=subprocess.Popen(cmd,stdout=subprocess.PIPE,shell=True, stderr=subprocess.PIPE)
			(output,err)=p.communicate()
			p_status=p.wait()
			error=err.decode('utf-8')
			if p_status != 0:
				raise Exception("Command failed with exit code {}: {}".format(p_status,error))
			
			if not error:
				output_original=output.strip().decode("utf-8")
				output=output_original.split()
				if 'TOTAL' in output:
					index = output.index('TOTAL') + 1
					data[qshape_metrics[i]] = int(output[index])
				else:
					data["status"]=0
					data["msg"]="qshape command output does not contain TOTAL"+output_original
			else:
				data["status"]=0
				data["msg"]=error
			
	except Exception as e:
		data["status"]=0
		if output:
			data["msg"]=str(e)+output.decode("utf-8")
		else:
			data["msg"]=str(e)
	return data
     
    
if __name__ == '__main__':
	data=get_data()
	print(json.dumps(data, indent=2, sort_keys=False))
