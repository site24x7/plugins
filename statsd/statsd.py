#!/usr/bin/python

"""

__author__ = Vijay, Zoho Corp
Language = Python

Tested in Ubuntu, Windows 8

"""

import statsd
import socket
import codecs
import re
import json

###################################### CONFIG SECTION START ###########################################

host = "localhost"
port = 8126

###################################### CONFIG SECTION START ###########################################


END_PATTERN = re.compile("^END\n$", re.MULTILINE)
HEALTH_END_PATTERN = re.compile("^(health: up|health: down)\n$", re.MULTILINE)
ERROR_PATTERN = re.compile("^ERROR\n$", re.MULTILINE)

DEFAULT_HOST = "localhost"
DEFAULT_PORT = 8126

# If any changes done in the plugin, plugin_version must be incremented by 1. For. E.g 2,3,4.. 
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"



class statsd():
    config = {}
    host = ""
    port = 0
    metrics = {}
    
    def __init__(self, config):
        self.config = config
        self.host = self.get_data("host", DEFAULT_HOST)
        self.port = self.get_data("port", DEFAULT_PORT)
        
    def getData(self, host, port, command, *end_patterns):
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
    
            s.sendall(codecs.encode(command))
            s.settimeout(2)
            chunk = s.recv(1024)
            res = ""
            while chunk:
                res += codecs.decode(chunk)
                chunk = s.recv(1024)
                if self._match_end(codecs.decode(chunk), *end_patterns):
                    break
        except socket.timeout as e:
            pass
        finally:
            s.close()
        return res
    
    def _match_end(self, data, *end_patterns):
        for pattern in end_patterns:
            if pattern.search(data):
                return True
        return False
            
    def get_data(self, key, default_value, *invalid_values):
        if key in self.config:
            val = self.config.get(key)
            if val in invalid_values:
                return default_value
            else:
                return val
        return  default_value
    
    def get_statsd_length(self, jsonString):
        try:
            jsonString = jsonString.replace("'", "\"")
            return len(json.loads(jsonString))
        except Exception as e:
            pass
        return 0
            
    def get_metrics(self):
        self.metrics['plugin_version'] = PLUGIN_VERSION
        self.metrics['heartbeat_required'] = HEARTBEAT
        
        health_data = self.getData(self.host, self.port, "health", HEALTH_END_PATTERN, END_PATTERN, ERROR_PATTERN)
        if str(health_data.strip()) == "health: up":
            self.metrics['health'] = 1
        else :
            self.metrics['health'] = 0
            
        stats_data = self.getData(self.host, self.port, "stats", END_PATTERN, ERROR_PATTERN)
        for stat in stats_data.split("\n"):
            try:
                data = stat.strip().split(":")
                if len(data) == 2:
                    self.metrics[data[0]] = float(data[1])
            except Exception as e :
                continue
            
        timer_data = self.getData(self.host, self.port, "timers", END_PATTERN, ERROR_PATTERN)
        self.metrics["timers.count"] = self.get_statsd_length(timer_data)
        counter_data = self.getData(self.host, self.port, "counters", END_PATTERN, ERROR_PATTERN)
        self.metrics["counters.count"] = self.get_statsd_length(counter_data)
        gauge_data = self.getData(self.host, self.port, "gauges", END_PATTERN, ERROR_PATTERN)
        self.metrics["gauges.count"] = self.get_statsd_length(gauge_data)
        
        return self.metrics
    
if __name__ == "__main__":
    config = {'host':host, 'port' : port}
    mon = statsd(config)
    metrics = mon.get_metrics()
    print(json.dumps(metrics))