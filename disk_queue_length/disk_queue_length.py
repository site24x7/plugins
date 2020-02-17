import subprocess,sys,json,traceback,six

DISKS = []

PLUGIN_VERSION="1"

HEARTBEAT="true"

data ={}
data['plugin_version'] = PLUGIN_VERSION
data['heartbeat_required'] = HEARTBEAT

def parse_iostats(cmd_output):
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
                if (dev in DISKS) or not DISKS:
                    iostats[dev] = d
    except Exception as e:
        traceback.print_exc()
    return iostats

try:
    args = '%s %s %s %s' % ('/usr/bin/iostat','-xmt',1,3)

    child = subprocess.Popen(args,bufsize=1,shell=True,stdout=subprocess.PIPE,close_fds=True)

    (stdout, stderr) = child.communicate()
    ecode = child.poll()
    disk_stats = parse_iostats(str(stdout))
except Exception as e:
    traceback.print_exc()

for k,v in disk_stats.items():
    if k=='Device:' or k=='\'':
        continue
    data[k+'_disk_queue']=v[7]

print(json.dumps(data,indent=4))