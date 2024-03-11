#!/bin/bash

#trap Function To reset terminal colours 
func_exit() {
    tput sgr0 # Reset Terminal Colors
    exit 0 # Cleanly exit script
}

#Trap for ctr+c(SIGINT) and ctrl+z(SIGTSTP)

trap func_exit SIGINT SIGTSTP

# Agent and Plugin Directory
plugin=apache_monitoring
agent_dir=/opt/site24x7/monagent

# Enable
debian_path=/etc/apache2/mods-available
centos_path=/etc/httpd/conf.d
status_conf_file=status.conf
endpoint="/server-status"
content="\n\t<Location /server-status>\n\t\tSetHandler server-status\n\t\tRequire local\n\t</Location>"

agent_check(){
# Check if the service exists
    if  ! [ -d $agent_dir"/bin"  ]; then

      tput setaf 3
      if [ $i -eq 0 ]; then
        echo "The Site24x7LinuxAgent is not installed in the default $agent_dir directory."
      fi
      echo -e "Enter the path of the directory where the Site24x7LinuxAgent is installed: \c"
      read -r  agent_dir
      tput sgr0
      
    fi

}


for (( i=0; i<3; i++ )); do
  agent_check
  if [ -z $agent_dir ]; then
    tput setaf 1
    echo
    echo "The Site24x7LinuxAgent is required to install the Apache plugin. Enter the correct directory path of the agent to proceed."
    agent_dir=/opt/site24x7/monagent
    tput sgr0
  else
    agent_status=$($agent_dir/bin/monagent status)
    if ! echo "$agent_status" | grep -q "Site24x7 monitoring agent service" ; then
        tput setaf 1
        echo
        echo "The Site24x7LinuxAgent is required to install the Apache plugin. Enter the correct directory path of the agent to proceed."
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

        download_files https://raw.githubusercontent.com/site24x7/plugins/master/apache_monitoring/apache_monitoring.py
        download_files https://raw.githubusercontent.com/site24x7/plugins/master/apache_monitoring/apache_monitoring.cfg

    else
        output=$(mkdir -p $temp_dir)
         if [ $? -ne 0 ]; then
            tput setaf 1
            echo "------------Error Occured------------"
            echo $output
            tput sgr0
            exit
        fi

        download_files https://raw.githubusercontent.com/site24x7/plugins/master/apache_monitoring/apache_monitoring.py
        download_files https://raw.githubusercontent.com/site24x7/plugins/master/apache_monitoring/apache_monitoring.cfg
        
    fi

}

get_plugin_data() {
    tput setaf 3
    echo
    echo "------------Connection Details------------"
    echo 

    echo "The default Apache status URL found is: http://localhost:80$endpoint?auto"
    read -p "Do you want to configure an alternate port or status URL?? (y or n):" change_url
    echo
    
    if [ -z "$change_url" ] || [ $change_url = "n" -o $change_url = "N" ] ; then
        url="http://localhost:80$endpoint?auto"
    elif [ $change_url = "y" -o $change_url = "Y" ] ; then
        tput setaf 4
        read -r -p  "  Enter the required URL: " url
    else
        tput setaf 4
        read -r -p "  Enter the required URL: " url
    fi

    tput setaf 4
    echo
    echo "  Provide authentication credentials below to access the Status URL."
    echo "  Note: The username and password you provide will be securely encrypted in the agent and will not be stored in any of the Site24x7 databases."
    echo
    echo "  Press Enter to skip if you don't have any credentials set for the endpoint."
    echo
    read -r -p "  Enter the User Name: " username
    read -r -p "  Enter the Password: " password
    echo $password
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

    output=$($python $py_file --url "$url" --username "$username" --password "$password")
    if  [ $? -ne 0 ]; then
        tput setaf 1
        echo "------------Error Occured------------"
        echo $output
        echo
        echo $(grep -E '"status": 0' <<< "$output" )
        echo $(grep -E '"msg": *' <<< "$output" )
        tput sgr0
        exit
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
        exit

    elif ! echo "$output" | grep -qE "\"busy_workers\":|\"idle_workers\":"; then
        tput setaf 3
        echo "The output does not contain metrics. Check if you have provided the correct endpoint for the status URL."
        echo "An example of a status URL: http://localhost:80$endpoint?auto"
        error_handler 1 "$output"

    else
        tput setaf 3
        echo "------------Successful test execution------------"
        echo
        tput setaf 2
        echo $output
        tput sgr0

    fi


}

add_conf() {
    echo
    #echo "before"
    #cat $cfg_file
    output=$(sed -i "/url*/c\url = \"$url\""  "$cfg_file")
    error_handler $? $output
    username=$(echo "$username" | sed 's/\\/\\\\/g')
    output=$(sed -i "/username*/c\username = \"$username\"" $cfg_file)
    error_handler $? $output
    password=$(echo "$password" | sed 's/\\/\\\\/g')
    output=$(sed -i "/password*/c\password = \"$password\""  $cfg_file)
    error_handler $? $output
    #echo "after"
    #cat $cfg_file
    
}

