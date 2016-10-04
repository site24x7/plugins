#!/usr/bin/python

 ### Monitoring CPU Performance

 ### It uses top command to get the raw server performance data
 ### cpustats.py unlike normal server cpu monitoring metrics, gives data of all the CPU metrics returned in top command output like (user cpu time, system cpu time, user nice cpu time, idle cpu time, io wait cpu time, hardware irq, software irq and steal time)
 ### Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server
 
 ### Author: Narmadha, Zoho Corp
 ### Language : Python
 ### Tested in Ubuntu, Centos, Rhel

import subprocess
import json

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Mention the units of your metrics in this python dictionary. If any new metrics are added make an entry here for its unit.
METRIC_UNITS={'user_percentage':'%','system_percentage':'%','nicetime_percentage':'%','idle_percentage':'%','iowait_percentage':'%','hardwareirq_percentage':'%','software_irq':'%','steal_time':'%'}

if __name__ == '__main__':
    cmd = 'top -b -d1 -n1 | grep -i "Cpu(s)"'
    data = {}
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
     
    ## Wait for date to terminate. Get return returncode ##
    p_status = p.wait()
    
    info = output.split(',')
    for index, _ in enumerate(info):
        if index==0:
            cpu_val =  _.strip().split(':')[1].strip()
            if '%' in cpu_val :
                info[index] = cpu_val.split('%')[0]
            else:
                info[index] = _.strip().split(':')[1].strip().split()[0]
        else:
            cpu_val =  _.strip()
            if '%' in cpu_val :
                info[index] = _.strip().split('%')[0]
            else:
                info[index] = _.strip().split()[0]

    
    data['user_percentage'] = info[0]
    data['system_percentage'] = info[1]
    data['nicetime_percentage'] = info[2]
    data['idle_percentage'] = info[3]
    data['iowait_percentage'] = info[4]
    data['hardwareirq_percentage'] = info[5]
    data['software_irq'] = info[6]
    data['steal_time'] = info[7]
    
    data['heartbeat_required'] = HEARTBEAT
    data['plugin_version'] = PLUGIN_VERSION
    data['units'] = METRIC_UNITS
    print(json.dumps(data, indent=2, sort_keys=False))
    
