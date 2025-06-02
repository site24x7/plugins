#!/bin/bash
set -e

PACKAGE_REQUIRED=("redis")

CONFIGURATION_REQUIRED=("host" "port" "password")

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

# Check if the configuration file exists
CONFIG_FILE="${CURRENT_DIR_NAME}/$monitorName.cfg"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file '$CONFIG_FILE' not found."
    exit 1
fi
source "${CURRENT_DIR_NAME}/$monitorName.cfg" &> /dev/null || :

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