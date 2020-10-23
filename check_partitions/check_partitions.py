#!/usr/bin/python

import subprocess,json

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"


data = {}
data['plugin_version'] = PLUGIN_VERSION
data['heartbeat_required']=HEARTBEAT

disk_part_cmd = 'lsblk --raw --noheading'

mount_cmd = "blkid -o list | grep 'not mounted'"

def get_cmd_output(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate() 
    p_status = p.wait()
    return output.strip()


output = get_cmd_output(disk_part_cmd)
outpur = str(output)
a = output.splitlines()

part_list = []
disk_list = []

for each in a:
    each = str(each)
    inner_list = each.split()
    name = inner_list[0] 
    if 'disk' in each:
        disk_list.append(name)
    if 'part' in each:
        part_list.append(name)

for disk in disk_list:
    if disk in str(part_list):
        data['status']=1
    else:
        data['status']=0
        data['msg']="{} is not having any partitions ".format(disk)
        break

output = get_cmd_output(mount_cmd)
unmounted_partitions = []
p = output.splitlines()

for each in p:
    name = each.split()[0]
    if '/' in name and name.split('/')[2] in part_list:
        unmounted_partitions.append(each.split()[0])

if unmounted_partitions:
    if 'msg' in data:
        data['msg'] = data['msg'] + " &  " + "unmounted partitions found : {}".format(str(unmounted_partitions))
    else:
        data['msg'] =  "unmounted partitions found : {}".format(str(unmounted_partitions))
        data['status'] = 0

print(json.dumps(data))