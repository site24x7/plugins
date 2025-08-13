
import json
import platform
import subprocess

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

TOPCOMMAND='top','-b', '-n', '1'

def metricCollector():
    data = {}
    data['plugin_version'] = PLUGIN_VERSION
    data['heartbeat_required']=HEARTBEAT

    try:
        proc = subprocess.Popen(TOPCOMMAND,stdout=subprocess.PIPE,close_fds=True)
        top_output = proc.communicate()[0].decode()
        for line in top_output.split('\n'):
            if not line:
                continue
            if line.startswith('Tasks') and line.endswith('zombie'):
                try:
                    zombies_raw = line.split(',')[-1]
                    if 'zombie' in zombies_raw:
                        data['zombies'] = zombies_raw.split()[0]
                        break
                except Exception as e:
                    data['status']=0
                    data['msg']=str(e)

    except Exception as e:
        data['status']=0
        data['msg']='error while parsing top output'+str(e)
    
    return data


def run(param=None):
    obj=metricCollector()
    return obj


if __name__ == '__main__':
    
    print(json.dumps(metricCollector(), indent=4, sort_keys=True))
