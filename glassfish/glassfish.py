#!/usr/bin/python3
import json
import requests
import platform
import traceback
import warnings

warnings.filterwarnings("ignore")
from requests.auth import HTTPBasicAuth

PLUGIN_VERSION = 1
HEARTBEAT = True
METRICS_UNITS = {
    "Committed Heap Size": "bytes",
    "Committed Non Heap Size": "bytes",
    "Init HeapSize": "bytes",
    "Init Non Heap Size": "bytes",
    "MaxHeap Size": "bytes",
    "Max Non Heap Size": "bytes",
    "Used Heap Size": "bytes",
    "Used Non Heap Size": "bytes",
    "Current Thread CPU Time": "ms",
    "Current Thread User Time": "ms",
    "Max Time": "ms",
    "Avg Processing Time": "ms",
    "Bytes Received": "bytes",
    "Bytes Transmitted": "bytes",
    "Uptime": "s",
}

metric_keys = {
    "memory": {
        "usednonheapsize-count": "Used Non Heap Size",  # Amount of used non-heap memory in bytes
        "maxheapsize-count": "MaxHeap Size",  # Maximum amount of heap memory in bytes that can be used for memory management
        "initheapsize-count": "Init HeapSize",  # Amount of heap memory in bytes that the JVM initially requests from OS for memory management
        "initnonheapsize-count": "Init Non Heap Size",  # Amount of non-heap memory in bytes that the JVM initially requests from OS for memory management
        "usedheapsize-count": "Used Heap Size",  # Amount of used heap memory in bytes
        "committednonheapsize-count": "Committed Non Heap Size",  # Amount of non-heap memory in bytes that is committed for the JVM to use
        "objectpendingfinalizationcount-count": "Object Pending Finalization Count",  # Approximate number of objects for which finalization is pending
        "maxnonheapsize-count": "Max Non Heap Size",  # Maximum amount of non-heap memory in bytes that can be used for memory management
        "committedheapsize-count": "Committed Heap Size",  # Amount of heap memory in bytes that is committed for the JVM to use
    },
    "thread": {
        "deadlockedthreads": "Dead Locked Threads",  # No of threads in deadlock waiting to acquire object monitors or ownable synchronizers
        "totalstartedthreadcount": "Total Started Thread Count",  # No of threads created and also started since the Java virtual machine started
        "daemonthreadcount": "Daemon Thread Count",  # No of live daemon threads
        "monitordeadlockedthreads": "Monitor Dead Locked Threads",  # number of threads in deadlock waiting to acquire object monitors
        "currentthreadusertime": "Current Thread User Time",  # CPU time for a thread executed in user mode
        "peakthreadcount": "Peak Thread Count",  # the peak live thread count since the Java virtual machine started or peak was reset
        "threadcount": "Thread Count",  # number of live threads including both daemon and non-daemon threads
        "currentthreadcputime": "Current Thread CPU Time",  # total CPU time for the current thread in nanoseconds
    },
    "requests": {
        "errorcount": "Error Count",  # Cumulative value of the error count, with error count representing the number of cases where the response code was greater than or equal to 400
        "processingtime": "Avg Processing Time",  # Average request processing time
        "requestcount": "Request Count",  # Cumulative number of requests processed so far
        "maxtime": "Max Time",  # Longest response time for a request; not a cumulative value, but the largest response time from among the response times
    },
    "servlet": {
        "activeservletsloadedcount": "Active Servlets Loaded",  # Number of Servlets loaded
        "servletprocessingtimes": "Servlet Processing Times",  # Cumulative Servlet processing times
        "totalservletsloadedcount": "Total Servlets Loaded",  # Total number of Servlets loaded
    },
    "Request_Status_Code_Class": {
        "countbytesreceived": "Bytes Received",  # Total number of bytes received
        "countbytestransmitted": "Bytes Transmitted",  # Total number of bytes transmitted
        "count200": "Responses with status code of 200",  # Number of responses with a status code of 200
        "count401": "Responses with status code of 401",  # Number of responses with a status code of 401
        "count404": "Responses with status code of 404",  # Number of responses with a status code of 404
        "count503": "Responses with status code of 503",  # Number of responses with a status code of 503
    },
    "transactions": {
        "committedcount": "Transactions Committed",  # Number of committed transactions
        "rolledbackcount": "Transactions Rolled Back",  # Number of rolled back transactions
    },
    "sessions": {
        "sessionstotal": "Total Sessions",  # Total number of sessions
        "activesessionscurrent": "Active Sessions",  # Number of active sessions
        "expiredsessionstotal": "Expired Sessions",  # Total number of expired sessions
        "rejectedsessionstotal": "Rejected Sessions",  # Total number of rejected sessions
    },
    "garbage": {
        "collectioncount-count": "GC Count",  # Number of garbage collections that have occurred
        "collectiontime-count": "GC Time",  # Approximate accumulated collection elapsed time in milliseconds
    },
    "classloading": {
        "loadedclass-count": "Classes Loaded",  # Number of classes that are currently loaded in the JVM
        "totalloadedclass-count": "Total Classes Loaded",  # Total number of classes that have been loaded since the JVM has started execution
        "unloadedclass-count": "Classes Unloaded",  # Total number of classes that have been unloaded since the JVM has started execution
    },
    "uptime": {
        "uptime": "Uptime",  # Amount of time the server has been running in seconds
    },
}

