#!/bin/bash
set -e

PACKAGE_REQUIRED=("psycopg2-binary")
PACKAGE_IMPORT_NAMES=("psycopg2")

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

SHEBANG_PYTHON_PATH=""
PIP_CMD="$PYTHON_CMD -m pip"

for i in "${!PACKAGE_REQUIRED[@]}"; do
    package="${PACKAGE_REQUIRED[$i]}"
    import_name="${PACKAGE_IMPORT_NAMES[$i]}"
    if $PYTHON_CMD -c "import $import_name" &> /dev/null; then
        echo "Package '$package' is already installed globally."
        SHEBANG_PYTHON_PATH=$(command -v "$PYTHON_CMD")
    else
        echo "Info: Package '$package' is not installed globally. Attempting global installation..."
        if $PYTHON_CMD -m pip install "$package" &> /dev/null; then
            echo "Package '$package' installed successfully globally."
            if $PYTHON_CMD -c "import $import_name" &> /dev/null; then
                echo "Package '$package' verified successfully globally."
                SHEBANG_PYTHON_PATH=$(command -v "$PYTHON_CMD")
            else
                echo "Error: Package '$package' installation verification failed globally."
                exit 1
            fi
        else
            echo "Warning: Failed to install the package '$package' globally. Will try in virtual environment."
            VENV_DIR=$(dirname "$(dirname "$CURRENT_DIR_NAME")")/.plugin-venv
            VENV_RELATIVE_PATH="../.plugin-venv"
            if [ ! -d "$VENV_DIR" ]; then
                echo "Attempting to create virtual environment at: $VENV_RELATIVE_PATH"
                if $PYTHON_CMD -m venv "$VENV_DIR" &>/dev/null; then
                    echo "Virtual environment created successfully."
                else
                    echo "Warning: Failed to create virtual environment."
                    exit 1
                fi
            fi
            VENV_PYTHON="$VENV_DIR/bin/python"
            VENV_PIP="$VENV_DIR/bin/pip"
            if [ -f "$VENV_PYTHON" ] && [ -f "$VENV_PIP" ]; then
                if "$VENV_PIP" install "$package" &> /dev/null; then
                    echo "Package '$package' installed successfully in virtual environment."
                    if "$VENV_PYTHON" -c "import $import_name" &> /dev/null; then
                        echo "Package '$package' verified successfully in virtual environment."
                        SHEBANG_PYTHON_PATH="$VENV_PYTHON"
                    else
                        echo "Error: Package '$package' installation verification failed in virtual environment."
                        exit 1
                    fi
                else
                    echo "Error: Failed to install the package '$package' in virtual environment."
                    exit 1
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
