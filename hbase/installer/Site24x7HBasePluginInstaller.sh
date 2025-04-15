#!/bin/bash

echo
echo "Select the HBase node type to monitor:"
echo "  1. HBase Master Server (default)"
echo "  2. HBase RegionServer"
read -r -p "Enter your choice [1 or 2] (default: 1): " node_choice

case "$node_choice" in
  1|"")
    plugin="hbase"
    ;;
  2)
    plugin="hbase_regionserver"
    ;;
  *)
    echo "Invalid choice. Please enter 1 or 2."
    read -r -p "Enter your choice [1 or 2] (default: 1): " second_try

    case "$second_try" in
      1|"")
        plugin="hbase"
        ;;
      2)
        plugin="hbase_regionserver"
        ;;
      *)
        tput setaf 1
        echo "Invalid input again. Exiting script."
        tput sgr0
        exit 1
        ;;
    esac
    ;;
esac


agent_dir=/opt/site24x7/monagent
temp_dir=$agent_dir/temp/plugins/$plugin
py_file="$temp_dir/$plugin.py"
cfg_file="$temp_dir/$plugin.cfg"
reinstall=false
plugin_dir=$agent_dir/plugins/
flag=0

func_exit() {
    tput sgr0 
    exit 0 
}

trap func_exit SIGINT SIGTSTP

error_handler() {
    if  [ $1 -ne 0 ]; then
        tput setaf 1
        echo  "------------Error occured.---------"
        echo $2
        tput sgr0
        exit
    fi
}

agent_check(){
    if  ! [ -d $agent_dir"/bin"  ]; then
      agent_path_change=true
      output=$(ls $agent_dir )
      if ! echo "$output" | grep -qE ": Permission denied"; then
            error_handler $? $output
      fi

      tput setaf 3
      if [ $i -eq 0 ]; then
        echo "The Site24x7LinuxAgent is not installed in the default $agent_dir directory."
      fi
      echo -e "Enter the path of the directory where the Site24x7LinuxAgent is installed: \c"
      read -r  agent_dir
      tput sgr0

    else 
        if [ $i -gt 0 ] ; then
            echo "The agent Directory is $agent_dir"
        fi
      
    fi

}

for (( i=0; i<3; i++ )); do
  agent_check
  if [ -z $agent_dir ]; then
    tput setaf 1
    echo
    echo "The Site24x7LinuxAgent is required to install the $plugin plugin. Enter the correct directory path of the agent to proceed."
    agent_dir=/opt/site24x7/monagent
    tput sgr0
  else
    agent_status=$($agent_dir/bin/monagent status)
    if ! echo "$agent_status" | grep -q "Site24x7 monitoring agent service" ; then
        tput setaf 1
        echo
        echo "The Site24x7LinuxAgent is required to install the $plugin plugin. Enter the correct directory path of the agent to proceed."
        tput sgr0

    else
        break
    fi
  fi

  if [ $i -eq 2 ]; then
      echo "No such file or directory found. Install the Site24x7LinuxAgent and try installing the plugin again."
      exit
  fi
done

download_files() {

    file_name=$1 
    echo "Downloading: $file_name"
    echo
    
    output=$(wget -P $temp_dir $file_name  2>&1 )

    if [ $? -ne 0 ]; then
        tput setaf 1
        error=$(grep -E 'HTTP' <<< "$output" )
        echo $error
        if echo "$error" | grep -q "200"; then
            echo $output
        else
            error_handler $? "$output"
        fi
        tput sgr0
        exit
    else
        tput setaf 2
        echo $(grep -E 'HTTP' <<< "$output" )
        echo $(grep -E 'saved' <<< "$output" )
        tput sgr0
        
        
    fi
    echo

}

