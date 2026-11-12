#!/usr/bin/python

import json 
import subprocess

PLUGIN_VERSION = 1

HEARTBEAT = True


def get_process_details(process_name):
    process_cmd = "ps -eo ruser,pid,args  | grep -wiE '"+process_name+"' | grep -v grep | grep -v process_availability "
    p = subprocess.Popen(process_cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    output = output.rstrip()
    return output

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--process', help='process to be monitored', type=str, nargs='?')
    args = parser.parse_args()
    
    process_data = {}    
    process_name = args.process
    process_data['plugin_version'] = PLUGIN_VERSION
    process_data['heartbeat_required'] = HEARTBEAT
    process_data['process_name'] = process_name
    process_cmd_output = get_process_details(process_name)
    
    if type(process_cmd_output) != str :
        process_cmd_output = process_cmd_output.decode("utf-8") 
    
    
    
    count = 0
    if process_cmd_output:
        process_data['status'] = 0
        process_data['msg'] = "Process {} : Running".format(process_name)
        for line in process_cmd_output.split("\n") :
            count = count+1
            data = line.split()
    else:
        process_data['status'] = 1
        process_data['msg'] = "Process {} : Not Running".format(process_name)
    
    process_data['process_running'] = count
    
    print(json.dumps(process_data, indent=4, sort_keys=True))
