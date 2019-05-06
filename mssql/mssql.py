#!/usr/bin/env python

import json
import time

DRIVER='FreeTDS'
SERVER='localhost'
USER='S24X7PLUGIN'
PASSWORD='S24x7PLUGIN'
DATABASE='TESTDB'
PORT=1433



COUNTER = {}
### Raw Counter variables
COUNTER['Data File(s) Size (KB)'] = {'KEY' :'Datefile Size' , 'UNIT' : 'KB'}
COUNTER['Percent Log Used'] = {'KEY' :'Log Used' , 'UNIT' : '%'}
COUNTER['Active Transactions'] = {'KEY' :'Active Transactions' , 'UNIT' : 'count'}
COUNTER['Log Growths'] = {'KEY' :'Log Growths' , 'UNIT' : 'count'}
COUNTER['Log Shrinks'] = {'KEY' :'Log Shrinks' , 'UNIT' : 'count'}
COUNTER['Log Truncations'] = {'KEY' :'Log Truncations' , 'UNIT' : 'count'}

### Processed counter variables
COUNTER['Transactions per sec'] = {'KEY' :'Transactions' , 'UNIT' : 'per sec'}
COUNTER['Log Cache Hit Ratio'] = {'KEY' :'Log Cache Hit Ratio' , 'UNIT' : ''}
COUNTER['Log Flushes per sec'] = {'KEY' :'Log Flushes' , 'UNIT' : 'per sec'}

class MsSql():
    def __init__(self):
        self.data = {}
        self.unit = {}
        self.connect()
    
    def _get_raw_counter_values(self, cur) :
        cur.execute("SELECT counter_name,cntr_value FROM sysperfinfo WHERE counter_name IN('Data File(s) Size (KB)' ,'Percent Log Used', 'Active Transactions', 'Log Growths', 'Log Shrinks', 'Log Truncations') AND instance_name='" + DATABASE + "'; ")
        for row in cur:
            if row.counter_name.strip() in COUNTER : 
                key = COUNTER[row.counter_name.strip()]
                self.data[key['KEY']]  = str(row.cntr_value)
                self.unit[key['KEY']] = key['UNIT']

    def _transactions_per_sec(self, cur):
        value = 0
        cur.execute("SELECT cntr_value FROM sysperfinfo WHERE counter_name='Transactions/sec' AND instance_name='" + DATABASE + "';")
        begin = cur.fetchone()[0]
        time.sleep(3)
        cur.execute("SELECT cntr_value FROM sysperfinfo WHERE counter_name='Transactions/sec' AND instance_name='" + DATABASE + "';")
        value = ( cur.fetchone()[0] - begin ) / 3
        key = COUNTER['Transactions per sec'];
        self.data[key['KEY']] = value
        self.unit[key['KEY']] = key['UNIT']

    def _log_cache_hit_ratio(self, cur):
        value = 0
        cur.execute("SELECT cntr_value FROM sysperfinfo WHERE counter_name='Log Cache Hit Ratio' AND instance_name='" + DATABASE + "';")
        top = cur.fetchone()[0]
        cur.execute("SELECT cntr_value FROM sysperfinfo WHERE counter_name='Log Cache Hit Ratio Base' AND instance_name='" + DATABASE + "';")
        bot = cur.fetchone()[0]
        if bot == 0: value = 0
        else: value = (float(top) / bot) * 100
        key = COUNTER['Log Cache Hit Ratio']
        self.data[key['KEY']] = value
        self.unit[key['KEY']] = key['UNIT']

    def _log_flushes_per_sec(self, cur):
        value = 0
        cur.execute("SELECT cntr_value FROM sysperfinfo WHERE counter_name='Log Flushes/sec' AND instance_name='" + DATABASE + "';")
        begin = cur.fetchone()[0]
        time.sleep(3)
        cur.execute("SELECT cntr_value FROM sysperfinfo WHERE counter_name='Log Flushes/sec' AND instance_name='" + DATABASE + "';")
        value = ( cur.fetchone()[0] - begin ) / 3
        key = COUNTER['Log Flushes per sec']
        self.data[key['KEY']] = value
        self.unit[key['KEY']] = key['UNIT']

    def connect(self):
        conn = None
        try:
            import pyodbc
            begin = time.time()
            conn = pyodbc.connect("DRIVER=%s;SERVER=%s;PORT=%s;DATABASE=%s;UID=%s;PWD=%s" % (DRIVER,SERVER,PORT,DATABASE,USER,PASSWORD))
            end   = time.time()
            self.data['Time to Connect'] = round( end - begin , 3 )

            cur = conn.cursor()
            
            ##Raw counter values
            self._get_raw_counter_values(cur)

            ##Transactions per sec
            self._transactions_per_sec(cur)

            ##Log Cache Hit Ratio
            self._log_cache_hit_ratio(cur)

            ##Log Flushes Per Second
            self._log_flushes_per_sec(cur)
            
        except Exception as e :
            self.data['msg'] = str(e)
        finally : 
            if conn is not None : conn.close()
            self.data['units'] = self.unit
if __name__ == '__main__':
    mssql = MsSql()
    print(json.dumps(mssql.data, indent=4, sort_keys=True))
