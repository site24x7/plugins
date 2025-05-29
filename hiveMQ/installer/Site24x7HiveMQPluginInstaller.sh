#!/bin/bash

plugin=hiveMQ
agent_dir=/opt/site24x7/monagent
temp_dir=$agent_dir/temp/plugins/$plugin
py_file="$temp_dir/$plugin.py"
cfg_file="$temp_dir/$plugin.cfg"
reinstall=false
plugin_dir=$agent_dir/plugins/
flag=0
agent_path_change=false
python=""

func_exit() {
    tput sgr0
    exit 0
}

trap func_exit SIGINT SIGTSTP

error_handler() {
    if [ $1 -ne 0 ]; then
        tput setaf 1
        echo "------------Error occurred. Process exited.---------"
        echo $2
        tput sgr0
        exit 1
    fi
}

agent_check() {
    if ! [ -d "$agent_dir/bin" ]; then
        agent_path_change=true
        output=$(ls $agent_dir)
        if ! echo "$output" | grep -qE ": Permission denied"; then
            error_handler $? "$output"
        fi
        tput setaf 3
        echo "The Site24x7LinuxAgent is not found at $agent_dir"
        echo -e "Enter the path where the Site24x7LinuxAgent is installed: \c"
        read -r agent_dir
        tput sgr0
    fi
}

for (( i=0; i<3; i++ )); do
  agent_check
  if [ -z "$agent_dir" ]; then
    tput setaf 1
    echo "Please provide the correct path to the Site24x7LinuxAgent."
    agent_dir=/opt/site24x7/monagent
    tput sgr0
  else
    agent_status=$($agent_dir/bin/monagent status)
    if ! echo "$agent_status" | grep -q "Site24x7 monitoring agent service"; then
        tput setaf 1
        echo "Invalid Site24x7 agent directory."
        tput sgr0
    else
        break
    fi
  fi

  if [ $i -eq 2 ]; then
      echo "Agent not found. Exiting."
      exit 1
  fi
done

download_files() {
    file_name=$1
    echo "Downloading: $file_name"
    echo
    output=$(wget -P $temp_dir $file_name 2>&1)
    error_handler $? "$output"
    tput setaf 2
    echo "$(grep -E 'HTTP|saved' <<< "$output")"
    tput sgr0
    echo
}

install() {
    mkdir -p $temp_dir
    rm -f "$py_file" "$cfg_file"
    download_files https://raw.githubusercontent.com/site24x7/plugins/refs/heads/master/$plugin/$plugin.cfg
    download_files https://raw.githubusercontent.com/site24x7/plugins/refs/heads/master/$plugin/$plugin.py
}

get_plugin() {
    install
}

get_plugin_data() {
    default_host="localhost"
    default_jmx_port="9010"
    tput setaf 3
    echo
    echo "------------Provide HiveMQ connection details------------"
    tput sgr0
    echo "Press Enter to keep default values."
    echo
    tput setaf 6
    tput bold
    read -r -p "  Enter the hostname (default: $default_host): " host
    host=${host:-$default_host}
    read -r -p "  Enter the JMX port (default: $default_jmx_port): " jmx_port
    jmx_port=${jmx_port:-$default_jmx_port}
    tput sgr0
    echo
}

check_jmx_port() {
    echo "Checking if JMX port $jmx_port is open on $host..."
    if timeout 2 bash -c "</dev/tcp/$host/$jmx_port" 2>/dev/null; then
        echo "✅ JMX port $jmx_port is open."
    else
        tput setaf 1
        echo "❌ JMX port $jmx_port is not open on $host."
        echo
        echo "To enable JMX monitoring, please do the following:"
        echo "➤ Edit HiveMQ's run.sh (usually in /opt/hivemq/bin/run.sh)"
        echo "➤ Add these lines to JAVA_OPTS:"
        echo
        tput bold
        echo " -Dcom.sun.management.jmxremote \\"
        echo " -Dcom.sun.management.jmxremote.port=$jmx_port \\"
        echo " -Dcom.sun.management.jmxremote.authenticate=false \\"
        echo " -Dcom.sun.management.jmxremote.ssl=false \\"
        echo " -Djava.rmi.server.hostname=$host"
        tput sgr0
        echo
        echo "Then restart HiveMQ to apply changes."
        echo
        read -p "Do you want to continue plugin installation anyway? (y/n): " proceed
        if [[ "$proceed" != "y" && "$proceed" != "Y" ]]; then
            echo "Exiting setup. Please enable JMX and rerun the script."
            exit 1
        fi
    fi
}