tabs = {
        "Sessions and Transactions": {
        "order": 1,
        "tablist": [
            "Transactions Committed",
            "Transactions Rolled Back",
            "Total Sessions",
            "Active Sessions",
            "Expired Sessions",
            "Rejected Sessions",
            "Total Parse Count Per Sec",
            "Total Parse Count Per Txn",
        ],
    },
    "Memory": {
        "order": 2,
        "tablist": [
            "Used Non Heap Size",
            "MaxHeap Size",
            "Init HeapSize",
            "Init Non Heap Size",
            "Used Heap Size",
            "Committed Non Heap Size",
            "Object Pending Finalization Count",
            "Max Non Heap Size",
            "Committed Heap Size",
        ],
    },
    "Thread": {
        "order": 3,
        "tablist": [
            "Dead Locked Threads",
            "Total Started Thread Count",
            "Daemon Thread Count",
            "Monitor Dead Locked Threads",
            "Current Thread User Time",
            "Peak Thread Count",
            "Thread Count",
            "Current Thread CPU Time",
        ],
    },
    "Request Status": {
        "order": 4,
        "tablist": [
            "Responses with status code of 200",
            "Responses with status code of 401",
            "Responses with status code of 404",
            "Responses with status code of 503",
            "Request_Status_Code_Class",
        ],
    },
    "Class Loading and GC Metrics": {
        "order": 5,
        "tablist": [
            "GC Count",
            "GC Time",
            "Classes Loaded",
            "Total Classes Loaded",
            "Classes Unloaded",
        ],
    },
}


