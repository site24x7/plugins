#!/usr/bin/python3
import json
import time
import os
import urllib3
import requests
import warnings
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings()
warnings.filterwarnings("ignore")

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS = { 'JVM garbage collector old generation time':'ms',
                  'Average JVM memory usage in garbage collector(%)' : '%',
                  'CPU used (%)':'%',
                  'OS memory used(%)':'%', 
                  'OS memory free(%)':'%',
                  'JVM heap memory used (%)':'%',
                  'Time spent on fetches':'ms',
                  "Time spent on queries":'ms',
                  "Total time on GET requests where the document was missing":'ms',
                  "JVM heap memory committed":'bytes',
                  "Active shards percent":'%'

                }

script_directory = os.path.dirname(os.path.abspath(__file__))

counterFilePath = os.path.join(script_directory, "counter.json")

all_metrics={

"standard_metrics":{

    "Queries hit count":("indices","query_cache","hit_count"),
    "Query cache memory size":("indices","query_cache","memory_size_in_bytes"),
    "Query cache miss count":("indices","query_cache","miss_count"),
    "Request cache hit count":("indices","request_cache","hit_count"),
    "Number of evictions":("indices","request_cache","evictions"),
    "Request cache memory size":("indices","request_cache","memory_size_in_bytes")
},


"os_metrics":{

    "CPU used (%)":("os","cpu","percent"),
    "OS memory free(%)":("os","mem","free_percent"),
    "OS memory used(%)":("os","mem","used_percent")
},

"search_performance_metrics":{

    "Total queries":("indices","search","query_total"),
    "Time spent on queries":("indices","search","query_time_in_millis"),
    "Queries in progress":("indices","search","query_current"),
    "Number of fetches":("indices","search","fetch_total"),
    "Time spent on fetches":("indices","search","fetch_time_in_millis"),
    "Fetches in progress":("indices","search","fetch_current"),
},

"index_performance_metrics":{
    "Documents indexed":('indices','indexing','index_total'),
    "Time of indexing documents":('indices','indexing','index_time_in_millis'),
    "Documents currently indexed":("indices","indexing","index_current"),
    "Index refreshes":("indices","refresh","total"),
    "Time spent on refreshing indices":("indices","refresh","total_time_in_millis"),
    "Index flushes to disk":("indices","flush","total"),
    "Time spent on flushing indices to disk":("indices","flush","total_time_in_millis"),
    "Indices docs count":("indices","docs","count"),
    "Indices docs deleted":("indices","docs","deleted"),
},

"http_connection_metrics":{

    "HTTP connections currently open":("http","current_open"),
    "HTTP connections opened over time":("http","total_opened")
},

"unsuccessful_get_metrics":{
    "Number of GET requests where the document was missing":("indices","get","missing_total"),
    "Total time on GET requests where the document was missing":("indices","get","missing_time_in_millis")
},

"jvm_metrics":{

    "JVM heap memory used (%)":("jvm","mem","heap_used_percent"),
    "JVM heap memory committed":("jvm","mem","heap_committed_in_bytes")
}
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
    "Delayed unassigned shards":('delayed_unassigned_shards'),
    "Active shards":("active_shards"),
    "Active shards percent":("active_shards_percent_as_number")
    
}

