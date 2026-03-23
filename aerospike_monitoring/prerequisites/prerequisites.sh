#!/bin/bash

# Aerospike Monitoring Plugin - Prerequisites Setup
# Creates a monitoring user with minimum privileges for the plugin
# Note: Aerospike info commands require zero roles — only authentication is needed

# Trap to reset terminal on exit
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

echo_success() {
    tput setaf 2
    echo "Successful"
    tput sgr0
}

# ──────────────────────────────────────────────
# Check asadm availability
# ──────────────────────────────────────────────

echo
echo "Checking for asadm..."

if ! command -v asadm &>/dev/null; then
    tput setaf 1
    echo "Error: 'asadm' command not found."
    echo
    echo "Please install Aerospike Admin (asadm) before running this script."
    echo "Refer to: https://docs.aerospike.com/tools/asadm"
    tput sgr0
    exit 1
fi

tput setaf 2
echo "Found: $(asadm --version | head -1)"
tput sgr0

# ──────────────────────────────────────────────
# Collect Aerospike connection details
# ──────────────────────────────────────────────

echo
echo "Enter the Aerospike host and port"
tput setaf 6
tput bold
echo

read -r -p "Enter the Aerospike host (default: localhost): " host
if [ -z "$host" ]; then
    host="localhost"
fi

read -r -p "Enter the Aerospike port (default: 3000): " port
if [ -z "$port" ]; then
    port="3000"
fi

tput sgr0

# ──────────────────────────────────────────────
# Check if security is enabled
# ──────────────────────────────────────────────

echo
echo "Checking if security is enabled on the Aerospike server..."

no_auth_result=$(asinfo -h "$host" -p "$port" -v "cluster-name" 2>&1)
no_auth_exit=$?

if [ $no_auth_exit -eq 0 ]; then
    tput setaf 3
    echo "Security is NOT enabled on this Aerospike server."
    echo "The monitoring plugin can connect without authentication."
    echo "No user creation is needed. Set username and password to 'None' in the plugin config."
    tput sgr0
    echo
    exit 0
fi

tput setaf 2
echo "Security is enabled. Proceeding with user setup..."
tput sgr0

# ──────────────────────────────────────────────
# Collect admin credentials
# ──────────────────────────────────────────────

echo
echo "Enter the Aerospike admin credentials"
tput setaf 6
tput bold
echo

read -r -p "Enter the admin username: " admin_username
if [ -z "$admin_username" ]; then
    echo
    echo "No admin username supplied!"
    exit 1
fi

read -r -s -p "Enter the admin password: " admin_password
echo

tput sgr0

# ──────────────────────────────────────────────
# Validate admin connection
# ──────────────────────────────────────────────

echo
echo "Validating admin connection..."

result=$(asinfo -h "$host" -p "$port" -U "$admin_username" -P "$admin_password" -v "cluster-name" 2>&1)
if [ $? -ne 0 ]; then
    tput setaf 1
    echo "------------Error Occurred---------"
    echo "Failed to connect to Aerospike with the provided admin credentials."
    echo "$result"
    tput sgr0
    exit 1
fi

echo_success

# ──────────────────────────────────────────────
# Collect monitoring user details
# ──────────────────────────────────────────────

echo
echo "Enter the monitoring user details"
echo
echo "Note:"
echo "1. Aerospike info commands require zero roles — only a valid user account is needed."
echo "2. If the user already exists, no changes will be made."

tput setaf 6
tput bold
echo

read -r -p "Enter the monitoring username: " username
if [ -z "$username" ]; then
    echo
    echo "No username supplied!"
    exit 1
fi

tput sgr0

# ──────────────────────────────────────────────
# Check if user exists
# ──────────────────────────────────────────────

echo
echo "Checking if user '$username' exists in Aerospike..."

user_list=$(asadm -h "$host" -p "$port" -U "$admin_username" -P "$admin_password" -e "show users" 2>&1)

if [ $? -ne 0 ]; then
    tput setaf 1
    echo "------------Error Occurred---------"
    echo "Failed to retrieve user list."
    echo "$user_list"
    tput sgr0
    exit 1
fi

if echo "$user_list" | grep -qw "$username"; then
    # ── User exists ──
    tput setaf 3
    echo "User '$username' already exists in Aerospike."
    echo "No additional roles or privileges are required for monitoring."
    tput sgr0
else
    # ── User does not exist — create ──
    echo "User '$username' does not exist in Aerospike."
    echo

    tput setaf 6
    tput bold
    read -r -s -p "Enter the password for new user '$username': " password
    echo
    tput sgr0

    if [ -z "$password" ]; then
        echo "No password supplied!"
        exit 1
    fi

    echo
    echo "Creating user '$username'..."

    result=$(asadm -h "$host" -p "$port" -U "$admin_username" -P "$admin_password" --enable \
        -e "manage acl create user $username password $password" 2>&1)

    if echo "$result" | grep -qi "successfully"; then
        echo_success
    else
        tput setaf 1
        echo "------------Error Occurred---------"
        echo "$result"
        tput sgr0
        exit 1
    fi
fi

# ──────────────────────────────────────────────
# Summary
# ──────────────────────────────────────────────

echo
tput setaf 2
echo "────────────────────────────────────────────"
echo " Monitoring user is ready!"
echo "────────────────────────────────────────────"
echo " Use the following in the plugin config:"
echo "   username = \"$username\""
echo "   password = \"<the password you set>\""
echo "────────────────────────────────────────────"
tput sgr0
echo
