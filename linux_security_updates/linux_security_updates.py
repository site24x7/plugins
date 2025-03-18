#!/usr/bin/python3
import json
import os
import os.path
import subprocess
import hashlib
from datetime import datetime


PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={}


class security_update_check:            

    def __init__(self):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS
        self.log_enabled="True"
        self.logtypename="Linux Pending Updates"
        self.logfilepath="/opt/site24x7/monagent/plugins/linux_security_updates/updates_list*.txt"

    def calculate_sha256_hash(self,input_string):

        sha256_hash = hashlib.sha256()
        sha256_hash.update(input_string.encode('utf-8'))
        return sha256_hash.hexdigest()
           
    def get_command_updates_output(self,command):

        p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)
        (updates_output, err) = p.communicate()
        
        p_status = p.wait()
        return updates_output
    
    def log_creator(self, command, reboot_required_packages):
            current_datetime = datetime.now()
            file_time=current_datetime.strftime("%Y-%m-%d-%H:%M:%S")
            plugin_script_path=os.path.dirname(os.path.realpath(__file__))
            updates_output =self.get_command_updates_output(command).decode()
            og_updates_output=updates_output.split("\n")
            log_count=len(og_updates_output)//4

            if reboot_required_packages:
                for pkg in reboot_required_packages:
                    if "debian" in self.os_name or "suse" in self.os_name:
                        updates_output+="\nPackage: {}".format(pkg)
                        updates_output+="\nVersion: Installed"
                        updates_output+="\nInstalled-Size: - - "
                        updates_output+="\nDescription: Installed but Reboot is required for this package."
                    else:
                        updates_output+="\nName        : {}".format(pkg)
                        updates_output+="\nVersion         : Installed"
                        updates_output+="\nSize        : - -"
                        updates_output+="\nDescription        : Installed but Reboot is required for this package."

            output_hash=self.calculate_sha256_hash(updates_output)                
            log_details_raw=updates_output.split("\n")
            log_details_raw.remove('')
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
            return log_count


    def metriccollector(self):
        try:
            
            os_content=""
            self.os_name=""
            distro_file="/etc/os-release"
            if not os.path.isfile(distro_file):
                self.maindata['msg']=distro_file+", Does not exist"
                self.maindata['status']=0
                return self.maindata
            
            with open(distro_file, 'r') as f:
                os_content=f.read()

            fileContent = os_content.splitlines()
            if fileContent == []:
                self.maindata['msg']="{} is empty".format(distro_file)
                self.maindata['status']=0
                return self.maindata

            for line in fileContent:
                if line.startswith('ID_LIKE='):
                    _, self.os_name = line.split('=', 1)
                    self.os_name = self.os_name.strip('"')
                    break  
                
            if not self.os_name:
                self.maindata['msg'] = "Distro information not found in {}".format(distro_file)
                self.maindata['status'] = 0
                return self.maindata

            if "debian" in self.os_name:

                reboot_required_packages_list="/var/run/reboot-required.pkgs"
                reboot_required_packages=None
                if os.path.isfile("/var/run/reboot-required"):
                    self.maindata['Reboot Required for packages']="True"
                    if os.path.isfile(reboot_required_packages_list):
                        try:
                            with open(reboot_required_packages_list, "r") as f:
                                reboot_required_packages = [pkg for pkg in f.read().split("\n") if pkg]
                            self.maindata['Reboot Required Packages Count']=len(reboot_required_packages)
                        except Exception as e:
                            self.maindata['msg']=str(e)
                            self.maindata['status']=0
                else:
                    self.maindata['Reboot Required for packages']="False"
                    self.maindata['Reboot Required Packages Count']=0

                ubuntu_command="""apt list --upgradable 2> /dev/null| awk -F'/' '{print $1}' | xargs apt show 2> /dev/null | grep -E "Package:|Version:|Installed-Size:|Description:\""""
                upgrades_count=self.log_creator(ubuntu_command, reboot_required_packages)
                if upgrades_count:
                    self.maindata['Upgrades Available For Installed Packages']=upgrades_count
                else:
                    self.maindata['Upgrades Available For Installed Packages']=0


                install_count_cmd="apt list --installed 2> /dev/null | grep -Ev 'Listing' | wc -l"
                res=self.get_command_updates_output(install_count_cmd).decode('utf-8').strip()
                if res.isdigit():
                    self.maindata['Installed Packages Count']=int(res)-1
                else:
                    self.maindata['Installed Packages Count']=0


                file_path='/var/lib/update-notifier/updates-available'
                if os.path.isfile(file_path):
                    try:
                        with open(file_path, 'r') as f:
                            lines = [line.strip('\n') for line in f]
                        self.maindata['Security Updates'] = 0
                        for line in lines:
                            if line:
                                if ( 'packages can be updated' in line ) or ('can be installed immediately' in line ) or ('can be applied immediately' in line):
                                    self.maindata['Packages to be Updated'] = line.split()[0]
                                if ('updates are security updates' in line) or ('updates are standard security updates' in line) or ("updates is a standard security update" in line):
                                    self.maindata['Security Updates'] = line.split()[0]
                    except Exception as e:
                        self.maindata['msg'] = str(e)
                        self.maindata['status'] = 0
                else:
                    self.maindata['msg'] = "{} does not exist".format(file_path)
                    self.maindata['status'] = 0
                            


            elif "fedora" in self.os_name:


                reboot_required=self.get_command_updates_output("needs-restarting -r").decode()

                reboot_required_packages=[]

                if "Reboot is required to fully utilize these updates." in reboot_required:
                    self.maindata['Reboot Required for packages']="True"
                    if "Core libraries or services have been updated since boot-up:" in reboot_required:
                        for lines in reboot_required.split("\n"):
                            if lines.startswith("  * "):
                                reboot_required_packages.append(lines.replace("  * ",""))
                                #print(lines)
                    self.maindata['Reboot Required Packages Count']=len(reboot_required_packages)
                else:
                    self.maindata['Reboot Required for packages']="False"
                    self.maindata['Reboot Required Packages Count']=0

                updates_check=self.get_command_updates_output("yum list updates")
                updates_check=updates_check.decode()
                
                if "Available Upgrades" in updates_check:
                    centos_command="""yum list updates -q | awk '{print $1}' | xargs yum info | grep -E "^Name|^Version|^Size|^Description\""""
                else:
                    upgrades_count=0
                    centos_command=""

                upgrades_count=self.log_creator(centos_command,reboot_required_packages)

                if upgrades_count:
                    self.maindata['Upgrades Available For Installed Packages']=upgrades_count
                else:
                    self.maindata['Upgrades Available For Installed Packages']=0

                install_count_cmd="rpm -qa | wc -l"
                res=self.get_command_updates_output(install_count_cmd).decode('utf-8').strip()
                if res.isdigit():
                    self.maindata['Installed Packages Count']=res
                else:
                    self.maindata['Installed Packages Count']=0

                command="yum updateinfo list security | grep -Ev \"Updating Subscription Management repositories.|Last metadata expiration check\" | wc -l"
                updates_output = self.get_command_updates_output(command)

                if updates_output:
                    updates_output=updates_output.decode()
                    security_count = updates_output.rstrip()
                    self.maindata['Security Updates'] = security_count
                else:
                    self.maindata['Security Updates'] = 0

            elif "suse" in self.os_name:

                reboot_required=self.get_command_updates_output("zypper needs-rebooting").decode()

                reboot_required_packages=[]

                if "Reboot is suggested to ensure that your system benefits from these updates.Reboot is required to fully utilize these updates." in reboot_required:
                    self.maindata['Reboot Required for packages']="True"
                else:
                    self.maindata['Reboot Required for packages']="False"

                suse_command="""zypper list-updates --all | awk '{print $5}' | xargs zypper info | grep -E "^Name|^Version|^Installed Size|^Summary\""""
                upgrades_count=self.log_creator(suse_command, reboot_required_packages)
                if upgrades_count:
                    self.maindata['Upgrades Available For Installed Packages']=upgrades_count
                else:
                    self.maindata['Upgrades Available For Installed Packages']=0

                install_count_cmd="zypper packages --installed-only | grep -Ev \"Listing|Warning|Loading|Reading\" | wc -l"
                res=self.get_command_updates_output(install_count_cmd).decode('utf-8').strip()
                if res.isdigit():
                    self.maindata['Installed Packages Count']=res
                else:
                    self.maindata['Installed Packages Count']=0

                command="zypper lp -g security | grep -i 'patch needed'"
                updates_output = self.get_command_updates_output(command)
                
                if updates_output:
                    updates_output=updates_output.decode()
                    updates_output = updates_output.rstrip()
                    count = updates_output.split(" ")
                    security_count = count[0].split()[0]
                    if security_count == 'No':
                        self.maindata['Security Updates'] = 0
                    else:
                        self.maindata['Security Updates'] = security_count
                else:
                    self.maindata['Security Updates'] = 0
                        
            else:
                self.maindata['msg']="{} not supported".format(self.os_name)
                self.maindata['status']=0


        except Exception as e:
             self.maindata['msg']=str(e)
             self.maindata['status']=0

        applog={}
        if(self.log_enabled in ['True', 'true', '1']):
                applog["logs_enabled"]=True
                applog["log_type_name"]=self.logtypename
                applog["log_file_path"]=self.logfilepath
        else:
                applog["log_details_enabled"]=False
        self.maindata['applog'] = applog
        return self.maindata


def run(param=None):
    obj=security_update_check()
    result=obj.metriccollector()
    return result

if __name__ == "__main__":
    obj = security_update_check()
    result = obj.metriccollector()
    print(json.dumps(result, indent=True))
