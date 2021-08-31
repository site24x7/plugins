#!/usr/bin/python

import json
import urllib
import urllib.request as connector

metric_units={
    "total_freespace":"bytes",
    "total_spaceused":"bytes",
    "total_space":"bytes",
    "tcp_established":"bytes",
    "tcp_listening":"bytes",
    "tcp_closing":"bytes",
    "network_in":"bytes",
    "network_out":"bytes",
    "network_in_errors":"bytes",
    "network_out_dropped":"bytes",
    "network_out_errors":"bytes",
    "syn_sent":"bytes",
    "syn_recv":"bytes"
}



class Filebeat(object):

    def __init__(self, args):
        self.host=args.host
        self.port=args.port
        self.plugin_version=args.plugin_version
        self.heartbeat=args.heartbeat  
        self.resultjson = {}
        
        self.metrics_collector()
        
        self.resultjson['plugin_version'] = self.plugin_version
        self.resultjson['heartbeat_required'] = self.heartbeat
     
    def metrics_collector(self):

        try:
            url="http://"+self.host+":"+self.port+"/metricbeat-*/_search?pretty"
            response=((connector.urlopen(url)).read()).decode("UTF-8")
            response=json.loads(response)
            data=response["hits"]["hits"][1]["_source"]
            self.resultjson["system_type"]=data["service"]["type"]
            self.resultjson["network1_name"]=data["system"]["network"]["name"]
            name=data["system"]["network"]["name"]
            self.resultjson[name+"_out"]=data["system"]["network"]["out"]["bytes"]
            self.resultjson[name+"_out_errors"]=data["system"]["network"]["out"]["errors"]
            self.resultjson[name+"_out_dropped"]=data["system"]["network"]["out"]["dropped"]
            self.resultjson[name+"_in"]=data["system"]["network"]["in"]["bytes"]
            self.resultjson[name+"_in_errors"]=data["system"]["network"]["in"]["bytes"]
            self.resultjson[name+"_out_dropped"]=data["system"]["network"]["in"]["dropped"]
            data=response["hits"]["hits"][3]["_source"]
            self.resultjson["network2_name"]=data["system"]["network"]["name"]
            name=data["system"]["network"]["name"]
            self.resultjson[name+"_out"]=data["system"]["network"]["out"]["bytes"]
            self.resultjson[name+"_out_errors"]=data["system"]["network"]["out"]["errors"]
            self.resultjson[name+"_out_dropped"]=data["system"]["network"]["out"]["dropped"]
            self.resultjson[name+"_in"]=data["system"]["network"]["in"]["bytes"]
            self.resultjson[name+"_in_errors"]=data["system"]["network"]["in"]["bytes"]
            self.resultjson[name+"_out_dropped"]=data["system"]["network"]["in"]["dropped"]       
            data=response["hits"]["hits"][5]["_source"]["system"]["fsstat"]
        
            self.resultjson["total_freespace"]=data["total_size"]["free"]
            self.resultjson["total_spaceused"]=data["total_size"]["used"]
            self.resultjson["total_space"]=data["total_size"]["total"]
            self.resultjson["total_files"]=data["total_files"]
            data=response["hits"]["hits"][7]["_source"]["system"]["socket"]["summary"]["tcp"]["all"]
            self.resultjson["tcp_listening"]=data["listening"]
            self.resultjson["tcp_established"]=data["established"]
            self.resultjson["tcp_closing"]=data["closing"]
            self.resultjson["tcp_count"]=data["count"]
            self.resultjson["syn_recv"]=data["syn_recv"]
            self.resultjson["syn_sent"]=data["syn_sent"]
       
        except Exception as e:
            self.resultjson["msg"]=str(e)
            self.resultjson["status"]=0
        return self.resultjson

if __name__=='__main__':
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?', default= "localhost")
    parser.add_argument('--port',help="Port",nargs='?', default= "9200")
    parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=1)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=True)
    args=parser.parse_args()
	
    filebeat = Filebeat(args)
    resultjson = filebeat.metrics_collector()
    resultjson['units'] = metric_units
    print(json.dumps(resultjson, indent=4, sort_keys=True))
