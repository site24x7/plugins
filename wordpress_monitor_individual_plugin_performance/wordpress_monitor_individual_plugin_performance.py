#!/usr/bin/python3
import requests,json,subprocess,os
import multiprocessing,argparse,psutil

PLUGIN_VERSION = "1"
HEARTBEAT="true"
data={}
cores=multiprocessing.cpu_count()


def datacollector(url,username,app_password,plugin_name):

	try:
		response = requests.get(url, auth=(username,app_password))
		rtext=response.text
		ltext=rtext.split("[{",1)[-1]
		ltext="[{"+ltext
		rjson=json.loads(ltext)
	
		for i in rjson:
	   		if plugin_name==i["name"]:
	   			data[i["name"]]=i["status"]
	   			if i["status"] == "active":
	       				data[i["name"]+" Status"]=1
	   			else:
	       				data[i["name"]+" Status"]=0
	except Exception as e:
		data['status']=0
		data['msg']=str(response)
	   
	
def metricCollector(plugin_folder):
	
	try:
	     output = subprocess.check_output("sudo lsof +D "+plugin_folder[1]+" 2> /dev/null | awk {'print$2'}", shell=True)
	     out=output.decode()
	     #print("----",out,"----")
	     
	     out=out.replace("PID","")
	     out=out.split("\n")
	     try:
	         while True:
	           out.remove('')
	     except ValueError:
	         pass
	     out=set(out)
	     data[plugin_folder[0]+" Process Count"]=len(out)
	     cpu=0
	     mem=0
	     if len(out)!=0:
	     	for i1 in out:
	        	#print(i1)
	        	process = psutil.Process(int(i1))
	        	cpu += float(process.cpu_percent(interval=1))
	        	memory_info = process.memory_info()
	        	mem += int(memory_info.rss)
	        	#print(cpu,mem)
	        
	     cpu=round(cpu/cores,2)
	     mem=round(mem,2)
	     data[plugin_folder[0]+" CPU Usage"]= cpu
	     data[plugin_folder[0]+" Memory Usage"]= mem/1048576
	except Exception as e:
	      #print(e)
	      data[plugin_folder[0]+" CPU Usage"]= 0
	      data[plugin_folder[0]+" Memory Usage"]= 0
	      #data[i+" Exception"]=str(e)
 	  
      
if __name__ == "__main__":
  parser=argparse.ArgumentParser()
  parser.add_argument('--url',help="REST api url")
  parser.add_argument('--username',help="Wordpress Username")
  parser.add_argument('--app_password',help="Application Password for Authentication")
  parser.add_argument('--plugin_path',help="Exact name of the plugin,Path of the plugin you want to monitor")
  args=parser.parse_args()
  plugin=args.plugin_path.split(",")
  if os.path.isdir(plugin[1]):
  	datacollector(args.url,args.username,args.app_password,plugin[0])
  	metricCollector(plugin)
  else:
  	data['status']=0
  	data['msg']='Plugin Folder not found, Check the path of the folder'

  data['plugin_version'] = PLUGIN_VERSION
  data['heartbeat_required']=HEARTBEAT
  METRIC_UNITS ={plugin[0]+" CPU Usage":"%",plugin[0]+" Memory Usage":"MB"}
  data['units'] = METRIC_UNITS
  #print(METRIC_UNITS)
  print(json.dumps(data, indent=4, sort_keys=True))
