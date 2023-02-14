#!/usr/bin/python3
import json
import re

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={'memory_free_pct':'%',
               'memory_used_bytes':'bytes'}

metrics={

    'namespace_num':[
        'dead_partitions',
        'memory_free_pct',
        'unavailable_partitions',
        'client_delete_error',
        'client_read_error',
        'client_udf_error',
        'client_write_error',
        'memory_used_bytes',
        'pi_query_aggr_error',
    ],

    'namespace_bool':[

        'clock_skew_stop_writes',
        'stop_writes',
        
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
        self.namespace=args.namespace

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
                'hosts': [hosts]
            }
            client = aerospike.client(config).connect(self.username,self.password)

            try:
                
                request = f"namespace/{self.namespace}"
                for node, (err, res) in list(client.info_all(request).items()):
                    if str(node)==self.node_id:
                        if res is not None:
                            for metric in metrics['namespace_num']:
                                data=re.findall(f'{metric}=[0-9]+',res)
                                if data!=[]:
                                    self.maindata[metric]=re.findall("[0-9]+",data[0])[0]

                            for metric in metrics['namespace_bool']:
                                data=re.findall(f"{metric}=(false|true);",res)
                                if data!=[]:
                                    self.maindata[metric]=data[0]
                client.close()

            except Exception as e:
                self.maindata['msg']=str(e)
                self.maindata['status']=0
                return self.maindata


        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return self.maindata
        
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
    
    hostname="localhost"
    port=3000
    username=None
    password=None
    node_id="BB90C7D8FE07440"
    namespace='test'

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
    parser.add_argument('--namespace', help='namespace of aerospike',default=namespace)

    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()

    obj=aero(args)

    result=obj.metriccollector()
    
    print(json.dumps(result,indent=True))
