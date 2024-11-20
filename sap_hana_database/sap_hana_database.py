#!/usr/bin/python3

from hdbcli import dbapi
import simplejson as json
from decimal import *

host = "localhost"
port = 39017
username = "SYSTEM"
password = "Password"

PLUGIN_VERSION = "1"
HEARTBEAT = True

metric_units = {
    "Index Server Memory Pool Used Size": "GB",
    "Index Server Memory Pool Heap Used Size": "GB",
    "Index Server Memory Pool Shared Used Size": "GB",
    "Name Server Memory Pool Used Size": "GB",
    "Name Server Memory Pool Heap Used Size": "GB",
    "Name Server Memory Pool Shared Used Size": "GB",
    "Start Time of Services": "Seconds",
    "Free Physical Memory": "GB",
    "Used Physical Memory": "GB",
    "Total CPU Idle Time": "minutes",
    "Plan Cache Size": "GB",
    "CATALOG_BACKUP Disk Free Size": "GB",
    "DATA Disk Free Size": "GB",
    "DATA_BACKUP Disk Free Size": "GB",
    "services": {
        "cpu": "%",
        "cpu_time": "s",
        "total_cpu_time": "count",
        "process_memory": "GB",
        "total_memory": "GB",
        "available_memory": "GB",
        "physical_memory": "GB",
        "active_thread_count": "count",
    },
}


