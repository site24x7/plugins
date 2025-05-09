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
CURRENT_DIR_NAME=$(basename "$PWD")
TARGET_PY_FILE="${CURRENT_DIR_NAME}.py"

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

# Check if psutil is installed
if ! $PYTHON_CMD -c "import psutil" &> /dev/null; then
    echo "psutil is not installed. Installing..."
    if $PIP_CMD install psutil --break-system-packages &> /dev/null; then
        echo "psutil installed successfully."
    else
        echo "Failed to install psutil."
        exit 1
    fi
else
    echo "psutil is already installed."
fi
