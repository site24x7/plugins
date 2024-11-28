#!/usr/bin/python3
import json
import os
import time
import warnings
warnings.filterwarnings("ignore")

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={'execution_time':'ms'}


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
        
        self.query = self.read_query_from_file()
        
        
    def read_query_from_file(self):
        """Read the query from the query.sql file."""
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            query_file_path = os.path.join(script_dir, 'query.sql')

            with open(query_file_path, 'r') as file:
                return file.read().strip()
        except Exception as e:
            self.maindata['status'] = 0
            self.maindata['msg'] = f"Failed to read query from file: {str(e)}"
            return None


    def metriccollector(self):
        
        try:
            import oracledb
        except Exception as e:
            self.maindata['status'] = 0
            self.maindata['msg'] = str(e)
            return self.maindata

        try:
            start_time=time.time()

            try:
                conn = oracledb.connect(user=self.username, password=self.password, dsn=f"{self.hostname}:{self.port}/{self.sid}")
                c = conn.cursor()
            except Exception as e:
                self.maindata['status']=0
                self.maindata['msg']='Exception while making connection: '+str(e)
                return self.maindata

            c.execute(self.query)
            col_names = [row[0] for row in c.description]
            tot_cols=len(col_names)            

            for row in c:
                for i in range(tot_cols):
                    self.maindata[col_names[i]]=row[i]
                break
            self.maindata['tags']=f"oracle_hostname:{self.hostname},oracle_sid:{self.sid}"
            end_time=time.time()
            total_time=(end_time-start_time) * 1000
            self.maindata['execution_time']="%.3f" % total_time 


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
    oracle_home='/opt/oracle/product/19c/dbhome_1'
    
    import argparse
    parser=argparse.ArgumentParser()

    parser.add_argument('--hostname', help='hostname for oracle',default=hostname)
    parser.add_argument('--port', help='port number for oracle',default=port)
    parser.add_argument('--sid', help='sid for oracle',default=sid)
    parser.add_argument('--username', help='username for oracle',default=username)
    parser.add_argument('--password', help='password for oracle',default=password)
    parser.add_argument('--oracle_home',help='oracle home path',default=oracle_home)

    args=parser.parse_args()
    os.environ['ORACLE_HOME']=args.oracle_home
    obj=oracle(args)
    

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
