#!/usr/bin/python

### For monitoring the performance metrics of your Elasticsearch cluster using Site24x7 Server Monitoring Plugins.

### 1. Have the site24x7 server monitoring agent up and running.
### 2. Download the plugin from github https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearch/
### 3. Create a folder in name of the plugin under agent plugins directory (/opt/site24x7/monagent/plugins/)
### 4. Place the plugin inside the folder 

### Author: Tarun, Zoho Corp
### Language : Python
### Tested in Ubuntu


import json, os,sys
import time

'''
This is Default configuration. 
Change the Elasticsearch configuration accordingly
in the configuration file elasticsearch.cfg.

Configuration File will have more Priority
'''
HOST='localhost'
PORT='9200'
USERNAME = None   #Add the username if any authentication is set for ES stats api
PASSWORD = None   #Add the password if any authentication is set for ES stats api


#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = True

METRICS_UNITS = { 'jvm_gc_old_coll_time':'ms',
                  'jvm_mem_pool_old_used_perc' : '%'
                }

counterFilePath = '/opt/site24x7/monagent/plugins/elasticsearch/counter.json'

dictStatusValue = { 'yellow' : '2', 'green' : '1', 'red' : '0' }



PYTHON_MAJOR_VERSION = sys.version_info[0]
if PYTHON_MAJOR_VERSION == 3:
    import urllib.request as urlconnection
    from urllib.request import HTTPError,URLError
    from http.client import InvalidURL 
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as urlconnection
    from urllib2 import HTTPError,URLError
    from httplib import InvalidURL

class escluster():
    def __init__(self,host_name,port,username,password):
        self._url = 'http://'+host_name+':'+port
        self._userName = username
        self._userPass = password
        self._realm = None
        self.dictEsPluginData = {}
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
    
    def metricCollector(self):
        str_nodesData = self._openURL2('/_nodes/stats')
        if str_nodesData:
            self.parseNodesData(str_nodesData)
        str_clusterData = self._openURL2('/_cluster/health')
        if str_clusterData:
            self.parseClusterData(str_clusterData)
        self.dictEsPluginData['units'] = METRICS_UNITS        
        
        return self.dictEsPluginData
    
    def _openURL2(self,str_URLsuffix):
        str_responseData = None
        url = None
        try:
            url = self._url + str_URLsuffix
            password_mgr = urlconnection.HTTPPasswordMgr()
            password_mgr.add_password(None, url, self._userName, self._userPass)
            auth_handler = urlconnection.HTTPBasicAuthHandler(password_mgr)
            proxy = urlconnection.ProxyHandler({}) # Uses NO Proxy
            opener = urlconnection.build_opener(proxy, auth_handler)
            urlconnection.install_opener(opener)
            response = urlconnection.urlopen(url, timeout = 5)
            if response.getcode() == 200:
                byte_responseData = response.read()
                str_responseData = byte_responseData.decode('UTF-8')
            else:
                self.dictEsPluginData['status'] = '0'
                self.dictEsPluginData['msg'] = 'Invalid response after opening URL : ' + str(response.getcode())
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
    
    def parseNodesData(self, str_nodesData):
        dictNodesData = json.loads(str_nodesData)
        num_disk_reads = 0
        num_disk_writes = 0
        jvm_gc_old_coll_count = 0
        jvm_gc_old_coll_time = 0
        query_time = 0
        query_total = 0
        fetch_time = 0 
        mem_used_perc_list = []
        if 'nodes' in dictNodesData:
            dictNodes = dictNodesData['nodes']
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
            self.dictEsPluginData['disk_write_read_ratio'] = float(num_disk_writes/num_disk_reads)
        except Exception as e:
            pass
        try:
            self.dictEsPluginData['fetch_to_query_ratio'] = float(fetch_time/query_time)
        except Exception as e:
            pass
        try:
            self.dictEsPluginData['query_latency'] = float(query_time/query_total)
        except Exception as e:
            pass
        dcTime = time.time()
        if (('jvm_gc_old_coll_count' and 'ct') in self.dictCounterValues):
            try:
                self.dictEsPluginData['jvm_gc_old_coll_count'] = jvm_gc_old_coll_count - int(self.dictCounterValues['jvm_gc_old_coll_count'])
            except Exception as e:
                pass
        else:
            self.dictEsPluginData['jvm_gc_old_coll_count'] = 0
        if (('jvm_gc_old_coll_time' and 'ct') in self.dictCounterValues):
            try:
                self.dictEsPluginData['jvm_gc_old_coll_time'] = jvm_gc_old_coll_time - int(self.dictCounterValues['jvm_gc_old_coll_time'])
            except Exception as e:
                pass
        else:
            self.dictEsPluginData['jvm_gc_old_coll_time'] = 0
        self.dictCounterValues['jvm_gc_old_coll_count'] = jvm_gc_old_coll_count
        self.dictCounterValues['jvm_gc_old_coll_time'] = jvm_gc_old_coll_time
        self.dictCounterValues['ct'] = dcTime
        self.updateCounterValues(self.dictCounterValues)
        try:
            self.dictEsPluginData['jvm_mem_pool_old_used_perc'] = float(sum(mem_used_perc_list)/len(mem_used_perc_list))
        except Exception as e:
            pass

    def parseClusterData(self, str_clusterData):
        dictClusterData = json.loads(str_clusterData)
        if 'status' in dictClusterData:
            self.dictEsPluginData['status'] = dictStatusValue[dictClusterData['status']]
        if 'number_of_nodes' in dictClusterData:
            self.dictEsPluginData['num_nodes'] = dictClusterData['number_of_nodes']
        if 'number_of_data_nodes' in dictClusterData:
            self.dictEsPluginData['num_data_nodes'] = dictClusterData['number_of_data_nodes']
        if 'active_primary_shards' in dictClusterData:
            self.dictEsPluginData['active_prim_shards'] = dictClusterData['active_primary_shards']
        if 'active_shards' in dictClusterData:
            self.dictEsPluginData['active_shards'] = dictClusterData['active_shards']
        if 'relocating_shards' in dictClusterData:
            self.dictEsPluginData['relocating_shards'] = dictClusterData['relocating_shards']
        if 'initializing_shards' in dictClusterData:
            self.dictEsPluginData['init_shards'] = dictClusterData['initializing_shards']
        if 'unassigned_shards' in dictClusterData:
            self.dictEsPluginData['unassigned_shards'] = dictClusterData['unassigned_shards']
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host to be monitored',nargs='?', default=HOST)
    parser.add_argument('--port', help='port number', type=int,  nargs='?', default=PORT)
    parser.add_argument('--username', help='user name of the elasticsearch', nargs='?', default=USERNAME)
    parser.add_argument('--password', help='password of the elasticsearch', nargs='?', default=PASSWORD)
    
    parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=PLUGIN_VERSION)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=HEARTBEAT)
    args = parser.parse_args()
    
    host_name=args.host
    port=str(args.port)
    username=args.username
    password=args.password
    
    
    esc = escluster(host_name,port,username,password)
    result = esc.metricCollector()
    result['plugin_version'] = args.plugin_version
    result['heartbeat_required'] = args.heartbeat
    
    print(json.dumps(result, indent=4, sort_keys=True))
