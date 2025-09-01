#!/bin/bash

plugin=kafka
agent_dir=/opt/site24x7/monagent
temp_dir=$agent_dir/temp/plugins/$plugin
py_file="$temp_dir/$plugin.py"
cfg_file="$temp_dir/$plugin.cfg"
reinstall=false
plugin_dir=$agent_dir/plugins/
flag=0

func_exit() {
    tput sgr0 # Reset Terminal Colors
    exit 0 # Cleanly exit script
}

#Trap for ctr+c(SIGINT) and ctrl+z(SIGTSTP)

trap func_exit SIGINT SIGTSTP

error_handler() {
    if  [ $1 -ne 0 ]; then
        tput setaf 1
        echo  "------------Error occured. Download failed. Process exited.---------"
        echo $2
        tput sgr0
        exit
    fi
}

agent_check(){
# Check if the service exists
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

install (){
    
    if [[ -d $temp_dir ]] ; then

        if ( [[ -f $py_file ]] ) ; then 
            rm $py_file
        fi
        if ( [[ -f $cfg_file ]] ) ; then 
            rm $cfg_file
        fi

        download_files https://raw.githubusercontent.com/site24x7/plugins/refs/heads/master/$plugin/$plugin.cfg
        download_files https://raw.githubusercontent.com/site24x7/plugins/refs/heads/master/$plugin/$plugin.py

    else
        output=$(mkdir -p $temp_dir)
         if [ $? -ne 0 ]; then
            tput setaf 1
            echo "------------Error occured. Process exited.------------"
            echo $output
            tput sgr0
            exit
        fi

        download_files https://raw.githubusercontent.com/site24x7/plugins/refs/heads/master/$plugin/$plugin.cfg
        download_files https://raw.githubusercontent.com/site24x7/plugins/refs/heads/master/$plugin/$plugin.py
        
    fi

}

get_plugin(){
    install
}

get_plugin_data() {
    default_host="localhost"
    default_jmx_port="9999"
    tput setaf 3
    echo
    echo "------------Provide connection details to connect to $plugin------------"
    tput sgr0
    echo 
    echo " Press Enter to keep the default values. If you hit Enter, the default values will be used for the connection."
    echo
    echo

    
    tput setaf 6
    tput bold
    read -r -p  "  Enter the hostname (default: $default_host): " host
    if [ -z $host ] ; then
        host=$default_host
    fi
    read -r -p "  Enter the JMX port (default: $default_jmx_port): " jmx_port
    if [ -z $jmx_port ] ; then
        jmx_port=$default_jmx_port
    fi
    tput sgr0
    echo
}


check_plugin_execution() {

    output=$($python $py_file --kafka_host "$host" --kafka_jmx_port "$jmx_port")

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
        echo "Status and Error Message:"
        echo $(grep -E '"status": 0' <<< "$output" )
        echo $(grep -E '"msg": *' <<< "$output" )
        tput sgr0
        flag=$((flag + 1))

    elif ! echo "$output" | grep -qE "\"Partition Count\":|\"Leader Count\":"; then
        tput setaf 3
        echo "The output does not contain metrics. Check if you have provided the correct topic."
        echo ""
        echo $output
        echo
        tput sgr0
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
    > "$cfg_file"

    {
        echo "[kafka]"
        echo "kafka_host = \"$host\""
        echo "kafka_jmx_port = \"$jmx_port\""
    } >> "$cfg_file"

    echo "Configuration for the Kafka instance has been added to $cfg_file."
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
