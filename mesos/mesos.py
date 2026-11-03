
import json
import urllib.request

PLUGIN_VERSION = 1
HEARTBEAT = True

HOSTNAME = 'localhost'
PORT = '5050'
PROTOCOL = 'http'
USERNAME = 'None'
PASSWORD = 'None'
VERIFY_SSL = 'true'

METRICS_UNITS = {
    'CPU Usage': '%',
    'Memory Usage': '%',
    'Disk Usage': '%',
    'GPU Usage': '%',
    'Disk Total': 'MB',
    'Disk Used': 'MB',
    'Memory Total': 'MB',
    'Memory Used': 'MB',
    'State Fetch Time': 'min',
    'State Store Time': 'min',
}

summary_metrics = {
    'master/elected': 'Master Elected',
    'master/dropped_messages': 'Dropped Messages',
    'master/frameworks_active': 'Active Frameworks',
    'master/slaves_active': 'Active Agents',
    'master/slaves_connected': 'Connected Agents',
    'master/tasks_running': 'Running Tasks',
    'master/cpus_percent': 'CPU Usage',
    'master/mem_percent': 'Memory Usage',
    'master/disk_percent': 'Disk Usage',
    'master/uptime_secs': 'Uptime',
}

tab_metrics = {
    'Agents': {
        'master/slave_registrations': 'Agent Registrations',
        'master/slave_reregistrations': 'Agent Re-registrations',
        'master/slave_removals': 'Agent Removals',
        'master/slave_shutdowns_scheduled': 'Agent Shutdowns Scheduled',
        'master/slave_shutdowns_canceled': 'Agent Shutdowns Canceled',
        'master/slave_shutdowns_completed': 'Agent Shutdowns Completed',
        'master/slaves_disconnected': 'Disconnected Agents',
        'master/slaves_inactive': 'Inactive Agents',
    },
    'Tasks': {
        'master/tasks_dropped': 'Tasks Dropped',
        'master/tasks_error': 'Tasks Error',
        'master/tasks_failed': 'Tasks Failed',
        'master/tasks_finished': 'Tasks Finished',
        'master/tasks_gone': 'Tasks Gone',
        'master/tasks_gone_by_operator': 'Tasks Gone By Operator',
        'master/tasks_killed': 'Tasks Killed',
        'master/tasks_killing': 'Tasks Killing',
        'master/tasks_lost': 'Tasks Lost',
        'master/tasks_staging': 'Tasks Staging',
        'master/tasks_starting': 'Tasks Starting',
        'master/tasks_unreachable': 'Tasks Unreachable',
    },
    'Resources': {
        'master/cpus_used': 'CPUs Used',
        'master/disk_total': 'Disk Total',
        'master/disk_used': 'Disk Used',
        'master/gpus_percent': 'GPU Usage',
        'master/gpus_total': 'GPUs Total',
        'master/gpus_used': 'GPUs Used',
        'master/mem_total': 'Memory Total',
        'master/mem_used': 'Memory Used',
    },
    'System': {
        'master/valid_status_updates': 'Valid Status Updates',
        'master/invalid_status_updates': 'Invalid Status Updates',
        'registrar/queued_operations': 'Registrar Queued Operations',
        'registrar/registry_size_bytes': 'Registry Size',
        'registrar/state_fetch_ms': 'State Fetch Time',
        'registrar/state_store_ms': 'State Store Time',
    },
    'Messages': {
        'master/messages_authenticate': 'Messages Authenticate',
        'master/messages_deactivate_framework': 'Messages Deactivate Framework',
        'master/messages_decline_offers': 'Messages Decline Offers',
        'master/messages_executor_to_framework': 'Messages Executor To Framework',
        'master/messages_exited_executor': 'Messages Exited Executor',
        'master/messages_framework_to_executor': 'Messages Framework To Executor',
        'master/messages_kill_task': 'Messages Kill Task',
        'master/messages_launch_tasks': 'Messages Launch Tasks',
        'master/messages_reconcile_operations': 'Messages Reconcile Operations',
        'master/messages_reconcile_tasks': 'Messages Reconcile Tasks',
        'master/messages_register_framework': 'Messages Register Framework',
        'master/messages_register_slave': 'Messages Register Agent',
        'master/messages_reregister_framework': 'Messages Re-register Framework',
        'master/messages_reregister_slave': 'Messages Re-register Agent',
        'master/messages_resource_request': 'Messages Resource Request',
        'master/messages_revive_offers': 'Messages Revive Offers',
        'master/messages_status_update': 'Messages Status Update',
        'master/messages_suppress_offers': 'Messages Suppress Offers',
        'master/messages_unregister_framework': 'Messages Unregister Framework',
        'master/messages_unregister_slave': 'Messages Unregister Agent',
        'master/messages_update_slave': 'Messages Update Agent',
        'master/messages_status_update_acknowledgement': 'Messages Status Update Ack',
        'master/messages_operation_status_update_acknowledgement': 'Messages Operation Status Update Ack',
    },
}


def is_none(value):
    return value is None or str(value).strip().lower() in ['none', '']


