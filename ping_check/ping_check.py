#!/usr/bin/python

import subprocess

import json,os,sys

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

# if the ping needs to happen via an specific source/interface kindly provide the ip or name here
INTERFACE_IP=None

HOST='172.20.11.11'

METRICS_UNITS={'packet_loss':'%'}

def get_ping_status(HOST_TO_PING,data):
    try:
        if sys.platform == 'win32':
            if INTERFACE_IP:    
                cmd = 'ping -S '+INTERFACE_IP+' -n 3 '+HOST+' > /dev/null 2>&1'
            else:
                cmd = 'ping -n 3 '+HOST+' > /dev/null 2>&1'    
        if sys.platform.startswith('linux'):
            if INTERFACE_IP:    
                cmd = 'ping -I '+INTERFACE_IP+' -c 3 '+HOST+' > /dev/null 2>&1'
            else:
                cmd = 'ping -c 3 '+HOST+' > /dev/null 2>&1'    
        response = os.system(cmd)
        if response == 0:
            data['ping_status'] = 1
        elif response == 512:
            data['ping_status'] = 0
            data['status']=0
            data['msg'] = 'unknown host'
        elif response == 256:
            data['ping_status'] = 0
            data['status'] = 0
            data['msg'] = 'ping timed out'
        else:
            data['ping_status'] = 0
    except Exception as e:
        data['status'] = 0
        data['msg'] = str(e)
    return data

def get_packet_loss(HOST,data):
    try:
        cmd='ping -c 3 '+HOST
        if sys.platform == 'win32':
            cmd='ping -n 3 '+HOST
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        p_status = p.wait()
        if output:
            if sys.platform == 'win32':
                packetloss = float([x for x in output.decode('utf-8').split('\n') if x.find('loss') != -1][0].split('%')[0].split(' ')[-1].split('(')[-1])
            else:
                packetloss = float([x for x in output.decode('utf-8').split('\n') if x.find('packet loss') != -1][0].split('%')[0].split(' ')[-1])
            data['packet_loss']= str(packetloss)
    except Exception as e:
        pass
    return data

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='remote host for ping')
    args = parser.parse_args()
    if args.host:
        HOST=args.host
    data = {}
    data['plugin_version']=PLUGIN_VERSION
    data['heartbeat_required']=HEARTBEAT
    data = get_ping_status(HOST,data)
    data = get_packet_loss(HOST,data)
    data['units']=METRICS_UNITS
    print(json.dumps(data, indent=4, sort_keys=True))
