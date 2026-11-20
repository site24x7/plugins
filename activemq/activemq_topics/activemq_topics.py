#!/usr/bin/python3
import json
import socket
import ipaddress

PLUGIN_VERSION=1
HEARTBEAT=True

ACTIVEMQ_TOPICS_LOGS_LOG_TYPE_NAME = "ActiveMQ Logs"

METRICS_UNITS={
     
     "AverageBlockedTime":"ms",
     "AverageEnqueueTime":"ms",
     "AverageMessageSize":"bytes",
     "BlockedProducerWarningInterval":"ms",
     "MaxEnqueueTime":"ms",
     "MaxMessageSize":"bytes",
     "MaxPageSize":"bytes",
     "MemoryLimit":"bytes",
     "MemoryPercentUsage":"%",
     "MinEnqueueTime":"ms",
     "MinMessageSize":"bytes",
     "QueueSize":"bytes",
     "StoreMessageSize":"bytes",
     "TotalBlockedTime":"ms"
}

metrics={   
            "AlwaysRetroactive":"Always Retroactive", 
            "AverageBlockedTime":"Average Blocked Time", 
            "AverageEnqueueTime":"Average Enqueue Time", 
            "AverageMessageSize":"Average Message Size", 
            "BlockedProducerWarningInterval":"Blocked Producer Warning Interval", 
            "BlockedSends":"Blocked Sends", 
            "ConsumerCount":"Consumer Count", 
            "DLQ":"DLQ", 
            "DequeueCount":"Dequeue Count",
            "DispatchCount":"Dispatch Count", 
            "DuplicateFromStoreCount":"Duplicate From Store Count",
            "EnqueueCount":"Enqueue Count",
            "ExpiredCount":"Expired Count",
            "ForwardCount":"Forward Count",
            "InFlightCount":"In Flight Count",
            "MaxAuditDepth":"Max Audit Depth",
            "MaxEnqueueTime":"Max Enqueue Time",
            "MaxMessageSize":"Max Message Size",
            "MaxPageSize":"Max Page Size",
            "MaxProducersToAudit":"Max Producers To Audit",
            "MemoryLimit":"Memory Limit",
            "MemoryPercentUsage":"Memory Percent Usage",
            "MemoryUsageByteCount":"Memory Usage Byte Count",
            "MemoryUsagePortion":"Memory Usage Portion",
            "MinEnqueueTime":"Min Enqueue Time",
            "MinMessageSize":"Min Message Size",
            "PrioritizedMessages":"Prioritized Messages",
            "ProducerCount":"Producer Count",
            "ProducerFlowControl":"Producer Flow Control",
            "QueueSize":"Queue Size",
            "SendDuplicateFromStoreToDLQ":"Send Duplicate From Store To DLQ",
            "StoreMessageSize":"Store Message Size",
            "TempUsageLimit":"Temp Usage Limit",
            "TempUsagePercentUsage":"Temp Usage Percent Usage",
            "TotalBlockedTime":"Total Blocked Time",
            "UseCache":"Use Cache"
            }

def resolve_ip_address(host):
    if not host:
        return host
    if host == "localhost":
        return "localhost"
    try:
        ipaddress.ip_address(host)
        return host
    except ValueError:
        pass
    try:
        return socket.gethostbyname(host)
    except Exception:
        return host

class appname:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS
        self.logsenabled=args.activemq_topics_logs_enabled
        self.logfilepath=args.activemq_topics_logs_file_path
        
        self.hostname=args.hostname
        self.port=args.port
        self.broker_name=args.broker_name
        self.topic_name=args.topic_name


    def mbean_attributes(self,jmxconnection, QUERY, javax, metric_arg):
    
        result = {}
        try:
            for metric in metric_arg:
                output = jmxconnection.getAttribute(javax.management.ObjectName(QUERY), metric)
                result[metric_arg[metric]] = output
        except Exception as e:
            if "javax.management.AttributeNotFoundException: No such attribute" in str(e):
              pass
            else:
              result["status"] = 0
              result["msg"] = str(e)
        return result


    def metriccollector(self):
        try:
            try:
                import jpype
                from jpype import java
                from jpype import javax

            except Exception as e:
                self.maindata['msg']=str(e)
                self.maindata['status']=0
                return self.maindata
            
            URL = "service:jmx:rmi:///jndi/rmi://" + self.hostname + ":" + self.port + "/jmxrmi"
            jpype.startJVM(convertStrings=False)
            jhash = java.util.HashMap()
            jmxurl = javax.management.remote.JMXServiceURL(URL)
            jmxsoc = javax.management.remote.JMXConnectorFactory.connect(jmxurl, jhash)

            jmxconnection = jmxsoc.getMBeanServerConnection()

            query=f"org.apache.activemq:type=Broker,brokerName={self.broker_name},destinationType=Topic,destinationName={self.topic_name}"
            result=self.mbean_attributes(jmxconnection, query, javax, metrics)
            self.maindata.update(result)

        except Exception as e:            
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return self.maindata
    
        applog={}
        if(self.logsenabled in ['True', 'true', '1']):
                applog["logs_enabled"]=True
                applog["log_type_name"]=ACTIVEMQ_TOPICS_LOGS_LOG_TYPE_NAME
                applog["log_file_path"]=self.logfilepath
        else:
                applog["logs_enabled"]=False
        self.maindata['applog'] = applog
        self.maindata['s247config'] = {
            "ip_address": resolve_ip_address(self.hostname)
        }
        return self.maindata



if __name__=="__main__":

    hostname="localhost"
    port="1099"
    broker_name="localhost"
    topic_name="ActiveMQ.Advisory.MasterBroker"
    
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--activemq_topics_logs_enabled', help='enable log collection for ActiveMQ logs',default="False")
    parser.add_argument('--activemq_topics_logs_file_path', help='list of comma separated log file paths', nargs='?', default="/var/log/apache-activemq*/data/activemq*.log")
    parser.add_argument('--hostname', help='activemq hostname', nargs='?', default=hostname)
    parser.add_argument('--port', help='activemq port', nargs='?', default=port)
    parser.add_argument('--broker_name', help='activemq broker name', nargs='?', default=broker_name)
    parser.add_argument('--topic_name', help='activemq topic name', nargs='?', default=topic_name)

    args=parser.parse_args()

    obj=appname(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