class Sap_hana(object):
    def __init__(self, args):
        self.host = args.host
        self.port = args.port
        self.username = args.username
        self.password = args.password
        
        self.logsenabled=args.logs_enabled
        self.logtypename=args.log_type_name
        self.logfilepath=args.log_file_path
        
        self.resultjson = {}

    def metrics_collector(self):
        try:
            db = dbapi.connect(
                address=self.host,
                port=self.port,
                user=self.username,
                password=self.password,
            )
            cursor = db.cursor()

            cursor.execute(
                'SELECT * FROM "M_CONNECTIONS" WHERE SECONDS_BETWEEN(START_TIME,CURRENT_TIMESTAMP)<300'
            )
            result = cursor.fetchall()
            running_connection = 0
            idle_connection = 0
            queuing_connection = 0
            for row in result:
                if row["CONNECTION_STATUS"] == "RUNNING":
                    running_connection += 1
                elif row["CONNECTION_STATUS"] == "IDLE":
                    idle_connection += 1
                if row["CONNECTION_STATUS"] == "QUEUING":
                    queuing_connection += 1
            self.resultjson["Running Connections"] = running_connection
            self.resultjson["Idle Connections"] = idle_connection
            self.resultjson["Queuing Connections"] = queuing_connection

            cursor.execute("SELECT * FROM M_DISKS")
            result = cursor.fetchall()
            for row in result:
                self.resultjson[(row["USAGE_TYPE"]) + " Disk Free Size"] = str(
                    round((row["TOTAL_SIZE"] - row["USED_SIZE"]) / 1024.0**3, 4)
                )

            cursor.execute("SELECT * FROM M_SERVICE_NETWORK_IO")
            result = cursor.fetchall()
            self.resultjson["Total Network I/O Operations"] = len(result)

            cursor.execute("SELECT * FROM M_SERVICE_THREADS")
            result = cursor.fetchall()
            active_thread = 0
            for row in result:
                if row["IS_ACTIVE"]:
                    active_thread += 1
            self.resultjson["Active Threads"] = active_thread

            cursor.execute(
                "SELECT * FROM M_TRANSACTIONS WHERE SECONDS_BETWEEN(START_TIME,CURRENT_TIMESTAMP)<300"
            )
            result = cursor.fetchall()
            active_transaction = 0
            inactive_transaction = 0
            for row in result:
                if row["TRANSACTION_STATUS"] == "INACTIVE":
                    inactive_transaction += 1
                if row["TRANSACTION_STATUS"] == "ACTIVE":
                    active_transaction += 1
            self.resultjson["Inactive Transactions"] = inactive_transaction
            self.resultjson["Active Transactions"] = active_transaction

            cursor.execute(
                "SELECT TOTAL_MEMORY_USED_SIZE, CODE_SIZE, STACK_SIZE, HEAP_MEMORY_ALLOCATED_SIZE, HEAP_MEMORY_USED_SIZE, SHARED_MEMORY_ALLOCATED_SIZE, SHARED_MEMORY_USED_SIZE FROM M_SERVICE_MEMORY WHERE Service_name='indexserver'"
            )
            result = cursor.fetchall()
            if result:
                self.resultjson["Index Server Memory Pool Used Size"] = str(
                    round(result[0][0] / 1024.0**3, 4)
                )
                self.resultjson["Index Server Memory Pool Heap Used Size"] = str(
                    round(result[0][4] / 1024.0**3, 4)
                )
                self.resultjson["Index Server Memory Pool Shared Used Size"] = str(
                    round(result[0][6] / 1024.0**3, 4)
                )
            else:
                self.resultjson["Index Server Memory Pool Used Size"] = 0
                self.resultjson["Index Server Memory Pool Heap Used Size"] = 0
                self.resultjson["Index Server Memory Pool Shared Used Size"] = 0

            cursor.execute(
                "SELECT TOTAL_MEMORY_USED_SIZE, CODE_SIZE, STACK_SIZE, HEAP_MEMORY_ALLOCATED_SIZE, HEAP_MEMORY_USED_SIZE, SHARED_MEMORY_ALLOCATED_SIZE, SHARED_MEMORY_USED_SIZE FROM M_SERVICE_MEMORY WHERE Service_name='nameserver'"
            )
            result = cursor.fetchall()
            if result:
                self.resultjson["Name Server Memory Pool Used Size"] = str(
                    round(result[0][0] / 1024.0**3, 4)
                )
                self.resultjson["Name Server Memory Pool Heap Used Size"] = str(
                    round(result[0][4] / 1024.0**3, 4)
                )
                self.resultjson["Name Server Memory Pool Shared Used Size"] = str(
                    round(result[0][6] / 1024.0**3, 4)
                )
            else:
                self.resultjson["Name Server Memory Pool Used Size"] = 0
                self.resultjson["Name Server Memory Pool Heap Used Size"] = 0
                self.resultjson["Name Server Memory Pool Shared Used Size"] = 0

            cursor.execute("SELECT * FROM M_SERVICE_REPLICATION")
            result = cursor.fetchall()
            error_replication = 0
            syncing = 0
            for row in result:
                if row["REPLICATION_STATUS"] == "ERROR":
                    error_replication += 1
                elif row["REPLICATION_STATUS"] == "SYNCING":
                    syncing += 1
            self.resultjson["Replication Errors"] = error_replication
            self.resultjson["Replication Syncing"] = syncing

            cursor.execute(
                "SELECT * FROM M_DELTA_MERGE_STATISTICS WHERE TYPE='MERGE' AND SUCCESS='FALSE' AND SECONDS_BETWEEN(START_TIME,CURRENT_TIMESTAMP)<300"
            )
            result = cursor.fetchall()
            self.resultjson["Total Delta Merge Errors"] = len(result)

            cursor.execute(
                "SELECT * FROM M_EXPENSIVE_STATEMENTS WHERE SECONDS_BETWEEN(START_TIME,CURRENT_TIMESTAMP)<300"
            )
            result = cursor.fetchall()
            self.resultjson["Total Expensive Statements"] = len(result)

            cursor.execute(
                "SELECT * FROM M_BACKUP_CATALOG WHERE SECONDS_BETWEEN(SYS_START_TIME,CURRENT_TIMESTAMP)<300"
            )
            result = cursor.fetchall()
            self.resultjson["Backup Catalogs"] = len(result)

            cursor.execute(
                "SELECT * FROM M_CS_UNLOADS WHERE SECONDS_BETWEEN(UNLOAD_TIME,CURRENT_TIMESTAMP)<300"
            )
            result = cursor.fetchall()
            self.resultjson["Total Column Unloads"] = len(result)

            cursor.execute(
                "SELECT * FROM M_PREPARED_STATEMENTS WHERE STATEMENT_STATUS = 'ACTIVE'"
            )
            result = cursor.fetchall()
            self.resultjson["Total Active Statements"] = len(result)

            cursor.execute("SELECT * FROM M_CACHES")
            result = cursor.fetchall()
            self.resultjson["Total Caches"] = len(result)

            cursor.execute("SELECT (sum(DURATION)/1000) FROM SYS.M_DEV_RECOVERY_")
            result = cursor.fetchall()
            if result:
                self.resultjson["Start Time of Services"] = Decimal(result[0][0])
            else:
                self.resultjson["Start Time of Services"] = 0

            cursor.execute(
                "SELECT * FROM _SYS_STATISTICS.STATISTICS_ALERT_THRESHOLDS WHERE SECONDS_BETWEEN(REACHED_AT,CURRENT_TIMESTAMP)<300"
            )
            result = cursor.fetchall()
            self.resultjson["Total Alerts"] = len(result)

            cursor.execute(
                "SELECT FREE_PHYSICAL_MEMORY, USED_PHYSICAL_MEMORY, TOTAL_CPU_IDLE_TIME FROM M_HOST_RESOURCE_UTILIZATION WHERE HOST='"
                + self.host
                + "'"
            )
            result = cursor.fetchall()
            if result:
                self.resultjson["Free Physical Memory"] = str(
                    round(result[0][0] / 1024.0**3, 4)
                )
                self.resultjson["Used Physical Memory"] = str(
                    round(result[0][1] / 1024.0**3, 4)
                )
                self.resultjson["Total CPU Idle Time"] = str(
                    round(result[0][2] / 60000)
                )
            else:
                self.resultjson["Free Physical Memory"] = 0
                self.resultjson["Used Physical Memory"] = 0
                self.resultjson["Total CPU Idle Time"] = 0

            cursor.execute("SELECT * FROM M_HOST_INFORMATION")
            result = cursor.fetchall()
            self.resultjson["HANA Nodes"] = len(result)

            def bytes_to_gb(bytes_value):
                return round(bytes_value / (1024**3), 2) if bytes_value != -1 else -1

            def ms_to_seconds(ms_value):
                return round(ms_value / 1000, 2) if ms_value != -1 else -1

            cursor.execute("SELECT * FROM M_SERVICE_STATISTICS")
            results = cursor.fetchall()

            services = []

            for row in results:
                service = {}

                service["name"] = row[2]
                service["process_id"] = row[3]
                service["cpu"] = row[8]
                service["total_cpu_time"] = ms_to_seconds(row[11])
                service["process_memory"] = bytes_to_gb(row[12])
                service["total_memory"] = bytes_to_gb(row[14])
                service["available_memory"] = bytes_to_gb(row[15])
                service["physical_memory"] = bytes_to_gb(row[16])
                service["active_thread_count"] = row[23]

                service["status"] = 1 if row[5] == "YES" else 0

                services.append(service)

            self.resultjson["services"] = services
            
            query = """
            SELECT SERVICE_NAME, REQUESTS_PER_SEC, TOTAL_CPU, FINISHED_NON_INTERNAL_REQUEST_COUNT,
                ALL_FINISHED_REQUEST_COUNT, PROCESS_MEMORY
            FROM M_SERVICE_STATISTICS
            """
            cursor.execute(query)
            results = cursor.fetchall()

            workload = []
            for row in results:
                service_name = row[0] 
                requests_per_sec = row[1]
                total_cpu = row[2]
                finished_requests = row[3]
                all_requests = row[4]  
                process_memory = row[5]

                execution_rate_per_min = max(round((requests_per_sec or 0) * 60, 2), 0)
                compilation_rate_per_min = max(round((total_cpu or 0) * 60, 2), 0)
                transaction_rate_per_min = max(round((finished_requests or 0) * 60, 2), 0)
                commit_rate_per_min = max(round((all_requests or 0) * 60, 2), 0)
                memory_usage_rate_per_min = max(round((process_memory or 0) / (1024 * 1024), 2), 0)  # Convert bytes to MB

                workload.append({
                    "name": service_name,
                    "current_execution_rate_per_min": execution_rate_per_min,
                    "current_compilation_rate_per_min": compilation_rate_per_min,
                    "current_transaction_rate_per_min": transaction_rate_per_min,
                    "current_commit_rate_per_min": commit_rate_per_min,
                    "current_memory_usage_rate_per_min": memory_usage_rate_per_min
                })
                
            
            self.resultjson["workload"] = workload

            cursor.execute("SELECT VERSION FROM SYS.M_DATABASE")
            result = cursor.fetchall()
            self.resultjson["database_version"] = (
                result[0][0] + "_v" if result else "Unknown"
            )

            self.resultjson["tabs"] = {
                "Disks": {
                    "order": 4,
                    "tablist": [
                        "CATALOG_BACKUP Disk Free Size",
                        "DATA Disk Free Size",
                        "DATA_BACKUP Disk Free Size",
                        "LOG Disk Free Size",
                        "LOG_BACKUP Disk Free Size",
                        "TRACE Disk Free Size",
                    ],
                },
                "Memory": {
                    "order": 5,
                    "tablist": [
                        "Free Physical Memory",
                        "Index Server Memory Pool Heap Used Size",
                        "Index Server Memory Pool Shared Used Size",
                        "Index Server Memory Pool Used Size",
                        "Name Server Memory Pool Heap Used Size",
                        "Name Server Memory Pool Shared Used Size",
                        "Name Server Memory Pool Used Size",
                        "Used Physical Memory",
                    ],
                },
                "Operations and Performance": {
                    "order": 2,
                    "tablist": [
                        "Total Active Statements",
                        "Total Expensive Statements",
                        "Total Caches",
                        "Total Column Unloads",
                        "Total Delta Merge Errors",
                        "Total Network I/O Operations",
                        "Total Alerts",
                    ],
                },
                "Backup and Replication": {
                    "order": 3,
                    "tablist": [
                        "Backup Catalogs",
                        "Replication Errors",
                        "Replication Syncing",
                    ],
                },
                "Services and Workload": {
                    "order": 1,
                    "tablist": ["Start Time of Services", "services", "workload"],
                },
            }

            return self.resultjson
        except Exception as e:
            self.resultjson["msg"] = str(e)
            self.resultjson["status"] = 0
            return self.resultjson


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="Host Name", nargs="?", default=host)
    parser.add_argument("--port", help="Port", nargs="?", default=port)
    parser.add_argument("--username", help="username", default=username)
    parser.add_argument("--password", help="Password", default=password)

    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application',default="False")
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=None)

    args = parser.parse_args()

    saphana = Sap_hana(args)
    resultjson = saphana.metrics_collector()
    resultjson["plugin_version"] = PLUGIN_VERSION
    resultjson["heartbeat_required"] = HEARTBEAT
    resultjson["units"] = metric_units
    print(json.dumps(resultjson, indent=4, sort_keys=True))
