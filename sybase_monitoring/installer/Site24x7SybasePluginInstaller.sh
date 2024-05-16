#!/bin/bash

plugin_name="sybase_monitoring"
plugin_url="https://raw.githubusercontent.com/site24x7/plugins/master/"


blue='\033[0;34m'   
green='\033[0;32m'
red='\033[0;31m'
reset='\033[0m'

#echo "${green}Hiiiiiii${reset}"

agent_path="/opt/site24x7/monagent/" 
agent_temp_path=$agent_path"temp/"
agent_plugin_path=$agent_path"plugins/"
    
# checking the existence of Agent Temporary Directory
if [ ! -d $agent_temp_path ] ; then
    echo "${red}The Site24x7LinuxAgent directory is not present. Install the Site24x7LinuxAgent and try installing the plugin again (or) Run the Installation script as root user${reset}"
    return 0
        
fi


install_plugin(){
    echo "${green}------------------------------ Starting plugin installation ------------------------------${reset}"
    echo
        
    # Creating the Agent Plugin Temporary Directory
    plugins_temp_path=$agent_temp_path"plugins/"
    if [ ! -d $plugins_temp_path ] ; then
        mkdir $plugins_temp_path
        if [ ! -d $plugins_temp_path ] ; then
            echo "${red}------------------------------  Error occured. Process exited.------------------------------${reset}"
            echo
            return 0
        fi
    fi
    mkdir $plugins_temp_path$plugin_name
    # Downloading the files from GitHub
    echo "${blue}Downloading the plugin files from the Site24x7 GitHub repository.${reset}"

    temp_plugin_path=$plugins_temp_path$plugin_name

    java_file_url=$plugin_url$plugin_name/sybaseDB.java
    sh_file_url=$plugin_url$plugin_name/$plugin_name.sh
    jar1_file_url=$plugin_url$plugin_name/jconn4.jar
    jar2_file_url=$plugin_url$plugin_name/json-20140107.jar
    java_installer=$plugin_url$plugin_name/installer/sybaseInstaller.java
    sh_permission=$plugin_url$plugin_name/installer/Site24x7SybasePluginInstallerAddOn.sh
    
    
    wget -O "$temp_plugin_path/sybaseDB.java" "$java_file_url"
    if [ $? -eq 0 ]; then
        echo ""
    else
        echo "${red}------------------------------ Download failed. Process exited.------------------------------${reset}"
        return 0
    fi
    
    wget -O "$temp_plugin_path/sybase_monitoring.sh" "$sh_file_url"
    if [ $? -eq 0 ]; then
        echo ""
    else
        echo "${red}------------------------------ Download failed. Process exited.------------------------------${reset}"
        return 0
    fi
    
    wget -O "$temp_plugin_path/jconn4.jar" "$jar1_file_url"
    if [ $? -eq 0 ]; then
        echo ""
    else
        echo "${red}------------------------------ Download failed. Process exited.------------------------------${reset}"
        return 0
    fi
    
    wget -O "$temp_plugin_path/json-20140107.jar" "$jar2_file_url"
    if [ $? -eq 0 ]; then
        echo ""
    else
        echo "${red}------------------------------ Download failed. Process exited.------------------------------${reset}"
        return 0
    fi

    wget -O "$temp_plugin_path/sybaseInstaller.java" "$java_installer"
    if [ $? -eq 0 ]; then
        echo ""
    else
        echo "${red}------------------------------ Download failed. Process exited.------------------------------${reset}"
        return 0
    fi

    wget -O "$temp_plugin_path/Site24x7SybasePluginInstallerAddOn.sh" "$sh_permission"
    if [ $? -eq 0 ]; then
        echo ""
    else
        echo "${red}------------------------------ Download failed. Process exited.------------------------------${reset}"
        return 0
    fi
    
    echo "${green}Plugin files downloaded successfully.${reset}"
    
    echo 
    
    java_path=$(which java)
    java_path=$(echo $java_path | awk '{print substr($0, 1, length($0)-5)}')
    if [ $java_path ] ; then
        echo ""
    else
        echo "${red}Ensure latest Java is installed and then run the installer again to proceed with the plugin installation.${reset}"
        return 0
    fi
    
    which javac
    if [ $? -eq 0 ] ; then
        echo ""
    else
        echo "${red}Ensure latest Java compiler is installed and then run the installer again to proceed with the plugin installation.${reset}"
        return 0
    fi

    i=1
    echo
    while [ $i -le 3 ]
    do
        if [ $i = 3 ];then
            echo "${red}Without a hostname, Sybase can't be monitored${reset}"
            return 0
        fi 
        echo "  Enter the hostname :"
        read hostname
        echo
        if [ ${#hostname} -ne 0  ];then
            break;
        fi
        i=$(($i+1))
    done

    while [ $i -le 3 ]
    do
        if [ $i = 3 ];then
            echo "${red}Without a port, Sybase can't be monitored${reset}"
            return 0
        fi 
        echo "Enter the port :"
        read port
        echo
        if [ ${#port} -ne 0  ];then
            break;
        fi
        i=$(($i+1))
    done

    while [ $i -le 3 ]
    do
        if [ $i = 3 ];then
            echo "${red}Without a username, Sybase can't be monitored${reset}"
            return 0
        fi 
        echo "Enter the username : "
        read username
        echo
        if [ ${#username} -ne 0  ];then
            break;
        fi
        i=$(($i+1))
    done

    echo "Enter the password :"
    read password
    echo

    syb_permission="sybase_monitoring/Site24x7SybasePluginInstallerAddOn.sh"
    syb_perm_temp_path=$plugins_temp_path$syb_permission
    replace_string_in_file $syb_perm_temp_path 'HOST=""' 'HOST="'$hostname'"'
    replace_string_in_file $syb_perm_temp_path 'PORT=""' 'PORT="'$port'"'
    replace_string_in_file $syb_perm_temp_path 'USERNAME=""' 'USERNAME="'$username'"'
    replace_string_in_file $syb_perm_temp_path 'PASSWORD=""' 'PASSWORD="'$password'"'
    replace_string_in_file $syb_perm_temp_path 'JAVA_HOME="/usr/bin"' 'JAVA_HOME="'$java_path'"'
    replace_string_in_file $syb_perm_temp_path 'PLUGIN_PATH=""' 'PLUGIN_PATH="/opt/site24x7/monagent/temp/plugins/sybase_monitoring"'

    sh $syb_perm_temp_path

    if [ $? -ne 0 ]; then
        echo -e "${red}Error occured. Execution failed. Process exited.${reset}"
        return 0
    fi


    
    echo "${blue}Adding the configurations in the .sh file.${reset}"
    plugin_dir_name="sybase_monitoring/sybase_monitoring.sh"
    cmd="chmod +x ${plugins_temp_path}${plugin_name}"
    eval "$cmd"
    sybase_temp_path=$plugins_temp_path$plugin_dir_name
    
    replace_string_in_file $sybase_temp_path 'HOST=""' 'HOST="'$hostname'"'
    replace_string_in_file $sybase_temp_path 'PORT=""' 'PORT="'$port'"'
    replace_string_in_file $sybase_temp_path 'USERNAME=""' 'USERNAME="'$username'"'
    replace_string_in_file $sybase_temp_path 'PASSWORD=""' 'PASSWORD="'$password'"'
    replace_string_in_file $sybase_temp_path 'JAVA_HOME="/usr/bin"' 'JAVA_HOME="'$java_path'"'
    replace_string_in_file $sybase_temp_path 'PLUGIN_PATH="/opt/site24x7/monagent/plugins/sybase_monitoring"' 'PLUGIN_PATH="/opt/site24x7/monagent/temp/plugins/sybase_monitoring"'
    
    
    
    # Setting Executable Permissions for the Plugin
    cmd="chmod 744 ${plugins_temp_path}/${plugin_name}/${plugin_name}.sh"
    eval "$cmd"
    
    if [ $? -ne 0 ] ; then
        return 0
    fi
    
    # Validating the plugin output
    echo "${blue}Validating the plugin.${reset}"
    file=".sh"
    sh $plugins_temp_path$plugin_name/$plugin_name$file

    if [ $? -ne 0 ]; then
        echo -e "${red}Error occured. Execution failed. Process exited.${reset}"
        return 0
    else
        echo "${green}Plugin output validated successfully.${reset}"
        replace_string_in_file $sybase_temp_path 'PLUGIN_PATH="/opt/site24x7/monagent/temp/plugins/sybase_monitoring"' 'PLUGIN_PATH="/opt/site24x7/monagent/plugins/sybase_monitoring"'
        
    fi

    echo
    echo "${blue} Installation in progress.${reset}"

    rm $syb_perm_temp_path
    syb_rm="sybase_monitoring/sybaseInstaller.java"
    rm $plugins_temp_path$syb_rm
    syb_rm_class="sybase_monitoring/sybaseInstaller.class"
    rm $plugins_temp_path$syb_rm_class


    if [ ! -d $agent_plugin_path$plugin_name ] ; then

        mv $plugins_temp_path$plugin_name $agent_plugin_path$plugin_name

        if [ $? -ne 0 ] ; then
            echo "${red}Process exited.${reset}"
            return 0
            
        else
            echo "${green}Plugin installed successfully.${reset}"
            echo
        fi

    else
        echo "${blue}A Sybase plugin already exists in the agent directory.${reset}"
        echo
            
        i=1
        while [ $i -le 3 ]
        do
            echo "Do you want to proceed with replacing the existing Sybase monitoring ? (Y or N) "
            read cx_inp
            echo

            if [ $cx_inp = "Y" ] || [ $cx_inp = "y" ]; then

                rm -r $agent_plugin_path$plugin_name
                mv $plugins_temp_path$plugin_name $agent_plugin_path$plugin_name

                if [ $? -ne 0 ] ; then
                    echo "${red}Process exited.${reset}"
                    return 0
                    
                else
                    echo "${green}Plugin installed successfully.${reset}"
                    echo
                    break
                    
                fi

            elif [ $cx_inp = "N" ] || [ $cx_inp = "n" ]; then
                echo "${red}Process exited.${reset}"
                return 0
            else
                if [ $i = 3 ];then
                    echo "${red}Process exited.${reset}"
                    return 0
                fi
                echo "${blue}Valid input is required.${reset}"
                i=$(($i+1))

            fi
        done
    fi


    
}     
    


replace_string_in_file(){

    #sed -i "s/$2/$3/g" "$1"
    sed -i "s|$2|$3|g" "$1"
    return 1
}

install_plugin
