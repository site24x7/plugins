#!/usr/bin/python3
import json
import re

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={
    'system_free_mem_kbytes':'kb',
    'system_free_mem_pct':'%',
    'heap_efficiency_pct':'%'
}

metrics={
    'statistics':[  
                    'client_connections',
                    'client_connections_opened',
                    'cluster_size',
                    'fabric_connections_opened',
                    'heartbeat_connections_opened',
                    'system_free_mem_kbytes',
                    'system_free_mem_pct',
                    'batch_index_error',
                    'heap_efficiency_pct',
                    'rw_in_progress'
                ]
}

class aero:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS
        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path

        self.username=args.username
        self.password=args.password
        self.hostname=args.hostname
        self.port=args.port
        self.node_id=args.node_id

        # tls details
        self.tls_enable=args.tls_enable
        self.tls_name=args.tls_name
        self.cafile=args.cafile

    def metriccollector(self):
        try:
            import aerospike 

        except Exception as e:
            self.maindata['msg']=str(e) 
            self.maindata['status']=0
        
        try:

            if self.tls_enable=='true':
                tls_config={
                    'cafile':self.cafile,
                    'enable':True
                }

                hosts=(self.hostname,self.port,self.tls_name)
            else:
                hosts=(self.hostname,self.port)

            config = {
                'hosts': [hosts],
            }
            client = aerospike.client(config).connect(self.hostname, self.port)
            try:
                
                request = "statistics"
                for node, (err, res) in list(client.info_all(request).items()):
                    if str(node)==self.node_id:
                        if res is not None:
                            for metric in metrics['statistics']:
                                data=re.findall(f'{metric}=[0-9]+',res)
                                self.maindata[metric]=re.findall("[0-9]+",data[0])[0]

                client.close()
            except Exception as e:
                self.maindata['msg']=str(e)
                self.maindata['status']=0

        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0

        applog={}
        if(self.logsenabled in ['True', 'true', '1']):
                applog["logs_enabled"]=True
                applog["log_type_name"]=self.logtypename
                applog["log_file_path"]=self.logfilepath
        else:
                applog["logs_enabled"]=False
        self.maindata['applog'] = applog

        return self.maindata


if __name__=="__main__":
    
    hostname="127.0.0.1"
    port=3000
    username=None
    password=None
    node_id=None

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--tls_enable', help='tls enable (true or false)',default="false")
    parser.add_argument('--tls_name', help='tls name of aerospike',default=None)
    parser.add_argument('--cafile', help='cafile path for tls',default=None)
    parser.add_argument('--hostname', help='hostname of aerospike',default=hostname)
    parser.add_argument('--port', help='port number for aerospike',default=port)
    parser.add_argument('--username', help='username for aerospike',default=username)
    parser.add_argument('--password', help='password for aerospike',default=password)
    parser.add_argument('--node_id', help='node id of aerospike',default=node_id)

    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    obj=aero(args)

    result=obj.metriccollector()
    
    print(json.dumps(result,indent=True))


