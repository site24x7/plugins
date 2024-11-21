#!/usr/bin/python3

import json
import argparse
import urllib
import urllib.request as urlconnection
from urllib.error import URLError, HTTPError
from urllib.request import ProxyHandler
import requests
from requests.auth import HTTPBasicAuth


metric_units = {
    "jobs_scheduled_rate": "events/minute",
    "jobs_buildable_duration": "sec",
    "jobs_blocked_duration": "sec",
    "jobs_execution_time": "sec",
    "jobs_queuing_duration": "sec",
    "jobs_total_duration": "sec",
    "jobs_waiting_duration": "sec",
    "heap_memory_commited": "bytes",
    "heap_memory_initiated": "bytes",
    "maximum_heap_memory": "bytes",
    "heap_memory_used": "bytes",
    "non-heap_memory_commited": "bytes",
    "non-heap_memory_initiated": "bytes",
    "maximum_non-heap_memory": "bytes",
    "non-heap_memory_used": "bytes",
    "total_memory_commited": "bytes",
    "total_memory_initiated": "bytes",
    "total_maximum_memory": "bytes",
    "total_memory_used": "bytes",
    "health-check_duration": "sec",
    "builds_blocked_duration": "sec",
    "builds_execution_duration": "sec",
    "builds_queuing_duration": "sec",
    "builds_waiting_duration": "sec",
    "request_duration": "seconds",
    "jobs":{
        "last_build_number": "count",
        "recent_build_health_in_percentage": "%",
        "last_build_duration_in_minute": "m",
        "last_build_estimated_duration_in_minute": "m"
    }
}


