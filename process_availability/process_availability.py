#!/usr/bin/python

import json 
import subprocess


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
    parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=1)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=True)
    args = parser.parse_args()
    
    process_data = {}    
    process_name = args.process
    process_data['plugin_version'] = args.plugin_version
    process_data['heartbeat_required'] = args.heartbeat
    process_data['process_name'] = process_name
    process_cmd_output = get_process_details(process_name)
    
    if type(process_cmd_output) != str :
        process_cmd_output = process_cmd_output.decode("utf-8") 
    
    
    
    users = []
    count = 0
    if process_cmd_output:
        for line in process_cmd_output.split("\n") :
            count = count+1
            data = line.split()
            users.append(data[0])
    else:
        process_data['status'] = 0
        process_data['msg'] = "Process {} Not Running".format(process_name)
    
    process_data['process_running'] = count
    
    print(json.dumps(process_data, indent=4, sort_keys=True))