class MesosMonitoring:

    def __init__(self, args):
        self.maindata = {}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required'] = HEARTBEAT
        self.maindata['units'] = METRICS_UNITS

        self.hostname = args.hostname
        self.port = args.port
        self.protocol = args.protocol
        self.username = args.username
        self.password = args.password
        self.verify_ssl = args.verify_ssl.strip().lower() == 'true'

        if is_none(self.username):
            self.username = None
        if is_none(self.password):
            self.password = None

    def metriccollector(self):
        try:
            import ssl

            url = f"{self.protocol}://{self.hostname}:{self.port}/metrics/snapshot"

            if self.username and self.password:
                pwd_manager = urllib.request.HTTPPasswordMgrWithDefaultRealm()
                pwd_manager.add_password(None, url, self.username, self.password)
                auth_handler = urllib.request.HTTPBasicAuthHandler(pwd_manager)
            else:
                auth_handler = None

            if self.protocol == 'https' and not self.verify_ssl:
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                https_handler = urllib.request.HTTPSHandler(context=ssl_context)
            else:
                https_handler = None

            handlers = [h for h in [auth_handler, https_handler] if h is not None]
            if handlers:
                opener = urllib.request.build_opener(*handlers)
                response = opener.open(url, timeout=10)
            else:
                req = urllib.request.Request(url)
                response = urllib.request.urlopen(req, timeout=10)

            data = json.loads(response.read().decode())

            for api_key, display_name in summary_metrics.items():
                self.maindata[display_name] = data.get(api_key, None)

            for tab_name, metrics_map in tab_metrics.items():
                for api_key, display_name in metrics_map.items():
                    self.maindata[display_name] = data.get(api_key, None)

            uptime_secs = self.maindata.get('Uptime', 0) or 0
            if uptime_secs >= 3600:
                self.maindata['Uptime'] = str(round(uptime_secs / 3600, 2)) + " Hours"
            else:
                self.maindata['Uptime'] = str(round(uptime_secs / 60, 2)) + " Minutes"

            registry_bytes = self.maindata.get('Registry Size', 0) or 0
            if registry_bytes >= 1048576:
                self.maindata['Registry Size'] = str(round(registry_bytes / 1048576, 2)) + " MB"
            elif registry_bytes >= 1024:
                self.maindata['Registry Size'] = str(round(registry_bytes / 1024, 2)) + " KB"
            else:
                self.maindata['Registry Size'] = str(int(registry_bytes)) + " Bytes"

            for key in ('State Fetch Time', 'State Store Time'):
                ms_val = self.maindata.get(key)
                if ms_val is not None:
                    self.maindata[key] = round(ms_val / 60000, 4)

        except Exception as e:
            self.maindata['msg'] = str(e)
            self.maindata['status'] = 0

        self.maindata['tabs'] = {
            'Agents': {
                'order': 1,
                'tablist': list(tab_metrics['Agents'].values()),
            },
            'Tasks': {
                'order': 2,
                'tablist': list(tab_metrics['Tasks'].values()),
            },
            'Resources': {
                'order': 3,
                'tablist': list(tab_metrics['Resources'].values()),
            },
            'System': {
                'order': 4,
                'tablist': list(tab_metrics['System'].values()),
            },
            'Messages': {
                'order': 5,
                'tablist': list(tab_metrics['Messages'].values()),
            }
        }

        return self.maindata


def clean_quotes(value):
    if not value:
        return value
    value_str = str(value)
    if value_str.startswith('"') and value_str.endswith('"'):
        return value_str[1:-1]
    elif value_str.startswith("'") and value_str.endswith("'"):
        return value_str[1:-1]
    return value_str


def run(param):
    hostname = clean_quotes(param.get("hostname")) if param and param.get("hostname") else HOSTNAME
    port = clean_quotes(param.get("port")) if param and param.get("port") else PORT
    protocol = clean_quotes(param.get("protocol")) if param and param.get("protocol") else PROTOCOL
    username = clean_quotes(param.get("username")) if param and param.get("username") else USERNAME
    password = clean_quotes(param.get("password")) if param and param.get("password") else PASSWORD
    verify_ssl = clean_quotes(param.get("verify_ssl")) if param and param.get("verify_ssl") else VERIFY_SSL

    class Args:
        def __init__(self, hostname, port, protocol, username, password, verify_ssl):
            self.hostname = hostname
            self.port = port
            self.protocol = protocol
            self.username = username
            self.password = password
            self.verify_ssl = verify_ssl

    args = Args(hostname, port, protocol, username, password, verify_ssl)
    obj = MesosMonitoring(args)
    result = obj.metriccollector()
    return result


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', help='Hostname of Mesos Master', default=HOSTNAME)
    parser.add_argument('--port', help='Port number for Mesos Master', default=PORT)
    parser.add_argument('--protocol', help='Protocol (http or https)', default=PROTOCOL)
    parser.add_argument('--username', help='Username for Mesos authentication', default=USERNAME)
    parser.add_argument('--password', help='Password for Mesos authentication', default=PASSWORD)
    parser.add_argument('--verify_ssl', help='Verify SSL certificate (true or false)', default=VERIFY_SSL)
    args = parser.parse_args()

    obj = MesosMonitoring(args)
    result = obj.metriccollector()
    print(json.dumps(result, indent=4))