class Jenkins(object):

    def __init__(self, args):
        self.host = args.host
        self.port = args.port
        self.username = args.username
        self.password = args.password
        self.apikey = args.apikey
        self.plugin_version = args.plugin_version
        self.heartbeat = args.heartbeat
        self.resultjson = {}

        self.metrics_collector()

        self.resultjson["plugin_version"] = self.plugin_version
        self.resultjson["heartbeat_required"] = self.heartbeat
        
    def process_jenkins_jobs(self, data):
        processed_jobs = []

        for job in data.get("jobs", []):
            name = job.get("name", "unknown")

            last_build = job.get("lastBuild", {})
            last_build_number = last_build.get("number", 0)
            last_build_result = last_build.get("result", "UNKNOWN").upper()
            last_build_status = 1 if last_build_result == "SUCCESS" else 0
            last_build_duration = round(last_build.get("duration", 0) / 60, 2)
            last_build_estimated_duration = round(last_build.get("estimatedDuration", 0) / 60, 2)

            health_report = job.get("healthReport", [])
            recent_build_health = health_report[0].get("score", 0) if health_report else 0

            processed_job = {
                "name": name,
                "last_build_number": last_build_number,
                "status": last_build_status,
                "recent_build_health_in_percentage": recent_build_health,
                "last_build_duration_in_minute": last_build_duration,
                "last_build_estimated_duration_in_minute": last_build_estimated_duration
            }

            processed_jobs.append(processed_job)

        return processed_jobs

    def get_jenkins_jobs(self):
        url = f"http://{self.host}:{self.port}/api/json?tree=jobs[name,lastBuild[number,result,duration,estimatedDuration],healthReport[description,score]]&pretty=true"

        try:
            response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password))
            response.raise_for_status()  

            data = response.json()
            return data

        except requests.exceptions.RequestException as e:
            self.resultjson['msg']=str(e)
            self.resultjson['status']=0
            return None

    def metrics_collector(self):
        try:
            url = (
                "http://"
                + self.host
                + ":"
                + self.port
                + "/metrics/"
                + self.apikey
                + "/metrics?pretty=true"
            )
            
            auth_handler = urlconnection.HTTPBasicAuthHandler(
                (urlconnection.HTTPPasswordMgrWithDefaultRealm()).add_password(
                    None, url, self.username, self.password
                )
            )
            response = (urlconnection.urlopen(url)).read().decode("UTF-8")
            response = json.loads(response)
            
            gauges = response["gauges"]
            meters = response["meters"]
            timers = response["timers"]
            counters = response["counters"]

            self.resultjson["jenkins_version"] = (
                f"{gauges['jenkins.versions.core']['value']}_V"
            )

            self.resultjson["jobs_scheduled_rate"] = meters["jenkins.job.scheduled"][
                "mean_rate"
            ]
            self.resultjson["jobs_blocked_duration"] = timers[
                "jenkins.job.blocked.duration"
            ]["mean"]
            self.resultjson["jobs_buildable_duration"] = timers[
                "jenkins.job.buildable.duration"
            ]["mean"]
            self.resultjson["jobs_execution_time"] = timers[
                "jenkins.job.execution.time"
            ]["mean"]
            self.resultjson["jobs_queuing_duration"] = timers[
                "jenkins.job.queuing.duration"
            ]["mean"]
            self.resultjson["jobs_total_duration"] = timers[
                "jenkins.job.total.duration"
            ]["mean"]
            self.resultjson["jobs_waiting_duration"] = timers[
                "jenkins.job.waiting.duration"
            ]["mean"]

            self.resultjson.update(
                {
                    "blocked_thread": gauges["vm.blocked.count"]["value"],
                    "thread_count": gauges["vm.count"]["value"],
                    "deadlock_count": gauges["vm.deadlock.count"]["value"],
                    "file_descriptor_ratio": gauges["vm.file.descriptor.ratio"][
                        "value"
                    ],
                    "heap_memory_commited": gauges["vm.memory.heap.committed"]["value"],
                    "heap_memory_initiated": gauges["vm.memory.heap.init"]["value"],
                    "maximum_heap_memory": gauges["vm.memory.heap.max"]["value"],
                    "heap_memory_used": gauges["vm.memory.heap.used"]["value"],
                    "non-heap_memory_commited": gauges["vm.memory.non-heap.committed"][
                        "value"
                    ],
                    "non-heap_memory_initiated": gauges["vm.memory.non-heap.init"][
                        "value"
                    ],
                    "maximum_non-heap_memory": gauges["vm.memory.non-heap.max"][
                        "value"
                    ],
                    "non-heap_memory_used": gauges["vm.memory.non-heap.used"]["value"],
                    "total_memory_commited": gauges["vm.memory.total.committed"][
                        "value"
                    ],
                    "total_memory_initiated": gauges["vm.memory.total.init"]["value"],
                    "total_maximum_memory": gauges["vm.memory.total.max"]["value"],
                    "total_memory_used": gauges["vm.memory.total.used"]["value"],
                    "new_threads": gauges["vm.new.count"]["value"],
                    "running_threads": gauges["vm.runnable.count"]["value"],
                    "terminated_threads": gauges["vm.terminated.count"]["value"],
                    "suspended_threads": gauges["vm.timed_waiting.count"]["value"],
                    "waiting_threads": gauges["vm.waiting.count"]["value"],
                }
            )

            self.resultjson.update(
                {
                    "total_executors_count": gauges["jenkins.executor.count.value"][
                        "value"
                    ],
                    "executors_free_count": gauges["jenkins.executor.free.value"][
                        "value"
                    ],
                    "executors_inuse_count": gauges["jenkins.executor.in-use.value"][
                        "value"
                    ],
                    "node_count": gauges["jenkins.node.count.value"]["value"],
                    "nodes_offline": gauges["jenkins.node.offline.value"]["value"],
                    "nodes_online": gauges["jenkins.node.online.value"]["value"],
                    "projects_count": gauges["jenkins.project.count.value"]["value"],
                    "projects_disabled": gauges["jenkins.project.disabled.count.value"][
                        "value"
                    ],
                    "projects_enabled": gauges["jenkins.project.disabled.count.value"][
                        "value"
                    ],
                    "queues_blocked": gauges["jenkins.queue.blocked.value"]["value"],
                    "jobs_in_queue": gauges["jenkins.queue.buildable.value"]["value"],
                    "queues_pending": gauges["jenkins.queue.pending.value"]["value"],
                    "queues_size": gauges["jenkins.queue.size.value"]["value"],
                    "queues_stuck": gauges["jenkins.queue.stuck.value"]["value"],
                    "health-check_count": gauges["jenkins.health-check.count"]["value"],
                    "plugins_active": gauges["jenkins.plugins.active"]["value"],
                    "plugins_failed": gauges["jenkins.plugins.failed"]["value"],
                    "plugins_inactive": gauges["jenkins.plugins.inactive"]["value"],
                    "plugins_withupdate": gauges["jenkins.plugins.withUpdate"]["value"],
                    "health-check_duration": timers["jenkins.health-check.duration"][
                        "mean"
                    ],
                    "builds_blocked_duration": timers["jenkins.task.blocked.duration"][
                        "mean"
                    ],
                    "build_creation_time": timers["jenkins.task.buildable.duration"][
                        "mean"
                    ],
                    "builds_execution_duration": timers[
                        "jenkins.task.execution.duration"
                    ]["mean"],
                    "builds_queuing_duration": timers["jenkins.task.queuing.duration"][
                        "mean"
                    ],
                    "builds_waiting_duration": timers["jenkins.task.waiting.duration"][
                        "mean"
                    ],
                }
            )

            self.resultjson.update(
                {
                    "total_activerequests": counters["http.activeRequests"]["count"],
                    "total_badrequest": meters["http.responseCodes.badRequest"][
                        "count"
                    ],
                    "total_responsecode_created": meters["http.responseCodes.created"][
                        "count"
                    ],
                    "total_forbidden_responsecode": meters[
                        "http.responseCodes.forbidden"
                    ]["count"],
                    "nocontent_responsecode": meters["http.responseCodes.noContent"][
                        "count"
                    ],
                    "notfound_responsecode": meters["http.responseCodes.notFound"][
                        "count"
                    ],
                    "unmodified_responsecode": meters["http.responseCodes.notModified"][
                        "count"
                    ],
                    "success_responsecode": meters["http.responseCodes.ok"]["count"],
                    "non_informational_responsecode": meters[
                        "http.responseCodes.other"
                    ]["count"],
                    "servererror_responsecode": meters[
                        "http.responseCodes.serverError"
                    ]["count"],
                    "service_unavailable": meters[
                        "http.responseCodes.serviceUnavailable"
                    ]["count"],
                    "request_duration": timers["http.requests"]["mean"],
                }
            )

            self.resultjson["tabs"] = {
                "Job Metrics": {
                    "order": 1,
                    "tablist": [
                        "jobs",
                        "jobs_scheduled_rate",
                        "jobs_blocked_duration",
                        "jobs_buildable_duration",
                        "jobs_execution_time",
                        "jobs_queuing_duration",
                        "jobs_total_duration",
                        "jobs_waiting_duration",
                    ],
                },
                "JVM Metrics": {
                    "order": 2,
                    "tablist": [
                        "blocked_thread",
                        "thread_count",
                        "deadlock_count",
                        "file_descriptor_ratio",
                        "heap_memory_commited",
                        "heap_memory_initiated",
                        "maximum_heap_memory",
                        "heap_memory_used",
                        "non-heap_memory_commited",
                        "non-heap_memory_initiated",
                        "maximum_non-heap_memory",
                        "non-heap_memory_used",
                        "total_memory_commited",
                        "total_memory_initiated",
                        "total_maximum_memory",
                        "total_memory_used",
                        "new_threads",
                        "running_threads",
                        "terminated_threads",
                        "suspended_threads",
                        "waiting_threads",
                    ],
                },
                "Performance Metrics": {
                    "order": 3,
                    "tablist": [
                        "total_executors_count",
                        "executors_free_count",
                        "executors_inuse_count",
                        "projects_count",
                        "projects_disabled",
                        "projects_enabled",
                        "queues_blocked",
                        "queues_pending",
                        "queues_size",
                        "queues_stuck",
                        "build_creation_time",
                        "builds_execution_duration",
                        "builds_queuing_duration",
                        "builds_waiting_duration",
                    ],
                },
                "Web Metrics": {
                    "order": 4,
                    "tablist": [
                        "total_activerequests",
                        "total_badrequest",
                        "total_responsecode_created",
                        "total_forbidden_responsecode",
                        "nocontent_responsecode",
                        "notfound_responsecode",
                        "unmodified_responsecode",
                        "success_responsecpde",
                        "non_informational_responsecode",
                        "servererror_responsecode",
                        "service_unavailable",
                        "request_duration",
                    ],
                },
            }
            
            jobs_data = self.get_jenkins_jobs()
            if jobs_data:
                self.resultjson["jobs"] = self.process_jenkins_jobs(jobs_data)

        except Exception as e:
            self.resultjson["msg"] = str(e)
            self.resultjson["status"] = 0
        return self.resultjson


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host", help="Host Name", nargs="?", default="localhost")
    parser.add_argument("--port", help="Port", nargs="?", default="8080")
    parser.add_argument("--username", help="username", default="username")
    parser.add_argument("--password", help="password", default="password")
    parser.add_argument(
        "--apikey",
        help="apikey",
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "--plugin_version",
        help="plugin template version",
        type=int,
        nargs="?",
        default=1,
    )
    parser.add_argument(
        "--heartbeat",
        help="alert if monitor does not send data",
        type=bool,
        nargs="?",
        default=True,
    )
    args = parser.parse_args()

    jenkins = Jenkins(args)
    resultjson = jenkins.metrics_collector()
    resultjson["units"] = metric_units
    print(json.dumps(resultjson))
