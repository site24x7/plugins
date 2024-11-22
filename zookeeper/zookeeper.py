#!/usr/bin/python3

import socket
import json

PLUGIN_VERSION = "1"
HEARTBEAT = "true"

ZOOKEEPER_HOST = '127.0.0.1'
ZOOKEEPER_PORT = 2181


class ZooKeeper:
    def __init__(self, config):
        self.configurations = config
        self.zookeeper_commands = ['mntr', 'srvr', 'ruok', 'conf']
        self.host = self.configurations.get('host', 'localhost')
        self.port = int(self.configurations.get('port', 2181))

    def check_connection(self):
        """Check if ZooKeeper is accessible by connecting to the host and port."""
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(4)
                s.connect((self.host, self.port))
                return True
        except socket.error as e:
            return False

    def metricCollector(self):
        data = {
            'plugin_version': PLUGIN_VERSION,
            'heartbeat_required': HEARTBEAT,
        }
        errors = []

        if not self.check_connection():
            data['status'] = 0
            data['msg'] = f'Unable to connect to ZooKeeper at {self.host}:{self.port}'
            return data

        for command in self.zookeeper_commands:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(4)
                    s.connect((self.host, self.port))
                    s.sendall(command.encode())
                    reply = s.recv(8192).decode()

                    if command == 'conf':
                        data = self.parse_conf(data, reply, 'Configuration')
                    elif command == 'ruok':
                        data = self.parse_ruok(data, reply, 'AreYouOk')
                    elif command == 'srvr':
                        data = self.parse_srvr(data, reply, 'Server')
                    elif command == 'mntr':
                        data = self.parse_mntr(data, reply, 'Monitor')

            except Exception as e:
                errors.append(f'Failed to execute command "{command}": {str(e)}')

        if errors:
            data['msg'] = '; '.join(errors)

        return data

    def parse_conf(self, data, reply, prefix):
        for line in reply.split('\n'):
            if '=' in line:
                try:
                    key, value = line.split('=', 1)
                    data[f'{prefix}.{key.lower()}'] = value.strip()
                except ValueError:
                    pass
        return data

    def parse_mntr(self, data, reply, prefix):
        state_map = {'standalone': 0, 'leader': 1, 'follower': 2}
        for line in reply.split('\n'):
            if '\t' in line:
                try:
                    key, value = line.split('\t', 1)
                    if key == 'zk_server_state':
                        data[f'{prefix}.{key.lower()}'] = state_map.get(value.strip(), -1)
                    else:
                        data[f'{prefix}.{key.lower()}'] = int(value) if value.isdigit() else value
                except ValueError:
                    pass
        return data

    def parse_ruok(self, data, reply, prefix):
        data[f'{prefix}.ok'] = 1 if reply.strip() == 'imok' else 0
        return data

    def parse_srvr(self, data, reply, prefix):
        for line in reply.split('\n'):
            line = line.strip()
            if line and ':' in line:
                try:
                    key, value = line.split(':', 1)
                    key = key.strip().lower()
                    value = value.strip()
                    if key.startswith('latency min/avg/max'):
                        latencies = value.split('/')
                        if len(latencies) == 3:
                            data[f'{prefix}.latency_min'], data[f'{prefix}.latency_avg'], data[f'{prefix}.latency_max'] = map(int, latencies)
                    elif key.startswith('proposal sizes last/min/max'):
                        proposals = value.split('/')
                        if len(proposals) == 3:
                            data[f'{prefix}.proposal_sizes_last'], data[f'{prefix}.proposal_sizes_min'], data[f'{prefix}.proposal_sizes_max'] = map(int, proposals)
                    else:
                        data[f'{prefix}.{key}'] = int(value) if value.isdigit() else value
                except ValueError:
                    pass
        return data


if __name__ == "__main__":
    configurations = {'host': ZOOKEEPER_HOST, 'port': ZOOKEEPER_PORT}
    zookeeper_plugin = ZooKeeper(configurations)
    result = zookeeper_plugin.metricCollector()
    print(json.dumps(result, indent=4, sort_keys=True))
