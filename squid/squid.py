#!/usr/bin/python


import json
import sys
import argparse
import os.path
import time
import urllib.request as urlconnection


# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = 1

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

# Enter the host name configures for the Kong
HOST_NAME = ""

# Enter the port configured for the Kong
PORT = ""

# Check whether the os is Windows or Linux for path of plugin
if sys.platform == "linux":
    FILE_PATH = "/opt/site24x7/monagent/plugins/squid/squid_metrics.json"
elif sys.platform == "win32":
    FILE_PATH = "C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\squid\squid_metrics.json"

URL = ""
result_json = {}

#to store previous_data and current_data time data for calculating per second value
output = []
previous_data = {}
current_data = {}


METRIC_UNITS = {
    "client_http.requests" : "requests/second",
    "client_http.hits" : "hits/second",
    "client_http.errors" : "errors/second",
    "client_http.kbytes_in" : "kibibytes/second",
    "client_http.kbytes_out" : "kibibytes/second",
    "client_http.hit_kbytes_out" : "kibibytes/second",
    "server.all.requests" : "requests/second",
    "server.all.errors" : "errors/second",
    "server.all.kbytes_in" : "kibibytes/second",
    "server.all.kbytes_out" : "kibibytes/second",
    "server.http.requests" : "requests/second",
    "server.http.errors" : "errors/second",
    "server.http.kbytes_in" : "kibibytes/second",
    "server.http.kbytes_out" : "kibibytes/second",
    "server.ftp.requests" : "requests/second",
    "server.ftp.errors" : "errors/second",
    "server.ftp.kbytes_in" : "kibibytes/second",
    "server.ftp.kbytes_out" : "kibibytes/second",
    "server.other.requests" : "requests/second",
    "server.other.errors" : "errors/second",
    "server.other.kbytes_in" : "kibibytes/second",
    "server.other.kbytes_out" : "kibibytes/second",
    "unlink.requests" : "requests/second",
    "page_faults" : "faults/second",
    "aborted_requests" : "requests/second"
}


#try connection to URL and resturn output
def get_squid_counter():
    try:
        URL = "http://" + HOST_NAME + ":" + PORT + "/squid-internal-mgr/counters"
        response = urlconnection.urlopen(URL)
        output = response.read()
        output = output.strip()
        output = output.decode("utf-8")
        output = output.split('\n')
        
    except Exception as e:
        output = [False, str(e)]
        
    return output


#method to filter data from HTTP response output
def get_output():
    squid_counter = {}
    try:
        output = get_squid_counter()
        for each in output:
            counter, value = each.split(" = ")
            if counter in METRIC_UNITS.keys():
                squid_counter[counter] = value
        squid_counter['time'] = time.time()
                
    except Exception as e:
        squid_counter["status"] = 0
        squid_counter["msg"] = str(e)
        
    return squid_counter
    
    

#calculate per second with previous output or calculate per second value with time difference between previous_data and current_data
def calculate_persecond(previous_data, current_data):
    result = {}
    try:
        time_diff = int(current_data['time'] - previous_data['time'])
        current_data = get_output()
        for each in METRIC_UNITS:
            result[each] = format((float(current_data[each]) - float(previous_data[each])) / time_diff, '.2f')
                    
    except Exception as e:
        result["status"] = 0
        result["msg"] = str(e)
            
    with open(FILE_PATH, 'w') as outfile:
        json.dump(current_data, outfile)
        
    return result


def collect_data():
    result = {}
    try:
        output = get_squid_counter()
        if not output[0]:
            if os.path.exists('/squid_metrics.json'):
                os.remove(FILE_PATH)
            result['status'] = 0
            result['msg'] = output[1]
        else:
            if os.path.exists(FILE_PATH):
                with open(FILE_PATH) as json_file:
                    previous_data = json.load(json_file)
        
            else:
                previous_data = get_output()
                time.sleep(20)
                
            current_data = get_output()
            result = calculate_persecond(previous_data, current_data)
                
    except Exception as e:
        result["status"] = 0
        result["msg"] = str(e)
                
    return result
        

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--host_name', help="squid host_name", type=str)
    parser.add_argument('--port', help="squid port", type=str)
    args = parser.parse_args()
    
    if args.host_name:
        HOST_NAME = args.host_name
    if args.port:
        PORT = args.port
        
    #check squid running, if no delete previous file, if yes check if previous file exist, if yes take previous_data as prvious file, else take two data with 20sec time interval
    result_json = collect_data()
        
    result_json['plugin_version'] = PLUGIN_VERSION
    result_json['heartbeat_required'] = HEARTBEAT
    result_json['units'] = METRIC_UNITS
    
    print(json.dumps(result_json, indent=4, sort_keys=False))
