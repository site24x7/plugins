#!/bin/bash
set -e

PACKAGE_REQUIRED=("csv")

pip_check(){
    PIP_CMD="$PYTHON_CMD -m pip"
    if $PIP_CMD --version &> /dev/null; then
        PIP_VERSION=$($PIP_CMD --version | awk '{print $2}')
        echo "Pip is available with version: $PIP_VERSION"
    else
        echo "Error: Pip is not installed."
        exit 1
    fi
}

HAPROXY_CFG_LOCATIONS=(
    "/etc/haproxy/haproxy.cfg"
    "/usr/local/etc/haproxy/haproxy.cfg"
    "/opt/haproxy/haproxy.cfg"
    "/usr/local/haproxy/haproxy.cfg"
)
HAPROXY_CFG_PATH=""

for cfg in "${HAPROXY_CFG_LOCATIONS[@]}"; do
    if [ -f "$cfg" ]; then
        HAPROXY_CFG_PATH="$cfg"
        echo "Found HAProxy configuration at $HAPROXY_CFG_PATH"
        break
    fi
done

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

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
PARENT_DIR=$(dirname "$SCRIPT_DIR")
CFG_FILE=""

for cfg in "$PARENT_DIR"/*.cfg; do
    if [ -f "$cfg" ]; then
        CFG_FILE="$cfg"
        break
    fi
done

if [ -z "$CFG_FILE" ]; then
    echo "Error: Plugin configuration file (.cfg) not found in parent directory."
    exit 1
fi

echo "Found plugin configuration file: $CFG_FILE"

USERNAME=$(grep "^username" "$CFG_FILE" | sed 's/^username[[:space:]]*=[[:space:]]*//' | tr -d '"')
PASSWORD=$(grep "^password" "$CFG_FILE" | sed 's/^password[[:space:]]*=[[:space:]]*//' | tr -d '"')
URL=$(grep "^url" "$CFG_FILE" | sed 's/^url[[:space:]]*=[[:space:]]*//' | tr -d '"')

PORT="8404"
if [ -n "$URL" ] && [ "$URL" != "None" ]; then
    PORT=$(echo "$URL" | grep -oE ':[0-9]+' | cut -d':' -f2)
    if [ -z "$PORT" ]; then
        PORT="8404"
    fi
fi

if [ -n "$USERNAME" ] && [ "$USERNAME" != "None" ] && [ -n "$PASSWORD" ] && [ "$PASSWORD" != "None" ]; then
    STATS_BLOCK="
listen stats
    bind 0.0.0.0:$PORT
    mode http
    stats enable
    stats uri /stats
    stats realm Strictly\\ Private
    stats auth $USERNAME:$PASSWORD
"
else
    STATS_BLOCK="
listen stats
    bind 0.0.0.0:$PORT
    mode http
    stats enable
    stats uri /stats
    stats realm Strictly\\ Private
"
fi

if [ -z "$HAPROXY_CFG_PATH" ]; then
    echo "Warning: HAProxy configuration file not found in common locations or via process."
    echo "Skipping HAProxy configuration append."
else
    if grep -q "^listen stats" "$HAPROXY_CFG_PATH"; then
        echo "'listen stats' already exists in haproxy.cfg. Skipping append."
    else
        BACKUP_PATH="${HAPROXY_CFG_PATH}.$(date +%Y%m%d_%H%M%S).bak"
        cp "$HAPROXY_CFG_PATH" "$BACKUP_PATH"
        if [ $? -ne 0 ]; then
            echo "haproxy.cfg backup: FAIL"
            exit 1
        fi
        echo "Backup of haproxy.cfg created at $BACKUP_PATH"

        echo "Appending listen stats configuration to haproxy.cfg..."
        echo "$STATS_BLOCK" >> "$HAPROXY_CFG_PATH"
        if [ $? -ne 0 ]; then
            echo "haproxy.cfg config: FAIL (append failed)"
            exit 1
        fi

        if sudo systemctl reload haproxy 2>/dev/null; then
            echo "haproxy.cfg config added and HAProxy reloaded successfully."
        else
            echo "haproxy.cfg config addition succeeded, but HAProxy reload failed."
            exit 1
        fi
    fi
fi

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

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
CURRENT_DIR_NAME=$(dirname "$SCRIPT_DIR")
monitorName=$(basename "$CURRENT_DIR_NAME")
TARGET_PY_FILE="${CURRENT_DIR_NAME}/$monitorName.py"

if [ ! -f "$TARGET_PY_FILE" ]; then
    echo "Error: Python script '$TARGET_PY_FILE' not found in the expected directory."
    exit 1
fi

sed -i "1s|^.*$|#!$PYTHON_PATH|" "$TARGET_PY_FILE"

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
