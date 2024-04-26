#!/bin/bash

#trap Function To reset terminal colours 
func_exit() {
    tput sgr0 # Reset Terminal Colors
    exit 0 # Cleanly exit script
}

#Trap for ctr+c(SIGINT) and ctrl+z(SIGTSTP)

trap func_exit SIGINT SIGTSTP

# Agent and Plugin Directory
plugin=nginx
agent_dir=/opt/site24x7/monagent

# Enable
nginx_conf_file=nginx.conf
nginx_conf_path=/etc/nginx
nginx_conf=$nginx_conf_path/$nginx_conf_file
endpoint="/nginx_status"
content=" #Added By Site24x7 Installer For Monitoring\n\tlocation /nginx_status {\n\t\tstub_status on;\n\t\tallow 127.0.0.1;\n\t}"
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
    echo "The Site24x7LinuxAgent is required to install the NGINX plugin. Enter the correct directory path of the agent to proceed."
    agent_dir=/opt/site24x7/monagent
    tput sgr0
  else
    agent_status=$($agent_dir/bin/monagent status)
    if ! echo "$agent_status" | grep -q "Site24x7 monitoring agent service" ; then
        tput setaf 1
        echo
        echo "The Site24x7LinuxAgent is required to install the NGINX plugin. Enter the correct directory path of the agent to proceed."
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

        download_files https://raw.githubusercontent.com/site24x7/plugins/master/nginx/nginx.py
        download_files https://raw.githubusercontent.com/site24x7/plugins/master/nginx/nginx.cfg

    else
        output=$(mkdir -p $temp_dir)
         if [ $? -ne 0 ]; then
            tput setaf 1
            echo "------------Error Occured------------"
            echo $output
            tput sgr0
            exit
        fi

        download_files https://raw.githubusercontent.com/site24x7/plugins/master/nginx/nginx.py
        download_files https://raw.githubusercontent.com/site24x7/plugins/master/nginx/nginx.cfg
        
    fi

}

get_plugin_data() {
    default_nginx_status_url="http://localhost:80$endpoint"
    default_username="None"
    default_password="None"
    tput setaf 3
    echo
    echo "------------Connection Details------------"
    echo 
    tput sgr0

    echo " 1.Provide the URL and authentication credentials (if any) below to access the NGINX status URL (nginx_status_url)."
    echo " 2.Press Enter to keep the default values. If you hit Enter, the default values will be used for the connection."
    echo
    echo " $(tput setaf 3)$(tput bold)Note$(tput sgr0): The username and password you provide will be securely encrypted in the agent and will not be stored in any of the Site24x7 databases."
    echo
    
    tput setaf 4
    read -r -p  "  Enter the required nginx_status_url( default: $default_nginx_status_url ): " nginx_status_url
    if [ -z $nginx_status_url ] ; then
        nginx_status_url=$default_nginx_status_url
    fi
    read -r -p "  Enter the username( default: $default_username ): " username
    if [ -z $username ] ; then
        username=$default_username
    fi
    read -r -p "  Enter the password( default: $default_password ): " password
    if [ -z $password ] ; then
        password=$default_password
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

    output=$($python $py_file --nginx_status_url "$nginx_status_url" --username "$username" --password "$password")
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

    elif ! echo "$output" | grep -qE "\"Count of successful client connections\":|\"Count of client requests\":"; then
        tput setaf 3
        echo "The output does not contain metrics. Check if you have provided the correct endpoint for the status URL(nginx_status_url)."
        echo "An example of an nginx_status_url: http://localhost:80$endpoint"
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
    output=$(sed -i "/nginx_status_url*/c\nginx_status_url = \"$nginx_status_url\""  "$cfg_file")
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
        echo "The NGINX monitoring plugin folder already exists in the Plugins directory."
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


    if [[ -d $nginx_conf_path ]] ; then  
        echo "$nginx_conf_path directory exists."
        echo
        return 0
    else
        echo "$nginx_conf_path directory does not exist."
        for (( i=0; i<3; i++)) ; do
            read -p "Enter the alternate directory if you have nginx.conf in a different directory: " nginx_conf_path
            if [ -z $nginx_conf_path ]; then
                echo "Enter the correct path to the NGINX directory."
            else
                if [[ -d $nginx_conf_path ]] ; then  
                    echo "$nginx_conf_path directory exists."
                    nginx_conf=$nginx_conf_path/$nginx_conf_file
                    echo
                    break
                else   
                    echo "Enter the correct path to them NGINX directory."
                fi
            fi

            if [ $i -eq 2 ] ; then
                echo "The path does not exist. Please check if you have the correct path."
                error_handler 1  
                return 1 
            fi
        done
    fi
}


check_if_file_exists() {


    nginx_conf=$nginx_conf_path/$nginx_conf_file
    if [[ -f $nginx_conf ]] ; then
        
        echo "$nginx_conf_file file exists."
        
        echo
        tput setaf 3
        echo
        echo "------------Checking if the NGINX status page is enabled------------"
        echo
        tput sgr0
        enabled_or_not
        
        return 0
    else

        tput setaf 3
        echo "------------nginx.conf does not exist------------" 
        echo
        tput sgr0
        
        echo "The $nginx_conf does not exist. Enter the alternate directory if you have nginx.conf in a different directory."
        echo
    fi



}

