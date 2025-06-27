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


Site24x7ElasticSearchPluginInstallerAddOn.py

if command -v python3 &>/dev/null; then
    echo "Python is installed."    
else
    echo "Python 3.6 or above is required to monitor Elasticsearch using the plugin. 
          Ensure Python 3.7 or a later version is installed and then run the installer again to proceed with the plugin installation."
    exit 1
fi



if [[ -f "Site24x7ElasticSearchPluginInstallerAddOn.py" ]]; then
    rm -rf ./Site24x7ElasticSearchPluginInstallerAddOn.py
fi

echo ""
echo -e "${GREEN}Downloding related installation files from our GitHub repository. ${RESET}"
wget "https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearch/installer/Site24x7ElasticSearchPluginInstallerAddOn.py" &> /dev/null
if [[ $? -ne 0 ]]; then
    echo -e "${RED} Download failed. Process exited.${RESET}"
    exit 1
fi

echo -e "${GREEN}Download completed.${RESET}"



echo "Executing the Elasticsearch installer."
python3 Site24x7ElasticSearchPluginInstallerAddOn.py
if [[ $? -ne 0 ]]; then
    echo -e "${RED}Error occured. Execution failed. Process exited.${RESET}"
    exit 1
fi
