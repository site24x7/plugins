#!/bin/bash

# ClickHouse Monitoring Plugin - Prerequisites Setup
# Creates or updates a monitoring user with required permissions

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

query_error() {
    local result="$*"
    if echo "$result" | grep -qi "error\|exception\|UNKNOWN_USER\|ACCESS_DENIED"; then
        tput setaf 1
        echo "------------Error Occurred---------"
        echo "$result"
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
# Check clickhouse-client availability
# ──────────────────────────────────────────────

echo
echo "Checking for clickhouse-client..."

if ! command -v clickhouse-client &>/dev/null; then
    tput setaf 1
    echo "Error: 'clickhouse-client' command not found."
    echo
    echo "Please install clickhouse-client before running this script."
    echo "Refer to: https://clickhouse.com/docs/en/install"
    tput sgr0
    exit 1
fi

tput setaf 2
echo "Found: $(clickhouse-client --version)"
tput sgr0

# ──────────────────────────────────────────────
# Collect ClickHouse connection details
# ──────────────────────────────────────────────

echo
echo "Enter the ClickHouse host, port, and admin credentials"
tput setaf 6
tput bold
echo

read -r -p "Enter the ClickHouse host (default: localhost): " host
if [ -z "$host" ]; then
    host="localhost"
fi

read -r -p "Enter the ClickHouse port (default: 9000): " port
if [ -z "$port" ]; then
    port="9000"
fi

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

result=$(clickhouse-client -h "$host" --port "$port" -u "$admin_username" --password "$admin_password" -q "SELECT 1" 2>&1)
if [ $? -ne 0 ]; then
    tput setaf 1
    echo "------------Error Occurred---------"
    echo "Failed to connect to ClickHouse with the provided admin credentials."
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
echo "1. This user will be granted: SELECT ON *.* (read-only access for full monitoring)."
echo "2. If the user already exists, only permissions will be updated."

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
echo "Checking if user '$username' exists in ClickHouse..."

user_exists=$(clickhouse-client -h "$host" --port "$port" -u "$admin_username" --password "$admin_password" \
    -q "SELECT count() FROM system.users WHERE name = '$username'" 2>&1)

query_error "$user_exists"

if [ "$user_exists" -eq 1 ]; then
    # ── User exists ──
    tput setaf 3
    echo "User '$username' already exists in ClickHouse."
    tput sgr0
    echo
    read -r -p "Do you want to update permissions for '$username'? (y/n): " update_choice

    if [ "$update_choice" = "y" ] || [ "$update_choice" = "Y" ]; then
        echo
        echo "Granting SELECT ON *.* to '$username'..."

        result=$(clickhouse-client -h "$host" --port "$port" -u "$admin_username" --password "$admin_password" \
            -q "GRANT SELECT ON *.* TO '$username';" 2>&1)
        query_error "$result"
        echo_success
    else
        echo
        echo "Skipping permission update."
    fi
else
    # ── User does not exist — create ──
    echo "User '$username' does not exist in ClickHouse."
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

    result=$(clickhouse-client -h "$host" --port "$port" -u "$admin_username" --password "$admin_password" \
        -q "CREATE USER '$username' IDENTIFIED BY '$password';" 2>&1)
    query_error "$result"
    echo_success

    echo
    echo "Granting SELECT ON *.* to '$username'..."

    result=$(clickhouse-client -h "$host" --port "$port" -u "$admin_username" --password "$admin_password" \
        -q "GRANT SELECT ON *.* TO '$username';" 2>&1)
    query_error "$result"
    echo_success
fi

echo
