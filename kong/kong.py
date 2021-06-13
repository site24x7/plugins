#!/usr/bin/python


import json
import argparse
import sys

PYTHON_VERSION = sys.version_info[0]
if PYTHON_VERSION == 3:
    import urllib.request as urlconnection
elif PYTHON_VERSION == 2:
    import urllib2 as urlconnection


# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = 1

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = ""

# Enter the host name configures for the Kong
HOST_NAME = ""

# Enter the port configured for the Kong
PORT = ""

# Enter the service name to be monitored from kong
SERVICE_NAME = ""

URL = ""
result_json = {}


METRIC_UNITS = {
    "connections_accepted" : "connections",
    "connections_active" : "connections",
    "connections_handled" : "connections",
    "connections_reading" : "connections",
    "connections_waiting" : "connections",
    "connections_writing" : "connections",
    "total_requests" : "requests",
    "kong_bandwidth.egress" : "bytes",
    "kong_bandwidth.ingress" : "bytes",
    "kong_datastore_reachable" : "connection",
    "kong_http_status" : "",
    "kong_latency_bucket.kong" : "millisecond",
    "kong_latency_bucket.request" : "millisecond",
    "kong_latency_bucket.upstream" : "millisecond",
    "kong_latency_count.kong" : "millisecond",
    "kong_latency_count.request" : "millisecond",
    "kong_latency_count.upstream" : "millisecond",
    "kong_latency_sum.kong" : "millisecond",
    "kong_latency_sum.request" : "millisecond",
    "kong_latency_sum.upstream" : "millisecond",
}


def prometheus_metrics(output):
    result = {}
    try:
        for each in output:
            if "kong_bandwidth" in each and SERVICE_NAME in each:
                if "type=\"egress\"" in each:
                    each = each.split(" ")
                    result["kong_bandwidth.egress"] = each[1]
                if "type=\"ingress\"" in each:
                    each = each.split(" ")
                    result["kong_bandwidth.ingress"] = each[1]
                    
            if "kong_datastore_reachable" in each and "#" not in each:
                each = each.split(" ")
                if "1" in each[1]:
                    result["kong_datastore_reachable"] = "SAFE"
                if "0" in each[1]:
                    result["kong_datastore_reachable"] = "CRITICAL"
                    
            if "kong_http_status" in each and SERVICE_NAME in each:
                each = each.split(" ")
                result["kong_http_status"] = each[1]
                
            if "kong_latency_bucket" in each and "le=\"+Inf\"" in each and SERVICE_NAME in each:
                if "type=\"kong\"" in each:
                    each = each.split(" ")
                    result["kong_latency_bucket.kong"] = each[1]
                if "type=\"request\"" in each:
                    each = each.split(" ")
                    result["kong_latency_bucket.request"] = each[1]
                if "type=\"upstream\"" in each:
                    each = each.split(" ")
                    result["kong_latency_bucket.upstream"] = each[1]
                    
            if "kong_latency_count" in each and SERVICE_NAME in each:
                if "type=\"kong\"" in each:
                    each = each.split(" ")
                    result["kong_latency_count.kong"] = each[1]
                if "type=\"request\"" in each:
                    each = each.split(" ")
                    result["kong_latency_count.request"] = each[1]
                if "type=\"upstream\"" in each:
                    each = each.split(" ")
                    result["kong_latency_count.upstream"] = each[1]
                    
            if "kong_latency_sum" in each and SERVICE_NAME in each:
                if "type=\"kong\"" in each:
                    each = each.split(" ")
                    result["kong_latency_sum.kong"] = each[1]
                if "type=\"request\"" in each:
                    each = each.split(" ")
                    result["kong_latency_sum.request"] = each[1]
                if "type=\"upstream\"" in each:
                    each = each.split(" ")
                    result["kong_latency_sum.upstream"] = each[1]
                
    except Exception as e:
        result["status"] = 0
        result["msg"] = str(e)
                
    return result 
        

def get_output():
    result = {}
    try:
        URL = "http://" + HOST_NAME + ":" + PORT + "/status/"
        response = urlconnection.urlopen(URL)
        output = response.read()
        output = output.strip()
        output = output.decode("utf-8")
        output = json.loads(output)
        
        result = output["server"]
        
        URL = "http://" + HOST_NAME + ":" + PORT + "/metrics/"
        response = urlconnection.urlopen(URL)
        output = response.read()
        output = output.strip()
        output = output.decode("utf-8")
        output = output.split("\n")
        
        result.update(prometheus_metrics(output))
        
        
        
    except Exception as e:
        result["status"] = 0
        result["msg"] = str(e)
                
    return result 	



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host_name', help="kong host_name", type=str)
    parser.add_argument('--port', help="kong port", type=str)
    parser.add_argument('--service_name', help="kong service_name", type=str)
    args = parser.parse_args()
    
    if args.host_name:
        HOST_NAME = args.host_name
    if args.port:
        PORT = args.port
    if args.service_name:
        SERVICE_NAME = args.service_name
        
    result_json = get_output()
    
    result_json['plugin_version'] = PLUGIN_VERSION
    result_json['heartbeat_required'] = HEARTBEAT
    result_json['units'] = METRIC_UNITS
    
    print(json.dumps(result_json, indent=4, sort_keys=False))
