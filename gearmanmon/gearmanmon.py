#!/usr/bin/python

"""

__author__ = Vijay, Zoho Corp
Language = Python

Tested in Ubuntu, Windows 8

"""

import gearman
import json

############################ CONFIG SECTION START #############################

host = "localhost"
port = 4730

############################ CONFIG SECTION END #############################


DEFAULT_HOST = "localhost"
DEFAULT_PORT = 4730


# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"


class GearmanMon():
    metrics = {}

    def __init__(self, config):
        self.host = config.get("host", DEFAULT_HOST)
        self.port = config.get("port", DEFAULT_PORT)

        server_url = "%s:%s" % (self.host, self.port)
        self.gm_admin_client = gearman.GearmanAdminClient([server_url])

    def get_worker_stats(self, tasks):
        workers = 0
        running = 0
        queued = 0

        for task in tasks:
            workers += task['workers']
            running += task['running']
            queued += task['queued']

        self.metrics['workers'] = workers
        self.metrics['running'] = running
        self.metrics['queued'] = queued

        self.metrics['unique_tasks'] = len(tasks)

    def get_metrics(self):
        self.metrics['plugin_version'] = PLUGIN_VERSION
        self.metrics['heartbeat_required'] = HEARTBEAT
        try :
            response_time = self.gm_admin_client.ping_server()
            self.metrics['response_time'] = response_time

            status_response = self.gm_admin_client.get_status()
            self.get_worker_stats(status_response)

        except gearman.errors.ServerUnavailable as e:
            self.metrics['msg'] = "server not reachable"
        except AssertionError as e:
            self.metrics['msg'] = "check host name and port"

        return self.metrics


if __name__ == '__main__':
    config = {"host" : host, "port" : port}
    mon = GearmanMon(config)
    metrics = mon.get_metrics()

    print(json.dumps(metrics))





