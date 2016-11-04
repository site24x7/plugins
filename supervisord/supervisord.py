#!/usr/bin/python

"""

__author__ = Vijay, Zoho Corp
Language = Python

Tested in Ubuntu

"""

import supervisor.xmlrpc
import xmlrpclib
import supervisor
import socket
import json

################### CONFIG SECTION START #######################

SERVER_URL = "unix:///var/run//supervisor.sock"		# Give full unix socket path or http server path. eg: http://localhost:9001 or unix:///var/run//supervisor.sock
USER_NAME = None					#If authorization required for accessing the supervisord server, provide username and password.
PASSWORD = None
MONITOR_PROCESS_NAMES = []				#Only provided process names will be monitored, if empty all process will be monitored

################### CONFIG SECTION END ########################

DEFAULT_SERVER_URL = "http://localhost:9001"



# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

class SupervisordMon():
    server = None
    process_names = None

    def __init__(self, config):
        self.process_names = config.get("process_names", None)
        self.server = self._connect_to_server(config)


    def _connect_to_server(self, config):
        server_url = config.get("server_url", DEFAULT_SERVER_URL)
        user = config.get("user_name", None)
        pwd = config.get("password", None)
        if str.startswith(server_url, "http://") or str.startswith(server_url, "https://"):
            if user and pwd:
                auth = "%s:%s@" % (user, pwd)
                server_url = server_url.replace("://", "://"+auth)
            return self.__connect_to_http_server(server_url)
        else:
            return self.__connect_to_unix_server(server_url)

    def __connect_to_http_server(self, full_server_url):
        server = xmlrpclib.Server(full_server_url)

        return server

    def __connect_to_unix_server(self, full_server_url):
        server = xmlrpclib.Server('http://127.0.0.1',
                               transport=supervisor.xmlrpc.SupervisorTransport(
                                    None, None, serverurl=full_server_url))
        return server

    def get_metrics(self):
        metrics = {}
        metrics['plugin_version'] = PLUGIN_VERSION
        metrics['heartbeat_required'] = HEARTBEAT
        try:
            metrics["supervisord_state"] = self.server.supervisor.getState().get('statecode')
            if self.process_names and len(self.process_names) > 0:
                allProcess = []
                for proc_name in self.process_names:
                    try:
                        allProcess.append(self.server.supervisor.getProcessInfo(proc_name))
                    except xmlrpclib.Fault:
                        continue
            else:
                allProcess = self.server.supervisor.getAllProcessInfo()
            metrics["total_process_count"] = len(allProcess)
            stopped = 0
            running = 0
            unknown = 0
            fatal = 0
            for process in allProcess:
                if process["state"] == 20:
                    running += 1
                elif process["state"] == 0:
                    stopped += 1
                elif process["state"] == 1000:
                    unknown += 1
                elif process["state"] == 200:
                    fatal += 1

            metrics["fatal_process_count"] = fatal
            metrics["stopped_process_count"] = stopped
            metrics["running_process_count"] = running
            metrics["unknown_status_process_count"] = unknown
        except socket.error as e:
            metrics["supervisord_state"] = -1
        except xmlrpclib.ProtocolError as e1:
            metrics["msg"] = "Authorization issue"

        return metrics

if __name__ == '__main__':
    config = {"server_url" : SERVER_URL, "user_name" : USER_NAME, "password" :PASSWORD, "process_names" : MONITOR_PROCESS_NAMES}
    mon = SupervisordMon(config)
    metrics = mon.get_metrics()
    print(json.dumps(metrics))
