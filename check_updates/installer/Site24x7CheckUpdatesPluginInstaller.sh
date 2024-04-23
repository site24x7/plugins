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
echo "Ensure you meet the following prerequisites before proceeding. 
Continue if you meet the prerequisites, or run the installer again once the prerequisites are met.

  1. Ensure you have Site24x7 Linux monitoring agent installed in the server."

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

check_updates_path=$temp_plugin_path"check_updates/"
if [[ -d $check_updates_path ]];then
    mkdir -p $check_updates_path
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}Unable to create temporary check_updates plugins directory. Process exited.${RESET}"
        exit 1
    fi
fi

url_py="https://raw.githubusercontent.com/site24x7/plugins/master/check_updates/check_updates.py"
url_cfg="https://raw.githubusercontent.com/site24x7/plugins/master/check_updates/check_updates.cfg"



if [[ -e $check_updates_path"check_updates.py"  ]]; then
    rm -rf $check_updates_path"check_updates.py"
fi

if [[ -e $check_updates_path"check_updates.cfg"  ]]; then
    rm -rf $check_updates_path"check_updates.cfg"
fi

echo 
echo "Downloading the plugin files."
wget -P $check_updates_path $url_py
if [[ $? -ne 0 ]]; then
    echo -e "${RED}check_updates.py file not downloaded. Process exited.${RESET}"
    exit 1
fi 

wget -P $check_updates_path $url_cfg
if [[ $? -ne 0 ]]; then
    echo -e "${RED}check_updates.cfg file not downloaded. Process exited.${RESET}"
    exit 1
fi 


chmod 744 $check_updates_path"check_updates.py"
if [[ $? -ne 0 ]]; then
    echo -e "${RED} Error occured. Process exited.${RESET}"
    exit 1
fi 


echo "Executing the plugin to check for valid metrics."
json_output=$($check_updates_path/check_updates.py)
result=$(echo "$json_output" | grep -o '"status": 0')
echo 
echo $json_output
if [[ $result ]]; then
    echo -e "${RED} Error occured. Process exited.${RESET}"
    exit 1
fi


if [[ -d $agent_plugin_path"check_updates" ]]; then
    echo -e "${BLUE}The check_updates plugin already exist in the plugin directory and needs to be reinstalled.${RESET}"

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
        rm -rf $agent_plugin_path"check_updates"
        if [[ $? -ne 0 ]]; then
            echo -e "${RED}Error occured. Process exited.${RESET}"
            exit 1
        fi

        mv $check_updates_path $agent_plugin_path
        if [[ $? -ne 0 ]]; then
            echo -e "${RED}Error occured. Process exited.${RESET}"
            exit 1
        fi

    elif [[ "$response" =~ ^(no|n)$ ]]; then
        echo -e "${RED} Invalid response. Process exited.${RESET}"
        exit 1
    fi

    else

    mv $check_updates_path $agent_plugin_path
    if [[ $? -ne 0 ]]; then
        echo -e "${RED}Error occured. Process exited.${RESET}"
        exit 1
    fi

fi

echo " ------------------------------------------------------- check_updates plugin successfully installed ----------------------------------------------- "
echo " -----------------------------------------   Navigate to the Plugins tab in Site24x7 to view the plugin monitor.  --------------------------------------"
