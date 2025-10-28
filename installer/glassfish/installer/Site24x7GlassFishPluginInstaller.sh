#!/bin/bash

#trap Function To reset terminal colours 
func_exit() {
    tput sgr0 # Reset Terminal Colors
    exit 0 # Cleanly exit script
}

#Trap for ctr+c(SIGINT) and ctrl+z(SIGTSTP)

trap func_exit SIGINT SIGTSTP

# Agent and Plugin Directory
plugin=glassfish
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
    echo "The Site24x7LinuxAgent is required to install the Glassfish plugin. Enter the correct directory path of the agent to proceed."
    agent_dir=/opt/site24x7/monagent
    tput sgr0
  else
    agent_status=$($agent_dir/bin/monagent status)
    if ! echo "$agent_status" | grep -q "Site24x7 monitoring agent service" ; then
        tput setaf 1
        echo
        echo "The Site24x7LinuxAgent is required to install the Glassfish plugin. Enter the correct directory path of the agent to proceed."
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


install (){
    
    if [[ -d $temp_dir ]] ; then

        if ( [[ -f $py_file ]] ) ; then 
            rm $py_file
        fi
        if ( [[ -f $cfg_file ]] ) ; then 
            rm $cfg_file
        fi

        download_files https://raw.githubusercontent.com/site24x7/plugins/master/glassfish/glassfish.py
        download_files https://raw.githubusercontent.com/site24x7/plugins/master/glassfish/glassfish.cfg

    else
        output=$(mkdir -p $temp_dir)
        if [ $? -ne 0 ]; then
            tput setaf 1
            echo "------------Error Occured------------"
        fi

        download_files https://raw.githubusercontent.com/site24x7/plugins/master/glassfish/glassfish.py
        download_files https://raw.githubusercontent.com/site24x7/plugins/master/glassfish/glassfish.cfg
    
    fi

}

get_plugin_data() {

    default_host="localhost"
    default_port="4848"
    default_ssl="false"
    default_insecure="false"
    default_username="None"
    default_password="None"
    tput setaf 3
    echo
    echo "------------Connection Details------------"
    echo 
    tput sgr0
    echo " 1.Provide the host, port and authentication credentials (if any) below to access Glassfish to fetch metrics. These will be used in the .cfg file."
    echo " 2.Press Enter to keep the default values. If you hit Enter, the default values will be used for the connection."
    echo " 3.Provide true in $(tput bold)SSL$(tput sgr0) option if you want the plugin to connect using $(tput bold)https$(tput sgr0) instead of $(tput bold)http$(tput sgr0)."
    echo " 4.Providing true to $(tput bold)insecure$(tput sgr0) will connect to the servers with invaild certificates in testing environment."
    echo
    echo " $(tput setaf 3)$(tput bold)Note$(tput sgr0): The password you provide will be securely encrypted in the agent and will not be stored in any of the Site24x7 databases."
    echo
    tput setaf 6
    tput bold

    read -r -p  "  Enter the host (default: $default_host): " glassfish_host
    if [ -z $glassfish_host ] ; then
        glassfish_host=$default_host
    fi

    read -r -p  "  Enter the port (default: $default_port): " glassfish_port
    if [ -z $glassfish_port ] ; then
        glassfish_port=$default_port
    fi

    read -r -p  "  Connect using SSL(https) (default: $default_ssl): " glassfish_ssl
    if [ -z $default_ssl ] ; then
        glassfish_ssl=$default_ssl
    fi

    read -r -p  "  Insecure connection (default: $default_insecure): " glassfish_insecure
    if [ -z $glassfish_insecure ] ; then
        glassfish_insecure=$default_insecure
    fi

    read -r -p "  Enter the username (default: $default_username): " username
    if [ -z $username ] ; then
        username=$default_username
    fi

    read -r -s -p "  Enter the password (default: $default_password): " password
    if [ -z $password ] ; then
        password=$default_password
    fi

    tput sgr0
}


python_path_update() {
    echo
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

    output=$($python $py_file --host "$glassfish_host" --port "$glassfish_port" --ssl "$glassfish_ssl"  --insecure "$glassfish_insecure" --username "$username" --password "$password")


    if  [ $? -ne 0 ]; then
        tput setaf 1
        echo
        echo "------------Error Occured------------"
        echo $output
        echo
        echo $(grep -E '"status": 0' <<< "$output" )
        echo $(grep -E '"msg": *' <<< "$output" )
        tput sgr0
        
        return 0
    fi

    if echo "$output" | grep -qE "\[SSL: CERTIFICATE_VERIFY_FAILED\] certificate verify failed: self-signed certificate \(_ssl.c:1007\)"; then
       
       tput setaf 1
       echo
       echo "------------Error Occured------------"
       echo
       echo "Status and Error Message:"
       tput sgr0
       echo $(grep -E '"status": 0' <<< "$output" )
       echo $(grep -E '"msg": *' <<< "$output" )
       echo
       tput setaf 3
       read -p "The SSL certificate verification failed. Would you like to proceed with an insecure connection? (y or n):" insecure

       if [ -z "$insecure" ] || [ $insecure = "y" -o $insecure = "Y" ] ; then
            glassfish_ssl="true"
            glassfish_insecure="true"
            check_plugin_execution
            ssl_flag=$?
            if [ "$ssl_flag" != "1" ]; then 
                return 0
            else
                return 1
            fi 
       else
            glassfish_insecure=false
       fi
       tput setaf 1
       echo

       return 0
    fi

    if grep -qE '"status": 0' <<< "$output"  ; then
        tput setaf 1
        echo
        echo "------------Error Occured------------"
        tput sgr0
        echo $output
        echo
        tput setaf 1
        echo "Status and Error Message:"
        tput sgr0
        echo $(grep -E '"status": 0' <<< "$output" )
        echo $(grep -E '"msg": *' <<< "$output" )
        tput sgr0
        
        return 0

    elif ! echo "$output" | grep -qE "\"Committed Heap Size\":|\"Init HeapSize\":"; then
       tput setaf 3
       echo
       echo "The output does not contain metrics. Check if you have provided the correct details."
       tput setaf 1
       echo $output
       echo

       return 0

    else
        tput setaf 3
        echo
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
    output=$(sed -i "/^host*/c\host = \"$glassfish_host\""  "$cfg_file")
    error_handler $? $output
    output=$(sed -i "/^port*/c\port = \"$glassfish_port\""  "$cfg_file")
    error_handler $? $output
    output=$(sed -i "/^ssl*/c\ssl = \"$glassfish_ssl\""  "$cfg_file")
    error_handler $? $output
    output=$(sed -i "/^insecure*/c\insecure = \"$glassfish_insecure\""  "$cfg_file")
    error_handler $? $output
    output=$(sed -i "/^username*/c\username = \"$username\""  "$cfg_file")
    error_handler $? $output
    password=$(echo "$password" | sed 's/\\/\\\\/g')
    output=$(sed -i "/^password*/c\password = \"$password\""  $cfg_file)
    error_handler $? $output
    #echo "after"
    #cat $cfg_file
    
}

check_plugin_exists() {
    if  [[ -d "$plugin_dir/$plugin" ]]  ; then 
        echo "The Glassfish monitoring plugin folder already exists in the Plugins directory."
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
    echo "The installer helps you to install the Glassfish plugin for monitoring in Site24x7."
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

    echo
    echo 

    get_plugin_data
    
    add_conf

    python_path_update

    check_plugin_execution

    execution_flag=$?

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
