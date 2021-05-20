#!/usr/bin/python

import json
import argparse

# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = 1

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

# Enter the host name configures for the Solr JMX
HOST_NAME = ""

# Enter the port configures for the Solr JMX
PORT = ""

# Enter the domain name configures for the Solr Instance
DOMAIN = ""

URL = ""
QUERY = ""

result_json = {}


METRIC_UNITS = {
    "document_cache_evictions": "evictions/second",
    "document_cache_hits": "hits/second",
    "document_cache_inserts": "sets/second",
    "document_cache_lookups": "gets/second",
    "filter_cache_evictions": "evictions/second",
    "filter_cache_hits": "hits/second",
    "filter_cache_inserts": "sets/second",
    "filter_cache_lookups": "gets/second",
    "query_result_cache_evictions": "evictions/second",
    "query_result_cache_hits": "hits/second",
    "query_result_cache_inserts": "sets/second",
    "query_result_cache_lookups": "gets/second",
    "query_requests": "requests/second",
    "query_timeouts": "responses/second",
    "query_errors": "count",
    "query_time": "milliseconds",
    "searcher_maxdoc": "documents",
    "searcher_numdocs": "documents",
    "searcher_warmup_time": "milliseconds",
    "query_request_times_50thpercent": "milliseconds",
    "query_request_times_75thpercent": "milliseconds",
    "query_request_times_95thpercent": "milliseconds",
    "query_request_times_98thpercent": "milliseconds",
    "query_request_times_999thpercent": "milliseconds",
    "query_request_times_99thpercent": "milliseconds",
    "query_request_times_mean": "milliseconds",
    "query_request_times_mean_rate": "requests/second",
    "query_request_times_oneminuterate": "requests/second"
}


metric_map = {
    "maxDoc" : {
        "Value": "searcher_maxdoc",
    },
    "numDoc" : {
        "Value": "searcher_numdocs",
    },
    "warmupTime" : {
        "Value": "searcher_warmup_time",
    },
    "documentCache" : {
        "lookups" : "document_cache_lookups",
        "hits" : "document_cache_hits",
        "inserts" : "document_cache_inserts",
        "evictions" : "document_cache_evictions",
    },
    "queryResultCache" : {
        "lookups" : "query_result_cache_lookups",
        "hits" : "query_result_cache_hits",
        "inserts" : "query_result_cache_inserts",
        "evictions" : "query_result_cache_evictions",
    },
    "filterCache" : {
        "lookups" : "filter_cache_lookups",
        "hits" : "filter_cache_hits",
        "inserts" : "filter_cache_inserts",
        "evictions" : "filter_cache_evictions",
    },
    "requests" : {
        "Count": "query_requests",
    },
    "timeouts" : {
        "Count": "query_timeouts",
    },
    "errors" : {
        "Count": "query_errors",
    },
    "totalTime" : {
        "Count": "query_time",
    },
    "requestTimes" : {
        "Mean" : "query_request_times_mean",
        "MeanRate" : "query_request_times_mean_rate",
        "50thPercentile" : "query_request_times_50thpercent",
        "75thPercentile" : "query_request_times_75thpercent",
        "95thPercentile" : "query_request_times_95thpercent",
        "98thPercentile" : "query_request_times_98thpercent",
        "99thPercentile" : "query_request_times_99thpercent",
        "999thPercentile" : "query_request_times_999thpercent",
        "OneMinuteRate" : "query_request_times_oneminuterate",
    },
}


# JMX Query is executed and getting the Performance metric data after filtering the output
def get_metrics_from_jmx(jmxconnection, QUERY, javax, metric_arg):
    result = {}
    try:
        for metric in metric_arg:
            output = jmxconnection.getAttribute(javax.management.ObjectName(QUERY), metric)
            result[metric_arg[metric]] = output

    except Exception as e:
        result["status"] = 0
        result["msg"] = str(e)

    return result


