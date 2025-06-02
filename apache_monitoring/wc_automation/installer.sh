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

monitorName="${parts[-1]}"

CURRENT_DIR_NAME=$(echo "${parts[*]}" | sed 's/ /\//g')
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
    source "${CURRENT_DIR_NAME}/$monitorName.cfg" &> /dev/null || :
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
        if $PIP_CMD install "$package" --break-system-packages &> /dev/null; then
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

# --- Apache mod_status enable section starts here ---

# Check if apache2 is installed
if command -v apache2 &> /dev/null; then
    echo "Apache detected. Enabling mod_status..."

    # Enable mod_status module (Debian/Ubuntu style)
    sudo a2enmod status

    # Create mod_status config snippet
    STATUS_CONF="/etc/apache2/conf-available/server-status.conf"

    sudo tee "$STATUS_CONF" > /dev/null << EOF
<Location /server-status>
    SetHandler server-status
    Require local
</Location>
EOF

    # Enable the configuration
    sudo a2enconf server-status

    # Reload Apache to apply changes
    sudo systemctl reload apache2

    echo "Apache mod_status enabled and /server-status URL activated."
    echo "You can access it at: http://localhost/server-status?auto"

elif command -v httpd &> /dev/null; then
    echo "Apache httpd detected. Enabling mod_status..."

    # Try to enable mod_status by editing /etc/httpd/conf.modules.d/ or main config
    # This part may vary depending on the distro

    # Check if mod_status is already loaded, else load it
    if ! grep -q "mod_status.so" /etc/httpd/conf.modules.d/*.conf; then
        echo "LoadModule status_module modules/mod_status.so" | sudo tee /etc/httpd/conf.modules.d/00-status.conf
    fi

    # Create mod_status config snippet
    STATUS_CONF="/etc/httpd/conf.d/server-status.conf"

    sudo tee "$STATUS_CONF" > /dev/null << EOF
<Location /server-status>
    SetHandler server-status
    Require local
</Location>
EOF

    # Restart Apache to apply changes
    sudo systemctl reload httpd

    echo "Apache mod_status enabled and /server-status URL activated."
    echo "You can access it at: http://localhost/server-status?auto"

else
    echo "Apache is not installed or not found. Skipping Apache mod_status configuration."
fi

# --- Apache mod_status enable section ends here ---

## Additional actions for apache_monitoring end here


output=$("$PYTHON_PATH" "$TARGET_PY_FILE" $(for config in "${CONFIGURATION_REQUIRED[@]}"; do 
    if [ -n "${!config}" ]; then 
        echo "--$config ${!config}"; 
    fi; 
done))

if grep -qE '"status": 0' <<< "$output" ; then
    echo "Error: $(grep -oP '"msg"\s*:\s*"\K(\\.|[^"\\])*' <<< "$output")"
    exit 1
else
    echo "Execution completed successfully."
fi
