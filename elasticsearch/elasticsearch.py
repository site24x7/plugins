#!/usr/bin/python3
import json
import time
import os
import urllib3
urllib3.disable_warnings()

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
                  "JVM heap memory committed":'KB'

                }

counterFilePath="counter.json"

#Metrics
standard_metrics2={

    "Queries hit count":("indices","query_cache","hit_count"),
    "Query cache memory size":("indices","query_cache","memory_size_in_bytes"),
    "Query cache miss count":("indices","query_cache","miss_count"),
    "Request cache hit count":("indices","request_cache","hit_count"),
    "Number of evictions":("indices","request_cache","evictions"),
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



class esk:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS

        self.hostname=args.hostname
        self.port=args.port
        self.nodename=args.nodename
        self.username=args.username
        self.password=args.password
        self.ssl_option=args.ssl_option
        self.cafile=args.cafile

        if self.ssl_option.lower()=="true":
            self.url="https://"+self.hostname+":"+str(self.port)
        elif self.ssl_option.lower()=="false":
            self.url="http://"+self.hostname+":"+str(self.port)


        self.dictCounterValues = {}
        self.loadCounterValues()

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
        
    def response_data(self, endpoint):
        try:
            import requests
            from requests.auth import HTTPBasicAuth

            url=self.url+endpoint
            r=requests.get(url, timeout=5, auth = HTTPBasicAuth(self.username,  self.password), verify=False)
            r.raise_for_status()
        
        except requests.exceptions.HTTPError as herror:
            self.maindata['msg']=str(herror)
            self.maindata['status']=0
            return False
        except requests.exceptions.ReadTimeout as errrt: 
            self.maindata['msg']=f"Timeout Error"
            self.maindata['status']=0
            return False
        except requests.exceptions.ConnectionError as conerr: 
            self.maindata['msg']=f"Connection Error"
            self.maindata['status']=0
            return False
        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return False
        return r.content
        
    def StandardMetrics(self):
        endpoint='/_nodes/stats'
        searchdata=self.response_data(endpoint)
        if not searchdata:
            return self.maindata

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

    def parseMetrics(self,datapath):

        try:
            endpoint='/_nodes/stats'
            searchdata=self.response_data(endpoint)
            if not searchdata:
                return self.maindata
            searchdata=json.loads(searchdata)
            nodes=searchdata['nodes'].keys()
            nodedata=searchdata['nodes']
            is_node_present=False
            resultback={}

            for node in nodes:

                if searchdata['nodes'][node]['name']==self.nodename:
                    is_node_present=True
                    self.maindata['Status of the node']=1
                    self.maindata["Node Availability"]="Available"
                    nodedata =searchdata['nodes'][node]

                    for key1 in datapath:
                        resultback=nodedata
                        for key2 in datapath[key1]:
                            resultback=resultback[key2]
                        self.maindata[key1]=resultback

            if not is_node_present:
                for key1 in datapath:
                        self.maindata[key1]=0

                self.maindata['Status of the node']=0
                self.maindata["Node Availability"]="Node not Found"
                pass

        except Exception as e:
                self.maindata['msg']=str(e)        




    def metriccollector(self):
        self.StandardMetrics()
        self.parseMetrics(standard_metrics2)
        self.parseMetrics(os_metrics)
        self.parseMetrics(search_performance_metrics)
        self.parseMetrics(index_performance_metrics)
        self.parseMetrics(http_connection_metrics)
        self.parseMetrics(unsuccessful_get_metrics)
        self.parseMetrics(jvm_metrics)
        return self.maindata



if __name__=="__main__":

    hostname="localhost"
    port="9200"
    nodename="test-node"
    username=None
    password=None
    ssl_option="False"
    cafile=None



    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--hostname', help='Host to be monitored',nargs='?', default=hostname)
    parser.add_argument('--port',     help='Port number', type=int,  nargs='?', default=port)
    parser.add_argument('--nodename', help='Node name to be monitored', nargs='?', default=nodename)
    parser.add_argument('--username', help='Username of the Elasticsearch', nargs='?', default=username)
    parser.add_argument('--password', help='Password of the Elasticsearch', nargs='?', default=password)
    parser.add_argument('--ssl_option', help='Option for Elasticsearch ssl', nargs='?', default=ssl_option)
    parser.add_argument('--cafile', help='cafile for the Elasticsearch', nargs='?', default=cafile)

    args=parser.parse_args()
    obj=esk(args)


    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
