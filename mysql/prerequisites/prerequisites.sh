#!/bin/bash

#trap Function To reset terminal colours 
func_exit() {
    tput sgr0 # Reset Terminal Colors
    exit 0 # Cleanly exit script
}

#Trap for ctr+c(SIGINT) and ctrl+z(SIGTSTP)

trap func_exit SIGINT SIGTSTP

MySQL=0
MariaDB=0

error_handler() {
    if  [ $1 -ne 0 ]; then
        tput setaf 1
        echo  "------------Error Occured---------"
        echo $2
        tput sgr0
        exit
    fi
}

check_db_type() {
    echo "Comfirm if you are using MySQL or MariaDB"
    PS3="Please select your database type (1 for MySQL, 2 for MariaDB): "
    select i in MySQL MariaDB
    do
        case $i in

        MySQL ) 
            MySQL=1
            echo "MySQL is selected"
            break
        ;;
        MariaDB ) 
            MariaDB=1
            echo "MariaDB is selected"
            break
        ;;
        * ) 
            echo "Illegal character is selected"
        ;;
        esac
    done

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

echo_success(){
    tput setaf 2
    echo "Successful"
    tput sgr0
}

create_user(){
    create_user_query="CREATE USER '$username'@'$user_host' IDENTIFIED BY '$password';"
    result=$(mysql -h "$host" -P "$port" -u "$admin_username" -p"$admin_password" -e "$create_user_query" -s -N  2>&1 | grep -v "Warning")
    echo $result
    error_handler $? $result
    query_error $result
    echo_success
}

set_permissions(){

    echo
    echo "Setting permissions"

    if [ "$MySQL" -eq 1 ]; then
        privilege_query="UPDATE mysql.user SET Super_Priv='Y' WHERE user='$username' AND host='$user_host'; UPDATE mysql.user SET Repl_client_priv='Y' WHERE user='$username' AND host='$user_host';UPDATE mysql.user SET Show_db_priv='Y' WHERE user='$username' AND host='$user_host'; FLUSH PRIVILEGES;"
    else
        privilege_query="GRANT SELECT ON *.* TO '$username'@'$user_host'; GRANT SHOW DATABASES ON *.* TO '$username'@'$user_host'; GRANT SUPER ON *.* TO '$username'@'$user_host'; GRANT REPLICATION SLAVE, REPLICATION CLIENT ON *.* TO '$username'@'$user_host'; FLUSH PRIVILEGES;"
    fi

    result=$(mysql -h "$host" -P "$port" -u "$admin_username" -p"$admin_password" -e "$privilege_query" -s -N 2>&1 | grep -v "Warning")
    echo $result
    error_handler $? $result
    query_error $result
    echo_success

}

check_db_type

echo
echo "Enter the Host, port, Admin credentials to create a user"

tput setaf 6
tput bold
echo

# Prompt for the user's host
read -r -p "Enter the MySQL host (default: localhost): " host
if [ -z "$host" ]; then
    host="127.0.0.1"
fi

if [ "$host" = "localhost" ]; then
    host="127.0.0.1"
fi

# Prompt for the user's host
read -r -p "Enter the MySQL port (default: 3306): " port
if [ -z "$port" ]; then
    port="3306"
fi

read -r -p "Enter the Admin username: " admin_username
if [ -z "$admin_username" ] ; then
    echo
    echo "No Username Supplied!!!"
    exit 1
fi

read -r -p "Enter the Admin password: " admin_password


tput sgr0

echo
echo "Enter the username to be created or grant privileges to an existing user"
echo
echo "Note:"
echo "1. Privileges to be granted: SUPER and REPLICATION CLIENT privilege(s)."
# Print what user_host is
echo "2. The user host specifies the host from which the user is allowed to connect to the MySQL server."
echo "For example, if 'user_host' is set to 'localhost', the user can only connect from the same machine where the MySQL server is running."
echo "If 'user_host' is set to '%', the user can connect from any host."
tput setaf 6
tput bold
echo

read -r -p "Enter the username to be created: " username
if [ -z "$username" ] ; then
    echo
    echo "No Username Supplied!!!"
    exit 1
fi

# Prompt for the user
read -r -p "Enter the user's host (e.g., localhost or %): " user_host
if [ -z "$user_host" ]; then
    echo
    echo "No User's Host Supplied!!!"
    exit 1
fi

read -r -p "Enter the password to be created: " password
if [ -z "$password" ] ; then
    echo
    echo "No Password Supplied!!!"
    exit 1
fi

tput sgr0

echo
echo "Checking if user '$username' exists in MySQL..."

result=$(mysql -h "$host" -P "$port" -u "$admin_username" -p"$admin_password" -e "SELECT EXISTS(SELECT 1 FROM mysql.user WHERE user = '$username');" -s -N 2>&1 | grep -v "Warning")
#error_handler $? $result
query_error $result

if [ "$result" -eq 1 ]; then
    echo "User '$username' exists in MySQL."
    set_permissions
else
    echo "User '$username' does not exist in MySQL."
    echo
    echo "Creating User $username"
    create_user
    set_permissions 
fi
