#!/bin/bash
set -e

PACKAGE_REQUIRED=()

CONFIGURATION_REQUIRED=("url" "username" "password")

# Check for python or python3
for version in python python3; do
    if command -v "$version" &> /dev/null; then
        PYTHON_CMD=$version
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "Error: Python is not installed or not available in the PATH."
    exit 1
fi

PYTHON_PATH=$(command -v "$PYTHON_CMD")
echo "Python executable found at: $PYTHON_PATH"

# Get current file name
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
IFS=/ read -ra parts <<< "$SCRIPT_DIR"
unset "parts[-1]"

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
sed -i "1s|^.*$|#!$PYTHON_PATH|" "$TARGET_PY_FILE"

# Check if the configuration file exists only if CONFIGURATION_REQUIRED is not empty
if [ ${#CONFIGURATION_REQUIRED[@]} -ne 0 ]; then
    CONFIG_FILE="${CURRENT_DIR_NAME}/$monitorName.cfg"
    if [ ! -f "$CONFIG_FILE" ]; then
        echo "Error: Configuration file '$CONFIG_FILE' not found."
        exit 1
    fi

    while IFS='=' read -r key value; do
    key=$(echo "$key" | xargs)  
    value=$(echo "$value" | xargs)
    [[ "$key" =~ ^#.*$ || -z "$key" || "$key" == \[*\] ]] && continue
    eval "$key=\"$value\""
    done < "$CONFIG_FILE"

fi

# Check if pip is installed
PIP_CMD="$PYTHON_CMD -m pip"

if $PIP_CMD --version &> /dev/null; then
    PIP_VERSION=$($PIP_CMD --version | awk '{print $2}')
    echo "Pip is available with version: $PIP_VERSION"
else
    echo "Error: Pip is not installed."
    exit 1
fi

# Check if required packages are installed
for package in "${PACKAGE_REQUIRED[@]}"; do
    if ! $PYTHON_CMD -c "import $package" &> /dev/null; then
        echo "Info: Package '$package' is not installed. Attempting installation..."
        if $PIP_CMD install "$package" &> /dev/null; then
            echo "Package '$package' installed successfully."
        else
            echo "Error: Failed to install the package '$package'."
            exit 1
        fi
    else
        echo "Package '$package' is already installed."
    fi
done

# Execute the Python script with the provided parameters
for config in "${CONFIGURATION_REQUIRED[@]}"; do
    if [ -z "${!config+x}" ]; then
        echo "Error: Configuration parameter '$config' is missing."
        exit 1
    fi
done


## Additional actions for apache_monitoring start here
# Check if urllib is available (standard library)
if $PYTHON_CMD -c "import urllib.request" &> /dev/null; then
    echo "urllib is available."
else
    echo "urllib is not available."
    exit 1
fi


url_host=$(echo "$url" | sed -E 's#https?://([^/:]+).*#\1#')

# Define a function to check if the host is local
is_local_host() {
    [[ "$1" == "localhost" || "$1" == "127.0.0.1" || "$1" == "::1" ]]
}

if is_local_host "$url_host"; then

if curl -s --max-time 3 "$url" | grep -q "Total Accesses"; then
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
<Location /server-status>
    SetHandler server-status
    Require local
</Location>
EOF

            sudo a2enconf server-status > /dev/null
            if [ $? -ne 0 ]; then
                echo "Error: Failed to enable server-status configuration for Apache2."
                exit 1
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
<Location /server-status>
    SetHandler server-status
    Require local
</Location>
EOF

            sudo systemctl reload httpd
        fi

        echo "Apache mod_status enabled and /server-status URL activated."
        echo "You can access it at: http://localhost/server-status?auto"

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
## Additional actions for apache_monitoring end here

ARGS=""
for config in "${CONFIGURATION_REQUIRED[@]}"; do 
    if [ -n "${!config}" ]; then 
        ARGS+="--$config \"${!config}\" "
    fi
done

output=$(eval "\"$PYTHON_PATH\" \"$TARGET_PY_FILE\" $ARGS")

if grep -qE '"status": 0' <<< "$output" ; then
    echo "Error: $(grep -oP '"msg"\s*:\s*"\K(\\.|[^"\\])*' <<< "$output")"
    exit 1
else
    echo "Execution completed successfully."
fi
