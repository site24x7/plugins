#!/usr/bin/python3


# Other Modules
import json, os,sys
import time


# URL Modules
from urllib.error import URLError, HTTPError
from http.client import InvalidURL
import requests
from requests.auth import HTTPBasicAuth 



PLUGIN_VERSION = "1"
HEARTBEAT =True
METRICS_UNITS = { 'JVM garbage collector old generation time':'ms',
                  'Average JVM memory usage in garbage collector(%)' : '%',
                  'CPU used (%)':'%',
                  'OS memory used(%)':'%', 
                  'OS memory free(%)':'%',
                  'JVM heap memory used (%)':'%',
                  'Time spent on fetches':'ms',
                  "Time spent on queries":'ms',
                  "Total time on GET requests where the document was missing":'ms',
                  "JVM heap memory committed":'KB'

                }


# Credentials
HOST='localhost'
PORT='9200'
USERNAME = None
PASSWORD = None
NODE = None # Name of the node
os.environ['NO_PROXY'] = 'localhost'
CAFILE= '/opt/cert/certs/ca/ca.crt' # Add the crt file which was used in your elasticsearch

counterFilePath = '/opt/site24x7/monagent/plugins/elasticsearch_monitoring/counter.json'


custom_metrics=["Status of the node", "Node Availability"]

standard_metrics=[

    'disk_reads',
    'disk_writes',
    'query_time_in_millis',
    'query_total',
    'fetch_time',
    'jvm_gc_old_coll_count',
    'jvm_gc_old_coll_time',
    'jvm_mem_pool_old_used_perc'
]

standard_metrics2={

    "Queries hit count":("indices","query_cache","hit_count"),
    "Query cache memory size":("indices","query_cache","memory_size_in_bytes"),
    "Query cache miss count":("indices","query_cache","miss_count"),
    "Request cache hit count":("indices","request_cache","hit_count"),
    "Number of evictions":("indices","request_cache","evictions"), #Done
    "Request cache memory size":("indices","request_cache","memory_size_in_bytes")

}


os_metrics={
    "CPU used (%)":("os","cpu","percent"),
    "OS memory free(%)":("os","mem","free_percent"),
    "OS memory used(%)":("os","mem","used_percent")
}


search_performance_metrics={

    "Total queries":("indices","search","query_total"),
    "Time spent on queries":("indices","search","query_time_in_millis"),
    "Queries in progress":("indices","search","query_current"),
    "Number of fetches":("indices","search","fetch_total"),
    "Time spent on fetches":("indices","search","fetch_time_in_millis"),
    "Fetches in progress":("indices","search","fetch_current"),

}


index_performance_metrics={

    "Documents indexed":('indices','indexing','index_total'),
    "Time of indexing documents":('indices','indexing','index_time_in_millis'),
    "Documents currently indexed":("indices","indexing","index_current"),
    "Index refreshes":("indices","refresh","total"),
    "Time spent on refreshing indices":("indices","refresh","total_time_in_millis"),
    "Index flushes to disk":("indices","flush","total"),
    "Time spent on flushing indices to disk":("indices","flush","total_time_in_millis"),
    "Indices docs count":("indices","docs","count"),
    "Indices docs deleted":("indices","docs","deleted"),

}

http_connection_metrics={

    "HTTP connections currently open":("http","current_open"),
    "HTTP connections opened over time":("http","total_opened")
}

cluster_health_node_availability_metrics={
    "Cluster Name":("cluster_name"),
    "Cluster status":("status"),
    "Number of Nodes":("number_of_nodes"),
    "Number of data nodes":("number_of_data_nodes"),
    "Initializing shards":("initializing_shards"),
    "Unassigned shards":("unassigned_shards"),
    "Active primary shards":("active_primary_shards"),
    "Relocating shards":("relocating_shards"),
    "Delayed unassigned shards":('delayed_unassigned_shards')
    
}


unsuccessful_get_metrics={
    "Number of GET requests where the document was missing":("indices","get","missing_total"),
    "Total time on GET requests where the document was missing":("indices","get","missing_time_in_millis")
}



jvm_metrics={

    "JVM heap memory used (%)":("jvm","mem","heap_used_percent"),
    "JVM heap memory committed":("jvm","mem","heap_committed_in_bytes")
}