class esk:


    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS

        self.hostname=args.host
        self.port=args.port
        self.username=args.username
        self.password=args.password
        self.ssl_option=args.ssl_option
        self.cafile=args.cafile
        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path
        self.node_metrics = {}


        self.maindata["tabs"]={

            "Search and Query Performance":{
                "order":1,
                "tablist":[
                "Total queries",
                "Time spent on queries",
                "Queries in progress",
                "Number of fetches",
                "Time spent on fetches",
                "Fetches in progress",
                "Queries hit count",
                "Query cache memory size",
                "Query cache miss count",
                "Request cache hit count",
                "Number of evictions",
                "Request cache memory size",
                "Number of GET requests where the document was missing",
                "Total time on GET requests where the document was missing"
                ]},


            "Index Performance":{
                "order":2,
                "tablist":[
                "Documents indexed",
                "Time of indexing documents",
                "Documents currently indexed",
                "Index refreshes",
                "Time spent on refreshing indices",
                "Index flushes to disk",
                "Time spent on flushing indices to disk",
                "Indices docs count",
                "Indices docs deleted"
                ]
            },

            "System Performance":{
                "order":3,
                "tablist":[
                "CPU used (%)",
                "OS memory free(%)",
                "OS memory used(%)",
                "HTTP connections currently open",
                "HTTP connections opened over time",
                "JVM heap memory used (%)",
                "JVM heap memory committed"
                ]
            }
        }


        if self.username=="None":
            self.username=None

        if self.password=="None":
            self.password=None

        if self.ssl_option.lower()=="false":
            self.ssl_option=False
            self.url="http://"+self.hostname+":"+str(self.port)

        else:
            self.url="https://"+self.hostname+":"+str(self.port)
            self.ssl_option=True



        self.dictCounterValues = {}
        self.loadCounterValues()


    def loadCounterValues(self):
        if not os.path.exists(counterFilePath):
            with open(counterFilePath, 'w') as f:
                json.dump({"counter": {}, "node_metrics": {}} , f)
        else:
            with open(counterFilePath, 'r') as f:
                str_counterValues = f.read()
                if str_counterValues:
                    full_data = json.loads(str_counterValues)
                    self.dictCounterValues = full_data.get("counter", {})
                    self.node_metrics = full_data.get("node_metrics", {})

    def updateCounterValues(self, dict_valuesToUpdate):
        full_data = {
            "counter": dict_valuesToUpdate,
            "node_metrics": self.node_metrics  
        }
        with open(counterFilePath, 'w') as f:
            json.dump(full_data, f, indent=4)


    def overall_metrics(self, searchdata):

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
            self.maindata['disk_write_read_ratio'] = float(num_disk_writes/num_disk_reads)
        except Exception as e:
            pass
        try:
            self.maindata['Fetch to query ratio'] = float(fetch_time/query_time)
        except Exception as e:
            pass
        try:
            self.maindata['Latency of the query'] = float(query_time/query_total)
        except Exception as e:
            pass
        dcTime = time.time()
        if (('jvm_gc_old_coll_count' and 'ct') in self.dictCounterValues):
            try:
                self.maindata['JVM garbage collector old generation count'] = jvm_gc_old_coll_count - int(self.dictCounterValues['jvm_gc_old_coll_count'])
            except Exception as e:
                pass
        else:
            self.maindata['JVM garbage collector old generation count'] = 0
        if (('jvm_gc_old_coll_time' and 'ct') in self.dictCounterValues):
            try:
                self.maindata['JVM garbage collector old generation time'] = jvm_gc_old_coll_time - int(self.dictCounterValues['jvm_gc_old_coll_time'])
            except Exception as e:
                pass
        else:
            self.maindata['JVM garbage collector old generation time'] = 0

        self.dictCounterValues['jvm_gc_old_coll_count'] = jvm_gc_old_coll_count
        self.dictCounterValues['jvm_gc_old_coll_time'] = jvm_gc_old_coll_time
        self.dictCounterValues['ct'] = dcTime
        self.updateCounterValues(self.dictCounterValues)
        try:
            self.maindata['Average JVM memory usage in garbage collector(%)'] = float(sum(mem_used_perc_list)/len(mem_used_perc_list))
        except Exception as e:
            pass


    def response_data(self, url):
        try:
            r=requests.get(url, timeout=5, auth = HTTPBasicAuth(self.username,  self.password), verify=False)
            r.raise_for_status()
        
        except requests.exceptions.HTTPError as herror:
            self.maindata['msg']=str(herror)
            self.maindata['status']=0
            return False
        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return False
        return r.content


    def get_all(self):
        endpoint='/_nodes/stats'
        url=self.url+endpoint

        response=self.response_data(url)
        if not response:
             return False
        return response
    

    def find_master(self):
        url=self.url+"/_cat/master"
        response=self.response_data(url)
        if not response:
            return False
        node_id=response.decode().split()[0]
        return node_id


    def node_check(self, complete_data, node_id):
        node=complete_data.get("nodes").get(node_id)
        return node


    def parseMetrics(self,datapath, nodedata):

        try:
            resultback={}
            self.maindata['Status of the node']=1
            self.maindata["Node Availability"]="Available"

            for key1 in datapath:
                resultback=nodedata
                for key2 in datapath[key1]:
                    try:
                        resultback=resultback[key2]
                    except KeyError:
                        pass
                    except Exception as e:
                        self.maindata['msg']=str(e)
                        self.maindata['status']=0
                self.maindata[key1]=resultback
            return True
        
        except Exception as e:
                self.maindata['msg']=str(e)      
                self.maindata['status']=0
                return False

    def all_node_metrics(self, nodesdata):
        try:
            chunk_size = 25
            existing_chunks = self.node_metrics.copy()

            current_nodes_flat = []
            for chunk in sorted(existing_chunks.keys(), key=lambda x: int(x.split("_")[-1])):
                current_nodes_flat.extend(existing_chunks[chunk])

            current_api_nodes = {v["name"]: v for k, v in nodesdata.items()}

            new_chunks = []
            buffer = []

            for node_name in current_nodes_flat:
                if node_name in current_api_nodes:
                    node_data = current_api_nodes[node_name]
                    buffer.append({
                        "name": node_name,
                        "time_spent_on_queries": node_data["indices"]["search"]["query_time_in_millis"],
                        "queries_in_progress": node_data["indices"]["search"]["query_current"],
                        "number_of_fetches": node_data["indices"]["search"]["fetch_total"],
                        "documents_indexed": node_data["indices"]["indexing"]["index_total"],
                        "cpu_used": node_data["os"]["cpu"]["percent"],
                        "status":1
                    })
                else:
                    buffer.append({
                        "name": node_name,
                        "time_spent_on_queries": 0,
                        "queries_in_progress": 0,
                        "number_of_fetches": 0,
                        "documents_indexed": 0,
                        "cpu_used": 0,
                        "status":0
                    })

                if len(buffer) == chunk_size:
                    new_chunks.append(buffer)
                    buffer = []

            if buffer:
                new_chunks.append(buffer)

            new_node_names = set(current_api_nodes.keys()) - set(current_nodes_flat)
            for new_node_name in sorted(new_node_names): 
                node_data = current_api_nodes[new_node_name]
                node_info = {
                    "name": new_node_name,
                    "time_spent_on_queries": node_data["indices"]["search"]["query_time_in_millis"],
                    "queries_in_progress": node_data["indices"]["search"]["query_current"],
                    "number_of_fetches": node_data["indices"]["search"]["fetch_total"],
                    "documents_indexed": node_data["indices"]["indexing"]["index_total"],
                    "cpu_used": node_data["os"]["cpu"]["percent"],
                    "status":1
                }
                if new_chunks and len(new_chunks[-1]) < chunk_size:
                    new_chunks[-1].append(node_info)
                else:
                    new_chunks.append([node_info])

            tablist_keys = []
            self.node_metrics = {}

            for idx, chunk_data in enumerate(new_chunks):
                key = f"node_metrics_{idx + 1}"
                self.maindata[key] = []

                for node in chunk_data:
                    renamed_node = {
                        "name": node["name"],
                        f"time_spent_on_queries_{idx + 1}": node["time_spent_on_queries"],
                        f"queries_in_progress_{idx + 1}": node["queries_in_progress"],
                        f"number_of_fetches_{idx + 1}": node["number_of_fetches"],
                        f"documents_indexed_{idx + 1}": node["documents_indexed"],
                        f"cpu_used_{idx + 1}": node["cpu_used"],
                        f"status": node["status"]
                    }
                    self.maindata[key].append(renamed_node)

                self.node_metrics[key] = [n["name"] for n in chunk_data]
                tablist_keys.append(key)

            self.updateCounterValues(self.dictCounterValues)

            if "tabs" not in self.maindata:
                self.maindata["tabs"] = {}

            self.maindata["tabs"]["Nodes"] = {
                "order": 4,
                "tablist": tablist_keys
            }
            self.maindata['s247config']={
            "childdiscovery":tablist_keys
        }

            return True

        except Exception as e:
            self.maindata['msg'] = str(e)
            self.maindata['status'] = 0
            return False


    def ClusterHealthMetrics(self, cluster_data, datapath):
        try:

            for key1 in datapath:
                data_key = datapath[key1]
                if data_key in cluster_data:
                    self.maindata[key1] = cluster_data[data_key]
                else:
                    self.maindata[key1] = -1
            return True
        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return False

    def metriccollector(self):

        all_data=self.get_all()

        if not all_data:
             return self.maindata
        all_data=json.loads(all_data)


        self.overall_metrics(all_data)

        node_id=self.find_master()

        node_data=self.node_check(all_data, node_id)
        if not node_data:
            self.maindata["msg"]='Master Node not found'
            self.maindata["status"]=0
            return self.maindata

        for metric in all_metrics:
            if not self.parseMetrics(all_metrics[metric], node_data):
                return self.maindata
        

        url=self.url+"/_cluster/health"
        cluster_data=self.response_data(url)
        if not cluster_data:
            return self.maindata
        cluster_data=json.loads(cluster_data)
        cluster_status=cluster_data.get('status', '').lower()
        
        status_map = {'green': 0, 'yellow': 1, 'red': 2}
        self.maindata["Cluster State"] = status_map.get(cluster_status, -1)
        self.maindata["msg"] = f"Cluster status is currently '{cluster_data.get('status', 'unknown')}'"


        if not self.ClusterHealthMetrics(cluster_data, cluster_health_node_availability_metrics):
            return self.maindata

        nodesdata=all_data["nodes"]
        self.all_node_metrics(nodesdata)

        applog={}
        if(self.logsenabled in ['True', 'true', '1']):
                applog["logs_enabled"]=True
                applog["log_type_name"]=self.logtypename
                applog["log_file_path"]=self.logfilepath
        else:
                applog["logs_enabled"]=False
        self.maindata['applog'] = applog

        return self.maindata


