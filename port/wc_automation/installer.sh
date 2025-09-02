#!/bin/bash
set -e

PACKAGE_REQUIRED=("psutil")

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

SHEBANG_PYTHON_PATH=""

for package in "${PACKAGE_REQUIRED[@]}"; do
    if $PYTHON_CMD -c "import $package" ; then
        echo "Package '$package' is already installed globally."
        SHEBANG_PYTHON_PATH=$(command -v "$PYTHON_CMD")
    else
        echo "Info: Package '$package' is not installed globally. Attempting global installation..."
        
        set +e
        output=$($PYTHON_CMD -m pip install "$package" 2>&1)
        exit_status=$?
        set -e
        
        echo "$output" | head -n 4
        
        if [ $exit_status -eq 0 ]; then
            echo "Package '$package' installed successfully globally."
            if $PYTHON_CMD -c "import $package" ; then
                echo "Package '$package' verified successfully globally."
                SHEBANG_PYTHON_PATH=$(command -v "$PYTHON_CMD")
            else
                echo "Error: Package '$package' installation verification failed globally."
                exit 1
            fi
        else
            echo "Global installation failed with exit status $exit_status"
            echo "Warning: Failed to install the package '$package' globally. Will try in virtual environment."
            VENV_DIR=$(dirname "$(dirname "$CURRENT_DIR_NAME")")/.plugin-venv
            VENV_RELATIVE_PATH=".plugin-venv"
            if [ ! -d "$VENV_DIR" ]; then
                echo "Attempting to create virtual environment: $VENV_RELATIVE_PATH"
                if $PYTHON_CMD -c "import venv"; then
                    if $PYTHON_CMD -m venv "$VENV_DIR"; then
                        echo "Virtual environment created successfully using built-in venv."
                    else
                        echo "Error: Failed to create virtual environment with built-in venv."
                        exit 1
                    fi
                elif command -v virtualenv && python3 -c "import virtualenv"; then
                    if virtualenv "$VENV_DIR"; then
                        echo "Virtual environment created successfully using virtualenv."
                    else
                        echo "Error: Failed to create virtual environment with virtualenv."
                        exit 1
                    fi
                else
                    echo "Error: Neither 'venv' module nor 'virtualenv' is available."
                    exit 1
                fi
            fi
            VENV_PYTHON="$VENV_DIR/bin/python"
            VENV_PIP="$VENV_DIR/bin/pip"
            if [ -f "$VENV_PYTHON" ] && [ -f "$VENV_PIP" ]; then
                set +e
                output=$("$VENV_PIP" install "$package" 2>&1)
                exit_status=$?
                set -e
                
                echo "$output" | head -n 4
                
                if [ $exit_status -ne 0 ]; then
                    echo "Virtual environment installation failed with exit status $exit_status"
                    exit 1
                else
                    echo "Package '$package' installed successfully in virtual environment."
                    if "$VENV_PYTHON" -c "import $package" ; then
                        echo "Package '$package' verified successfully in virtual environment."
                        SHEBANG_PYTHON_PATH="$VENV_PYTHON"
                    else
                        echo "Error: Package '$package' installation verification failed in virtual environment."
                        exit 1
                    fi
                fi
            else
                echo "Error: Virtual environment Python/pip not found."
                exit 1
            fi
        fi
    fi
done

if [ -n "$SHEBANG_PYTHON_PATH" ]; then
    sed -i "1s|^.*$|#!$SHEBANG_PYTHON_PATH|" "$TARGET_PY_FILE"
    echo "Updated shebang in plugin to use: $SHEBANG_PYTHON_PATH"
else
    echo "Warning: Could not determine Python path for shebang update."
fi