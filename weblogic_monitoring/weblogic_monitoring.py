#!/usr/bin/python3
import json

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={
    "ThreadPoolPercentSocketReaders":"%",
    "BytesReceivedCount":"bytes",
    "BytesSentCount":"bytes",
    "HeapMemoryUsage":"bytes"
    }

class Weblogic:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS
        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path

        self.hostname=args.hostname
        self.port=args.port
        self.server_name=args.server_name
        self.username=args.username
        self.password=args.password
        

    
    def metriccollector(self):
        
        try:
            global jmx
            import jmxquery as jmx
            jmxConnection = jmx.JMXConnection(f"service:jmx:rmi:///jndi/rmi://{self.hostname}:{self.port}/jmxrmi",jmx_username=self.username,jmx_password=self.password)
            metric_queries={
                
                "OpenSocketsCurrentCount":f"com.bea:Name={self.server_name},Type=ServerRuntime/OpenSocketsCurrentCount",
                "OpenSocketTotalCount":f"com.bea:Name={self.server_name},Type=ServerRuntime/SocketsOpenedTotalCount",
                "ThreadPoolPercentSocketReaders":f"com.bea:Name={self.server_name},Type=Server/ThreadPoolPercentSocketReaders",
                "MaxOpenSockCount":f"com.bea:Name={self.server_name},Type=Server/MaxOpenSockCount",
                "CompletedRequestCount":f"com.bea:ServerRuntime={self.server_name},Name=ThreadPoolRuntime,Type=ThreadPoolRuntime/CompletedRequestCount",
                "ExecuteThreadIdleCount":f"com.bea:ServerRuntime={self.server_name},Name=ThreadPoolRuntime,Type=ThreadPoolRuntime/ExecuteThreadIdleCount",
                "ExecuteThreadTotalCount":f"com.bea:ServerRuntime={self.server_name},Name=ThreadPoolRuntime,Type=ThreadPoolRuntime/ExecuteThreadTotalCount",
                "PendingUserRequestCount":f"com.bea:ServerRuntime={self.server_name},Name=ThreadPoolRuntime,Type=ThreadPoolRuntime/PendingUserRequestCount",
                "HoggingThreadCount":f"com.bea:ServerRuntime={self.server_name},Name=ThreadPoolRuntime,Type=ThreadPoolRuntime/HoggingThreadCount",
                "OverloadRejectedRequestsCount":f"com.bea:ServerRuntime={self.server_name},Name=ThreadPoolRuntime,Type=ThreadPoolRuntime/OverloadRejectedRequestsCount",
                "QueueLength":f"com.bea:ServerRuntime={self.server_name},Name=ThreadPoolRuntime,Type=ThreadPoolRuntime/QueueLength",
                "SharedCapacityForWorkManagers":f"com.bea:ServerRuntime={self.server_name},Name=ThreadPoolRuntime,Type=ThreadPoolRuntime/SharedCapacityForWorkManagers",
                "StandbyThreadCount":f"com.bea:ServerRuntime={self.server_name},Name=ThreadPoolRuntime,Type=ThreadPoolRuntime/StandbyThreadCount",
                "StuckThreadCount":f"com.bea:ServerRuntime={self.server_name},Name=ThreadPoolRuntime,Type=ThreadPoolRuntime/StuckThreadCount",
                "ThreadPoolRuntimeThroughput":f"com.bea:ServerRuntime={self.server_name},Name=ThreadPoolRuntime,Type=ThreadPoolRuntime/Throughput",
                "JMSConnectionsCurrentCount":f"com.bea:ServerRuntime={self.server_name},Name={self.server_name}.jms,Type=JMSRuntime/ConnectionsCurrentCount",
                "JMSConnectionsTotalCount":f"com.bea:ServerRuntime={self.server_name},Name={self.server_name}.jms,Type=JMSRuntime/ConnectionsTotalCount",
                "JMSServersTotalCount":f"com.bea:ServerRuntime={self.server_name},Name={self.server_name}.jms,Type=JMSRuntime/JMSServersTotalCount",
                "PendingRequests":f"com.bea:ServerRuntime={self.server_name},Name=weblogic.kernel.Default,Type=WorkManagerRuntime/PendingRequests",
                "CompletedRequests":f"com.bea:ServerRuntime={self.server_name},Name=weblogic.kernel.Default,Type=WorkManagerRuntime/CompletedRequests",
                "StuckThreadCount":f"com.bea:ServerRuntime={self.server_name},Name=weblogic.kernel.Default,Type=WorkManagerRuntime/StuckThreadCount",
                "BytesReceivedCount":f"com.bea:ServerRuntime={self.server_name},Name=Default[http][1],Type=ServerChannelRuntime/BytesReceivedCount",
                "BytesSentCount":f"com.bea:ServerRuntime={self.server_name},Name=Default[http][1],Type=ServerChannelRuntime/BytesSentCount",
                "MessagesReceivedCount":f"com.bea:ServerRuntime={self.server_name},Name=Default[http][1],Type=ServerChannelRuntime/MessagesReceivedCount",
                "MessagesSentCount":f"com.bea:ServerRuntime={self.server_name},Name=Default[http][1],Type=ServerChannelRuntime/MessagesSentCount",
                "ProcessCpuLoad":f"java.lang:type=OperatingSystem/ProcessCpuLoad",
                "SystemCpuLoad":f"java.lang:type=OperatingSystem/SystemCpuLoad",
                "HeapMemoryUsage":"java.lang:type=Memory/HeapMemoryUsage",
                "HealthState":f"com.bea:Name={self.server_name},Type=ServerRuntime/HealthState"

            }
            for metric in metric_queries:
                    
                jmxQuery = [jmx.JMXQuery(metric_queries[metric])]
                metric_result = jmxConnection.query(jmxQuery)
                if metric in ["MaxOpenSockCount","ExecuteThreadIdleCount","ExecuteThreadTotalCount","SharedCapacityForWorkManagers"]:
                    self.maindata[metric]="count : "+str(metric_result[0].value)
                else:
                    self.maindata[metric]=metric_result[0].value



            applog={}
            if(self.logsenabled in ['True', 'true', '1']):
                    applog["logs_enabled"]=True
                    applog["log_type_name"]=self.logtypename
                    applog["log_file_path"]=self.logfilepath
            else:
                    applog["logs_enabled"]=False
            self.maindata['applog'] = applog

        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return self.maindata

        return self.maindata




if __name__=="__main__":
    
    hostname="127.0.0.1"
    port="9010"
    server_name="AdminServer"
    username=None
    password=None

    import argparse
    parser=argparse.ArgumentParser()

    parser.add_argument('--hostname', help='host_name of weblogic',default=hostname)
    parser.add_argument('--port', help='port number of weblogic',default=port)
    parser.add_argument('--server_name', help='server_name of weblogic',default=server_name)
    parser.add_argument('--username', help='username for weblogic',default=username)
    parser.add_argument('--password', help='password for weblogic',default=password)

    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    obj=Weblogic(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))