#!/usr/bin/python3
import requests,json,subprocess,os
import multiprocessing,argparse,psutil

PLUGIN_VERSION = "1"
HEARTBEAT="true"

data={}
METRIC_UNITS ={}
cores=multiprocessing.cpu_count()
dcpu={}
dmem={}

def fetchDatafromURL(url,username,app_password):

	try:
		response = requests.get(url, auth=(username,app_password))
		rtext=response.text
		ltext=rtext.split("[{",1)[-1]
		ltext="[{"+ltext
		rjson=json.loads(ltext)
		Plugin_list={}
		for i in rjson:
	   		Plugin_list[i["name"]]=i["status"]
	   		'''if i["status"] == "active":
	       			Plugin_list[i["name"]+" Status"]=1
	   		else:
	       			Plugin_list[i["name"]+" Status"]=0
	   		'''
		data.update(Plugin_list)
	except Exception as e:
	   	data['status'] = 0
	   	data['msg'] = str(response)
	
def metricCollector():
	
	output=subprocess.check_output("ls /var/www/html/wp-content/plugins",shell=True).decode()
	folders=output.split("\n")
	folders.remove("hello.php")
	folders.remove("index.php")
	try:
	    while True:
	        folders.remove('')
	except ValueError:
	    	pass
	#print(folders)
	
	for i in folders:
 	  try:
	     output = subprocess.check_output("sudo lsof +D /var/www/html/wp-content/plugins/"+i+" 2> /dev/null | awk {'print$2'}", shell=True)
	     out=output.decode()
	     #print(out)
	     
	     out=out.replace("PID","")
	     out=out.split("\n")
	     try:
	         while True:
	           out.remove('')
	     except ValueError:
	         pass
	     out=set(out)
	     data[i+" Process Count"]=len(out)
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
	     dcpu[i+" CPU Usage"]= cpu
	     dmem[i+" Memory Usage"]= mem/1048576
 	  except Exception as e:
	      print(e)
	      dcpu[i+" CPU Usage"]= 0
	      dmem[i+" Memory Usage"]= 0
	      #data[i+" Exception"]=str(e)
 	  METRIC_UNITS[i+" CPU Usage"]="%"
 	  METRIC_UNITS[i+" Memory Usage"]="MB"
 	  
      
if __name__ == "__main__":
  parser=argparse.ArgumentParser()
  parser.add_argument('--url',help="REST api url")
  parser.add_argument('--username',help="Wordpress Username")
  parser.add_argument('--app_password',help="Application Password for Authentication")
  args=parser.parse_args()
  fetchDatafromURL(args.url,args.username,args.app_password)
  metricCollector()
  data.update(dcpu)
  data.update(dmem)
  data['plugin_version'] = PLUGIN_VERSION
  data['heartbeat_required']=HEARTBEAT
  data['units'] = METRIC_UNITS
  #print(METRIC_UNITS)
  print(json.dumps(data, indent=4, sort_keys=True))
