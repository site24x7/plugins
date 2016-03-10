#!/usr/bin/python

import socket
import json

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

#Config Section:
ZOOKEEPER_HOST='127.0.0.1'

ZOOKEEPER_PORT=2181


class ZooKeeper(object):
    def __init__(self,config):
        self.configurations=config
        self.zookeeper_commands = ['mntr','srvr','ruok','conf']
        self.host=self.configurations.get('host', 'localhost')
        self.port=self.configurations.get('port', '2181')

    def metricCollector(self):
        
        data = {}
        #defaults
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT
        
        for command in self.zookeeper_commands:

            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                s.settimeout(4)#socket timeout

                s.connect((self.host, self.port))

                s.sendall(command)
                reply = s.recv(1024)
                if command == 'conf':
                    data = self.parse_conf(data, reply)
                elif command == 'ruok':
                    data = self.parse_ruok(data, reply)
                elif command == 'srvr':
                    data = self.parse_srvr(data, reply)
                elif command == 'mntr':
                    data = self.parse_mntr(data, reply)

                del s
            except Exception as exception:
                data['status']=0
                data['msg']='failed to read from socket'

        return data

    def parse_conf(self, data, reply):
        
        for line in reply.split('\n'):
            if not line:
                continue
            key, value = line.split('=')
            if key in ['dataDir', 'dataLogDir']:
                continue
            data[key.lower()] = int(value)
        return data

    def parse_mntr(self, data, reply):
        
        data['zk_server_state'] = -1

        for line in reply.split('\n'):
            if not line:
                continue
            split_line = line.split('\t')
            key = split_line[0]
            if key == 'zk_version':
                continue

            value = split_line[1].split('.')[0]
            if key == 'zk_server_state':
                if value == 'standalone':
                    value = 0
                elif value == 'leader':
                    value = 1
                elif value == 'follower':
                    value = 2

            data[key.lower()] = int(value)

        return data

    def parse_ruok(self, data, reply):
        if reply == 'imok':
            data['imok'] = 0
        else:
            data['imok'] = 1
        return data

    def parse_srvr(self, data, reply):
        
        for line in reply.split('\n'):
            if not line or line.startswith('Zookeeper version'):
                continue
            key, value = line.split(':')

            if key in ['Mode', 'Zxid']:
                continue

            if key.startswith('Latency min/avg/max'):
                data['latency_min'] = int(value.split('/')[0])
                data['latency_avg'] = int(value.split('/')[1])
                data['latency_max'] = int(value.split('/')[2])
            else:
                data[key.lower()] = int(value.strip())
        return data

if __name__ == "__main__":
   
    configurations = {'host':ZOOKEEPER_HOST,'port':ZOOKEEPER_PORT}

    zookeeper_plugin = ZooKeeper(configurations)
   
    result = zookeeper_plugin.metricCollector()

    print json.dumps(result, indent=4, sort_keys=True)