class ElasticSearch():


    def __init__(self,username,password,host,port,nodename,ssl,logs_enabled,log_type_name,log_file_path):

        # Credentials to login
        self.Maindata={}
        self.username=username
        self.password=password
        self.host=host
        self.port=port
        self.nodename=nodename
        self.dictCounterValues = {}
        self.loadCounterValues()
        self._url= "http://"+self.host+":"+self.port
        self.ssl=ssl
        self.logsenabled=logs_enabled
        self.logtypename=log_type_name
        self.logfilepath=log_file_path

        applog={}
        
        if(self.logsenabled in ['True', 'true', '1']):
            applog["logs_enabled"]=True
            applog["log_type_name"]=self.logtypename
            applog["log_file_path"]=self.logfilepath
        else:
            applog["logs_enabled"]=False
            
        self.Maindata['applog'] = applog




    def loadCounterValues(self):
        file_obj = None
        if not os.path.exists(counterFilePath):
            file_obj = open(counterFilePath,'w')
            file_obj.close()
        else:
            file_obj = open(counterFilePath,'r')
            str_counterValues = file_obj.read()
            if str_counterValues:
                self.dictCounterValues = json.loads(str_counterValues)
            file_obj.close()


            
    def updateCounterValues(self,dict_valuesToUpdate):
        if os.path.exists(counterFilePath):
            file_obj = open(counterFilePath,'w')
            file_obj.write(json.dumps(dict_valuesToUpdate))
            file_obj.close()
    





    # Opening the url and parsing the data
    def _openURL2(self,str_URLsuffix):
        ssl_choice=None

        if self.ssl=="NO":
            ssl_choice=False
            return self.urlhttp(str_URLsuffix,ssl_choice)
        
        if self.ssl=="YES":
            ssl_choice=True
            return self.urlhttp(str_URLsuffix,ssl_choice)

        
                



    def urlhttp(self,str_URLsuffix,ssl_choice):

        str_responseData = None
        url = None
        try:
            if ssl_choice:
                url = 'https://'+self.host+':'+self.port + str_URLsuffix
            if not ssl_choice:
                url = 'http://'+self.host+':'+self.port + str_URLsuffix


            response = requests.get(url = url,  auth = HTTPBasicAuth(USERNAME,  PASSWORD), verify=CAFILE) 

            if response.status_code == 200 :
                byte_responseData = response.content
                str_responseData = byte_responseData.decode('UTF-8')
            else:
               
                self.dictEsPluginData['status'] = '0'
                self.dictEsPluginData['msg'] = 'Invalid response after opening URL : ' + str(response.status_code) 
            
        except HTTPError as e:
            self.dictEsPluginData['status'] = '0'
            self.dictEsPluginData['msg'] ='HTTP Error '+str(e.code)
        except URLError as e:
            self.dictEsPluginData['status'] = '0'
            self.dictEsPluginData['msg'] = 'URL Error '+str(e.reason)
        except InvalidURL as e:
            self.dictEsPluginData['status'] = '0'
            self.dictEsPluginData['msg'] = 'Invalid URL'
        except Exception as e:
            self.dictEsPluginData['status'] = '0'
            self.dictEsPluginData['msg'] = 'Exception while opening stats url in python 2 : ' + str(e)
        finally:
            return str_responseData 
    

    def StandardMetrics(self):
        suffix='/_nodes/stats'
        searchdata=self._openURL2(suffix)
        searchdata=json.loads(searchdata)        

        num_disk_reads = 0
        num_disk_writes = 0
        jvm_gc_old_coll_count = 0
        jvm_gc_old_coll_time = 0
        query_time = 0
        query_total = 0
        fetch_time = 0 
        mem_used_perc_list = []
        if 'nodes' in searchdata:
            dictNodes = searchdata['nodes']
            for each_node in dictNodes.keys():
                if 'disk_reads' in dictNodes[each_node]['fs']['total']:
                    try:
                        num_disk_reads += int(dictNodes[each_node]['fs']['total']['disk_reads'])
                    except Exception as e:
                        pass
                if 'disk_writes' in dictNodes[each_node]['fs']['total']:
                    try:
                        num_disk_writes += int(dictNodes[each_node]['fs']['total']['disk_writes'])
                    except Exception as e:
                        pass
                if (('old' in dictNodes[each_node]['jvm']['mem']['pools']) and (('used_in_bytes' and 'max_in_bytes') in dictNodes[each_node]['jvm']['mem']['pools']['old'])):
                    try:
                        mem_perc = round((float(dictNodes[each_node]['jvm']['mem']['pools']['old']['used_in_bytes'])/float(dictNodes[each_node]['jvm']['mem']['pools']['old']['max_in_bytes'])),2)*100
                        mem_used_perc_list.append(mem_perc) 
                    except Exception as e:
                        pass
                if (('old' in dictNodes[each_node]['jvm']['gc']['collectors']) and (('collection_count' and 'collection_time_in_millis') in dictNodes[each_node]['jvm']['gc']['collectors']['old'])):
                    try:
                        jvm_gc_old_coll_count += int(dictNodes[each_node]['jvm']['gc']['collectors']['old']['collection_count'])
                        jvm_gc_old_coll_time += int(dictNodes[each_node]['jvm']['gc']['collectors']['old']['collection_time_in_millis']) 
                    except Exception as e:
                        pass
                if ('query_time_in_millis' and 'query_total' and 'fetch_time_in_millis') in dictNodes[each_node]['indices']['search']:
                    try:
                        query_time += int(dictNodes[each_node]['indices']['search']['query_time_in_millis'])
                        query_total += int(dictNodes[each_node]['indices']['search']['query_total'])
                        fetch_time += int(dictNodes[each_node]['indices']['search']['fetch_time_in_millis'])
                    except Exception as e:
                        pass

                    
        try:
            self.Maindata['disk_write_read_ratio'] = float(num_disk_writes/num_disk_reads)
        except Exception as e:
            pass
        try:
            self.Maindata['Fetch to query ratio'] = float(fetch_time/query_time)
        except Exception as e:
            pass
        try:
            self.Maindata['Latency of the query'] = float(query_time/query_total)
        except Exception as e:
            pass
        dcTime = time.time()
        if (('jvm_gc_old_coll_count' and 'ct') in self.dictCounterValues):
            try:
                self.Maindata['JVM garbage collector old generation count'] = jvm_gc_old_coll_count - int(self.dictCounterValues['jvm_gc_old_coll_count'])
            except Exception as e:
                pass
        else:
            self.Maindata['JVM garbage collector old generation count'] = 0
        if (('jvm_gc_old_coll_time' and 'ct') in self.dictCounterValues):
            try:
                self.Maindata['JVM garbage collector old generation time'] = jvm_gc_old_coll_time - int(self.dictCounterValues['jvm_gc_old_coll_time'])
            except Exception as e:
                pass
        else:
            self.Maindata['JVM garbage collector old generation time'] = 0
        self.dictCounterValues['jvm_gc_old_coll_count'] = jvm_gc_old_coll_count
        self.dictCounterValues['jvm_gc_old_coll_time'] = jvm_gc_old_coll_time
        self.dictCounterValues['ct'] = dcTime
        self.updateCounterValues(self.dictCounterValues)
        try:
            self.Maindata['Average JVM memory usage in garbage collector(%)'] = float(sum(mem_used_perc_list)/len(mem_used_perc_list))
        except Exception as e:
            pass
    
    def MetricCollector(self):
        
        self.StandardMetrics()
        self.parseMetrics(standard_metrics2)
        self.parseMetrics(os_metrics)
        self.parseMetrics(search_performance_metrics)
        self.parseMetrics(index_performance_metrics)
        self.parseMetrics(http_connection_metrics)
        self.parseMetrics(unsuccessful_get_metrics)
        self.parseMetrics(jvm_metrics)
        self.ClusterHealthMetrics()

        return self.Maindata
        
    def parseMetrics(self,datapath):

        try:
            suffix='/_nodes/stats'
            searchdata=self._openURL2(suffix)
            searchdata=json.loads(searchdata)
            nodes=searchdata['nodes'].keys()
            nodedata=searchdata['nodes']
            is_node_present=False
            resultback={}

            for node in nodes:

                if searchdata['nodes'][node]['name']==self.nodename:
                    is_node_present=True
                    self.Maindata['Status of the node']=1
                    self.Maindata["Node Availability"]="Available"
                    nodedata =searchdata['nodes'][node]

                    for key1 in datapath:
                        resultback=nodedata
                        for key2 in datapath[key1]:
                            resultback=resultback[key2]
                        self.Maindata[key1]=resultback


            if not is_node_present:
                for key1 in datapath:
                        self.Maindata[key1]=0

                self.Maindata['Status of the node']=0
                self.Maindata["Node Availability"]="Node not Found"
                pass


        except Exception as e:
                self.Maindata['msg']=str(e)        



    def ClusterHealthMetrics(self):
        try:
            suffix='/_cluster/health'
            searchdata=self._openURL2(suffix)
            searchdata=json.loads(searchdata)
            result=searchdata
            
            for key1 in cluster_health_node_availability_metrics:
                self.Maindata[key1]=result[cluster_health_node_availability_metrics[key1]]

        except Exception as e:
            self.Maindata['msg']=str(e)


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host to be monitored',nargs='?', default=HOST)
    parser.add_argument('--port', help='port number', type=int,  nargs='?', default=PORT)
    parser.add_argument('--node_name', help='Node name to be monitored', nargs='?', default=NODE)
    parser.add_argument('--username', help='user name of the elasticsearch', nargs='?', default=USERNAME)
    parser.add_argument('--password', help='password of the elasticsearch', nargs='?', default=PASSWORD)
    parser.add_argument('--sslpath', help='elasticsearch ssl path', nargs='?', default=CAFILE)
    parser.add_argument('--ssl', help='ssl option', nargs='?', default="NO")
    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)


    args = parser.parse_args()
    host_name=args.host
    port=str(args.port)
    node_name=args.node_name    
    username=args.username
    password=args.password 
    sslpath=args.sslpath
    ssl=args.ssl
    logs_enabled = args.logs_enabled
    log_type_name = args.log_type_name
    log_file_path = args.log_file_path
    

    esk=ElasticSearch(username,password,host_name,port,node_name,ssl,logs_enabled,log_type_name,log_file_path)
    result=esk.MetricCollector()
    result["heartbeat_required"]=HEARTBEAT
    result["plugin_version"]=PLUGIN_VERSION
    result['units']=METRICS_UNITS
    print(json.dumps(result,indent=4))
