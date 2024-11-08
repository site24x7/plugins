#!/usr/bin/python3
import argparse
import psycopg2
import os
import glob
import json
import time
from datetime import datetime
import traceback

start_time = time.time()

PLUGIN_VERSION = "1"
HEARTBEAT = "true"
data = {}
data['plugin_version'] = PLUGIN_VERSION
data['heartbeat_required'] = HEARTBEAT

class YugabyteDB:
    
    def __init__(self, args):
        self.dbname = args.db
        self.host = args.hostname
        self.username = args.username
        self.password = args.password
        self.port = args.port
        self.connection = None
        self.current_file_path = os.path.dirname(os.path.abspath(__file__))
        self.log_file_path = self.current_file_path + "/query_output"
        self.base_path = self.log_file_path
    
    def format_timestamp(self, ts):
        """Format the timestamp to only include up to seconds."""
        return ts.strftime('%Y-%m-%d %H:%M:%S')
    
    def format_heading(self, heading):
        """Format the column heading."""
        words = heading.replace('_', ' ').split()
        return f"${''.join(word.capitalize() for word in words)}$"
    
    def read_file(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read(), True, ""
        except Exception as e:
            return "", False, str(e)
    
    def write_file(self, file_path, content):
        try:
            with open(file_path, 'w') as file:
                file.write(content)
            return True, ""
        except Exception as e:
            return False, str(e)

    def remove_old_files(self):
        try:
            pattern = self.base_path + "*"
            for filename in glob.glob(pattern):
                os.remove(filename)
            return True, ""
        except Exception as e:
            return False, str(e)
    
    def connect_db(self):
        try:
            self.connection = psycopg2.connect(
                dbname=self.dbname,
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
    
    def execute_query(self, query):
        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            headings = [desc[0] for desc in cursor.description]
            results = cursor.fetchall()
            cursor.close()
            return headings, results
        except Exception as e:
            data['status'] = 0
            data['msg'] = str(e)
            return None, None
    
    def log_results(self, headings, results):
        timestamp = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        self.log_file_path = f"{self.base_path}-{timestamp}.txt"
        
        status, msg = self.remove_old_files()
        if not status:
            data['status'] = 0
            data['msg'] = msg
            return
        
        formatted_headings = [self.format_heading(heading) for heading in headings]
        self.write_file(os.path.join(self.current_file_path, "log_pattern.txt"), " ".join(formatted_headings) + "\n")
        
        with open(self.log_file_path, 'w') as output_file:
            for row in results:
                formatted_row = " ".join(self.format_timestamp(item) if isinstance(item, datetime) else str(item) for item in row)
                output_file.write(f"{formatted_row}\n")

        data['msg'] = "Logs written to file successfully."

    def metric_collector(self):
        if not self.connect_db():
            return data
        
        query, read_status, error = self.read_file(os.path.join(self.current_file_path, "query.sql"))
        if not read_status:
            data['status'] = 0
            data['msg'] = error
            return data
        
        headings, results = self.execute_query(query)
        if headings is None or results is None:
            return data
        
        self.log_results(headings, results)
        
        data["query_status"] = "Executed successfully."
        data["Row_Count"] = len(results)
        return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', required=True, help='Username for YugabyteDB')
    parser.add_argument('--password', required=True, help='Password for YugabyteDB')
    parser.add_argument('--hostname', default='localhost', help='Host for YugabyteDB')
    parser.add_argument('--port', default='5433', help='Port for YugabyteDB')
    parser.add_argument('--db', required=True, help='Database name for YugabyteDB')
    
    args = parser.parse_args()
    try:
        yugabyte_plugin = YugabyteDB(args)
        result = yugabyte_plugin.metric_collector()
        end_time = time.time()
        execution_time = round(end_time - start_time, 2)
        result["Execution_Time"] = execution_time
        result["units"] = {"Execution Time": "s", "Row_Count": "count"}
    except Exception as e:
        result = data
        result['status'] = 0
        result['msg'] = str(traceback.format_exc())
    
    print(json.dumps(result, indent=4))
