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

USERNAME=$(grep "^username" "$CFG_FILE" | sed 's/^username[[:space:]]*=[[:space:]]*//' | tr -d '"'"'"'')
PASSWORD=$(grep "^password" "$CFG_FILE" | sed 's/^password[[:space:]]*=[[:space:]]*//' | tr -d '"'"'"'')
URL=$(grep "^url" "$CFG_FILE" | sed 's/^url[[:space:]]*=[[:space:]]*//' | tr -d '"'"'"'')

PORT="8404"
STATS_PATH="/stats"
if [ -n "$URL" ] && [ "$URL" != "None" ]; then
    PORT=$(echo "$URL" | grep -oE ':[0-9]+' | cut -d':' -f2)
    if [ -z "$PORT" ]; then
        PORT="8404"
    fi
    
    STATS_PATH=$(echo "$URL" | sed 's|^[^/]*//[^/]*||' | sed 's|;.*$||')
    if [ -z "$STATS_PATH" ] || [ "$STATS_PATH" = "/" ]; then
        STATS_PATH="/stats"
    fi
fi

if [ -n "$USERNAME" ] && [ "$USERNAME" != "None" ] && [ -n "$PASSWORD" ] && [ "$PASSWORD" != "None" ]; then
    STATS_BLOCK="
listen stats
    bind 0.0.0.0:$PORT
    mode http
    stats enable
    stats uri $STATS_PATH
    stats realm Strictly\\ Private
    stats auth $USERNAME:$PASSWORD
"
else
    STATS_BLOCK="
listen stats
    bind 0.0.0.0:$PORT
    mode http
    stats enable
    stats uri $STATS_PATH
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
        fi
        echo "Backup of haproxy.cfg created at $BACKUP_PATH"

        echo "Appending listen stats configuration to haproxy.cfg..."
        echo "$STATS_BLOCK" >> "$HAPROXY_CFG_PATH"
        if [ $? -ne 0 ]; then
            echo "haproxy.cfg config: FAIL (append failed)"
        fi

        if sudo systemctl reload haproxy 2>/dev/null; then
            echo "haproxy.cfg config added and HAProxy reloaded successfully."
        else
            echo "haproxy.cfg config addition succeeded, but HAProxy reload failed."
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

if [ -n "$PYTHON_PATH" ]; then
    sed -i "1s|^.*$|#!$PYTHON_PATH|" "$TARGET_PY_FILE"
    echo "Updated shebang in $TARGET_PY_FILE with Python path: $PYTHON_PATH"
else
    echo "Warning: Python path not available, skipping shebang update."
fi

for package in "${PACKAGE_REQUIRED[@]}"; do
    if ! $PYTHON_CMD -c "import $package" &> /dev/null; then
        echo "Info: Package '$package' is not installed. Attempting installation..."
        pip_check
        if $PIP_CMD install "$package" &> /dev/null; then
            echo "Package '$package' installed successfully."
        else
            echo "Error: Failed to install the package '$package'."
        fi
    else
        echo "Package '$package' is already installed."
    fi
done

check_value(){
    value=$1
    
    execution_pattern='\$\([^)]*\)|`[^`]*`|<\([^)]*\)|>\([^)]*\)|;\([^)]*\)|\|\|\([^)]*\)|&&\([^)]*\)'
    if [[ "$value" =~ $execution_pattern ]]; then
        echo "ERROR: Command execution pattern detected in value: '$value'"
        exit 1
    fi
}

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
    elif [[ "$value" =~ ^\'.*\'$ ]]; then
        value="${value#\'}"
        value="${value%\'}"   
    fi
    
    check_value "$value"
    
    config["$key"]="$value"
done < "$CONFIG_FILE"

declare -a CMD_ARGS_ARRAY

for key in "${!config[@]}"; do
    value="${config[$key]}"
    CMD_ARGS_ARRAY+=("--$key")
    CMD_ARGS_ARRAY+=("$value")
done

echo "Executing monitoring script..."

DISPLAY_CMD="$PYTHON_PATH \"$TARGET_PY_FILE\""
for ((i=0; i<${#CMD_ARGS_ARRAY[@]}; i+=2)); do
    key="${CMD_ARGS_ARRAY[i]}"
    value="${CMD_ARGS_ARRAY[i+1]}"
    DISPLAY_CMD="$DISPLAY_CMD $key '$value'"
done

# echo "Command: $DISPLAY_CMD"

if [ ${#CMD_ARGS_ARRAY[@]} -gt 0 ]; then
    OUTPUT=$("$PYTHON_PATH" "$TARGET_PY_FILE" "${CMD_ARGS_ARRAY[@]}")
fi

# echo "$OUTPUT"

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

echo "Monitoring script execution completed."
