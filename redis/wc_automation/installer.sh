#!/bin/bash
set -e

for version in python3 python; do
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

sed -i "1s|^.*$|#!$PYTHON_CMD|" "$TARGET_PY_FILE"
echo "Updated shebang in plugin to use: $PYTHON_CMD"
