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

pymysql_zip="$CURRENT_DIR_NAME/pymysql/pymysql.zip"
# Check if the file exists
if [ ! -f $pymysql_zip ]; then
    echo "Python file '$pymysql_zip' not found in the current directory."
    exit 1
fi

unzip $pymysql_zip -d $CURRENT_DIR_NAME && rm $pymysql_zip

# Source the config file
source "${CURRENT_DIR_NAME}/$monitorName.cfg" &> /dev/null

echo "port: $port"

output=$("$PYTHON_PATH" "$TARGET_PY_FILE" --host "$host" --port "$port" --username "$username" --password "$password")

if grep -qE '"status": 0' <<< "$output"  ; then
    echo "Failed: $(grep -oP '"msg"\s*:\s*"\K(\\.|[^"\\])*' <<< "$output")"
    exit 1
else
    echo "Success"
fi