#!/bin/bash

TEMP_DIR="/opt/site24x7/monagent/temp"
PLUGIN_DIR="/opt/site24x7/monagent/plugins"
ZIP_URL="https://staticdownloads.site24x7.com/plugins/internet_speed_check.zip"
ZIP_FILE="$TEMP_DIR/internet_speed_check.zip"
EXTRACT_DIR="$TEMP_DIR/internet_speed_check"

mkdir -p "$TEMP_DIR"

if PYTHON_PATH=$(command -v python3); then
    true
elif PYTHON_PATH=$(command -v python2); then
    true
elif PYTHON_PATH=$(command -v python); then
    true
else
    echo "Python path not found"
    exit 1
fi

wget -q -O "$ZIP_FILE" "$ZIP_URL"

if [ $? -ne 0 ]; then
    echo "Plugin zip file download failed!"
    exit 1
fi

unzip -q -o "$ZIP_FILE" -d "$TEMP_DIR"

if [ $? -ne 0 ]; then
    echo "Extraction failed!"
    exit 1
fi

TARGET_PYTHON_FILE="$EXTRACT_DIR/internet_speed_check.py"

if [ -f "$TARGET_PYTHON_FILE" ]; then
    sed -i "1s|.*|#!$PYTHON_PATH|" "$TARGET_PYTHON_FILE"
else
    echo "Error: $TARGET_PYTHON_FILE not found!"
    exit 1
fi

if [ -d "$PLUGIN_DIR/internet_speed_check" ]; then
    rm -rf "$PLUGIN_DIR/internet_speed_check"
fi

mv "$EXTRACT_DIR" "$PLUGIN_DIR"

if [ $? -eq 0 ]; then
    rm -f "$ZIP_FILE"
else
    echo "Plugin folder move failed!"
    exit 1
fi

echo "Installation completed successfully!"
