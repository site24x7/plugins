#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RESET='\033[0m'
echo 
echo -e "${GREEN}This installer helps you to install the Software Updates plugin for monitoring in Site24x7.
Follow the in-line instructions below to complete the installation successfully.${RESET}"

echo


echo ""
echo "Checking if Site24x7 Linux Agent is present in the server."
agent_dir=/opt/site24x7/monagent/
if [ -e $agent_dir ]; then
    echo -e "${GREEN}Site24x7 Linux Agent is present.${RESET}"
    echo ""
else
    echo -e "${RED}Site24x7 Linux Agent path is not present in the default path.${RESET}"
    echo -e "Enter the path of the directory where the Site24x7 Linux Agent is installed: \c"
    read -r  agent_dir
    if [ -e $agent_dir"/bin" ]; then
        echo -e "${GREEN}Site24x7 Linux Agent is present in the path provided.${RESET}"
        echo ""
    else
        echo -e "${RED}Site24x7 Linux Agent path is not present in the path provided. Install the Site24x7 Linux Agent and rerun the installer. Process exited.${RESET}"
        exit 1
    fi
fi

agent_path=$agent_dir


agent_temp_path=$agent_path"temp/"
agent_plugin_path=$agent_path"plugins/"
temp_plugin_path=$agent_temp_path"plugins/"

if [[ -d $temp_plugin_path ]];then
    mkdir -p $temp_plugin_path
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}Unable to create temporary plugins directory. Process exited.${RESET}"
        exit 1
    fi
fi

linux_security_updates_path=$temp_plugin_path"linux_security_updates/"
if [[ -d $linux_security_updates_path ]];then
    mkdir -p $linux_security_updates_path
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}Unable to create temporary linux_security_updates plugins directory. Process exited.${RESET}"
        exit 1
    fi
fi

url_py="https://raw.githubusercontent.com/site24x7/plugins/master/linux_security_updates/linux_security_updates.py"
url_cfg="https://raw.githubusercontent.com/site24x7/plugins/master/linux_security_updates/linux_security_updates.cfg"



if [[ -e $linux_security_updates_path"linux_security_updates.py"  ]]; then
    rm -rf $linux_security_updates_path"linux_security_updates.py"
fi

if [[ -e $linux_security_updates_path"linux_security_updates.cfg"  ]]; then
    rm -rf $linux_security_updates_path"linux_security_updates.cfg"
fi

echo 
echo "Downloading the plugin files."
wget -P $linux_security_updates_path $url_py
if [[ $? -ne 0 ]]; then
    echo -e "${RED}linux_security_updates.py file not downloaded. Process exited.${RESET}"
    exit 1
fi 

wget -P $linux_security_updates_path $url_cfg
if [[ $? -ne 0 ]]; then
    echo -e "${RED}linux_security_updates.cfg file not downloaded. Process exited.${RESET}"
    exit 1
fi 


chmod 744 $linux_security_updates_path"linux_security_updates.py"
if [[ $? -ne 0 ]]; then
    echo -e "${RED} Error occured. Process exited.${RESET}"
    exit 1
fi 


echo "Executing the plugin to check for valid metrics."
json_output=$($linux_security_updates_path/linux_security_updates.py)
result=$(echo "$json_output" | grep -o '"status": 0')
echo 
echo $json_output
if [[ $result ]]; then
    echo -e "${RED} Error occured. Process exited.${RESET}"
    exit 1
fi


if [[ -d $agent_plugin_path"linux_security_updates" ]]; then
    echo -e "${BLUE}The linux_security_updates plugin already exist in the plugin directory and needs to be reinstalled.${RESET}"

    read -p  "Press 'y' to reinstall." response
    response=${response,,}
    if [[ -z "$response" ]]; then

        read -p  "Reinstallion is required to add the plugin. Press 'y' to continue." response
        response=${response,,}
        if [[ -z "$response" ]]; then
            echo -e "${RED} Invalid response. Process exited.${RESET}"
            exit 1
        fi
            
    fi

    if [[ "$response" =~ ^(yes|y)$ ]]; then
        echo "${BLUE} Reinstalling the plugin. ${RESET}"
        rm -rf $agent_plugin_path"linux_security_updates"
        if [[ $? -ne 0 ]]; then
            echo -e "${RED}Error occured. Process exited.${RESET}"
            exit 1
        fi

        mv $linux_security_updates_path $agent_plugin_path
        if [[ $? -ne 0 ]]; then
            echo -e "${RED}Error occured. Process exited.${RESET}"
            exit 1
        fi

    elif [[ "$response" =~ ^(no|n)$ ]]; then
        echo -e "${RED} Invalid response. Process exited.${RESET}"
        exit 1
    fi

    else

    mv $linux_security_updates_path $agent_plugin_path
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}Error occured. Process exited.${RESET}"
        exit 1
    fi

fi

echo " ------------------------------------------------------- linux_security_updates plugin successfully installed ----------------------------------------------- "
echo " -----------------------------------------   Navigate to the Plugins tab in Site24x7 to view the plugin monitor.  --------------------------------------"
