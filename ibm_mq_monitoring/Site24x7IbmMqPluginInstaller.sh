#!/bin/bash

#trap Function To reset terminal colours 
func_exit() {
    tput sgr0 # Reset Terminal Colors
    exit 0 # Cleanly exit script
}

#Trap for ctr+c(SIGINT) and ctrl+z(SIGTSTP)

trap func_exit SIGINT SIGTSTP

# Agent and Plugin Directory
plugin=ibm_mq_monitoring
agent_dir=/opt/site24x7/monagent
agent_path_change=false


error_handler() {
    if  [ $1 -ne 0 ]; then
        tput setaf 1
        echo  "------------Error Occured---------"
        echo $2
        tput sgr0
        echo "------------Process Exited------------"
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
    echo "The Site24x7LinuxAgent is required to install the ibm_mq_monitoring plugin. Enter the correct directory path of the agent to proceed."
    agent_dir=/opt/site24x7/monagent
    tput sgr0
  else
    agent_status=$($agent_dir/bin/monagent status)
    if ! echo "$agent_status" | grep -q "Site24x7 monitoring agent service" ; then
        tput setaf 1
        echo
        echo "The Site24x7LinuxAgent is required to install the ibm_mq_monitoring plugin. Enter the correct directory path of the agent to proceed."
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

# Variables for the plugin installation
temp_dir=$agent_dir/temp/plugins/$plugin
plugin_dir=$agent_dir/plugins/
py_file="$temp_dir/$plugin.py"
cfg_file="$temp_dir/$plugin.cfg"
reinstall=false

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

loading_animation() {
    installation_command=$1
    output=$($installation_command) &
    pid=$! # Process Id of the previous running command

    spin='-\|/'

    i=0
    tput civis # cursor invisible
    while kill -0 $pid 2>/dev/null
    do
        i=$(( (i+1) %4 ))
        printf "\rInstalling $2... ${spin:$i:1}"
        sleep .1
    done
    wait $pid
    exit_status=$?
    tput cnorm
    echo
    if [ $exit_status -ne 0 ]; then
        tput setaf 1
        echo "------------Error Occured------------"
        echo $output
        tput sgr0
        exit
    fi
    echo "Installation completed!"
}

Install_pakages(){
    tput setaf 3
    echo
    echo "------------Installing the pymqi module------------"
    echo 
    tput sgr0
    
    echo "The pymqi python client is required to install the plugin."
    echo
    read -p "Do you wish to install pymqi python client. (y or n):" ibm_mq_monitoring
    tput sgr0
    
    echo
    if [ -z "$ibm_mq_monitoring" ] || [ $ibm_mq_monitoring = "y" -o $ibm_mq_monitoring = "Y" ] ; then
        loading_animation "pip3 install pymqi" "pymqi python client"

    else
        echo "Process exited."
            
    fi


}

install (){
    
    if [[ -d $temp_dir ]] ; then

        if ( [[ -f $py_file ]] ) ; then 
            rm $py_file
        fi
        if ( [[ -f $cfg_file ]] ) ; then 
            rm $cfg_file
        fi

        download_files https://raw.githubusercontent.com/site24x7/plugins/master/ibm_mq_monitoring/ibm_mq_monitoring.py
        download_files https://raw.githubusercontent.com/site24x7/plugins/master/ibm_mq_monitoring/ibm_mq_monitoring.cfg

    else
        output=$(mkdir -p $temp_dir)
        if [ $? -ne 0 ]; then
            tput setaf 1
            echo "------------Error Occured------------"
        fi

        download_files https://raw.githubusercontent.com/site24x7/plugins/master/ibm_mq_monitoring/ibm_mq_monitoring.py
        download_files https://raw.githubusercontent.com/site24x7/plugins/master/ibm_mq_monitoring/ibm_mq_monitoring.cfg
        
    
    fi

}

get_plugin_data() {

    default_queue_manager_name="QM1"
    default_channel_name="DEV.APP.SVRCONN"
    default_host="localhost"
    default_port="1414"
    default_username="app"
    default_password="None"
    tput setaf 3
    echo
    echo "------------Connection Details------------"
    echo 
    tput sgr0
    echo " 1.Provide the Queue manager, host, port and authentication credentials (if any) below to access IBM MQ to fetch metrics. These will be used in the .cfg file."
    echo " 2.Press Enter to keep the default values. If you hit Enter, the default values will be used for the connection."
    echo
    echo " $(tput setaf 3)$(tput bold)Note$(tput sgr0): The password you provide will be securely encrypted in the agent and will not be stored in any of the Site24x7 databases."
    echo
    
    tput setaf 6
    tput bold

    read -r -p  "  Enter the Queue Manager (default: $default_queue_manager_name): " ibm_mq_monitoring_QM
    if [ -z $ibm_mq_monitoring_QM ] ; then
        ibm_mq_monitoring_QM=$default_queue_manager_name
    fi

    read -r -p  "  Enter the Channel (default: $default_channel_name): " ibm_mq_monitoring_Channel
    if [ -z $ibm_mq_monitoring_Channel ] ; then
        ibm_mq_monitoring_Channel=$default_channel_name
    fi

    read -r -p  "  Enter the IBM MQ host (default: $default_host): " ibm_mq_monitoring_host
    if [ -z $ibm_mq_monitoring_host ] ; then
        ibm_mq_monitoring_host=$default_host
    fi

    read -r -p  "  Enter the port (default: $default_port): " ibm_mq_monitoring_port
    if [ -z $ibm_mq_monitoring_port ] ; then
        ibm_mq_monitoring_port=$default_port
    fi

    read -r -p "  Enter the username (default: $default_username): " username
    if [ -z $username ] ; then
        username="None"
    fi


    read -r -p "  Enter the password (default: $default_password): " password
    if [ -z $password ] ; then
        password="None"
    fi


    tput sgr0
}


python_path_update() {
    echo "Checking for python3"
    output=$(which python3)

    if [ $? -ne 0 ]; then

        echo $(python3 --version)
        echo
        echo "Checking for python2"
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

check_plugin_execution() {

    output=$($python $py_file --queue_manager_name "$ibm_mq_monitoring_QM" --channel_name "$ibm_mq_monitoring_Channel" --host "$ibm_mq_monitoring_host" --port "$ibm_mq_monitoring_port" --username "$username" --password "$password")

    if  [ $? -ne 0 ]; then
        tput setaf 1
        echo "------------Error Occured------------"
        echo $output
        echo
        echo $(grep -E '"status": 0' <<< "$output" )
        echo $(grep -E '"msg": *' <<< "$output" )
        tput sgr0
        

        return 0
    fi

    if grep -qE '"status": 0' <<< "$output"  ; then
        tput setaf 1
        echo "------------Error Occured------------"
        echo $output
        echo
        echo "Status and Error Message:"
        echo $(grep -E '"status": 0' <<< "$output" )
        echo $(grep -E '"msg": *' <<< "$output" )
        tput sgr0
        
        return 0

    elif ! echo "$output" | grep -qE "\"QManager\ Connection Count\":|\"QManager Status\":"; then
       tput setaf 3
       echo "The output does not contain metrics. Check if you have provided the correct details."
       tput setaf 1
       echo $output
       echo

       return 0

    else
        tput setaf 3
        echo "------------Successful test execution------------"
        echo
        tput setaf 2
        echo $output
        tput sgr0

        return 1

    fi


}

add_conf() {
    echo
    #echo "before"
    #cat $cfg_file
    output=$(sed -i "/^queue_manager_name*/c\queue_manager_name = \"$ibm_mq_monitoring_QM\""  "$cfg_file")
    error_handler $? $output
    output=$(sed -i "/^channel_name*/c\channel_name = \"$ibm_mq_monitoring_Channel\""  "$cfg_file")
    error_handler $? $output
    output=$(sed -i "/^host*/c\host = \"$ibm_mq_monitoring_host\""  "$cfg_file")
    error_handler $? $output
    output=$(sed -i "/^port*/c\port = \"$ibm_mq_monitoring_port\""  "$cfg_file")
    error_handler $? $output
    output=$(sed -i "/^username*/c\username = \"$default_username\""  "$cfg_file")
    error_handler $? $output
    password=$(echo "$password" | sed 's/\\/\\\\/g')
    output=$(sed -i "/^password*/c\password = \"$password\""  $cfg_file)
    error_handler $? $output
    #echo "after"
    #cat $cfg_file
    
}

check_plugin_exists() {
    if  [[ -d "$plugin_dir/$plugin" ]]  ; then 
        echo "The ibm_mq_monitoring monitoring plugin folder already exists in the Plugins directory."
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

restart_agent(){

    if $restart ; then
        read -p "Do you want to restart the Site24x7LinuxAgent?(y or n): " re_agent
        if  [ -z "$re_agent" ] || [ $re_agent = "y" -o $re_agent = "Y" ] ; then
        
            output=$($agent_dir/bin/monagent restart)
            error_handler $? $output
            echo "Completed."

        else
            echo "Process exited."
        fi
        echo "If you have installed the agent as non-root, execute the command below with appropriate details to allow the user access to the plugin folder."
        echo "For example, if the user is 'site24x7-agent' and the group is 'site24x7-group', the command would be:"
        echo "$(tput bold)chown -R site24x7-agent:site24x7-group $plugin_dir$plugin$(tput sgr0)"
    fi
}

move_plugin() {
    output=$(mv $temp_dir $plugin_dir )
    if  [ $? -ne 0 ]; then
        tput setaf 1
        echo "------------Error Occured------------"
        tput sgr0
    else
        echo "Completed."
    fi

}

install_plugin() {
    echo
    tput setaf 3
    echo "------------$(tput bold)Starting the installation$(tput sgr0)$(tput setaf 3)------------"
    tput sgr0
    echo
    echo "The installer helps you to install the ibm_mq_monitoring plugin for monitoring in Site24x7."
    echo "Follow the in-line instructions below to complete the installation successfully."
    echo
    
    check_plugin_exists

    tput setaf 3
    echo
    echo "------------Downloading the plugin files from Site24x7's GitHub repository------------"
    echo    
    tput sgr0

    install
    output=""
    Install_pakages

    echo
    echo 

    get_plugin_data

    

    python_path_update

    check_plugin_execution

    execution_flag=$?

    echo $execution_flag "---------"

    if [ "$execution_flag" != "1" ]; then 
        get_plugin_data
        check_plugin_execution
        execution_flag=$?

    fi
    
    if [ "$execution_flag" != "1" ]; then 

        tput setaf 1
        error_handler 1 "Plugin execution failed"
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