install () {

    if [[ -d $temp_dir ]] ; then
        [[ -f $py_file ]] && rm $py_file
        [[ -f $cfg_file ]] && rm $cfg_file
    else
        mkdir -p $temp_dir || {
            tput setaf 1
            echo "------------Error occurred. Process exited.------------"
            tput sgr0
            exit 1
        }
    fi

    if [[ "$plugin" == "hbase_regionserver" ]]; then
        download_files https://raw.githubusercontent.com/site24x7/plugins/master/hbase/$plugin/$plugin.cfg
        download_files https://raw.githubusercontent.com/site24x7/plugins/master/hbase/$plugin/$plugin.py
    else
        download_files https://raw.githubusercontent.com/site24x7/plugins/master/$plugin/$plugin.cfg
        download_files https://raw.githubusercontent.com/site24x7/plugins/master/$plugin/$plugin.py
    fi
}

get_plugin(){
    install
}

get_plugin_data() {
    default_host="localhost"
    default_port="16010"
    default_log_path="/var/log/*hbase*/*.log , /opt/*hbase*/logs/*.log* , /*hbase*/*log*/*.log"

    tput setaf 3
    echo
    echo "------------Provide connection details to connect to $plugin------------"
    tput sgr0
    echo 
    echo " Press Enter to keep the default values. If you hit Enter, the default values will be used for the connection."
    echo
    echo " $(tput setaf 3)$(tput bold)Note$(tput sgr0): The username and password you provide will be securely encrypted in the agent and will not be stored in any of the Site24x7 databases."
    echo

    
    tput setaf 6
    tput bold
    read -r -p  "  Enter the hostname (default: $default_host): " host
    if [ -z $host ] ; then
        host=$default_host
    fi
    read -r -p  "  Enter the port (default: $default_port): " port
    if [ -z $port ] ; then
        port=$default_port
    fi

     echo
    echo "By default, the plugin will look for HBase logs in the following locations:"
    echo "$default_log_path"
    echo
    read -r -p "  If HBase logs are in a different folder, enter the full path (or press Enter to use defaults): " log_path
    if [ -z "$log_path" ]; then
        log_path="$default_log_path"
    else
        if [[ "$log_path" == */ ]]; then
            log_path="${log_path}*.log"
        else
            log_path="${log_path}/*.log"
        fi
    fi


    tput sgr0
    echo
}


check_plugin_execution() {
    

    if [[ "$plugin" == "hbase" ]]; then
        metric_check='"Rit Oldest Age":|"Rit Count":'
        example_url="http://localhost:16010/jmx"
    elif [[ "$plugin" == "hbase_regionserver" ]]; then
        metric_check='"Total Tables":|"Put Count":'
        example_url="http://localhost:16030/jmx"
    fi

    output=$($python $py_file --host "$host" --port "$port")
    if  [ $? -ne 0 ]; then
        tput setaf 1
        echo "------------Error occured. Incorrect credentials provided.------------"
        echo $output
        echo
        echo $(grep -E '"status": 0' <<< "$output" )
        echo $(grep -E '"msg": *' <<< "$output" )
        tput sgr0
        flag=$((flag + 1))
    fi

    if grep -qE '"status": 0' <<< "$output"  ; then
        tput setaf 1
        echo "------------Error occured. Incorrect credentials provided.------------"
        echo $output
        echo
        tput sgr0
        flag=$((flag + 1))

    elif ! echo "$output" | grep -qE "$metric_check"; then
        tput setaf 1
        echo "The output does not contain metrics. Check if you have provided the correct endpoint for the status URL."
        echo "An example of a status URL: $example_url"
        flag=$((flag + 1))        

    else
        tput setaf 3
        echo "------------Test execution completed successfully------------"
        echo
        tput setaf 2
        echo $output
        tput sgr0
        flag=0

    fi

}

