#!/usr/bin/python3
import json
import os

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={}


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
        self.query=args.query


    def metriccollector(self):
        
        try:
            import cx_Oracle
        except Exception as e:
            self.maindata['status'] = 0
            self.maindata['msg'] = str(e)
            return self.maindata

        try:

            try:
                conn = cx_Oracle.connect(self.username,self.password,self.hostname+':'+str(self.port)+'/'+self.sid)
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
    query="select * from sitedata"
    oracle_home='/opt/oracle/product/19c/dbhome_1'

    import argparse
    parser=argparse.ArgumentParser()

    parser.add_argument('--hostname', help='hostname for oracle',default=hostname)
    parser.add_argument('--port', help='port number for oracle',default=port)
    parser.add_argument('--sid', help='sid for oracle',default=sid)
    parser.add_argument('--username', help='username for oracle',default=username)
    parser.add_argument('--password', help='password for oracle',default=password)
    parser.add_argument('--oracle_home',help='oracle home path',default=oracle_home)
    parser.add_argument('--query',help='oracle queries list',default=query)

    args=parser.parse_args()
    os.environ['ORACLE_HOME']=args.oracle_home
    obj=oracle(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))


