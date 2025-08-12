#!/bin/bash

# Trap Function To reset terminal colors
func_exit() {
    tput sgr0 # Reset Terminal Colors
    exit 0 # Cleanly exit script
}

# Trap for ctrl+c (SIGINT) and ctrl+z (SIGTSTP)
trap func_exit SIGINT SIGTSTP

error_handler() {
    if [ $1 -ne 0 ]; then
        tput setaf 1
        echo "------------Error Occurred---------"
        echo "$2"
        tput sgr0
        exit
    fi
}

query_error() {
    error=$@
    if echo "$error" | grep -qi "ORA-"; then
        tput setaf 1
        echo "------------Error Occurred---------"
        echo "$error"
        tput sgr0
        exit
    fi
}

echo_success() {
    tput setaf 2
    echo "Successful"
    tput sgr0
}

create_user() {
    create_user_query="CREATE USER $username IDENTIFIED BY \"$password\";"
    result=$(echo "$create_user_query" | sqlplus -s "$conn_str" 2>&1)
    echo "$result"
    error_handler $? "$result"
    query_error "$result"
    echo_success
}

set_permissions() {
    echo
    echo "Setting permissions"

    privilege_query="GRANT SELECT_CATALOG_ROLE TO $username;
GRANT CREATE SESSION TO $username;"
    
    result=$(echo "$privilege_query" | sqlplus -s "$conn_str" 2>&1)
    echo "$result"
    error_handler $? "$result"
    query_error "$result"
    echo_success
}


echo
echo "Enter the Host, Port, Service Name, and Admin credentials to create a user"

tput setaf 6
tput bold
echo

read -r -p "Enter the Oracle host (default: localhost): " host
if [ -z "$host" ]; then
    host="127.0.0.1"
fi

read -r -p "Enter the Oracle port (default: 1521): " port
if [ -z "$port" ]; then
    port="1521"
fi

read -r -p "Enter the Oracle service name (default: orcl): " service_name
if [ -z "$service_name" ]; then
    service_name="orcl"
fi

read -r -p "Enter the Admin username: " admin_username
if [ -z "$admin_username" ]; then
    echo
    echo "No Username Supplied!!!"
    exit 1
fi  

read -s -p "Enter the Admin password: " admin_password
echo

tput sgr0

echo
echo "Enter the username to be created or grant privileges to an existing user"
echo
read -r -p "Enter the username to be created: " username
if [ -z "$username" ]; then
    echo
    echo "No Username Supplied!!!"
    exit 1
fi

read -s -p "Enter the password to be created: " password
echo
if [ -z "$password" ]; then
    echo
    echo "No Password Supplied!!!"
    exit 1
fi

# Construct the connection string safely
conn_str="${admin_username}/\"${admin_password}\"@//${host}:${port}/${service_name}"

echo $conn_str

echo
echo "Checking if user '$username' exists in Oracle..."

check_user_query="SELECT COUNT(*) FROM dba_users WHERE username=UPPER('$username');"
result=$(echo "$check_user_query" | sqlplus -s "$conn_str" 2>&1)
query_error "$result"

if echo "$result" | grep -q "1"; then
    echo "User '$username' exists in Oracle."
    set_permissions
else
    echo "User '$username' does not exist in Oracle."
    echo
    echo "Creating User $username"
    create_user
    set_permissions
fi
