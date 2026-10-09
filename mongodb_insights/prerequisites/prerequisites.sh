#!/bin/bash

# Trap function to reset terminal colors and exit cleanly
func_exit() {
    tput sgr0
    exit 0
}

trap func_exit SIGINT SIGTSTP

error_handler() {
    if [ $1 -ne 0 ]; then
        tput setaf 1
        echo "------------Error Occurred---------"
        echo "$2"
        tput sgr0
        exit 1
    fi
}

query_error() {
    error=$@
    if echo "$error" | grep -q -i "error"; then
        tput setaf 1
        echo "------------Error Occurred---------"
        echo "$error"
        tput sgr0
        exit 1
    fi
}

echo_success() {
    tput setaf 2
    echo "Successful"
    tput sgr0
}

while true; do
    read -rp "Which MongoDB client do you want to use? (mongosh/mongo): " MONGO_CLIENT
    MONGO_CLIENT=${MONGO_CLIENT,,} 
    if [[ "$MONGO_CLIENT" == "mongosh" || "$MONGO_CLIENT" == "mongo" ]]; then
        if ! command -v "$MONGO_CLIENT" &> /dev/null; then
            tput setaf 1
            echo "Error: '$MONGO_CLIENT' is not available on your system."
            tput sgr0
            exit 1
        fi
        break
    else
        echo "Please enter 'mongosh' or 'mongo'."
    fi
done

read -rp "Enter MongoDB host (default: localhost): " MONGO_HOST
MONGO_HOST=${MONGO_HOST:-localhost}

read -rp "Enter MongoDB port (default: 27017): " MONGO_PORT
MONGO_PORT=${MONGO_PORT:-27017}

read -rp "Enter Admin authentication database (default: admin): " ADMIN_AUTH_DB
ADMIN_AUTH_DB=${ADMIN_AUTH_DB:-admin}

read -rp "Enter Admin username: " ADMIN_USER

read -rsp "Enter Admin password: " ADMIN_PASS
echo

read -rp "Enter the username to create or update: " USERNAME
if [ -z "$USERNAME" ]; then
    echo "No username supplied!"
    exit 1
fi

read -rsp "Enter the password for user '$USERNAME': " PASSWORD
echo
if [ -z "$PASSWORD" ]; then
    echo "No password supplied!"
    exit 1
fi

ROLES='[{"role": "clusterMonitor", "db": "'$ADMIN_AUTH_DB'"}, {"role": "readAnyDatabase", "db": "'$ADMIN_AUTH_DB'"}]'

CHECK_USER_JS="db.getSiblingDB('$ADMIN_AUTH_DB').getUser('$USERNAME') != null"

CHECK_RESULT=$($MONGO_CLIENT --host "$MONGO_HOST" --port "$MONGO_PORT" -u "$ADMIN_USER" -p "$ADMIN_PASS" --authenticationDatabase "$ADMIN_AUTH_DB" --quiet --eval "$CHECK_USER_JS" 2>&1)
error_handler $? "$CHECK_RESULT"
query_error "$CHECK_RESULT"

if [[ "$CHECK_RESULT" == "true" ]]; then
    echo "User '$USERNAME' exists. Updating roles..."

    UPDATE_USER_JS="db.getSiblingDB('$ADMIN_AUTH_DB').updateUser('$USERNAME', {roles: $ROLES})"

    UPDATE_RESULT=$($MONGO_CLIENT --host "$MONGO_HOST" --port "$MONGO_PORT" -u "$ADMIN_USER" -p "$ADMIN_PASS" --authenticationDatabase "$ADMIN_AUTH_DB" --quiet --eval "$UPDATE_USER_JS" 2>&1)
    error_handler $? "$UPDATE_RESULT"
    query_error "$UPDATE_RESULT"

    echo_success
else
    echo "User '$USERNAME' does not exist. Creating user..."

    CREATE_USER_JS="db.getSiblingDB('$ADMIN_AUTH_DB').createUser({user: '$USERNAME', pwd: '$PASSWORD', roles: $ROLES})"

    CREATE_RESULT=$($MONGO_CLIENT --host "$MONGO_HOST" --port "$MONGO_PORT" -u "$ADMIN_USER" -p "$ADMIN_PASS" --authenticationDatabase "$ADMIN_AUTH_DB" --quiet --eval "$CREATE_USER_JS" 2>&1)
    error_handler $? "$CREATE_RESULT"
    query_error "$CREATE_RESULT"

    echo_success
fi