add_conf() {
    echo

    host=$(echo "$host" | sed 's/\\/\\\\/g')
    output=$(sed -i "/^host*/c\host = \"$host\""  $cfg_file)
    error_handler $? "$output"

    port=$(echo "$port" | sed 's/\\/\\\\/g')
    output=$(sed -i "/^port*/c\port = \"$port\""  $cfg_file)
    error_handler $? "$output"

    log_path=$(echo "$log_path" | sed 's/\\/\\\\/g')
    if grep -q "^log_file_path" "$cfg_file"; then
        sed -i "/^log_file_path*/c\log_file_path = \"$log_path\"" "$cfg_file"
    else
        echo "log_file_path = \"$log_path\"" >> "$cfg_file"
    fi
    error_handler $? "Failed to write log_file_path"
}

python_path_update() {
    echo "Checking for Python 3"
    output=$(which python3)
    if [ $? -ne 0 ]; then

        echo $(python3 --version)
        echo
        echo "Checking for Python 2"
        output=$(which python)
        if [ $? -ne 0 ]; then
            tput setaf 1
            echo "------------The Python path could not be updated------------"
            echo 
            tput sgr0
            echo $(python --version)
            exit
        else
            python=python
            output=$(sed -i "1s|^.*|#! $output|" $py_file)
            if [ $? -ne 0 ]; then
                tput setaf 1
                echo "------------The Python path could not be updated------------"
                echo 
                tput sgr0
            
            else
                echo "Python path updated with $(python --version 2>&1)"
            fi
        fi

    else
        python=python3
         output=$(sed -i "1s|^.*|#! $output|" $py_file)
         if [ $? -ne 0 ]; then
            tput setaf 1
            echo "------------The Python path could not be updated------------"
            echo 
            tput sgr0
        else
            echo "Python path updated with $(python3 --version)"
        fi
    echo
    

    fi
}

restart_agent(){

    if $reinstall ; then
        read -p "Do you want to restart the Site24x7LinuxAgent?(y or n): " re_agent
        if  [ -z "$re_agent" ] || [ $re_agent = "y" -o $re_agent = "Y" ] ; then
        
            output=$($agent_dir/bin/monagent restart)
            error_handler $? $output
            echo "Completed."

        else
            echo "Process exited."
        fi
    fi
}

move_plugin() {
    output=$(mv $temp_dir $plugin_dir )
    if  [ $? -ne 0 ]; then
        tput setaf 1
        echo "------------Error occured. Process exited.------------"
        tput sgr0
        exit
    else
        echo "Completed."
    fi

}

check_plugin_exists() {
    if  [[ -d "$plugin_dir/$plugin" ]]  ; then 
        echo "The $plugin monitoring plugin folder already exists in the Plugins directory."
        read -p "Do you want to reinstall the plugin? (y or n):" reinstall
        if [ -z "$reinstall" ] || [ $reinstall = "y" -o $reinstall = "Y" ] ; then
            rm -rf "$plugin_dir/$plugin"
            reinstall=true
        else
            echo "Process exited."
            exit
        fi
        
    fi
}

install_plugin() {

    check_plugin_exists

    echo "Installing the $plugin plugin."

    get_plugin

    get_plugin_data

    python_path_update

    check_plugin_execution

    if [ $flag -eq 1 ]; then
        get_plugin_data
        python_path_update
        check_plugin_execution
    fi

    if [ $flag -eq 2 ]; then
        exit
    fi
    
    add_conf

    tput setaf 3
    echo
    echo "------------Moving plugin files to the Site24x7 Plugins directory------------"
    echo
    tput sgr0

    move_plugin
    tput setaf 3
    echo
    echo "------------Plugin installed successfully------------"
    tput sgr0
    restart_agent
    if  $agent_path_change ; then
        echo "If you have installed the agent as non-root, execute the command below with appropriate details to allow the user access to the plugin folder."
        echo "For example, if the user is 'site24x7-agent' and the group is 'site24x7-group', the command would be:"
        echo "$(tput bold)chown -R site24x7-agent:site24x7-group $plugin_dir$plugin$(tput sgr0)"
    fi

}

install_plugin
