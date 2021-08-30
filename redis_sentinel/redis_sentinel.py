#!/usr/bin/python
import json
import subprocess

PLUGIN_VERSION=1
HEARTBEAT="true"

port=""
master_name=""

metric_units={"sentinel_masters":"count","sentinel_running_scripts":"count","sentinel_scripts_queue_length":"count","link_pending_commands":"count","num_slaves":"count","num_other_sentinels":"count","role_reported_time":"ms"}

required_metrics={"sentinel_masters":"int","sentinel_running_scripts":"int","sentinel_scripts_queue_length":"int","sentinel_simulate_failure_flags":"int","link_pending_commands":"int","last_ping_sent":"int","last_ok_ping_reply":"int","last_ping_reply":"int","role_reported_time":"int","num_slaves":"int","num_other_sentinels":"int","quorum":"int"}

def get_data():
	try:
		result={}
		result['plugin_version']=PLUGIN_VERSION
		result['heartbeat_required']=HEARTBEAT
		result['units']=metric_units
		
		command="redis-cli -p "+port+" info Sentinel"
		p=subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
		(connect, err) = p.communicate()
		p_status = p.wait()
		
		collected_metrics=connect.decode("utf-8")
		collected_metrics=collected_metrics.split()
		
		for metric in collected_metrics:
			for req in required_metrics:
				if req in metric:
					value=metric.split(':')[1]
					if required_metrics[req]=='int':
						value=int(value)
					result[req]=value
					
		master_command="redis-cli -p "+port+" sentinel master "+master_name
		p=subprocess.Popen(master_command, stdout=subprocess.PIPE, shell=True)
		(connect, err) = p.communicate()
		p_status = p.wait()
		
		collected_metrics = connect.decode("utf-8")
		collected_metrics = collected_metrics.split()
		
		for metric in collected_metrics:
			if '-' in metric:
				fetch_name=metric.replace('-',"_")
			else:
				fetch_name=metric
			if fetch_name in required_metrics:
				index=collected_metrics.index(metric)
				value=collected_metrics[index+1]
				if required_metrics[fetch_name]=='int':
					value=int(value)
				result[fetch_name]=value
				
	except Exception as e:
		result['status']=0
		result['msg']=str(e)
		
	return result
		

if __name__=='__main__':
	import argparse
	parser=argparse.ArgumentParser()
	parser.add_argument('--port',help="Port for Sentinel",type=str)
	parser.add_argument('--master',help="Master Name in Sentinel",type=str)
	
	args=parser.parse_args()
	
	if args.port:
		port=args.port
	if args.master:
		master_name=args.master
	
	data=get_data()
	
	print(json.dumps(data,indent=4))
