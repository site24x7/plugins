#!/bin/bash
set -e

for version in python python3; do
    if command -v "$version" ; then
        PYTHON_CMD=$(command -v "$version")
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "Error: Python is not installed or not available in the PATH."
    exit 1
fi

echo "Python executable found at: $PYTHON_CMD"

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")"  && pwd)
CURRENT_DIR_NAME=$(dirname "$SCRIPT_DIR")
monitorName=$(basename "$CURRENT_DIR_NAME")

TARGET_PY_FILE="${CURRENT_DIR_NAME}/$monitorName.py"

if [ ! -f "$TARGET_PY_FILE" ]; then
    echo "Error: Python script '$TARGET_PY_FILE' not found in the expected directory."
    exit 1
fi

SHEBANG_PYTHON_PATH="$PYTHON_CMD"

if [ -n "$SHEBANG_PYTHON_PATH" ]; then
    sed -i "1s|^.*$|#!$SHEBANG_PYTHON_PATH|" "$TARGET_PY_FILE"
    echo "Updated shebang in plugin to use: $SHEBANG_PYTHON_PATH"
else
    echo "Warning: Could not determine Python path for shebang update."
    exit 1
fi

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

DISPLAY_CMD="$SHEBANG_PYTHON_PATH \"$TARGET_PY_FILE\""
for ((i=0; i<${#CMD_ARGS_ARRAY[@]}; i+=2)); do
    key="${CMD_ARGS_ARRAY[i]}"
    value="${CMD_ARGS_ARRAY[i+1]}"
    DISPLAY_CMD="$DISPLAY_CMD $key '$value'"
done

# echo "Command: $DISPLAY_CMD"

if [ ${#CMD_ARGS_ARRAY[@]} -gt 0 ]; then
    OUTPUT=$("$SHEBANG_PYTHON_PATH" "$TARGET_PY_FILE" "${CMD_ARGS_ARRAY[@]}")
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
