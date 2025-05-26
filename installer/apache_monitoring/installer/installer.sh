#!/bin/bash

# Check for python or python3
for version in python python3; do
    if command -v "$version" &> /dev/null; then
        PYTHON_CMD=$version
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "Python is not installed or not found in PATH."
    exit 1
fi

PYTHON_PATH=$(command -v "$PYTHON_CMD")

echo "Python executable path: $PYTHON_PATH"

# Get current directory name
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
IFS=/ read -ra parts <<< "$SCRIPT_DIR"
unset "parts[-1]"

monitorName="${parts[-1]}"

CURRENT_DIR_NAME=$(echo "${parts[*]}" | sed 's/ /\//g')
echo "current dir $CURRENT_DIR_NAME"
TARGET_PY_FILE="${CURRENT_DIR_NAME}/$monitorName.py"

# Check if the file exists
if [ ! -f "$TARGET_PY_FILE" ]; then
    echo "Python file '$TARGET_PY_FILE' not found in the current directory."
    exit 1
fi

echo "Updating Python path in: $TARGET_PY_FILE"

# Replace the first line with the correct path
sed -i "1s|^.*$|#!$PYTHON_PATH|" "$TARGET_PY_FILE"

echo "Python path updated to use: #!$PYTHON_PATH"

# Check if pip is installed
PIP_CMD="$PYTHON_CMD -m pip"

if $PIP_CMD --version &> /dev/null; then
    PIP_VERSION=$($PIP_CMD --version | awk '{print $2}')
    echo "pip is installed with version: $PIP_VERSION"
else
    echo "pip is not installed."
    exit 1
fi

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



# Source the config file
source "${CURRENT_DIR_NAME}/$monitorName.cfg" &> /dev/null

output=$("$PYTHON_PATH" "$TARGET_PY_FILE" --url "$url" --username "$username" --password "$password")

if grep -qE '"status": 0' <<< "$output"  ; then
    echo "Failed: $(grep -oP '"msg":\s*"\K[^"]+' <<< "$output")"
    exit 1
else
    echo "Success"
fi

