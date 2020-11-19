#!/usr/bin/python

import math , json , subprocess

def get_process_uptime(process_name):
    process_cmd = "ps -eo pid,comm,stime,etimes,args | grep -w "+process_name+" | grep -v process_uptime | grep -v grep | awk '{print $3,$4}'"
    p = subprocess.Popen(process_cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    p_status = p.wait()
    output = output.rstrip()
    return output

def timeConversion(time_in_ms,process_data):
    str_time=''
    days = math.floor(time_in_ms / 86400000)
    time_in_ms = time_in_ms-days*86400000

    hrs = math.floor(time_in_ms / 3600000)
    time_in_ms = time_in_ms-hrs*3600000

    mins = math.floor(time_in_ms / 60000)
    time_in_ms=time_in_ms-mins*60000
    
    secs=math.floor(time_in_ms/1000)
    ms=time_in_ms-secs*1000
    
    process_data['days'] = days
    process_data['hours'] = hrs
    process_data['mins'] = mins
    process_data['seconds'] = secs

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--process', help='process to be monitored')
    parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=1)
    parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=True)
    args = parser.parse_args()
    
    process_data = {}    
    process_name = args.process
    process_data['plugin_version'] = args.plugin_version
    process_data['heartbeat_required'] = args.heartbeat
    process_data['process_name'] = process_name
    process_cmd_output = get_process_uptime(process_name)
    if process_cmd_output:
        process_out = process_cmd_output.split()
        process_data['start_time'] = process_out[0]
        time_in_ms = process_out[1]
        time_in_ms = int(time_in_ms) * 1000
        timeConversion(time_in_ms,process_data)
    else:
        process_data['status'] = 0
        process_data['msg'] = "Process {} Not Running".format(process_name)
    
    print(json.dumps(process_data, indent=4, sort_keys=True))
