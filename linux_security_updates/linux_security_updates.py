#!/usr/bin/python3
import json
import os
import os.path
import subprocess
import argparse
import hashlib
import traceback
from datetime import datetime


PLUGIN_VERSION=1
HEARTBEAT=True
METRICS_UNITS={}
timeout=5

class security_update_check:            

    def __init__(self,timeout):
        
        self.maindata={}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required']=HEARTBEAT
        self.maindata['units']=METRICS_UNITS
        self.log_enabled="True"
        self.logtypename="Linux Pending Updates"
        self.logfilepath="/opt/site24x7/monagent/plugins/linux_security_updates/updates_list*.txt"
        self.timeout=int(timeout)
        self.plugin_script_path=os.path.dirname(os.path.realpath(__file__))
        self.package_list=os.path.join(self.plugin_script_path,"packages_list.txt")

    def calculate_sha256_hash(self,input_string):

        sha256_hash = hashlib.sha256()
        sha256_hash.update(input_string.encode('utf-8'))
        return sha256_hash.hexdigest()
           
    def get_command_updates_output(self,command):
        try:

            p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True,stderr=subprocess.PIPE)
            (updates_output, err) = p.communicate(timeout=self.timeout)
            p_status = p.wait()

        except subprocess.TimeoutExpired as e:
            #print(command)
            # traceback.print_exc()
            return ""
        except Exception as e:
            # traceback.print_exc()
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return ""
        return updates_output
    
    def get_updates_list(self,command1,command2,reboot_required_packages):

        try:
            first_output=self.get_command_updates_output(command1)
            if first_output=="":
                return ""
            if os.path.exists(self.package_list):
                if os.path.getsize(self.package_list) == 0:
                    return 0                                # Exit if the update packages list is empty
            second_output=self.get_command_updates_output(command2)
            if second_output=="":
                return ""
            updates_output=self.log_creator(second_output, reboot_required_packages)

        except Exception as e:
            # traceback.print_exc()
            self.maindata['msg']=str(e)
            self.maindata['status']=0
            return ""
        return updates_output
            

    
    def log_creator(self, updates_output, reboot_required_packages):
            current_datetime = datetime.now()
            file_time=current_datetime.strftime("%Y-%m-%d-%H:%M:%S") 
            updates_output = updates_output.decode()
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

            if os.path.exists("{}/config.json".format(self.plugin_script_path)):
                with open("{}/config.json".format(self.plugin_script_path), "r") as f:
                    config=json.load(f)
                    prev_hash=config['hash']
                    file_version=config['file_version']

                if prev_hash!=output_hash:
                    os.remove("{}/updates_list_{}.txt".format(self.plugin_script_path,file_version))
                    file_version=file_time
                    config={"file_version":file_version, "hash":output_hash}
                    with open("{}/config.json".format(self.plugin_script_path),"w") as f:
                        json.dump(config, f)
                    with open("{}/updates_list_{}.txt".format(self.plugin_script_path,file_version), 'a') as f:
                        for i in range(0, len(log_details_raw), 4):
                            log_details=" ".join(log_details_raw[i:i+4])
                            f.write(log_details)
                            f.write("\n")
            else:
                with open("{}/config.json".format(self.plugin_script_path),"x") as f:
                    config={"file_version":file_time, "hash":output_hash}
                    json.dump(config, f)
                with open("{}/updates_list_{}.txt".format(self.plugin_script_path, file_time), 'a') as f:
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

                # ubuntu_command="""apt list --upgradable 2> /dev/null| awk -F'/' '{print $1}' | xargs apt show 2> /dev/null | grep -E "Package:|Version:|Installed-Size:|Description:\""""
                # upgrades_count=self.log_creator(ubuntu_command, reboot_required_packages)

                upgrades_count=self.get_updates_list("apt list --upgradable 2> /dev/null | awk -F'/' '{print $1}' >"+self.package_list,"cat {}| xargs apt show 2> /dev/null | grep -E \"Package:|Version:|Installed-Size:|Description:\"".format(self.package_list), reboot_required_packages)
                
                if upgrades_count == "":
                    self.maindata['Upgrades Available For Installed Packages'] = -1
                if upgrades_count:
                    self.maindata['Upgrades Available For Installed Packages']=upgrades_count
                else:
                    self.maindata['Upgrades Available For Installed Packages']=0

                install_count_cmd="apt list --installed 2> /dev/null | grep -Ev 'Listing' | wc -l"
                res=self.get_command_updates_output(install_count_cmd)
                if res == "":
                    self.maindata['Installed Packages Count'] = -1
                else:
                    res=res.decode('utf-8').strip()
                if res.isdigit():
                    self.maindata['Installed Packages Count']=res
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

                reboot_required=self.get_command_updates_output("needs-restarting -r")

                reboot_required_packages=[]
                centos_command=""

                if reboot_required == "":
                    self.maindata['Reboot Required for packages']="False"
                    self.maindata['Reboot Required Packages Count']=-1
                else:
                    reboot_required=reboot_required.decode()

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

                # centos_command="""yum list updates --noplugins -q | awk '{print $1}' | xargs yum info --noplugins --available | grep -E "^Name|^Version|^Size|^Description\""""
                # upgrades_count=self.log_creator(centos_command,reboot_required_packages)

                upgrades_count=self.get_updates_list("yum list updates --noplugins -q | awk '{print $1}' > "+self.package_list,"cat {} | xargs yum info --noplugins --available | grep -E \"^Name|^Version|^Size|^Description\"".format(self.package_list), reboot_required_packages)

                if upgrades_count == "":
                    self.maindata['Upgrades Available For Installed Packages'] = -1
                elif upgrades_count:
                    self.maindata['Upgrades Available For Installed Packages']=upgrades_count
                else:
                    self.maindata['Upgrades Available For Installed Packages']=0

                install_count_cmd="rpm -qa | wc -l"
                res=self.get_command_updates_output(install_count_cmd)
                if res == "":
                    self.maindata['Installed Packages Count'] = -1
                else:
                    res=res.decode('utf-8').strip()
                if res.isdigit():
                    self.maindata['Installed Packages Count']=res
                else:
                    self.maindata['Installed Packages Count']=0

                command="yum updateinfo list security --noplugins | grep -Ev \"Updating Subscription Management repositories.|Last metadata expiration check\" | wc -l"
                updates_output = self.get_command_updates_output(command)

                if updates_output=="":
                    self.maindata['Security Updates'] = -1
                elif updates_output:
                    updates_output=updates_output.decode()
                    security_count = updates_output.rstrip()
                    self.maindata['Security Updates'] = security_count
                else:
                    self.maindata['Security Updates'] = 0

            elif "suse" in self.os_name:

                reboot_required=self.get_command_updates_output("zypper needs-rebooting")

                reboot_required_packages=[]

                if reboot_required == "":
                    self.maindata['Reboot Required for packages']=-1
                else:
                    reboot_required=reboot_required.decode()
                
                if "Reboot is suggested to ensure that your system benefits from these updates.Reboot is required to fully utilize these updates." in reboot_required:
                    self.maindata['Reboot Required for packages']="True"
                else:
                    self.maindata['Reboot Required for packages']="False"

                # suse_command="""zypper list-updates --all | awk '{print $5}' | xargs zypper info | grep -E "^Name|^Version|^Installed Size|^Summary\""""
                # upgrades_count=self.log_creator(suse_command, reboot_required_packages)
                
                upgrades_count=self.get_updates_list("zypper list-updates --all | awk '{print $5}' > "+self.package_list,"cat {} | xargs zypper info | grep -E \"^Name|^Version|^Installed Size|^Summary\"".format(self.package_list), reboot_required_packages)

                if upgrades_count == "":
                    self.maindata['Upgrades Available For Installed Packages'] = -1
                elif upgrades_count:
                    self.maindata['Upgrades Available For Installed Packages']=upgrades_count
                else:
                    self.maindata['Upgrades Available For Installed Packages']=0

                install_count_cmd="rpm -qa | wc -l"
                res=self.get_command_updates_output(install_count_cmd)

                if res == "":
                    self.maindata['Installed Packages Count']=-1
                else:
                    res=res.decode('utf-8').strip()
                if res.isdigit():
                    self.maindata['Installed Packages Count']=res
                else:
                    self.maindata['Installed Packages Count']=0

                command="zypper lp -g security | grep -i 'patch needed'"
                updates_output = self.get_command_updates_output(command)
                
                if updates_output=="":
                    self.maindata['Security Updates'] = -1
                elif updates_output:
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
             # traceback.print_exc()

        applog={}
        if(self.log_enabled in ['True', 'true', '1']):
                applog["logs_enabled"]=True
                applog["log_type_name"]=self.logtypename
                applog["log_file_path"]=self.logfilepath
        else:
                applog["log_details_enabled"]=False
        self.maindata['applog'] = applog
        return self.maindata


def run(param={}):

    obj=security_update_check(param.get('timeout',5))
    result=obj.metriccollector()
    return result

if __name__ == "__main__":

    parser=argparse.ArgumentParser()
    parser.add_argument('--timeout',help="Host Name",nargs='?', default=timeout)
    args=parser.parse_args()
    obj = security_update_check(args.timeout)
    result = obj.metriccollector()
    print(json.dumps(result, indent=True))