check_blocks(){
    
    server_block_pattern="^[^#]*\<server\s*{"
    path=$1
    output=$(grep $server_block_pattern $nginx_conf | wc -l)
    error_handler $? $output
    server_block_count=$output
    if [ $server_block_count -lt 1 ] ; then
        echo -e "No server block found in the $nginx_conf_file file. \n\nIf you have the configurations in seperate files or in a separate directory, add the below content inside the $(tput smul)server blocks$(tput sgr0) to enable the status page for monitoring."
        echo
        echo -e "$content"
        echo
        echo "Once the status page is enabled, rerun the installer to install the plugin."
        echo "If you have already enabled the status page, procced to install the plugin and provide the URL as input."
        read -p "Do you want to proceed with the plugin installation?(y or n):" continue
        if [ $continue = "n" -o $continue = "N" ] ; then
            echo "Process exited"
            exit
        else
            echo "Proceeding to install the plugin."
            install_plugin
            exit
        fi
    elif [ $server_block_count -gt 1 ] ; then
        echo "Multiple server blocks found in the $nginx_conf_file file."
        echo "To get metrics, the content below will be added in the $(tput smul)first server block$(tput sgr0) found in the $nginx_conf_file. If you need to enable the status page for other server blocks, add the below content manually in the respective server blocks."
        echo -e "$content"
    elif [ $server_block_count -eq 1 ] ; then
        echo "The installer will add the configuration below to $nginx_conf_file to enable the status page in the $nginx_conf_path directory."
        echo
        echo "The below content will be added below the $(tput setaf 4)server_name directive$(tput sgr0) in the server block in the $nginx_conf_file." 
        echo
        echo -e $content
        echo
    fi
}
enabled_or_not() {

    output=$(grep -E "^[^#]*\<stub_status on;"  $nginx_conf )
    exit_status=$?
    if [ $exit_status != 1 ] ; then
        error_handler $exit_status $output
    fi


    if [ -n "$output" ] ; then
        echo "The status page is enabled."
        get_endpoint
        
    else
        echo "The status page is not enabled."
        echo
        check_blocks
        tput setaf 3
        echo "------------Enable status page------------" 
        echo
        tput sgr0

        read -p "Do you want to enable the status page?(y or n):" continue

        if [ $continue = "n" -o $continue = "N" ] ; then
            echo "Proceeding to install the plugin."
            
        elif [ $continue = "y" -o $continue = "Y" ] ; then
            echo "Proceeding to install the plugin."
            echo "Taking a backup of the $nginx_conf_file file."
            output=$(cp $nginx_conf $nginx_conf_path/$nginx_conf_file.bak.$(date +%Y_%m_%d_%H_%M_%S))
            error_handler $? $output
            echo "Completed."
            echo "Adding the configuration to enable the status page."
            add_content 
            echo "Completed."
            restart_nginx

        else 
            echo "Invalid input."
            exit
        fi

    fi

}

get_endpoint(){
    line=$(grep -nE "^[^#]*\<stub_status on;"  $nginx_conf | awk -F: '{print $1}')
    error_handler $? $output
    l_no=$(( $line-1 ))

    while [ $l_no -gt 0 ] ; do
    
    text=$(sed -n $l_no"p" $nginx_conf)
    
    if echo $text | grep -qE "^[^#]*\location" ; then
        endpoint=$(echo $text | grep -oP 'location\s+\K[^{]*') 
        echo "The endpoint of status page is: $endpoint"
        echo "Proceeding to install the plugin."
        echo
        break
        
        
    else
        l_no=$(( $l_no-1 ))
    fi

    done


}

add_content() {

    output=$(grep -P -n -m 1 'server_name\s+[\w.-]+\s+;' $nginx_conf | awk -F: '{print $1}')
    error_handler $? $output
    line_no=$(($output+1))
    output=$(sed -i ""$line_no"i  $content"  $nginx_conf)
    error_handler $? $output

}

restart_nginx(){

     echo "The configuration changes will only reflect after restarting or reloading the NGINX web server."
     read -p "Do you want to reload the nginx web server? (y or n):" restart
        if  [ -z "$restart" ] || [ $restart = "y" -o $restart = "Y" ] ; then
            echo "Restarting the NGINX web server."
            output=$(systemctl reload nginx)
            error_handler $? $output
            echo "Completed."
            
        else
            echo "Process exited."
            
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
    if  $agent_path_change ; then
        echo "If you have installed the agent as non-root, execute the command below with appropriate details to allow the user access to the plugin folder."
        echo "For example, if the user is 'site24x7-agent' and the group is 'site24x7-group', the command would be:"
        echo "$(tput bold)chown -R site24x7-agent:site24x7-group $plugin_dir$plugin$(tput sgr0)"
    fi
}

if [[ -f /etc/debian_version ]] || [[ -f /etc/redhat-release ]] ; then
    run=true
else
    install_plugin
    exit
fi

tput setaf 3
echo
echo "------------Checking if $nginx_conf_file exists------------"
tput sgr0


echo
check_if_dir_exists     
check_if_file_exists

install_plugin
