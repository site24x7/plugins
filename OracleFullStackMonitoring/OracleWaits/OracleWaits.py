#!/usr/bin/python3
import json
import os
import warnings
warnings.filterwarnings("ignore")

PLUGIN_VERSION=1
HEARTBEAT=True




class oracle:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT

        self.username=args.username
        self.password=args.password
        self.sid=args.sid
        self.hostname=args.hostname
        self.port=args.port
        self.tls=args.tls.lower()
        self.wallet_location=args.wallet_location

        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path
        




    def metriccollector(self):
        

        metric_queries={
            "query":"""
            select n.name , round(m.time_waited,3) time_waited, m.wait_count from v$eventmetric m, v$event_name n where m.event_id=n.event_id and n.name in 
            ( 'free buffer waits' ,
            'buffer busy waits',
            'latch free',
            'library cache pin',
            'library cache load lock',
            'log buffer space',
            'library object reloads count',
            'enqueue waits',
            'db file parallel read',
            'db file parallel write',
            'control file sequential read',
            'control file parallel write',
            'write complete waits',
            'log file sync',
            'sort segment request',
            'direct path read',
            'direct path write')
            
            """
        }


        try:
            import oracledb
            oracledb.init_oracle_client()

        except Exception as e:
            self.maindata['status'] = 0
            self.maindata['msg'] = str(e) + "\n Solution : Use the following command to install oracledb\n pip install oracledb \n(or)\n pip3 install oracledb"
            return self.maindata

        try:
            try:
                if self.tls=="True":
                    dsn=f"""   (DESCRIPTION=
                            (ADDRESS=(PROTOCOL=tcps)(HOST={self.hostname})(PORT={self.port}))
                            (CONNECT_DATA=(SERVICE_NAME={self.sid}))
                            (SECURITY=(MY_WALLET_DIRECTORY={self.wallet_location}))
                            (SECURITY=(SSL_SERVER_CERT_DN=ON))
                            )"""
                else:
                        dsn=f"{self.hostname}:{self.port}/{self.sid}"


                conn = oracledb.connect(user=self.username, password=self.password, dsn=dsn)
                c = conn.cursor()
            except Exception as e:
                self.maindata['status']=0
                self.maindata['msg']='Exception while making connection: '+str(e)
                return self.maindata
        
            units={}
            c.execute(metric_queries['query'])
            for row in c:
                name,time_waited,wait_count=row
                self.maindata[name+"_time_waited"]=time_waited/100
                units[name+"_time_waited"]='sec'
                self.maindata[name+"_wait_count"]=wait_count

            self.maindata['units']=units
            c.close()
            conn.close()
                

       

            applog={}
            if(self.logsenabled in ['True', 'true', '1']):
                    applog["logs_enabled"]=True
                    applog["log_type_name"]=self.logtypename
                    applog["log_file_path"]=self.logfilepath
            else:
                    applog["logs_enabled"]=False
            self.maindata['applog'] = applog
            self.maindata['tags']=f"oracle_hostname:{self.hostname},oracle_sid:{self.sid}"



        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0


        return self.maindata




if __name__=="__main__":
    
    hostname="localhost"
    port="1521"
    sid="ORCLCDB"
    username=None
    password=None
    tls="False"
    wallet_location=None
    oracle_home=None

    import argparse
    parser=argparse.ArgumentParser()

    parser.add_argument('--hostname', help='hostname for oracle',default=hostname)
    parser.add_argument('--port', help='port number for oracle',default=port)
    parser.add_argument('--sid', help='sid for oracle',default=sid)
    parser.add_argument('--username', help='username for oracle',default=username)
    parser.add_argument('--password', help='password for oracle',default=password)
    parser.add_argument('--tls', help='tls support for oracle',default=tls)
    parser.add_argument('--wallet_location', help='oracle wallet location',default=wallet_location)

    parser.add_argument('--oracle_home',help='oracle home path',default=oracle_home)


    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)
    args=parser.parse_args()
    os.environ['ORACLE_HOME']=args.oracle_home

    obj=oracle(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
