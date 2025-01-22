#!/usr/bin/python3
import json
import requests

PLUGIN_VERSION = 1
HEARTBEAT = True
METRICS_UNITS = {
    "taskmanager.memory.process.size": "MB",
    "jobmanager.memory.off-heap.size": "MB",
    "jobmanager.memory.jvm-overhead.min": "MB",
    "jobmanager.memory.process.size": "MB",
    "jobmanager.memory.jvm-metaspace.size": "MB",
    "jobmanager.memory.heap.size": "MB",
    "jobmanager.memory.jvm-overhead.max": "MB",
    "refresh-interval": "ms"
}

class Flink:

    def __init__(self, args):
        self.host = args.host
        self.port = args.port
        self.jobs_overview_url = f'http://{self.host}:{self.port}/jobs/overview'
        self.jobmanager_config_url = f'http://{self.host}:{self.port}/jobmanager/config'
        self.jobmanager_environment_url = f'http://{self.host}:{self.port}/jobmanager/environment'
        self.flink_config_url = f'http://{self.host}:{self.port}/config'

    def convert_memory_value(self, value):
        """
        Converts memory values to a standardized format:
        - For values ending with 'm', return the numeric part.
        - For values ending with 'b', convert to MB and return.
        """
        if value.endswith('m'):
            return int(value[:-1])  
        elif value.endswith('b'):
            bytes_value = int(value[:-1])  
            return bytes_value // (1024 * 1024)
        else:
            return value 

    def fetch_jobs_overview(self, result):
        try:
            response = requests.get(self.jobs_overview_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                jobs = data.get("jobs", [])
                result["total_jobs"] = len(jobs)

                task_metrics = {
                    "total_tasks_running": 0,
                    "total_tasks_canceling": 0,
                    "total_tasks_canceled": 0,
                    "total_total_tasks": 0,
                    "total_tasks_created": 0,
                    "total_tasks_scheduled": 0,
                    "total_tasks_deploying": 0,
                    "total_tasks_reconciling": 0,
                    "total_tasks_finished": 0,
                    "total_tasks_initializing": 0,
                    "total_tasks_failed": 0
                }

                # Aggregate task metrics across all jobs
                for job in jobs:
                    tasks = job["tasks"]
                    task_metrics["total_tasks_running"] += tasks.get("running", 0)
                    task_metrics["total_tasks_canceling"] += tasks.get("canceling", 0)
                    task_metrics["total_tasks_canceled"] += tasks.get("canceled", 0)
                    task_metrics["total_total_tasks"] += tasks.get("total", 0)
                    task_metrics["total_tasks_created"] += tasks.get("created", 0)
                    task_metrics["total_tasks_scheduled"] += tasks.get("scheduled", 0)
                    task_metrics["total_tasks_deploying"] += tasks.get("deploying", 0)
                    task_metrics["total_tasks_reconciling"] += tasks.get("reconciling", 0)
                    task_metrics["total_tasks_finished"] += tasks.get("finished", 0)
                    task_metrics["total_tasks_initializing"] += tasks.get("initializing", 0)
                    task_metrics["total_tasks_failed"] += tasks.get("failed", 0)

                result.update(task_metrics)
            else:
                result["msg"] = "Flink is not running"
                result["status"] = 0
        except requests.exceptions.RequestException:
            result["msg"] = "Flink is not running"
            result["status"] = 0

    def fetch_jobmanager_config(self, result):
        try:
            response = requests.get(self.jobmanager_config_url, timeout=5)
            if response.status_code == 200:
                config_data = response.json()
                config_filtered = {
                    item["key"]: self.convert_memory_value(item["value"])
                    for item in config_data
                    if item["key"] != "env.java.opts.all"
                }
                result.update(config_filtered)
            else:
                result["msg"] = "Flink is not running"
                result["status"] = 0
        except requests.exceptions.RequestException:
            result["msg"] = "Flink is not running"
            result["status"] = 0

    def fetch_jobmanager_environment(self, result):
        try:
            response = requests.get(self.jobmanager_environment_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                jvm_info = data.get("jvm", {})
                result["jvm_version"] = jvm_info.get("version", "Unknown")
                result["jvm_arch"] = jvm_info.get("arch", "Unknown")
            else:
                result["msg"] = "Failed to fetch JobManager environment details"
        except requests.exceptions.RequestException:
            result["msg"] = "Failed to fetch JobManager environment details"

    def fetch_flink_config(self, result):
        try:
            response = requests.get(self.flink_config_url, timeout=5)
            if response.status_code == 200:
                data = response.json()
                result["refresh-interval"] = data.get("refresh-interval", "Unknown")
                result["timezone-name"] = data.get("timezone-name", "Unknown")
                result["timezone-offset"] = data.get("timezone-offset", "Unknown")
                result["flink-version"] = data.get("flink-version", "Unknown")
                result["flink-revision"] = data.get("flink-revision", "Unknown")
            else:
                result["msg"] = "Failed to fetch Flink config details"
        except requests.exceptions.RequestException:
            result["msg"] = "Failed to fetch Flink config details"

    def metriccollector(self):
        result = {
            "plugin_version": PLUGIN_VERSION,
            "heartbeat_required": HEARTBEAT,
            "total_jobs": 0,
            "units": METRICS_UNITS,
            "tabs" : {
                'JobManager': {
                    'order': 1,
                    'tablist': [
                        'jobmanager.memory.off-heap.size',
                        'jobmanager.memory.jvm-overhead.min',
                        'jobmanager.memory.process.size',
                        'jobmanager.memory.jvm-metaspace.size',
                        'jobmanager.memory.heap.size',
                        'jobmanager.memory.jvm-overhead.max'
                    ]
                }
}

        }

        self.fetch_jobs_overview(result)

        self.fetch_jobmanager_config(result)

        self.fetch_jobmanager_environment(result)

        self.fetch_flink_config(result)

        ports_to_modify = [
        "jobmanager.rpc.port", 
        "query.server.port", 
        "blob.server.port"
    ]
    
        for port_key in ports_to_modify:
            if port_key in result:
                result[port_key] = f"port_{result[port_key]}"
        
        if "msg" not in result:
            result["msg"] = "Flink is running"

        return result


if __name__ == "__main__":
    host = "localhost"
    port = 8081

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Flink host', default=host)
    parser.add_argument('--port', help='Flink port', default=port)

    args = parser.parse_args()

    obj = Flink(args)
    result = obj.metriccollector()
    print(json.dumps(result, indent=4))