check_plugin_execution() {
    output=$($python $py_file --hivemq_host "$host" --hivemq_jmx_port "$jmx_port")
    if  [ $? -ne 0 ] || echo "$output" | grep -qE '"status": 0'; then
        tput setaf 1
        echo "------------Error occurred.------------"
        echo "$output"
        tput sgr0
        flag=$((flag + 1))
    elif ! echo "$output" | grep -qE "\"Shared Subscription Cache Hit Rate\":|\"Shared Subscription Cache Eviction Count\":"; then
        tput setaf 3
        echo "No expected metrics found. Verify your JMX connection and topic settings."
        echo "$output"
        tput sgr0
        flag=$((flag + 1))
    else
        tput setaf 2
        echo "✅ Test execution completed successfully"
        echo "$output"
        tput sgr0
        flag=0
    fi
}

add_conf() {
    > "$cfg_file"
    {
        echo "[HiveMQ]"
        echo "hivemq_host = \"$host\""
        echo "hivemq_jmx_port = \"$jmx_port\""
    } >> "$cfg_file"
    echo "Configuration saved to $cfg_file."
}

python_path_update() {
    echo "Detecting Python..."
    
    if output=$(which python3 2>/dev/null); then
        python=$output
    elif output=$(which python 2>/dev/null); then
        python=$output
    else
        tput setaf 1
        echo "❌ Python not found automatically."
        echo "Cannot proceed without a valid Python interpreter."
        tput sgr0
        echo
        echo "🔍 Please provide the full path to Python manually."
        echo "Hint: You can find it using commands like: which python3.12"
        while true; do
            read -rp "Enter the full Python path (e.g., /usr/bin/python3.12): " user_path
            if [[ -x "$user_path" && "$($user_path -c 'print(42)' 2>/dev/null)" == "42" ]]; then
                python="$user_path"
                break
            else
                tput setaf 1
                echo "❌ Invalid Python path or not executable. Please try again."
                tput sgr0
            fi
        done
    fi

    # Update the Python shebang in the plugin script
    sed -i "1s|^.*|#!$python|" "$py_file"
    echo "✅ Using Python: $($python --version 2>&1)"
}


restart_agent(){
    if $reinstall ; then
        read -p "Do you want to restart the Site24x7LinuxAgent? (y/n): " re_agent
        if [[ "$re_agent" =~ ^[yY]$ ]]; then
            output=$($agent_dir/bin/monagent restart)
            error_handler $? "$output"
            echo "Agent restarted."
        fi
    fi
}

move_plugin() {
    mv "$temp_dir" "$plugin_dir" || error_handler $? "Failed to move plugin files"
    echo "Plugin installed to $plugin_dir"
}

check_plugin_exists() {
    if [[ -d "$plugin_dir/$plugin" ]]; then
        echo "Plugin already exists."
        read -p "Do you want to reinstall it? (y/n): " reinstall
        if [[ "$reinstall" =~ ^[yY]$ ]]; then
            rm -rf "$plugin_dir/$plugin"
            reinstall=true
        else
            echo "Exiting."
            exit
        fi
    fi
}

check_python_dependencies() {
    echo
    echo "Checking required Python modules..."
    missing_modules=()

    for module in jmxquery json argparse subprocess; do
        $python -c "import $module" 2>/dev/null
        if [ $? -ne 0 ]; then
            missing_modules+=("$module")
        fi
    done

    if [ ${#missing_modules[@]} -eq 0 ]; then
        echo "✅ All required Python modules are installed."
        return
    fi

    tput setaf 1
    echo "❌ Missing Python modules: ${missing_modules[*]}"
    tput sgr0
    read -p "Do you want to install the missing modules using pip? (y/n): " confirm
    if [[ "$confirm" =~ ^[yY]$ ]]; then
        for mod in "${missing_modules[@]}"; do
            echo "Installing $mod..."
            $python -m pip install "$mod"
            if [ $? -ne 0 ]; then
                tput setaf 1
                echo "❌ Failed to install $mod. Please install it manually and retry."
                tput sgr0
                exit 1
            fi
        done
        echo "✅ Required modules installed successfully."
    else
        echo "Exiting plugin setup due to missing Python dependencies."
        exit 1
    fi
}


install_plugin() {
    check_plugin_exists
    echo "Installing $plugin plugin."
    get_plugin
    get_plugin_data
    check_jmx_port
    python_path_update
    check_python_dependencies
    check_plugin_execution

    if [ $flag -eq 1 ]; then
        get_plugin_data
        check_jmx_port
        python_path_update
        check_python_dependencies
        check_plugin_execution
    fi

    if [ $flag -eq 2 ]; then
        exit
    fi

    add_conf
    tput setaf 3
    echo "------------Moving plugin files------------"
    tput sgr0
    move_plugin
    tput setaf 2
    echo "------------Plugin installed successfully------------"
    tput sgr0
    restart_agent

    if $agent_path_change; then
        echo "Run the following command to fix permissions (if needed):"
        echo "sudo chown -R site24x7-agent:site24x7-group $plugin_dir$plugin"
    fi
}

install_plugin
