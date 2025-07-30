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
    echo "Python3 is installed."
    python_cmd="python3"
else
    echo -e "${RED}Python3 command is not identified in the system PATH.${RESET}"
    echo "Python is required to monitor MongoDB using the plugin."
    echo ""
    read -r -p "Please enter your Python version (e.g., python3.10, python3.9, python3.11): " python_version
    
    if command -v "$python_version" &>/dev/null; then
        echo -e "${GREEN}$python_version found in system PATH.${RESET}"
        python_cmd="$python_version"
    else
        echo -e "${RED}$python_version is not found in the system PATH.${RESET}"
        echo "You can find your Python installation using:"
        echo "  - which $python_version"
        echo "  - which python3"
        echo ""
        read -r -p "Enter the full path to your Python 3 executable: " python_cmd
        
        if [ -x "$python_cmd" ]; then
            version=$($python_cmd --version 2>&1)
            if [[ $version == *"Python 3"* ]]; then
                echo -e "${GREEN}Python found at: $python_cmd${RESET}"
            else
                echo -e "${RED}The provided path does not point to Python 3. Please ensure you provide a valid Python 3 executable path.${RESET}"
                exit 1
            fi
        else
            echo -e "${RED}The provided path is not a valid executable. Please check the path and try again.${RESET}"
            exit 1
        fi
    fi
fi

if [ -f "Site24x7MongoDBPluginInstallerAddOn.py" ]; then
    rm -rf ./Site24x7MongoDBPluginInstallerAddOn.py
fi



echo ""
echo -e "${GREEN}Downloading related installation files from the Site24x7 GitHub repository. ${RESET}"
wget -q "https://raw.githubusercontent.com/site24x7/plugins/master/mongoDB/installer/Site24x7MongoDBPluginInstallerAddOn.py" &> /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED} Download failed. Process exited.${RESET}"
    exit 1
fi


if [ -f "pymongo.pyz" ]; then
    rm -rf ./pymongo.pyz
fi
echo ""

wget -q "https://github.com/site24x7/plugins/raw/master/mongoDB/pymongo.pyz" &> /dev/null
if [ $? -ne 0 ]; then
    echo -e "${RED} Download failed. Process exited.${RESET}"
    exit 1
fi



echo -e "${GREEN}Download completed.${RESET}"

if [[ "$python_cmd" = /* ]]; then
    python_full_path="$python_cmd"
else
    python_full_path=$(which "$python_cmd")
    if [ -z "$python_full_path" ]; then
        python_full_path=$($python_cmd -c "import sys; print(sys.executable)" 2>/dev/null)
        if [ -z "$python_full_path" ]; then
            python_full_path="$python_cmd"
        fi
    fi
fi

$python_cmd Site24x7MongoDBPluginInstallerAddOn.py "$python_full_path"
if [ $? -ne 0 ]; then
    echo -e "${RED}Error occured. Execution failed. Process exited.${RESET}"
    exit 1
fi
