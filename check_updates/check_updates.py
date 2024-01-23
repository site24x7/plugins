#!/usr/bin/python3
import json
import os
import subprocess
import hashlib
from datetime import datetime


PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={}


class update_check:

    def __init__(self):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS
        self.log_enabled="True"
        self.logtypename="Linux_Pending_Updates"
        self.logfilepath="/opt/site24x7/monagent/plugins/check_updates/updates_list*.txt"

    def calculate_sha256_hash(self,input_string):

        sha256_hash = hashlib.sha256()
        sha256_hash.update(input_string.encode('utf-8'))
        return sha256_hash.hexdigest()
            
    def get_command_updates_output(self,command):

        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
        (updates_output, err) = p.communicate()
        p_status = p.wait()
        return updates_output
    
    def log_creator(self, command):
        
            current_datetime = datetime.now()
            file_time=current_datetime.strftime("%Y-%m-%d-%H:%M:%S")
            plugin_script_path=os.path.dirname(os.path.realpath(__file__))
            updates_output =self.get_command_updates_output(command).decode()
            output_hash=self.calculate_sha256_hash(updates_output)                
            log_details_raw=updates_output.split("\n")
            log_details=""

            if os.path.exists("{}/config.json".format(plugin_script_path)):
                with open("{}/config.json".format(plugin_script_path), "r") as f:
                    config=json.load(f)
                    prev_hash=config['hash']
                    file_version=config['file_version']

                if prev_hash!=output_hash:
                    os.remove("{}/updates_list_{}.txt".format(plugin_script_path,file_version))
                    file_version=file_time
                    config={"file_version":file_version, "hash":output_hash}
                    with open("{}/config.json".format(plugin_script_path),"w") as f:
                        json.dump(config, f)
                    with open("{}/updates_list_{}.txt".format(plugin_script_path,file_version), 'a') as f:
                        for i in range(0, len(log_details_raw), 4):
                            log_details=" ".join(log_details_raw[i:i+4])
                            f.write(log_details)
                            f.write("\n")
            else:
                with open("{}/config.json".format(plugin_script_path),"x") as f:
                    config={"file_version":file_time, "hash":output_hash}
                    json.dump(config, f)
                with open("{}/updates_list_{}.txt".format(plugin_script_path, file_time), 'a') as f:
                    for i in range(0, len(log_details_raw), 4):
                            log_details=" ".join(log_details_raw[i:i+4])
                            f.write(log_details)
                            f.write("\n")


    def metriccollector(self):
        try:
            
            os_content=""
            distro_file="/etc/os-release"
            if not os.path.isfile(distro_file):
                self.maindata['msg']=distro_file+", Does not exist"
                self.maindata['status']=0
                return self.maindata
            
            with open(distro_file, 'r') as f:
                os_content=f.read()

            for line in os_content.splitlines():
                if line.startswith('NAME='):
                    _, os_name = line.split('=', 1)
                    os_name = os_name.strip('"')
                    break  


            if os_name=="Ubuntu":

                ubuntu_command="""apt list --upgradable 2> /dev/null| awk -F'/' '{print $1}' | xargs apt show 2> /dev/null | grep -E "Package:|Version:|Installed-Size:|Description:\""""
                self.log_creator(ubuntu_command)

                file_path='/var/lib/update-notifier/updates-available'
                lines = [line.strip('\n') for line in open(file_path)]
                for line in lines:
                    if line:
                        if ( 'packages can be updated' in line ) or ('can be installed immediately' in line ) or ('can be applied immediately' in line):
                            self.maindata['packages_to_be_updated'] = line.split()[0]
                        if ('updates are security updates' in line) or ('updates are standard security updates' in line):
                            self.maindata['security_updates'] = line.split()[0]
                        else:
                            self.maindata['security_updates'] = 0


            elif os_name=="CentOS Linux":

                centos_command="""yum list updates -q | awk '{print $1}' | xargs yum info | grep -E "^Name|^Version|^Size|^Description\""""
                self.log_creator(centos_command)

                command="yum check-update --security | grep -i 'needed for security'"
                updates_output = self.get_command_updates_output(command)
                if updates_output:
                    updates_output=updates_output.decode()
                    updates_output = updates_output.rstrip()
                    count = updates_output.split("needed for security")
                    security_count = count[0].split()[0]
                    if security_count == 'No':
                        self.maindata['security_updates'] = 0
                    else:
                        self.maindata['security_updates'] = security_count
                    packages_count = count[1].split()
                    for each in packages_count:
                        if each.isdigit():
                            self.maindata['packages_to_be_updated']=each
            else:
                self.maindata['msg']="{} not supported".format(os_name)
                self.maindata['status']=0


        except Exception as e:
             self.maindata['msg']=str(e)
             self.maindata['status']=0

        applog={}
        if(self.log_enabled in ['True', 'true', '1']):
                applog["log_enabled"]=True
                applog["log_type_name"]=self.logtypename
                applog["log_file_path"]=self.logfilepath
        else:
                applog["log_details_enabled"]=False
        self.maindata['applog'] = applog
        return self.maindata


def run(param=None):
    obj=update_check()
    result=obj.metriccollector()
    return result

if __name__=="__main__":
    
    obj=update_check()
    result=obj.metriccollector()
    print(json.dumps(result,indent=True))