def clean_quotes(value):
    if not value:
        return value
    
    value_str = str(value)
    
    if value_str.startswith('"') and value_str.endswith('"'):
        return value_str[1:-1]
    
    elif value_str.startswith("'") and value_str.endswith("'"):
        return value_str[1:-1]
    
    return value_str

def run(param):
    host = clean_quotes(param.get("host")) if param and param.get("host") else "localhost"
    port = clean_quotes(param.get("port")) if param and param.get("port") else "9200"
    username = clean_quotes(param.get("username")) if param and param.get("username") else "None"
    password = clean_quotes(param.get("password")) if param and param.get("password") else "None"
    ssl_option = clean_quotes(param.get("ssl_option")) if param and param.get("ssl_option") else "false"
    cafile = clean_quotes(param.get("cafile")) if param and param.get("cafile") else "None"
    logs_enabled = clean_quotes(param.get("logs_enabled")) if param and param.get("logs_enabled") else "True"
    log_type_name = clean_quotes(param.get("log_type_name")) if param and param.get("log_type_name") else "Elasticsearch Slow Log"
    log_file_path = clean_quotes(param.get("log_file_path")) if param and param.get("log_file_path") else "/var/log/elasticsearch/*_index_indexing_slowlog*.log"
    
    class Args:
        def __init__(self, host, port, username, password, ssl_option, cafile, logs_enabled, log_type_name, log_file_path):
            self.host = host
            self.port = int(port)
            self.username = username
            self.password = password
            self.ssl_option = ssl_option
            self.cafile = cafile
            self.logs_enabled = logs_enabled
            self.log_type_name = log_type_name
            self.log_file_path = log_file_path
    
    args = Args(host, port, username, password, ssl_option, cafile, logs_enabled, log_type_name, log_file_path)
    elasticsearch_instance = esk(args)
    result = elasticsearch_instance.metriccollector()
    return result


if __name__=="__main__":
    

    hostname="localhost"
    port="9200"
    username=None
    password=None
    ssl_option="false"
    cafile=None
    logs_enabled="True"
    log_type_name="Elasticsearch Slow Log"
    log_file_path="/var/log/elasticsearch/*_index_indexing_slowlog*.log"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host', help='Host to be monitored',nargs='?', default=hostname)
    parser.add_argument('--port',     help='Port number', type=int,  nargs='?', default=port)
    parser.add_argument('--username', help='Username of the Elasticsearch', nargs='?', default=username)
    parser.add_argument('--password', help='Password of the Elasticsearch', nargs='?', default=password)
    parser.add_argument('--ssl_option', help='Option for Elasticsearch ssl', nargs='?', default=ssl_option)
    parser.add_argument('--cafile', help='cafile for the Elasticsearch', nargs='?', default=cafile)
    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default=logs_enabled)
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=log_type_name)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=log_file_path)
    args=parser.parse_args()
    obj=esk(args)


    result=obj.metriccollector()
    print(json.dumps(result))
