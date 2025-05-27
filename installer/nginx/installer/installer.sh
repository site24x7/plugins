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

# Check if urllib is available (standard library)
if $PYTHON_CMD -c "import urllib.request" &> /dev/null; then
    echo "urllib is available."
else
    echo "urllib is not available."
    exit 1
fi

# === Insert stub_status block into nginx.conf ===
stub_status_block=" 
    location /nginx_status {
        stub_status on;
        allow 127.0.0.1;
    }"

insert_stub_status() {
    nginx_conf="/etc/nginx/nginx.conf"

    if [ ! -f "$nginx_conf" ]; then
        echo "stub_status config added: FAIL (nginx.conf not found)"
        return 1
    fi

    if grep -q "stub_status on;" "$nginx_conf"; then
        echo "stub_status config: already exists"
        return 0
    fi

    line_no=$(awk '/^[^#]*server_name[[:space:]]/ {print NR; exit}' "$nginx_conf")
    if [ -z "$line_no" ]; then
        echo "stub_status config added: FAIL (server_name not found)"
        return 1
    fi

    cp "$nginx_conf" "$nginx_conf.bak.$(date +%Y%m%d%H%M%S)"

    awk -v insert_line="$line_no" -v content="$stub_status_block" '
    NR == insert_line {
        print $0
        print content
        next
    }
    { print $0 }' "$nginx_conf" > "$nginx_conf.tmp" && mv "$nginx_conf.tmp" "$nginx_conf"

    if [ $? -ne 0 ]; then
        echo "stub_status config added: FAIL (insertion failed)"
        return 1
    fi

    if systemctl reload nginx 2>/dev/null; then
        echo "stub_status config added successfully."
    else
        echo "stub_status config addition failed."
        return 1
    fi
}

# Call insertion function (non-interactive)
insert_stub_status


# === Execute Python Plugin ===
source "${CURRENT_DIR_NAME}/$monitorName.cfg" &> /dev/null

output=$("$PYTHON_PATH" "$TARGET_PY_FILE" --nginx_status_url "$nginx_status_url" --username "$username" --password "$password")

if grep -qE '"status": 0' <<< "$output"; then
    echo "Failed: $(grep -oP '"msg":\s*"\K[^"]+' <<< "$output")"
    exit 1
else
    echo "Success"
fi
