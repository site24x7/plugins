#!/bin/bash

blue='\033[0;34m'   
green='\033[0;32m'
red='\033[0;31m'
reset='\033[0m'
echo
echo
echo "${blue}Installing the MySQL plugin.${reset}"
echo

agent_path="/opt/site24x7/monagent/" 
agent_temp_path=$agent_path"temp/"
    
# checking the existance of Agent Temporary Directory
if [ ! -d $agent_temp_path ] ; then
    echo "${red}The Site24x7LinuxAgent directory is not present. Install the Site24x7LinuxAgent and try installing the plugin again (or) Run the Installation script as root user${reset}"
    echo
    return 0
        
fi

python_version=$(python3 --version 2>&1)
# Extracting the major and minor version numbers from the Python version string
major_version=$(echo $python_version | cut -d ' ' -f 2 | cut -d '.' -f 1)
minor_version=$(echo $python_version | cut -d ' ' -f 2 | cut -d '.' -f 2)
if [ "$major_version" -eq 3 ] && [ $minor_version -ge 7 ] || [ $major_version -gt 3 ]; then
    echo ""
else
    echo "${red}Python 3.7 or above is required to monitor MySQL using the plugin. Ensure Python 3.7 or a later version is installed and then run the installer again to proceed with the plugin installation.${reset}"
    return 0
fi

echo "${blue}Downloading installation related files from the Site24x7 GitHub repository.${reset}"
wget https://raw.githubusercontent.com/site24x7/plugins/master/mysql_monitoring/installer/Site24x7MySQLPluginInstallerAddOn.py

if [ $? -ne 0 ] ; then
    echo "${red}Error occured. Process exited.${reset}"
    return 0
fi
echo ""
echo "${blue}Downloading pymysql binary to establish connection with MySQL.${reset}"
wget https://github.com/site24x7/plugins/raw/master/mysql_monitoring/pymysql/pymysql.zip && unzip pymysql.zip && rm pymysql.zip &> /dev/null
if [ $? -ne 0 ] ; then
    echo "${red}Error occured. Process exited.${reset}"
    return 0
fi
python3 Site24x7MySQLPluginInstallerAddOn.py
