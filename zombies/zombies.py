#!/usr/bin/python

import json
import platform
import subprocess

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"


class Zombies(object):

    def __init__(self):
        pass

    def metricCollector(self):
        data = {}
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT

        if platform.system() == 'Linux':
            try:
                proc = subprocess.Popen(['top', '-b', '-n', '1'],stdout=subprocess.PIPE,close_fds=True)
                top_output = proc.communicate()[0]
                for line in top_output.split('\n'):
                    if not line:
                        continue
                    if line.startswith('Tasks') and line.endswith('zombie'):
                        try:
                            zombies_raw = line.split(',')[-1]
                            if 'zombie' in zombies_raw:
                                data['zombies'] = zombies_raw.split()[0]
                        except Exception as exception:
                            data['status']=0
                            data['msg']='error while parsing top output'

            except Exception as exception:
                data['status']=0
                data['msg']='error while executing top command'
        else:
            data['status']=0
            data['msg']='OS not supported'
        
        return data


if __name__ == '__main__':
    
    zombies_check = Zombies()

    print json.dumps(zombies_check.metricCollector(), indent=4, sort_keys=True)