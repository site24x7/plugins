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
        self.tablespace_names=json.loads(args.tablespace_names)
        self.tls=args.tls.lower()
        self.wallet_location=args.wallet_location

        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path
        

    def metriccollector(self):
        


        try:
            import oracledb
            oracledb.init_oracle_client()

        except Exception as e:
            self.maindata['status'] = 0
            self.maindata['msg'] = str(e) + "\n Solution : Use the following command to install oracledb\n pip install oracledb \n(or)\n pip3 install oracledb"
            return self.maindata

        try:
            units={}
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
        

            for name in self.tablespace_names:

                c.execute(f"select a.USED_PERCENT, b.STATUS from dba_tablespace_usage_metrics a join dba_tablespaces b on a.TABLESPACE_NAME=b.TABLESPACE_NAME where a.TABLESPACE_NAME='{name}'")                
                for row in c:
                    self.maindata[name+'_Usage_Percent']=row[0]
                    self.maindata[name+'_Status']=row[1]
                    units[name+'_Usage_Percent']="%"

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
    tablespace_names='["SYSTEM","USERS"]'
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
    parser.add_argument('--tablespace_names', help='tablespace_names for oracle',default=tablespace_names)
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
