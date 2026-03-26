#!/bin/bash
set -e

check_value(){
    value=$1
    
    execution_pattern='\$\([^)]*\)|`[^`]*`|<\([^)]*\)|>\([^)]*\)|;\([^)]*\)|\|\|\([^)]*\)|&&\([^)]*\)'
    if [[ "$value" =~ $execution_pattern ]]; then
        echo "ERROR: Command execution pattern detected in value: '$value'"
        exit 1
    fi
}

for version in python3 python; do
    if command -v "$version" &> /dev/null; then
        PYTHON_CMD=$version
        break
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo "Error: Python is not installed or not available in the PATH."
fi

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" &> /dev/null && pwd)
CURRENT_DIR_NAME=$(dirname "$SCRIPT_DIR")
monitorName=$(basename "$CURRENT_DIR_NAME")

TARGET_PY_FILE="${CURRENT_DIR_NAME}/$monitorName.py"

if [ ! -f "$TARGET_PY_FILE" ]; then
    echo "Error: Python script '$TARGET_PY_FILE' not found in the expected directory."
    exit 1
fi

if [ -n "$PYTHON_CMD" ]; then
    PYTHON_PATH=$(command -v "$PYTHON_CMD")
    echo "Python executable found at: $PYTHON_PATH"
    sed -i "1s|^.*$|#!$PYTHON_PATH|" "$TARGET_PY_FILE"
fi

declare -A config

CONFIG_FILE="${CURRENT_DIR_NAME}/$monitorName.cfg"
if [ ! -f "$CONFIG_FILE" ]; then
    echo "Error: Configuration file '$CONFIG_FILE' not found."
    exit 1
fi

while IFS='=' read -r key value || [ -n "$key" ]; do
    key="${key#"${key%%[![:space:]]*}"}"   
    key="${key%"${key##*[![:space:]]}"}"   
    value="${value#"${value%%[![:space:]]*}"}"   
    value="${value%"${value##*[![:space:]]}"}" 
    
    [[ "$key" =~ ^#.*$ || -z "$key" || "$key" == \[*\] ]] && continue
    
    if [[ "$value" =~ ^\".*\"$ ]]; then
        value="${value#\"}"   
        value="${value%\"}"   
    elif [[ "$value" =~ ^\'.*\'$ ]]; then
        value="${value#\'}"
        value="${value%\'}"   
    fi
    
    # replacing for single quotes    
    value="${value//\'\\\'\'/\'}"
    
    check_value "$value"
    
    config["$key"]="$value"
done < "$CONFIG_FILE"

if $PYTHON_PATH -c "import urllib.request" &> /dev/null; then
    echo "urllib is available."
else
    echo "urllib is not available."
fi


echo "Checking Tomcat Manager API accessibility."

TOMCAT_HOST="${config[host]}"
TOMCAT_PORT="${config[port]}"
TOMCAT_PROTOCOL="${config[protocol]}"
TOMCAT_URL="/manager"
TOMCAT_USERNAME="${config[username]}"
TOMCAT_PASSWORD="${config[password]}"
TOMCAT_VERIFY_SSL="${config[verify_ssl]}"

MANAGER_API_URL="${TOMCAT_PROTOCOL}://${TOMCAT_HOST}:${TOMCAT_PORT}${TOMCAT_URL}/text/serverinfo"

if [[ "$TOMCAT_PROTOCOL" == "https" && "$TOMCAT_VERIFY_SSL" == "false" ]]; then
    CURL_SSL_OPTS="--insecure"
else
    CURL_SSL_OPTS=""
fi

HTTP_RESPONSE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 --max-time 3  \
    -u "${TOMCAT_USERNAME}:${TOMCAT_PASSWORD}" \
    $CURL_SSL_OPTS \
    "${MANAGER_API_URL}" 2>/dev/null) || HTTP_RESPONSE="000"

if [ "$HTTP_RESPONSE" == "200" ]; then
    echo "Manager API is accessible."
elif [ "$HTTP_RESPONSE" == "404" ]; then
    echo "ERROR: Manager API is not accessible. The API response is 404."
    exit 1
elif [ "$HTTP_RESPONSE" == "401" ] || [ "$HTTP_RESPONSE" == "403" ]; then
    echo "ERROR: Manager API authentication failed. The API response is $HTTP_RESPONSE."
    
    TOMCAT_SERVICE=$(systemctl list-units 'tomcat*.service' --type=service --all --no-legend 2>/dev/null | awk '{print $1}' | sed 's/.service$//' | head -1)
    
    if [ -z "$TOMCAT_SERVICE" ]; then
        echo "No Tomcat systemd service found."
        exit 1
    fi
    
    echo "Found Tomcat service: ${TOMCAT_SERVICE}"
    
    echo "Locating tomcat-users.xml file."
    CATALINA_INFO=$(systemctl show "${TOMCAT_SERVICE}" 2>/dev/null | grep -i "ReadWritePaths=")
    
    if [ -z "$CATALINA_INFO" ]; then
        echo "ERROR: Could not get ReadWritePaths from systemctl"
        exit 1
    fi
    
    CATALINA_DIR=$(echo "$CATALINA_INFO" | grep -oP '/[^ ]*Catalina' | head -1)
    
    if [ -z "$CATALINA_DIR" ]; then
        echo "ERROR: Could not find Catalina directory from ReadWritePaths"
        exit 1
    fi
    
    TOMCAT_CONF_DIR=$(dirname "$CATALINA_DIR")
    TOMCAT_USERS_XML="${TOMCAT_CONF_DIR}/tomcat-users.xml"
    
    if [ ! -f "$TOMCAT_USERS_XML" ]; then
        echo "ERROR: tomcat-users.xml file not found at ${TOMCAT_USERS_XML}"
        exit 1
    fi
    
    echo "Found tomcat-users.xml at: $TOMCAT_USERS_XML"
    
    # Check if user exists in uncommented lines (remove both multi-line and single-line comments)
    if sed -e '/<!--.*-->/d' -e '/<!--/,/-->/d' "$TOMCAT_USERS_XML" | grep -q "username=\"${TOMCAT_USERNAME}\""; then
        echo "User '${TOMCAT_USERNAME}' already exists in tomcat-users.xml"
        echo "Please verify if the password and roles are correct"
        exit 1
    fi
    
    echo "Adding user configuration to tomcat-users.xml."
    sed -i "/<\/tomcat-users>/i \  <user username=\"${TOMCAT_USERNAME}\" password=\"${TOMCAT_PASSWORD}\" roles=\"manager-gui,manager-script\"/>" "$TOMCAT_USERS_XML"
    
    echo "User '${TOMCAT_USERNAME}' added successfully with respective credentials."
    echo "Restarting Tomcat service."
    systemctl restart "${TOMCAT_SERVICE}"
      

elif [ "$HTTP_RESPONSE" == "000" ]; then
    echo "ERROR: Manager API is not accessible. Connection failed."
    if [ "$TOMCAT_PROTOCOL" == "https" ] && [ "$TOMCAT_VERIFY_SSL" == "true" ]; then
        echo "This is likely an SSL certificate verification failure."
        echo "For self-signed certificates, set verify_ssl = \"false\" "
    else
        echo "Please check if:"
        echo "  - Manager API is accessible (install tomcat-admin package if needed)"
        echo "  - Tomcat service is running"
    fi
    exit 1
else
    echo "ERROR: Manager API returned response code: $HTTP_RESPONSE"
    exit 1
fi


echo "Tomcat monitoring script execution completed."
