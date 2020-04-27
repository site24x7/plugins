#!/usr/bin/python

import subprocess,sys,json,traceback,six

DISK_NAME = ''

PLUGIN_VERSION="1"

HEARTBEAT="true"

def parse_iostats(cmd_output,DISK_NAME):
    iostats = {}
    try:
        device_index = cmd_output.rfind('Device:')
        ds = cmd_output[device_index:].rstrip().splitlines()
        if not six.PY3:
            last_data_set = ds
        else:
            last_data_set = ds.pop(0)
            last_data_set = last_data_set.split('\\n')
        for d in last_data_set:
            if d:
                d = d.split()
                dev = d.pop(0)
                if (dev in DISK_NAME) or not DISK_NAME:
                    iostats[dev] = d
    except Exception as e:
        traceback.print_exc()
        data['status']=0
        data['msg']=str(e)
    return iostats

def get_disk_queue_length(data,DISK_NAME):
    try:
        args = '%s %s %s %s' % ('/usr/bin/iostat','-xmt',1,3)

        child = subprocess.Popen(args,bufsize=1,shell=True,stdout=subprocess.PIPE,close_fds=True)

        (stdout, stderr) = child.communicate()
        ecode = child.poll()
        disk_stats = parse_iostats(str(stdout),DISK_NAME)
    except Exception as e:
        data['status']=0
        data['msg']=str(e)

    for k,v in disk_stats.items():
        if k=='Device:' or k=='\'' or 'loop' in k:
            continue
        data['disk_name']=k
        data['disk_queue']=v[7]
    return data
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--disk', help='disk to be monitored for disk queue length')
    args = parser.parse_args()
    if args.disk:
        DISK_NAME = args.disk
    data ={}
    data['plugin_version'] = PLUGIN_VERSION
    data['heartbeat_required'] = HEARTBEAT
    data = get_disk_queue_length(data,DISK_NAME)
    print(json.dumps(data,indent=4))
