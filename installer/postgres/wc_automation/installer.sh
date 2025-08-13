#!/bin/bash
set -e

PACKAGE_REQUIRED=("psycopg2-binary")

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

VENV_DIR=$(dirname "$CURRENT_DIR_NAME")/.plugin-venv
PLUGINS_DIR=$(dirname "$CURRENT_DIR_NAME")

if [ "$(basename "$PLUGINS_DIR")" != "plugins" ]; then
    echo "Error: plugins directory is not found"
    exit 1
fi

VENV_RELATIVE_PATH="plugins/.plugin-venv"

USE_VENV=false

if [ -d "$VENV_DIR" ]; then
    echo "Virtual environment found at: $VENV_RELATIVE_PATH"
    VENV_PYTHON="$VENV_DIR/bin/python"
    VENV_PIP="$VENV_DIR/bin/pip"
    
    if [ -f "$VENV_PYTHON" ] && [ -f "$VENV_PIP" ]; then
        PYTHON_PATH="$VENV_PYTHON"
        PIP_CMD="$VENV_PIP"
        USE_VENV=true
        echo "Using existing virtual environment Python: $VENV_RELATIVE_PATH/bin/python"
    else
        echo "Warning: Virtual environment exists but Python/pip not found."
    fi
fi

if [ "$USE_VENV" = false ]; then
    echo "Attempting to create virtual environment at: $VENV_RELATIVE_PATH"
    if $PYTHON_CMD -m venv "$VENV_DIR" &>/dev/null; then
        echo "Virtual environment created successfully."
        VENV_PYTHON="$VENV_DIR/bin/python"
        VENV_PIP="$VENV_DIR/bin/pip"
        
        if [ -f "$VENV_PYTHON" ] && [ -f "$VENV_PIP" ]; then
            PYTHON_PATH="$VENV_PYTHON"
            PIP_CMD="$VENV_PIP"
            USE_VENV=true
            echo "Using newly created virtual environment Python: $VENV_RELATIVE_PATH/bin/python"
        else
            echo "Warning: Virtual environment created but Python/pip not found."
        fi
    else
        echo "Warning: Failed to create virtual environment. Falling back to global Python installation."
    fi
fi

if [ "$USE_VENV" = false ]; then
    echo "Using global Python installation."
    PYTHON_PATH=$(command -v "$PYTHON_CMD")
    PIP_CMD="$PYTHON_CMD -m pip"
fi

TARGET_PY_FILE="${CURRENT_DIR_NAME}/$monitorName.py"

if [ ! -f "$TARGET_PY_FILE" ]; then
    echo "Error: Python script '$TARGET_PY_FILE' not found in the expected directory."
    exit 1
fi

sed -i "1s|^.*$|#!$PYTHON_PATH|" "$TARGET_PY_FILE"

if [ "$USE_VENV" = true ]; then
    if $PIP_CMD --version &> /dev/null; then
        PIP_VERSION=$($PIP_CMD --version | awk '{print $2}')
        echo "Pip is available in virtual environment with version: $PIP_VERSION"
    else
        echo "Error: Pip is not available in virtual environment."
        exit 1
    fi
else
    PIP_CMD="$PYTHON_CMD -m pip"
    if $PIP_CMD --version &> /dev/null; then
        PIP_VERSION=$($PIP_CMD --version | awk '{print $2}')
        echo "Pip is available with version: $PIP_VERSION"
    else
        echo "Error: Pip is not installed."
        exit 1
    fi
fi


for package in "${PACKAGE_REQUIRED[@]}"; do
    if [ "$USE_VENV" = true ]; then
        if ! "$PYTHON_PATH" -c "import $package" &> /dev/null; then
            echo "Info: Package '$package' is not installed in virtual environment. Attempting installation..."
            if $PIP_CMD install "$package" &> /dev/null; then
                echo "Package '$package' installed successfully in virtual environment."
                if "$PYTHON_PATH" -c "import $package" &> /dev/null; then
                    echo "Package '$package' verified successfully in virtual environment."
                else
                    echo "Error: Package '$package' installation verification failed in virtual environment."
                    exit 1
                fi
            else
                echo "Error: Failed to install the package '$package' in virtual environment."
                exit 1
            fi
        else
            echo "Package '$package' is already installed in virtual environment."
        fi
    else
        if ! $PYTHON_CMD -c "import $package" &> /dev/null; then
            echo "Info: Package '$package' is not installed. Attempting installation..."
            if $PIP_CMD install "$package" &> /dev/null; then
                echo "Package '$package' installed successfully."
                if $PYTHON_CMD -c "import $package" &> /dev/null; then
                    echo "Package '$package' verified successfully."
                else
                    echo "Error: Package '$package' installation verification failed."
                    exit 1
                fi
            else
                echo "Error: Failed to install the package '$package'."
                exit 1
            fi
        else
            echo "Package '$package' is already installed."
        fi
    fi
done
