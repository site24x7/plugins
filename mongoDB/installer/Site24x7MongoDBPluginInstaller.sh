#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RESET='\033[0m'
echo
echo -e "${GREEN}This installer helps you to install the MongoDB plugin for monitoring in Site24x7.
Follow the in-line instructions below to complete the installation successfully.${RESET}"

echo
echo "Ensure you meet the following prerequisites before proceeding. 
Continue if you meet the prerequisites, or run the installer again once the prerequisites are met.

  1. Ensure you have Site24x7 Linux monitoring agent installed in the server.
  2. Python 3 or a higher version should be installed in the server."

echo
echo "-------------------- Checking prerequisites --------------------"

echo ""
echo "Checking if the Site24x7 Linux Agent is present in the server."
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
    echo "Python is installed."    
else
    echo "Python is required to monitor MongoDB using the plugin. 
          Ensure Python 3 or higher version is installed and then run the installer again to proceed with the plugin installation."
    exit 1
fi



if [ -f "Site24x7MongoDBPluginInstallerAddOn.py" ]; then
    rm -rf ./Site24x7MongoDBPluginInstallerAddOn.py
fi



echo ""
echo -e "${GREEN}Downloading related installation files from the Site24x7 GitHub repository. ${RESET}"
wget -q "https://raw.githubusercontent.com/site24x7/plugins/mani/mongoDB/installer/Site24x7MongoDBPluginInstallerAddOn.py" &> /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED} Download failed. Process exited.${RESET}"
    exit 1
fi

if [ -f "pymongo.pyz" ]; then
    rm -rf ./pymongo.pyz
fi
echo ""

wget -q "https://github.com/site24x7/plugins/raw/mani/mongoDB/pymongo.pyz" &> /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED} Download failed. Process exited.${RESET}"
    exit 1
fi



echo -e "${GREEN}Download completed.${RESET}"



python3 Site24x7MongoDBPluginInstallerAddOn.py
if [ $? -ne 0 ]; then
    echo -e "${RED}Error occured. Execution failed. Process exited.${RESET}"
    exit 1
fi
