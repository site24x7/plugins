#!/usr/bin/python3
import argparse
import psycopg2
import json
import traceback
from decimal import Decimal

PLUGIN_VERSION = "1"
HEARTBEAT = "true"
data = {
    'plugin_version': PLUGIN_VERSION,
    'heartbeat_required': HEARTBEAT
}

def convert_decimal(obj):
    if isinstance(obj, dict):
        return {key: convert_decimal(value) for key, value in obj.items()}
    elif isinstance(obj, list):
        return [convert_decimal(item) for item in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    return obj

class YugabyteDB:
    
    def __init__(self, args):
        self.host = args.hostname
        self.username = args.username
        self.password = args.password
        self.port = args.port
        self.connection = None

    def connect_db(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                user=self.username,
                password=self.password,
                port=self.port
            )
        except Exception as e:
            data['status'] = 0
            data['msg'] = str(e)
            return False
        return True
    
    def metric_collector(self):
        if not self.connect_db():
            return data
        
        try:
            cursor = self.connection.cursor()
            
            cursor.execute("SHOW server_version;")
            data['YugabyteDB_Version'] = cursor.fetchone()[0]
            
            cursor.execute("""
                SELECT COUNT(*) 
                FROM pg_stat_activity 
                WHERE state = 'active';
            """)
            data['Active_Sessions'] = cursor.fetchone()[0] if cursor.rowcount > 0 else 0
            
            cursor.execute("SELECT count(*) FROM pg_stat_activity;")
            data['Total_Connection'] = cursor.fetchone()[0] if cursor.rowcount > 0 else 0
            
            cursor.execute("""
                SELECT 
                    datname AS name,
                    pg_size_pretty(pg_database_size(datname)) AS database_size,
                    numbackends AS active_connections,
                    xact_commit AS transactions_committed,
                    xact_rollback AS transactions_rolledback,
                    CASE WHEN blks_hit + blks_read > 0 THEN 
                        round(100 * blks_hit / (blks_hit + blks_read), 2)
                    ELSE 
                        NULL 
                    END AS cache_hit_ratio
                FROM pg_stat_database;
            """)
            
            db_details = []
            for db in cursor.fetchall():
                db_info = {
                    "name": db[0],
                    "Database_Size_in_bytes": db[1].split()[0] if db[1] else 0,
                    "Active_Connections": db[2] if db[2] else 0, 
                    "Transactions_Committed": db[3] if db[3] else 0,
                    "Transactions_Rolledback": db[4] if db[4] else 0,
                    "Cache_Hit_Ratio": db[5] if db[5] is not None else 0
                }
                db_details.append(db_info)
            
            data['Database_Details'] = db_details
            
            cursor.execute("""
                SELECT count(*) AS locks_count
                FROM pg_locks
                WHERE granted = true;
            """)
            data['Database_Locks'] = cursor.fetchone()[0] if cursor.rowcount > 0 else 0
            
            cursor.execute("""
                SELECT AVG(total_time) AS avg_query_time
                FROM pg_stat_statements;
            """)
            data['Avg_Query_Time'] = cursor.fetchone()[0] if cursor.rowcount > 0 else 0
            
            cursor.execute("""
                SELECT pg_size_pretty(pg_total_relation_size('pg_stat_activity')) AS total_disk_usage;
            """)
            total_disk_usage = cursor.fetchone()[0] if cursor.rowcount > 0 else '0 bytes'
            data['Total_Disk_Usage'] = 0 if total_disk_usage == '0 bytes' else total_disk_usage
            
            cursor.execute("""
                SELECT sum(calls) AS total_queries
                FROM pg_stat_statements;
            """)
            data['Throughput'] = cursor.fetchone()[0] if cursor.rowcount > 0 else 0

            cursor.execute("""
                SELECT sum(total_time) / sum(calls) AS avg_query_time
                FROM pg_stat_statements;
            """)
            data['Avg_Query_Time'] = cursor.fetchone()[0] if cursor.rowcount > 0 else 0
            
            cursor.execute("""
                SELECT sum(calls) AS total_queries
                FROM pg_stat_statements;
            """)
            data['Total_Queries'] = cursor.fetchone()[0] if cursor.rowcount > 0 else 0
        
        except Exception as e:
            data['status'] = 0
            data['msg'] = str(e)
        
        finally:
            cursor.close()
            self.connection.close()
            
        data['tabs'] = {
            'Database Metrics': {
                'order': 1,
                'tablist': ["Database_Details"]
            }
        }
        
        return convert_decimal(data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True, help='Username for YugabyteDB')
    parser.add_argument('--password', required=True, help='Password for YugabyteDB')
    parser.add_argument('--hostname', default='localhost', help='Host for YugabyteDB')
    parser.add_argument('--port', default='5433', help='Port for YugabyteDB')
    
    args = parser.parse_args()
    try:
        yugabyte_plugin = YugabyteDB(args)
        result = yugabyte_plugin.metric_collector()
    
    except Exception as e:
        result = data
        result['status'] = 0
        result['msg'] = str(traceback.format_exc())
    
    print(json.dumps(result, indent=4))
