#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RESET='\033[0m'



echo ""
echo "Checking if Site24x7 Linux Agent is present in the server."
agent_dir=/opt/site24x7/monagent/
if [ -e $agent_dir ]; then
    echo -e "${GREEN}Site24x7 Linux Agent is present.${RESET}"
    echo ""
else
    echo -e "${RED}Site24x7LinuxAgent path is not present in the default path.${RESET}"
    echo -e "Enter the path of the directory where the Site24x7LinuxAgent is installed: \c"
    read -r  agent_dir
    if [ -e $agent_dir"/bin" ]; then
        echo -e "${GREEN}Site24x7 Linux Agent is present in the path provided.${RESET}"
        echo ""
    else
        echo -e "${RED}Site24x7LinuxAgent path is not present in the path provided. Install the Site24x7LinuxAgent and rerun the installer. Process exited.${RESET}"
        exit 1
    fi
fi


if command -v python3 &>/dev/null; then
    python_version=$(python3 -c 'import sys; print(sys.version_info[:3][1])')
    if [ $python_version  -ge 7 ];then
        echo $python_version
    else
        echo -e "${RED}Python 3.7 or above is required to monitor Oracle DB using the plugin.\nEnsure Python 3.7 or a later version is installed and then run the installer again to proceed with the plugin installation.${RESET}"
            exit 1
    fi
else
    echo "Python 3.7 or above is required to monitor Oracle DB using the plugin. 
          Ensure Python 3.7 or a later version is installed and then run the installer again to proceed with the plugin installation."
          echo ""
    exit 1
fi

pip3 --version &> /dev/null
if [[ $? -ne 0 ]]; then
    echo -e "${RED}pip3 is required to monitor Oracle DB. Ensure pip3 is installed and then run the installer again to proceed with the plugin installation.${RESET}"
    echo ""
    exit 1
fi


echo "The oracledb Python module is required to connect to the Oracle DB instance."
read -p "Do you want to continue? (y/n): " response
response=${response,,}
if [[ -z "$response" ]]; then
    exit 1
fi

if [[ "$response" =~ ^(yes|y)$ ]]; then
    echo "Installing oracledb."
    pip3 install oracledb &> /dev/null
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}Error occured. oracledb python module could not be installed. Process exited.${RESET}"
        exit 1
    fi


elif [[ "$response" =~ ^(no|n)$ ]]; then
    echo "The oracledb Python module is required to install the plugin. Process exited."
    exit 1
fi



if [[ -f "Site24x7OraclePluginInstallerAddOn.py" ]]; then
    rm -rf ./Site24x7OraclePluginInstallerAddOn.py
fi

echo ""
echo -e "${GREEN}Downloding related installation files from our GitHub repository. ${RESET}"
wget "https://raw.githubusercontent.com/site24x7/plugins/master/oracle/Installer/Site24x7OraclePluginInstallerAddOn.py" &> /dev/null
if [[ $? -ne 0 ]]; then
    echo -e "${RED} Download failed. Process exited.${RESET}"
    exit 1
fi

echo -e "${GREEN}Download completed.${RESET}"

chmod 744 Site24x7OraclePluginInstallerAddOn.py
if [[ $? -ne 0 ]]; then
    echo -e "${GREEN}Adding execution permissions failed. Process exited.${RESET}"
    exit 1
fi
echo "Executing the Oracle installer."
./Site24x7OraclePluginInstallerAddOn.py
if [[ $? -ne 0 ]]; then
    echo -e "${RED}Error occured. Execution failed. Process exited.${RESET}"
    exit 1
fi
