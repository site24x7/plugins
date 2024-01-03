#! /bin/bash


PLUGIN_VERSION=1
HEARTBEAT="true"
PLUGIN_OUTPUT=$PLUGIN_OUTPUT"heartbeat_required:$HEARTBEAT|plugin_version:$PLUGIN_VERSION|"


if [[ -e /etc/os-release ]]; then

    distro_name=$(grep "^NAME" /etc/os-release | cut -d '=' -f2)
    if [[ $? -ne 0 ]]; then
        PLUGIN_OUTPUT=$PLUGIN_OUTPUT"status:0|msg:Distro name not found|"
        echo $PLUGIN_OUTPUT
        exit $?
    fi
else
    PLUGIN_OUTPUT=$PLUGIN_OUTPUT"status:0|msg:/etc/os-release file not found|"
    echo $PLUGIN_OUTPUT
    exit $?
fi


     
# Ubuntu

if [[ $distro_name == "\"Ubuntu\"" ]]; then

    ubuntu_updates_file=/var/lib/update-notifier/updates-available

    if [[ -e $ubuntu_updates_file ]]; then
        updates=$(grep "packages can be updated" $ubuntu_updates_file)
    
        if [[ $? -ne 0 ]]; then
            updates=$(grep "can be installed immediately" $ubuntu_updates_file)

            if [[ $? -ne 0 ]]; then
                updates=$(grep "can be applied immediately" $ubuntu_updates_file)

            else
                updates=""

            fi
        fi    


        security_updates=$(grep "updates are security updates" $ubuntu_updates_file)
    
        if [[ $? -ne 0 ]]; then
            security_updates=$(grep "updates are standard security updates" $ubuntu_updates_file)

            if [[ $? -ne 0 ]]; then
                security_updates=$(grep "additional security updates can be applied" $ubuntu_updates_file)           

            else
                security_updates=""
            fi
        fi    

    else
        PLUGIN_OUTPUT=$PLUGIN_OUTPUT"status:0|msg:/var/lib/update-notifier/updates-available not found.|"
        echo $PLUGIN_OUTPUT
        exit 1
    fi
fi

if [[ -z $updates ]]; then
    update_count="0"
else
    update_count=${updates:0:1}

fi

if [[ -z $security_updates ]]; then
    security_update_count="0"
else
    security_update_count=${security_updates:0:1}

fi


# CentOS

if [[ $distro_name == "\"CentOS Linux\"" ]]; then

    centos_updates_info=$(yum check-update --security | tail -n 1)  
    if [[ $? -ne 0 ]]; then
        PLUGIN_OUTPUT=$PLUGIN_OUTPUT"status:0|msg:Error during executing \"yum check-update --security | tail -n 1\" command.|"
        echo $PLUGIN_OUTPUT
        exit 1    
    fi

    out_verify=$(echo $centos_updates_info | grep -E "^([0-9]{1,3}|No) packages needed for security; ([0-9]{1,3}|No) packages available")
    if [[ $out_verify != $centos_updates_info ]]; then
        PLUGIN_OUTPUT=$PLUGIN_OUTPUT"status:0|msg:Error in command execution.|"
        echo $PLUGIN_OUTPUT
        exit 1
    fi

    centos_security_updates_raw=$(echo $centos_updates_info | cut -d ";" -f1)
    security_update_count=$(echo $centos_security_updates_raw | cut -d " " -f1)
    if [[ $security_update_count == "No" ]]; then
        security_update_count=0
    fi

    centos_updates_raw=$(echo $centos_updates_info | cut -d ";" -f2)
    update_count=$(echo $centos_updates_raw | cut -d " " -f1)

fi


PLUGIN_OUTPUT=$PLUGIN_OUTPUT"packages_to_be_updated:$update_count|security_updates:$security_update_count"
echo $PLUGIN_OUTPUT
exit 0
