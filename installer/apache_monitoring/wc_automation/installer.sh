#!/bin/bash
set -e

check_value(){
    value=$1
    
    execution_pattern='\$\([^)]*\)|`[^`]*`|~\([^)]*\)'
    if [[ "$value" =~ $execution_pattern ]]; then
        echo "ERROR: Command execution pattern detected in value: '$value'"
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

# Always check for configuration file
CONFIG_FILE="${CURRENT_DIR_NAME}/$monitorName.cfg"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file '$CONFIG_FILE' not found."
    exit 1
fi

while IFS='=' read -r key value || [ -n "$key" ]; do
    key="${key#"${key%%[![:space:]]*}"}"   
    key="${key%"${key##*[![:space:]]}"}"   
    value="${value#"${value%%[![:space:]]*}"}"   
    value="${value%"${value##*[![:space:]]}"}" 
    
    [[ "$key" =~ ^#.*$ || -z "$key" || "$key" == \[*\] ]] && continue
    
    if [[ "$value" =~ ^\".*\"$ ]]; then
        value="${value#\"}"   
        value="${value%\"}"   
    fi
    
    check_value "$value"
    
    config["$key"]="$value"
done < "$CONFIG_FILE"

## Additional actions for apache_monitoring start here
# Check if urllib is available (standard library)
if "$PYTHON_PATH" -c "import urllib.request" &> /dev/null; then
    echo "urllib is available."
else
    echo "urllib is not available."
fi


url_host=$(echo "${config[url]}" | sed -E 's#https?://([^/:]+).*#\1#')

# Define a function to check if the host is local
is_local_host() {
    [[ "$1" == "localhost" || "$1" == "127.0.0.1" || "$1" == "::1" ]]
}

if is_local_host "$url_host"; then

# Extract the path from the configured URL for Apache mod_status configuration
STATUS_PATH=$(echo "${config[url]}" | sed -E 's#https?://[^/]+(/[^?]*).*#\1#')
if [ -z "$STATUS_PATH" ] || [ "$STATUS_PATH" = "${config[url]}" ]; then
    STATUS_PATH="/"
fi
echo "Configuring Apache mod_status for path: $STATUS_PATH"

if curl -s --max-time 3 "${config[url]}" | grep -q "Total Accesses"; then
        echo "Apache mod_status already enabled. Skipping configuration."
    else
        echo "Apache mod_status not yet enabled. Proceeding to configure..."


# --- Apache mod_status enable section starts here ---
# Function to check if a systemd service is active
is_service_active() {
    local service_name=$1
    if systemctl is-active --quiet "$service_name"; then
        return 0
    else
        return 1
    fi
}


# Check if apache2 or httpd service is running
if systemctl status apache2 &>/dev/null; then
    SERVICE_NAME="apache2"
elif systemctl status httpd &>/dev/null; then
    SERVICE_NAME="httpd"
else
    SERVICE_NAME=""
fi

if [ -n "$SERVICE_NAME" ]; then
    if is_service_active "$SERVICE_NAME"; then
        echo "Apache service ($SERVICE_NAME) is running. Enabling mod_status..."

        if [ "$SERVICE_NAME" == "apache2" ]; then
            sudo a2enmod status > /dev/null
            if [ $? -ne 0 ]; then
                echo "Error: Failed to enable mod_status for Apache2."
                exit 1
            fi

            if [ -d "/etc/apache2" ]; then
                STATUS_CONF="/etc/apache2/conf-available/server-status.conf"
                # echo "Creating server-status configuration at if $STATUS_CONF"
            else
                 APACHECTL=$(command -v apachectl || command -v apache2ctl)
                if [ -n "$APACHECTL" ]; then
                    SERVER_ROOT=$($APACHECTL -V | grep -i 'HTTPD_ROOT' | awk -F'"' '{print $2}')
                    
                    STATUS_CONF="$SERVER_ROOT/conf-available/server-status.conf"
                fi
                # echo "Creating server-status configuration at else $STATUS_CONF"
            fi
            # echo "Creating server-status configuration at final $STATUS_CONF"
            if [ -z "$STATUS_CONF" ]; then
                echo "Error: Could not determine the configuration file path for Apache2 mod_status."
                exit 1
            fi
            echo "Creating server-status configuration at $STATUS_CONF"
            sudo tee "$STATUS_CONF" > /dev/null << EOF
<Location $STATUS_PATH>
    SetHandler server-status
    Require local
</Location>
EOF

            sudo a2enconf server-status > /dev/null
            if [ $? -ne 0 ]; then
                echo "Error: Failed to enable server-status configuration for Apache2."
            fi
            sudo systemctl reload apache2

        else
            # httpd service
            if ! grep -q "mod_status.so" /etc/httpd/conf.modules.d/*.conf 2>/dev/null; then
                echo "LoadModule status_module modules/mod_status.so" | sudo tee /etc/httpd/conf.modules.d/00-status.conf
            fi

             if [ -d "/etc/httpd/conf.d" ]; then
                STATUS_CONF="/etc/httpd/conf.d/server-status.conf"
            else
                APACHECTL=$(command -v apachectl || command -v httpd)
                if [ -n "$APACHECTL" ]; then
                    SERVER_ROOT=$($APACHECTL -V | grep -i 'HTTPD_ROOT' | awk -F'"' '{print $2}')
                    STATUS_CONF="$SERVER_ROOT/conf.d/server-status.conf"
                else
                    echo "Error: apachectl or httpd not found. Cannot determine httpd config path."
                    exit 1
                fi
            fi

            if [ -z "$STATUS_CONF" ]; then
                echo "Error: Could not determine the configuration file path for httpd mod_status."
                exit 1
            fi

            echo "Creating server-status configuration at $STATUS_CONF"
            sudo tee "$STATUS_CONF" > /dev/null << EOF
<Location $STATUS_PATH>
    SetHandler server-status
    Require local
</Location>
EOF

            sudo systemctl reload httpd
        fi

        echo "Apache mod_status enabled and /server-status URL activated."

    else
        echo "Error: Apache service ($SERVICE_NAME) is installed but not running or inactive."
        exit 1
    fi
else
    echo "Apache service not found. Skipping Apache mod_status configuration."
fi
fi   

# --- Apache mod_status enable section ends here ---

else
    echo "Remote URL detected."
fi

echo "Building command line arguments from configuration..."
declare -a CMD_ARGS_ARRAY

for key in "${!config[@]}"; do
    value="${config[$key]}"
    CMD_ARGS_ARRAY+=("--$key")
    CMD_ARGS_ARRAY+=("$value")
done

echo "Executing Apache monitoring script..."

DISPLAY_CMD="$PYTHON_PATH \"$TARGET_PY_FILE\""
for ((i=0; i<${#CMD_ARGS_ARRAY[@]}; i+=2)); do
    key="${CMD_ARGS_ARRAY[i]}"
    value="${CMD_ARGS_ARRAY[i+1]}"
    DISPLAY_CMD="$DISPLAY_CMD $key '$value'"
done

echo "Command: $DISPLAY_CMD"

if [ ${#CMD_ARGS_ARRAY[@]} -gt 0 ]; then
    OUTPUT=$("$PYTHON_PATH" "$TARGET_PY_FILE" "${CMD_ARGS_ARRAY[@]}")
fi

# Display the output
echo "$OUTPUT"

if [ -z "$OUTPUT" ]; then
    echo "Execution failed: Output is empty"
    exit 1
fi

if echo "$OUTPUT" | grep -q '"status": 0'; then
    ERROR_MSG=$(echo "$OUTPUT" | grep -o '"msg": *"[^"]*"' | sed 's/"msg": *"\([^"]*\)"/\1/')
    
    echo "Execution failed: $ERROR_MSG"
    exit 1
else
    echo "Executed successfully"
fi

echo "Apache monitoring script execution completed."