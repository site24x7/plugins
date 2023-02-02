#!/usr/bin/python3
import json

PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={}

class appname:

    def __init__(self,args):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS

        self.db_name=args.db_name
        self.username=args.username
        self.password=args.password
        self.hostname=args.hostname
        self.port=args.port
        self.query=args.query
        
    def metriccollector(self):
        
        try:
            import psycopg2

        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return self.maindata

        try:
            connection = psycopg2.connect(user=self.username,
                                  password=self.password,
                                  host=self.hostname,
                                  port=self.port,
                                  database=self.db_name)

            cursor=connection.cursor()

            try:
                cursor.execute(self.query)
                colnames = [desc[0] for desc in cursor.description]
                
                tot=len(colnames)
                data=cursor.fetchone()
                for i in range(tot):
                    self.maindata[colnames[i]]=str(data[i])
                    


            except Exception as e:
                self.maindata['msg']=str(e)
                self.maindata['status']=0
                return self.maindata
        
        except Exception as e:
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return self.maindata

        return self.maindata

if __name__=="__main__":

    DB = 'postgres'                 
    USERNAME = 'suraj'       
    PASSWORD = 'suraj'
    HOSTNAME = 'localhost'            
    PORT = 5432 
    QUERY="SELECT buffers_checkpoint, buffers_backend, maxwritten_clean, checkpoints_req, checkpoints_timed, buffers_alloc FROM pg_stat_bgwriter;"

    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--db_name', help='name of db',default=DB)
    parser.add_argument('--username', help='name of username',default=USERNAME)
    parser.add_argument('--password', help='password of db',default=PASSWORD)
    parser.add_argument('--hostname', help='name of hostname',default=HOSTNAME)
    parser.add_argument('--port', help='port of postgres',default=PORT)
    parser.add_argument('--query',help='query of the metric', default=QUERY)
    args=parser.parse_args()
    obj=appname(args)

    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