check_plugin_exists() {
    if  [[ -d "$plugin_dir/$plugin" ]]  ; then 
        echo "The Apache monitoring plugin folder already exists in the Plugins directory."
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

check_if_dir_exists() {

    if [[ -d $status_conf_path ]] ; then  
        echo "$status_conf_path directory exists."
        echo
        return 0
    else
        echo "$status_conf_path directory does not exists."
        error_handler 1  
        return 1 
    fi
}



error_handler() {
    if  [ $1 -ne 0 ]; then
        tput setaf 1
        echo  "------------Error Occured---------"
        echo $2
        tput sgr0
        exit
    fi
}
check_if_file_exists() {


    status_conf=$status_conf_path/$status_conf_file
    if [[ -f $status_conf ]] ; then
        
        echo "$status_conf_file file exists."
        
        echo
        tput setaf 3
        echo
        echo "------------Checking if mod_status is enabled------------"
        echo
        tput sgr0
        enabled_or_not
        
        return 0
    else

        tput setaf 3
        echo "------------Status.conf does not exist------------" 
        echo
        tput sgr0
        
        echo "The installer will create a status.conf file in the $status_conf_path directory and add the configuration below to enable mod_status."
        echo
        echo "The following configuration will be added in the $status_conf_file file:"
        echo -e $content
        echo
        read -p "Do you want to create the status.conf and enable mod_status??(y or n):" create_file


        
        if [ $create_file = "y" -o create_file = "Y" ] ; then
            echo "Creating the $status_conf_file file."
            output=$(touch $status_conf)
            error_handler $? $output
            echo
            echo "Adding the configuration to enable mod_status."
            output=$(echo -e $content >> $status_conf)
            error_handler $? $output
            echo "Completed."
            restart_apache
            return 1
        else
            echo "Proceeding to plugin installation."
        fi
    fi


}

enabled_or_not() {

    output=$(grep -E "^[^#]*\<SetHandler server-status\>"  $status_conf )
    exit_status=$?
    if [ $exit_status != 1 ] ; then
        error_handler $exit_status $output
    fi


    if [ -n "$output" ] ; then
        echo "mod_status is enabled."
        get_endpoint
        
    else
        echo "mod_status is not enabled"
        echo
        tput setaf 3
        echo "------------Enable mod_status------------" 
        echo
        tput sgr0

        echo "The installer will add the configuration below to status.conf to enable mod_status in the $status_conf_path directory."
        echo
        echo "The following configuration  will be added in the $status_conf_file file:"
        echo -e $content
        echo
        read -p "Do you want to enable mod_status??(y or n):" continue

        if [ $continue = "n" -o $continue = "N" ] ; then
            echo
            
        elif [ $continue = "y" -o $continue = "Y" ] ; then
            echo "Taking a backup of the $status_conf_file file."
            output=$(cp $status_conf $status_conf_path/$status_conf_file.bak.$(date +%Y_%m_%d_%H_%M_%S))
            error_handler $? $output
            echo
            echo "Adding the configuration to enable mod_status."
            add_content 
            echo "Completed."
            restart_apache

        else 
            echo "Invalid input"
            exit
        fi

    fi

}

get_endpoint(){
    line=$(grep -nE "^[^#]*\<SetHandler server-status\>" $status_conf | awk -F: '{print $1}')
    l_no=$(( $line-1 ))


    while [ $l_no -gt 0 ] ; do
    
    text=$(sed -n $l_no"p" $status_conf)
    
    if echo $text | grep -qE "^[^#]*\<Location\>" ; then
        endpoint=$(echo $text | grep  "^[^#]*\<Location\>" | sed -n 's/^.*<Location \([^>]*\)>.*/\1/p') 
        echo "The endpoint of mod_status is: $endpoint"
        echo "Proceeding to install the plugin."
        echo
        break
        
        
    else
        l_no=$(( $l_no-1 ))
    fi

    done


}

add_content() {

    output=$(sed -i "/^<IfModule mod_status.c>/a\ $content"  $status_conf)
    error_handler $? $output

}

restart_apache(){

     echo "The configuration changes will only reflect after restarting or reloading the Apache web server."
     read -p "Do you want to restart the Apache web server? (y or n):" restart
        if  [ -z "$restart" ] || [ $restart = "y" -o $restart = "Y" ] ; then
            echo "Restarting the Apache web server."
            if [[ -f /etc/debian_version ]] ; then
                output=$(systemctl restart apache2)
                error_handler $? $output
                echo "Completed."
            elif [[ -f /etc/redhat-release ]] ; then
                output=$(systemctl restart httpd)
                error_handler $? $output
                echo "Completed."
            fi
            
        else
            echo "Process exited."
            
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
        echo "chown -R site24x7-agent:site24x7-group $plugin_dir$plugin"
    fi
}

if [[ -f /etc/debian_version ]] ; then
    status_conf_path=$debian_path
elif [[ -f /etc/redhat-release ]] ; then
    status_conf_path=$centos_path
else
    install_plugin
    exit
fi



install_plugin() {

    check_plugin_exists
    tput setaf 3
    echo
    echo "------------Downloading the plugin files------------"
    echo    
    tput sgr0

    install

    echo
    echo 

    get_plugin_data

    add_conf

    python_path_update

    check_plugin_execution

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
}


tput setaf 3
echo
echo "------------Checking if $status_conf_file exists------------"
tput sgr0


echo
check_if_dir_exists     
check_if_file_exists

install_plugin