# JMX url is defined and JMX connection is established, Query and metric keys are passed to process
def get_output():
    result = {}
    URL = "service:jmx:rmi:///jndi/rmi://" + HOST_NAME + ":" + PORT + "/jmxrmi"
    try:
        import jpype
        from jpype import java
        from jpype import javax
        
        jpype.startJVM(convertStrings=False)
        
        jhash = java.util.HashMap()
        jmxurl = javax.management.remote.JMXServiceURL(URL)
        jmxsoc = javax.management.remote.JMXConnectorFactory.connect(jmxurl, jhash)
        jmxconnection = jmxsoc.getMBeanServerConnection()
        
        QUERY = "solr:dom1=core,dom2=" + DOMAIN + ",category=SEARCHER,scope=searcher,name=maxDoc"
        result = get_metrics_from_jmx(jmxconnection, QUERY, javax, metric_map["maxDoc"])

        QUERY = "solr:dom1=core,dom2=" + DOMAIN + ",category=SEARCHER,scope=searcher,name=numDocs"
        result.update(get_metrics_from_jmx(jmxconnection, QUERY, javax, metric_map["numDoc"]))
            
        QUERY = "solr:dom1=core,dom2=" + DOMAIN + ",category=SEARCHER,scope=searcher,name=warmupTime"
        result.update(get_metrics_from_jmx(jmxconnection, QUERY, javax, metric_map["warmupTime"]))
            
        QUERY = "solr:dom1=core,dom2=" + DOMAIN + ",category=CACHE,scope=searcher,name=documentCache"
        result.update(get_metrics_from_jmx(jmxconnection, QUERY, javax, metric_map["documentCache"]))
        
        QUERY = "solr:dom1=core,dom2=" + DOMAIN + ",category=CACHE,scope=searcher,name=queryResultCache"
        result.update(get_metrics_from_jmx(jmxconnection, QUERY, javax, metric_map["queryResultCache"]))
        
        QUERY = "solr:dom1=core,dom2=" + DOMAIN + ",category=CACHE,scope=searcher,name=filterCache"
        result.update(get_metrics_from_jmx(jmxconnection, QUERY, javax, metric_map["filterCache"]))
        
        QUERY = "solr:dom1=core,dom2=" + DOMAIN + ",category=QUERY,scope=/query,name=requestTimes"
        result.update(get_metrics_from_jmx(jmxconnection, QUERY, javax, metric_map["requestTimes"]))
        
        QUERY = "solr:dom1=core,dom2=" + DOMAIN + ",category=QUERY,scope=/query,name=requests"
        result.update(get_metrics_from_jmx(jmxconnection, QUERY, javax, metric_map["requests"]))
        
        QUERY = "solr:dom1=core,dom2=" + DOMAIN + ",category=QUERY,scope=/query,name=timeouts"
        result.update(get_metrics_from_jmx(jmxconnection, QUERY, javax, metric_map["timeouts"]))
        
        QUERY = "solr:dom1=core,dom2=" + DOMAIN + ",category=QUERY,scope=/query,name=errors"
        result.update(get_metrics_from_jmx(jmxconnection, QUERY, javax, metric_map["errors"]))
        
        QUERY = "solr:dom1=core,dom2=" + DOMAIN + ",category=QUERY,scope=/query,name=totalTime"
        result.update(get_metrics_from_jmx(jmxconnection, QUERY, javax, metric_map["totalTime"]))

    except Exception as e:
        result["status"] = 0
        result["msg"] = str(e)

    return result


# arguments are parsed from solr.cfg file and assigned with the variables
if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--host_name', help="solr host_name", type=str)
    parser.add_argument('--port', help="solr port", type=str)
    parser.add_argument('--domain_name', help="solr domain", type=str)
    args = parser.parse_args()
    if args.host_name:
        HOST_NAME = args.host_name
    if args.port:
        PORT = args.port
    if args.domain_name:
        DOMAIN = args.domain_name

    result_json = get_output()

    result_json['plugin_version'] = PLUGIN_VERSION
    result_json['heartbeat_required'] = HEARTBEAT
    result_json['units'] = METRIC_UNITS

    print(json.dumps(result_json, indent=4, sort_keys=True))
