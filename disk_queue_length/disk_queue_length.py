#!/usr/bin/python

import subprocess,sys,json,traceback,six

disks= ""

PLUGIN_VERSION= 1

HEARTBEAT="true"

def parse_iostats(cmd_output,disks):
    iostats = {}
    try:
        device_index = cmd_output.rfind('Device')
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
                if (dev in disks) or not disks:
                    iostats[dev] = d
    except Exception as e:
        traceback.print_exc()
        data['status']=0
        data['msg']=str(e)
    return iostats

def get_disk_queue_length(data,disks):
    try:
        args = '%s %s %s %s' % ('/usr/bin/iostat','-xmt',1,3)

        child = subprocess.Popen(args,shell=True,stdout=subprocess.PIPE,close_fds=True)

        (stdout, stderr) = child.communicate()
        ecode = child.poll()
        disk_stats = parse_iostats(str(stdout),disks)
    except Exception as e:
        data['status']=0
        data['msg']=str(e)
    for k,v in disk_stats.items():
        if k=='Device' or k=='\'' or 'loop' in k:
            continue
        data[ k+ '_disk_queue']=v[7]
    return data
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--disks', help='disk to be monitored for disk queue length', type=str)
    args = parser.parse_args()
    if args.disks:
        disks = args.disks
    if disks != '':
        disks= disks.split(',')
    data ={}
    data['plugin_version'] = PLUGIN_VERSION
    data['heartbeat_required'] = HEARTBEAT
    data = get_disk_queue_length(data,disks)
    print(json.dumps(data,indent=4))
