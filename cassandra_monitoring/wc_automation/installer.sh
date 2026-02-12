#!/bin/bash
set -e

PACKAGE_REQUIRED=("jmxquery")

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
use_venv=false

for package in "${PACKAGE_REQUIRED[@]}"; do
    if ! $PYTHON_CMD -c "import $package"; then
        echo "Info: Package '$package' is not installed globally. Attempting global installation..."
        set +e
        output=$($PYTHON_CMD -m pip install "$package" 2>&1)
        exit_status=$?
        set -e
        echo "$output" | head -n 4
        if [ $exit_status -ne 0 ]; then
            echo "Global installation failed. Will use virtual environment for all packages."
            use_venv=true
            break
        else
            echo "Package '$package' installed successfully globally."
        fi
    else
        echo "Package '$package' is already available globally."
    fi
done

venv_success=false

if [ "$use_venv" = "true" ]; then
    VENV_DIR=$(dirname "$(dirname "$CURRENT_DIR_NAME")")/.plugin-venv
    VENV_RELATIVE_PATH=".plugin-venv"
    if [ ! -d "$VENV_DIR" ]; then
        echo "Attempting to create virtual environment: $VENV_RELATIVE_PATH"
        if $PYTHON_CMD -c "import venv"; then
            if $PYTHON_CMD -m venv "$VENV_DIR"; then
                echo "Virtual environment created successfully using built-in venv."
                venv_success=true
            else
                echo "Error: Failed to create virtual environment with built-in venv."
            fi
        elif command -v virtualenv && $PYTHON_CMD -c "import virtualenv"; then
            if virtualenv "$VENV_DIR"; then
                echo "Virtual environment created successfully using virtualenv."
                venv_success=true
            else
                echo "Error: Failed to create virtual environment with virtualenv."
            fi
        else
            echo "Error: Neither 'venv' module nor 'virtualenv' is available."
        fi
    else
        echo "Virtual environment already exists at: $VENV_RELATIVE_PATH"
        venv_success=true
    fi
    
    if [ "$venv_success" = "true" ]; then
        VENV_PYTHON="$VENV_DIR/bin/python"
        VENV_PIP="$VENV_DIR/bin/pip"
    fi
fi

if [ "$use_venv" = "true" ] && [ "$venv_success" = "true" ]; then
    all_packages_success=true
    for package in "${PACKAGE_REQUIRED[@]}"; do
        set +e
        output=$("$VENV_PIP" install "$package" 2>&1)
        exit_status=$?
        set -e
        echo "$output" | head -n 4
        if [ $exit_status -ne 0 ]; then
            echo "Virtual environment package '$package' installation failed with exit status $exit_status"
            all_packages_success=false
        else
            echo "Package '$package' installed successfully in virtual environment."
            if "$VENV_PYTHON" -c "import $package"; then
                echo "Package '$package' verified successfully in virtual environment."
            else
                echo "Error: Package '$package' installation verification failed in virtual environment."
                all_packages_success=false
            fi
        fi
    done
    
    if [ "$all_packages_success" = "true" ]; then
        SHEBANG_PYTHON_PATH="$VENV_PYTHON"
        echo "All packages installed and verified successfully. Will use virtual environment Python."
    else
        echo "Packages installation failed in virtual environment. Will use global Python path."
    fi
elif [ "$use_venv" = "true" ] && [ "$venv_success" = "false" ]; then
    echo "Skipping virtual environment package installation due to venv creation failure."
fi

if [ -n "$SHEBANG_PYTHON_PATH" ]; then
    sed -i "1s|^.*$|#!$SHEBANG_PYTHON_PATH|" "$TARGET_PY_FILE"
    echo "Updated shebang in plugin to use: $SHEBANG_PYTHON_PATH"
else
    echo "Warning: Could not determine Python path for shebang update."
fi