#!/usr/bin/python3
import json
import os
import warnings
warnings.filterwarnings("ignore")

PLUGIN_VERSION=1
HEARTBEAT=True

METRICS_UNITS={
    "Used Space":"mb",
    "Tablespace Size":"mb",
    "Used Percent":"%"
}



class oracle:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS

        self.username=args.username
        self.password=args.password
        self.sid=args.sid
        self.hostname=args.hostname
        self.port=args.port
        self.tablespace_name=args.tablespace_name
        self.tls=args.tls.lower()
        self.wallet_location=args.wallet_location

        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path
        

    def metriccollector(self):
        

        metric_queries={
                "tbsquery1":f"select * from dba_tablespace_usage_metrics where TABLESPACE_NAME='{self.tablespace_name}'",
                "tbsquery2":f"select CONTENTS,LOGGING,STATUS from dba_tablespaces where TABLESPACE_NAME='{self.tablespace_name}'"
                
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
                db_block_size=8192
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

            c.execute("select value from v$parameter where name = 'db_block_size'")
            for row in c:
                db_block_size=row[0]
                break

            c.execute(metric_queries['tbsquery1'])                
            for row in c:
                self.maindata['Name']=row[0]
                self.maindata['Used Space']=int(row[1])*int(db_block_size)/1024/1024
                self.maindata['Tablespace Size']=int(row[2])*int(db_block_size)/1024/1024
                self.maindata['Used Percent']=row[3]

            c.execute(metric_queries['tbsquery2'])                
            for row in c:
                self.maindata['Content']=row[0]
                self.maindata['Log']=row[1]
                self.maindata['TB_Status']=row[2]
                
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
    tablespace_name="SYSTEM"
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
    parser.add_argument('--tablespace_name', help='tablespace_name for oracle',default=tablespace_name)
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