class glassfish:

    def __init__(self, args):

        self.maindata = {}
        self.maindata["plugin_version"] = PLUGIN_VERSION
        self.maindata["heartbeat_required"] = HEARTBEAT
        self.maindata["units"] = METRICS_UNITS
        self.maindata["tabs"] = tabs
        self.logsenabled = args.logs_enabled
        self.logtypename = args.log_type_name
        self.logfilepath = args.log_file_path

        if args.ssl == True or args.ssl.lower() == "true":
            self.url = "https://" + args.host + ":" + args.port
            # print(self.url)
        else:
            self.url = "http://" + args.host + ":" + args.port
            # print(self.url)

        self.username = args.username
        self.password = args.password
        self.connection_success = False

        if args.insecure == "true":
            self.insecure = False
        else:
            self.insecure = True

        ### Parse Lighttp Server Stats Data

    def parseData(self, line, metrics):
        # print output
        data = {}
        try:
            # line = json.loads(output)
            KEYS = metric_keys[metrics]
            verify_keys = KEYS.keys()
            # print(KEYS)

            if line["exit_code"] == "SUCCESS":
                elements = line["extraProperties"]
                elements = elements["entity"]
                # print(elements)


                if elements:

                    for key, value in elements.items():
                        # print(key, value["count"])

                        if key in verify_keys and "count" in value:
                            # print(key, value["count"])
                            if key in ["currentthreadcputime", "currentthreadusertime"]:
                                data[KEYS[key]] = value["count"] / 1e+6
                            else:
                                data[KEYS[key]] = value["count"]
                        elif key in verify_keys and "current" in value:
                            data[KEYS[key]] = value["current"]

                else:
                    data["msg"] = "Enable Monitoring"

        except Exception as e:
            data["msg"] = str(e)
            # traceback.print_exc()

        return data

    def urlGet(self, endpoint):

        maindata = {}
        try:
            if self.username.lower() != "none":
                response = requests.get(
                    self.url + endpoint,
                    auth=HTTPBasicAuth(self.username, self.password),
                    verify=self.insecure,
                )
            else:
                response = requests.get(self.url + endpoint, verify=self.insecure)
            response.raise_for_status()
            self.connection_success = True

        except requests.exceptions.HTTPError as err:
            self.maindata["msg"] = "HTTP status code " + str(err)
            # self.maindata["status"] = 0
            maindata["exit_code"] = 0
            return maindata

        except requests.exceptions.RequestException as err:
            self.maindata["msg"] = "Requests Exception found: " + str(err)
            # self.maindata["status"] = 0
            maindata["exit_code"] = 0
            return maindata

        except Exception as e:
            self.maindata["msg"] = str(e)
            # self.maindata["status"] = 0
            maindata["exit_code"] = 0
            return maindata

        result = response.json()

        return result

    def metricData(self, endpoints):

        maindata = {}
        for metric, endpoint in endpoints.items():

            # print("\n",metric,endpoint,"\n")
            interdata = self.parseData(self.urlGet(endpoint), metric)
            maindata.update(interdata)

            if "status" in interdata and interdata["status"] == 0:
                return maindata

        return maindata

    def metriccollector(self):
        try:

            api_endpoints = {
                "memory": "/monitoring/domain/server/jvm/memory.json",
                "thread": "/monitoring/domain/server/jvm/thread-system.json",
                "requests": "/monitoring/domain/server/web/request.json",
                "servlet": "/monitoring/domain/server/web/servlet.json",
                "transactions": "/monitoring/domain/server/transaction-service.json",
                "sessions": "/monitoring/domain/server/web/session.json",
                "garbage": "/monitoring/domain/server/jvm/garbage-collectors/G1%20Young%20Generation.json",
                "classloading": "/monitoring/domain/server/jvm/class-loading-system.json",
                "uptime": "/monitoring/domain/server.json",
            }

            interdata = self.metricData(api_endpoints)
            self.maindata.update(interdata)

            uptime = self.urlGet("/monitoring/domain/server.json")

            if uptime["exit_code"] == "SUCCESS":

                elements = uptime["extraProperties"]
                elements = elements["entity"]

                if elements:
                    self.maindata["Uptime"] = elements["uptime"]

            request_codes = self.urlGet(
                "/monitoring/domain/server/http-service/server/request.json"
            )
            requests_list = []

            if request_codes["exit_code"] == "SUCCESS":

                elements = request_codes["extraProperties"]
                elements = elements["entity"]
                requests_dict = {}
                

                if elements:
                    metrics = metric_keys["Request_Status_Code_Class"]
                    verify_keys=metrics.keys()

                    for key, value in elements.items():
                        requests_dict = {}

                        if (
                            "xx" in key or key == "countother"
                        ):  # Number of responses with a status code the 2xx, 3xx, 4xx, and 5xx range and outside of these ranges",

                            requests_dict["name"] = key.replace("count", "")
                            requests_dict["count"] = value["count"]
                            requests_list.append(requests_dict)

                        elif key in verify_keys:

                            self.maindata[metrics[key]] = value["count"]

            self.maindata["Request_Status_Code_Class"] = requests_list

            if not self.connection_success:
                self.maindata["status"] = 0

        except Exception as e:
            self.maindata["msg"] = str(e)
            self.maindata["status"] = 0
            return self.maindata

        applog = {}
        if self.logsenabled in ["True", "true", "1"]:
            applog["logs_enabled"] = True
            applog["log_type_name"] = self.logtypename
            applog["log_file_path"] = self.logfilepath
        else:
            applog["logs_enabled"] = False
        self.maindata["applog"] = applog
        return self.maindata


if __name__ == "__main__":

    glassfish_status_url = "http://localhost:4848"
    glassfish_host = "localhost"
    glassfish_port = "4848"
    glassfish_ssl = "false"
    glassfish_insecure = "false"

    username = "None"
    password = "None"

    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--logs_enabled",
        help="enable log collection for this plugin application",
        default="False",
    )
    parser.add_argument(
        "--log_type_name", help="Display name of the log type", nargs="?", default=None
    )
    parser.add_argument(
        "--log_file_path",
        help="list of comma separated log file paths",
        nargs="?",
        default=None,
    )
    parser.add_argument(
        "--host", help="glassfish host ip", nargs="?", default=glassfish_host
    )
    parser.add_argument(
        "--port", help="glassfish admin port", nargs="?", default=glassfish_port
    )
    parser.add_argument(
        "--ssl",
        help="Will connect using https if true and http if false",
        nargs="?",
        default=glassfish_ssl,
    )
    parser.add_argument(
        "--insecure",
        help="Insecure connection if true",
        nargs="?",
        default=glassfish_insecure,
    )
    parser.add_argument("--username", help="username", nargs="?", default=username)
    parser.add_argument("--password", help="password", nargs="?", default=password)
    args = parser.parse_args()

    obj = glassfish(args)
    result = obj.metriccollector()
    if (platform.system() == "Windows"):
        print(json.dumps(result))
    else:
        print(json.dumps(result, indent=True))
