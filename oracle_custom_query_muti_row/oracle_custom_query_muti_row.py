#!/usr/bin/python3

import json
import os
import glob
import time
import warnings
import traceback
import datetime
warnings.filterwarnings("ignore")

PLUGIN_VERSION = 1
HEARTBEAT = True
METRICS_UNITS = {"execution_time": "ms"}


class oracle:

    def __init__(self, args):

        self.maindata = {}
        self.maindata["plugin_version"] = PLUGIN_VERSION
        self.maindata["heartbeat_required"] = HEARTBEAT
        self.maindata["units"] = METRICS_UNITS

        self.username = args.username
        self.password = args.password
        self.sid = args.sid
        self.hostname = args.hostname
        self.port = args.port
        self.current_file_path = os.path.dirname(os.path.abspath(__file__))
        self.log_file_path = os.path.join(self.current_file_path, "query_output")
        self.base_path = self.log_file_path

        self.query = self.read_query_from_file()

    def is_file_empty(self, file_path):
        try:
            # Check if the file exists
            if not os.path.exists(file_path):
                return False  # File does not exist

            # Get file size
            file_size = os.stat(file_path).st_size

            # Check if file size is 0 bytes
            return file_size == 0

        except Exception as e:
            self.maindata["status"] = 0
            self.maindata["msg"] = str(e)
            return False

    def read_query_from_file(self):
        """Read the query from the query.sql file."""
        try:
            query_file_path = os.path.join(self.current_file_path, "query.sql")

            if self.is_file_empty(query_file_path):
                self.maindata["status"] = 0
                self.maindata["msg"] = ("The query.sql file is empty. Please enter a query.")
                return None

            with open(query_file_path, "r") as file:
                return file.read().strip()
        except Exception as e:
            self.maindata["status"] = 0
            self.maindata["msg"] = f"Failed to read query from file: {str(e)}"
            return None

    def write_to_logs(self, log_content, time):
        try:
            log_file_path = self.log_file_path + "-" + time + ".txt"
            pattern = self.base_path + "*"

            for filename in glob.glob(pattern):
                os.remove(filename)

            f = open(log_file_path, "x")
            f.write(log_content)
            f.close()
            self.maindata["msg"] = "Logs written to file successfully."

        except Exception as e:
            self.maindata["status"] = 0
            self.maindata["msg"] = str(e)

    def format_heading(self, heading):
        """Format the column heading."""
        words = heading.replace("_", " ").split()
        return f"{''.join(word.capitalize() for word in words)}"

    def metriccollector(self):

        try:
            import oracledb
        except Exception as e:
            self.maindata["status"] = 0
            self.maindata["msg"] = str(e)
            return self.maindata

        try:
            start_time = time.time()

            if self.query is None:
                return self.maindata

            try:
                conn = oracledb.connect(
                    user=self.username,
                    password=self.password,
                    dsn=f"{self.hostname}:{self.port}/{self.sid}",
                )
                c = conn.cursor()
            except Exception as e:
                self.maindata["status"] = 0
                self.maindata["msg"] = "Exception while making connection: " + str(e)
                return self.maindata

            c.execute(self.query)

            col_names = [self.format_heading(row[0]) for row in c.description]
            tot_cols = len(col_names)
            log_json = ""
            now=datetime.datetime.now()
            row_count = 0
            for row in c:
                #print(row)
                log_data = {}
                for i in range(tot_cols):
                    log_data[col_names[i]] = row[i]
                log_data["Datetime"] = (now - datetime.timedelta(seconds=row_count)).strftime("%Y-%m-%d %H:%M:%S")
                #print(json.dumps(log_data))
                log_json += json.dumps(log_data) + "\n"
                row_count += 1


            c.close()
            conn.close()
            self.maindata["tags"] = (f"oracle_hostname:{self.hostname},oracle_sid:{self.sid}")
            end_time = time.time()
            total_time = (end_time - start_time) * 1000
            self.maindata["execution_time"] = "%.3f" % total_time
            self.maindata["No of rows returned"] = row_count

            if row_count == 0:
                self.maindata["msg"] = "No rows were returned for the given query."
                return self.maindata
            else:
                self.write_to_logs(log_json, now.strftime("%Y-%m-%d-%H-%M-%S"))

        except Exception as e:
            self.maindata["msg"] = str(e)
            self.maindata["status"] = 0
            if 'c' in locals() and c:
                c.close()
            if 'conn' in locals() and conn:
                conn.close()

        return self.maindata


if __name__ == "__main__":

    hostname = "localhost"
    port = "1521"
    sid = "xe"
    username = "site24x7"
    password = "plugin"
    oracle_home = "/opt/oracle/product/19c/dbhome_1"

    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument("--hostname", help="hostname for oracle", default=hostname)
    parser.add_argument("--port", help="port number for oracle", default=port)
    parser.add_argument("--sid", help="sid for oracle", default=sid)
    parser.add_argument("--username", help="username for oracle", default=username)
    parser.add_argument("--password", help="password for oracle", default=password)
    parser.add_argument("--oracle_home", help="oracle home path", default=oracle_home)

    args = parser.parse_args()
    os.environ["ORACLE_HOME"] = args.oracle_home
    
    obj = oracle(args)
    result = obj.metriccollector()
    print(json.dumps(result, indent=True))
