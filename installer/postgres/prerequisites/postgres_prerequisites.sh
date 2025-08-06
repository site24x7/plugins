#!/bin/bash

#trap Function To reset terminal colours 
func_exit() {
    tput sgr0 # Reset Terminal Colors
    exit 0 # Cleanly exit script
}

#Trap for ctr+c(SIGINT) and ctrl+z(SIGTSTP)
trap func_exit SIGINT SIGTSTP

error_handler() {
    if [ $1 -ne 0 ]; then
        tput setaf 1
        echo "------------Error Occurred---------"
        echo $2
        tput sgr0
        exit
    fi
}

query_error(){
    error=$@
    if echo "$error" | grep -q "ERROR"; then
        tput setaf 1
        echo  "------------Error Occured---------"
        echo $error
        tput sgr0
        exit
    elif echo "$error" | grep -q "error"; then
        tput setaf 1
        echo  "------------Error Occured---------"
        echo $error
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
    create_user_query="CREATE USER $username WITH PASSWORD '$password';"
    result=$(PGPASSWORD="$admin_password" psql -h "$host" -p "$port" -U "$admin_username" -c "$create_user_query" 2>&1)
    echo $result
    error_handler $? $result
    query_error $result
    echo_success
}

set_permissions() {
    echo
    echo "Setting permissions"

    privilege_query="GRANT pg_monitor TO $username;"
    result=$(PGPASSWORD="$admin_password" psql -h "$host" -p "$port" -U "$admin_username" -c "$privilege_query" 2>&1)
    echo $result
    error_handler $? $result
    query_error $result
    echo_success
}

echo
echo "Enter the Host, port, Admin credentials to create a user"

tput setaf 6
tput bold
echo

read -r -p "Enter the PostgreSQL host (default: localhost): " host
if [ -z "$host" ]; then
    host="127.0.0.1"
fi

read -r -p "Enter the PostgreSQL port (default: 5432): " port
if [ -z "$port" ]; then
    port="5432"
fi

read -r -p "Enter the Admin username: " admin_username
if [ -z "$admin_username" ]; then
    echo
    echo "No Username Supplied!!!"
    exit 1
fi

read -r -p "Enter the Admin password: " admin_password

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

read -r -p "Enter the password to be created: " password
if [ -z "$password" ]; then
    echo
    echo "No Password Supplied!!!"
    exit 1
fi


echo
echo "Checking if user '$username' exists in PostgreSQL..."

result=$(PGPASSWORD="$admin_password" psql -h "$host" -p "$port" -U "$admin_username" -d "$database" -c "SELECT 1 FROM pg_roles WHERE rolname='$username';" 2>&1)
query_error $result

if echo "$result" | grep -q "1"; then
    echo "User '$username' exists in PostgreSQL."
    set_permissions
else
    echo "User '$username' does not exist in PostgreSQL."
    echo
    echo "Creating User $username"
    create_user
    set_permissions 
fi