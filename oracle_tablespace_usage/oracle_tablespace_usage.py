#!/usr/bin/python
"""

Site24x7 Oracle DB Plugin

"""

import json


# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication
# problem while posting plugin data to server
HEARTBEAT = "true"

# Config Section: Enter your configuration details to connect to the oracle database
ORACLE_HOST = "hostname"

ORACLE_PORT = "1521"

ORACLE_SID = "XE"

ORACLE_USERNAME = "sys"

ORACLE_PASSWORD = "test"

TABLESPACE_NAME = ["SYSTEM","USERS","SYSAUX"]  ####Edit this field and add the names of the tablespaces to be monitored. Names are separated by comma

# Mention the units of your metrics . If any new metrics are added, make an entry here for its unit if needed.
METRICS_UNITS = {'usage': '%'}


class Oracle(object):
    def __init__(self, config):
        self.configurations = config
        self.connection = None
        self.host = self.configurations.get('host', 'localhost')
        self.port = int(self.configurations.get('port', '1521'))
        self.sid = self.configurations.get('sid', 'XE')
        self.username = self.configurations.get('user', 'sys')
        self.password = self.configurations.get('password', 'admin')
        self.data = {'plugin_version': PLUGIN_VERSION, 'heartbeat_required': HEARTBEAT}
        units ={}
        for name in TABLESPACE_NAME:
        	units[name+'_usage'] = METRICS_UNITS['usage']
        self.data['units']=units

    def metricCollector(self):
        c=None
        conn=None
        try:
            import cx_Oracle
        except Exception as e:
            self.data['status'] = 0
            self.data['msg'] = str(e)
            return self.data

        try:
            dsnStr = cx_Oracle.makedsn(self.host, self.port, self.sid)
            conn = cx_Oracle.connect(user=self.username, password=self.password, dsn=dsnStr, mode=cx_Oracle.SYSDBA)
            c = conn.cursor()
            
            c.execute("select distinct NVL(rtrim(ltrim(to_char(used.used_bytes/total.total_bytes * 100, '999.99'))),0) usage,df.tablespace_name as name,df.status as status from sys.dba_tablespaces df,(select de.tablespace_name as name2, sum(de.bytes) used_bytes from dba_extents de group by de.tablespace_name) used,(select dd.tablespace_name as name1,sum(dd.bytes) total_bytes from sys.dba_data_files dd group by dd.tablespace_name) total where df.tablespace_name = used.name2(+) and df.tablespace_name=total.name1(+)")
            for row in c:
            	usage, name ,status= row
            	if name in TABLESPACE_NAME:
            		self.data[name+'_usage'] = usage
            		self.data[name+'_status'] = status

        except Exception as e:
            self.data['status'] = 0
            self.data['msg'] = str(e)
        finally:
            if c!= None : c.close()
            if conn != None : conn.close()
            return self.data
           
if __name__ == "__main__":
    configurations = {'host': ORACLE_HOST, 'port': ORACLE_PORT,
                      'user': ORACLE_USERNAME, 'password': ORACLE_PASSWORD, 'sid': ORACLE_SID}

    oracle_plugin = Oracle(configurations)

    result = oracle_plugin.metricCollector()

print(json.dumps(result, indent=4, sort_keys=True))
