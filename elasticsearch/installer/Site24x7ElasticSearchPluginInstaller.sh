#!/bin/bash

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
RESET='\033[0m'

PLUGIN_NAME="elasticsearch"
GITHUB_URL="https://raw.githubusercontent.com/site24x7/plugins/master/elasticsearch"

echo ""
echo -e "${GREEN}======================== Elasticsearch Plugin Installer ========================${RESET}"
echo ""

echo "Checking if Site24x7 Linux Agent is present in the server."
agent_dir="/opt/site24x7/monagent/"

if [ ! -e "$agent_dir" ]; then
    echo -e "${RED}Agent path not found. Kindly provide the agent path.${RESET}"
    echo -e "${YELLOW}Example: /opt/site24x7/monagent/${RESET}"
    read -p "Enter the agent path: " agent_dir
    
    [[ "${agent_dir}" != */ ]] && agent_dir="${agent_dir}/"
    
    if [ ! -e "$agent_dir" ]; then
        echo -e "${RED}Agent path does not exist. Process exited.${RESET}"
        exit 1
    fi
fi

echo -e "${GREEN}Site24x7 Linux Agent found at: ${agent_dir}${RESET}"
echo ""

temp_dir="${agent_dir}temp/plugins/${PLUGIN_NAME}/"
plugins_dir="${agent_dir}plugins/${PLUGIN_NAME}/"

echo -e "${BLUE}======================== Elasticsearch Configuration ========================${RESET}"
echo ""

read -p "Enter the hostname of Elasticsearch instance [localhost]: " hostname
hostname=${hostname:-localhost}

read -p "Enter the port of Elasticsearch instance [9200]: " port
port=${port:-9200}

read -p "Do you have SSL enabled? (y/n) [n]: " ssl_input
ssl_input=${ssl_input:-n}
if [[ "$ssl_input" == "y" || "$ssl_input" == "Y" ]]; then
    ssl_option="true"
else
    ssl_option="false"
fi

read -p "Do you have username/password enabled? (y/n) [n]: " auth_input
auth_input=${auth_input:-n}
if [[ "$auth_input" == "y" || "$auth_input" == "Y" ]]; then
    read -p "Enter Elasticsearch username: " username
    read -sp "Enter Elasticsearch password: " password
    echo ""
else
    username="None"
    password="None"
fi

echo ""
echo -e "${GREEN}Configuration received:${RESET}"
echo "  Hostname: $hostname"
echo "  Port: $port"
echo "  SSL: $ssl_option"
echo "  Username: $username"
echo ""

echo "Creating temporary directory..."
mkdir -p "$temp_dir"
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to create temporary directory. Process exited.${RESET}"
    exit 1
fi
echo -e "${GREEN}Temporary directory created.${RESET}"
echo ""

echo "Downloading plugin files from GitHub repository..."
wget -q "${GITHUB_URL}/${PLUGIN_NAME}.py" -O "${temp_dir}${PLUGIN_NAME}.py"
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to download ${PLUGIN_NAME}.py. Process exited.${RESET}"
    rm -rf "$temp_dir"
    exit 1
fi
echo -e "${GREEN}  ${PLUGIN_NAME}.py downloaded.${RESET}"

wget -q "${GITHUB_URL}/${PLUGIN_NAME}.cfg" -O "${temp_dir}${PLUGIN_NAME}.cfg"
if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to download ${PLUGIN_NAME}.cfg. Process exited.${RESET}"
    rm -rf "$temp_dir"
    exit 1
fi
echo -e "${GREEN}  ${PLUGIN_NAME}.cfg downloaded.${RESET}"
echo ""

echo "Updating configuration file with provided credentials..."
cat > "${temp_dir}${PLUGIN_NAME}.cfg" <<EOF
[global_configurations]
use_agent_python=1

[${hostname}]
host="${hostname}"
port="${port}"
username="${username}"
password="${password}"
ssl_option="${ssl_option}"
cafile="None"
EOF

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to update configuration file. Process exited.${RESET}"
    rm -rf "$temp_dir"
    exit 1
fi
echo -e "${GREEN}Configuration file updated.${RESET}"
echo ""

# Move to plugins directory
echo "Installing plugin to Site24x7 Agent plugins directory..."
if [ -d "$plugins_dir" ]; then
    echo -e "${YELLOW}Plugin directory already exists. Replacing with new installation...${RESET}"
    rm -rf "$plugins_dir"
fi

mv "$temp_dir" "$plugins_dir"

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to install plugin. Process exited.${RESET}"
    exit 1
fi

echo -e "${GREEN}Plugin installed successfully!${RESET}"
echo ""
echo -e "${GREEN}======================== Installation Complete ========================${RESET}"
echo -e "Plugin location: ${plugins_dir}"
echo ""
