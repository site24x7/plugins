#!/bin/bash
set -e

CONFIGURATION_REQUIRED=("nginx_status_url")

check_value(){
    value=$1
    suspicious_regex='[`$\\|;()]'
    command_regex='rm|curl|wget|shutdown|reboot|base64|mkfs'
    
    if [[ "$value" = ~$suspicious_regex ]] || [[ "$value" =~ $command_regex ]]; then
        echo "Suspicious content detected."
        exit 1
    fi
}

# Check for python or python3
for version in python python3; do
    if command -v "$version" &> /dev/null; then
        PYTHON_CMD=$version
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "Error: Python is not installed or not available in the PATH."
fi

# Get current file name
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
CURRENT_DIR_NAME=$(dirname "$SCRIPT_DIR")
monitorName=$(basename "$CURRENT_DIR_NAME")

TARGET_PY_FILE="${CURRENT_DIR_NAME}/$monitorName.py"

# Check if the Python file exists
if [ ! -f "$TARGET_PY_FILE" ]; then
    echo "Error: Python script '$TARGET_PY_FILE' not found in the expected directory."
    exit 1
fi

# Add Python shebang line to the top of the Python file
if [ -n "$PYTHON_CMD" ]; then
    PYTHON_PATH=$(command -v "$PYTHON_CMD")
    echo "Python executable found at: $PYTHON_PATH"
    sed -i "1s|^.*$|#!$PYTHON_PATH|" "$TARGET_PY_FILE"
fi

declare -A config

# Check if the configuration file exists
if [ ${#CONFIGURATION_REQUIRED[@]} -ne 0 ]; then
    CONFIG_FILE="${CURRENT_DIR_NAME}/$monitorName.cfg"
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "Error: Configuration file '$CONFIG_FILE' not found."
        exit 1
    fi

    while IFS='=' read -r key value || [ -n "$key" ]; do
        key=$(echo "$key" | xargs)  
        value=$(echo "$value" | xargs)
        [[ "$key" =~ ^#.*$ || -z "$key" || "$key" == \[*\] ]] && continue
        for required_key in "${CONFIGURATION_REQUIRED[@]}"; do
            if [[ "$key" == "$required_key" ]]; then
                check_value "$value"
                config["$key"]="$value"
                break
            fi
        done
    done < "$CONFIG_FILE"
fi

## Additional actions for nginx monitoring start here
# Check if urllib is available (standard library)
if $PYTHON_CMD -c "import urllib.request" &> /dev/null; then
    echo "urllib is available."
else
    echo "urllib is not available."
fi

# === Insert stub_status block into nginx.conf ===
stub_status_block=" 
    location /nginx_status {
        stub_status on;
        allow 127.0.0.1;
    }"

insert_stub_status() {
    nginx_conf="/etc/nginx/nginx.conf"

    if [ ! -f "$nginx_conf" ]; then
       nginx_conf=$(sudo nginx -t 2>&1 | grep "configuration file" | grep -oE '/[^ ]*nginx\.conf' | head -n 1)
    fi

    if [ ! -f "$nginx_conf" ]; then
        echo "stub_status config: FAIL (nginx.conf not found)"
        return 1
    fi

    if grep -q "stub_status on;" "$nginx_conf"; then
        echo "stub_status config: already exists"
        return 0
    fi

    line_no=$(awk '/^[^#]*server_name[[:space:]]/ {print NR; exit}' "$nginx_conf")
    if [ -z "$line_no" ]; then
        echo "stub_status config: FAIL (Server block not found)"
        return 1
    fi

    cp "$nginx_conf" "$nginx_conf.bak.$(date +%Y%m%d%H%M%S)"

    awk -v insert_line="$line_no" -v content="$stub_status_block" '
    NR == insert_line {
        print $0
        print content
        next
    }
    { print $0 }' "$nginx_conf" > "$nginx_conf.tmp" && mv "$nginx_conf.tmp" "$nginx_conf"

    if [ $? -ne 0 ]; then
        echo "stub_status config: FAIL (insertion failed)"
        return 1
    fi

    if sudo systemctl reload nginx 2>/dev/null; then
        echo "stub_status config added successfully."
    else
        echo "stub_status config addition failed."
        return 1
    fi
}

# Call insertion function (non-interactive)

url_host=$(echo "${config[nginx_status_url]}" | sed -E 's#https?://([^/:]+).*#\1#')

# Define a function to check if the host is local
is_local_host() {
    [[ "$1" == "localhost" || "$1" == "127.0.0.1" || "$1" == "::1" ]]
}


if is_local_host "$url_host"; then

if ! systemctl is-active --quiet nginx; then
        echo "Error: nginx service is not running or not active."
        exit 1
    fi
    
if curl -s --head --request GET "${config[nginx_status_url]}" | grep -q "200 OK"; then
    echo "URL is active."
else
    echo "URL is not active. Attempting to insert stub_status block..."
    insert_stub_status
fi

else
    echo "Remote URL detected."
fi
## Additional actions for nginx monitoring end here

sleep 5
