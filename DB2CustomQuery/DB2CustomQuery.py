#!/usr/bin/python3
import json
PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={}


class cdb2q:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS
        self.host=args.host
        self.port=args.port
        self.username=args.username
        self.password=args.password
        self.sample_db=args.sample_db
        self.query=args.query

        
    def metriccollector(self):
        try:
            try:
                import ibm_db
            except Exception as e:
                self.maindata['msg']=str(e)
                self.maindata['status']=0
                return self.maindata

            url="DATABASE="+self.sample_db+";HOSTNAME="+self.host+";PORT="+self.port+";PROTOCOL=TCPIP;UID="+self.username+";PWD="+self.password+";"
            db = ibm_db.connect(url, "", "")  
            self.connection = db
            stmt = ibm_db.exec_immediate(self.connection, query)
            result = ibm_db.fetch_both(stmt)
            for res in result:
                if isinstance(res,str):
                    self.maindata[res]=result[res]

                
        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return self.maindata

        return self.maindata



if __name__=="__main__":

    hostname='localhost'
    port='25000'
    username='db2inst1'
    password='db2inst1'
    sample_db='suraj'
    query='SELECT * FROM syscat.bufferpools'
    
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?', default= hostname)
    parser.add_argument('--port',help="Port",nargs='?', default= port)
    parser.add_argument('--username',help="username", default= username)
    parser.add_argument('--password',help="Password", default= password)
    parser.add_argument('--sample_db' ,help="Sample db",nargs='?', default= sample_db)
    parser.add_argument('--query' ,help="query to get data",nargs='?', default= query)

    args=parser.parse_args()
    obj=cdb2q(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
