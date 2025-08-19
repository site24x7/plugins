#!/bin/bash
set -e

PACKAGE_REQUIRED=("pandas")

pip_check(){
# Check if pip is installed
PIP_CMD="$PYTHON_CMD -m pip"

if $PIP_CMD --version &> /dev/null; then
    PIP_VERSION=$($PIP_CMD --version | awk '{print $2}')
    echo "Pip is available with version: $PIP_VERSION"
else
    echo "Error: Pip is not installed."
    exit 1
fi
}

# List of common haproxy.cfg locations
HAPROXY_CFG_LOCATIONS=(
    "/etc/haproxy/haproxy.cfg"
    "/usr/local/etc/haproxy/haproxy.cfg"
    "/opt/haproxy/haproxy.cfg"
    "/usr/local/haproxy/haproxy.cfg"
)

HAPROXY_CFG_PATH=""

# 1. Search for haproxy.cfg in common locations
for cfg in "${HAPROXY_CFG_LOCATIONS[@]}"; do
    if [ -f "$cfg" ]; then
        HAPROXY_CFG_PATH="$cfg"
        echo "Found HAProxy configuration at $HAPROXY_CFG_PATH"
        break
    fi
done

# 2. If not found, try to get the config path from the running haproxy process
if [ -z "$HAPROXY_CFG_PATH" ]; then
    HAPROXY_PID=$(pgrep haproxy | head -n 1)
    if [ -n "$HAPROXY_PID" ]; then
        HAPROXY_CMD=$(ps -p "$HAPROXY_PID" -o args=)
        CFG_FROM_PROC=$(echo "$HAPROXY_CMD" | grep -oE -- '-f[ ]*[^ ]+' | awk '{print $2}')
        if [ -n "$CFG_FROM_PROC" ] && [ -f "$CFG_FROM_PROC" ]; then
            HAPROXY_CFG_PATH="$CFG_FROM_PROC"
            echo "Found HAProxy configuration from process at $HAPROXY_CFG_PATH"
        fi
    fi
fi

# 3. Final check and append configuration
if [ -z "$HAPROXY_CFG_PATH" ]; then
    echo "Warning: HAProxy configuration file not found in common locations or via process."
    echo "Skipping HAProxy configuration append."
else
    # Take a backup with date and time before making changes
    BACKUP_PATH="${HAPROXY_CFG_PATH}.$(date +%Y%m%d_%H%M%S).bak"
    cp "$HAPROXY_CFG_PATH" "$BACKUP_PATH"
    # Check if the config already contains 'frontend http_front'
    if grep -q "^frontend http_front" "$HAPROXY_CFG_PATH"; then
        echo "'frontend http_front' already exists in haproxy.cfg. Skipping append."
    else
        echo "Appending frontend configuration to haproxy.cfg..."
        cat <<EOF >> "$HAPROXY_CFG_PATH"

frontend http_front
    bind *:80
    default_backend http_back

EOF
        echo "Configuration appended successfully."
    fi
fi

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

# Check if required packages are installed
for package in "${PACKAGE_REQUIRED[@]}"; do
    if ! $PYTHON_CMD -c "import $package" &> /dev/null; then
        echo "Info: Package '$package' is not installed. Attempting installation..."
        pip_check
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
