#!/bin/bash
set -e


pip_check(){
# Check if pip is installed
PIP_CMD="$PYTHON_CMD -m pip"

if $PIP_CMD --version &> /dev/null; then
    PIP_VERSION=$($PIP_CMD --version | awk '{print $2}')
    echo "Pip is available with version: $PIP_VERSION"
else
    echo "Error: Pip is not installed."
    exit 1
fi
}

Install_pakages(){

    deb_packages=("libpq-dev" "python3-dev" "gcc")
    redhat_packages=("postgresql-libs" "postgresql-devel" "python3-devel" "gcc")
    if [[ -f /etc/debian_version ]] ; then
        packages=("${deb_packages[@]}")
        command="apt install -y"
    elif [[ -f /etc/redhat-release ]] ; then
        packages=("${redhat_packages[@]}")
        command="yum install -y"

    fi
    
    echo "The psycopg2 module along with the following packages will installed."
    echo ${packages[@]}

    echo "Installing missing packages: ${install_packages[@]}"
    if $command "${install_packages[@]}" &> /dev/null; then
        echo "Dependencies were installed successfully."
    else
        echo "Error: Failed to install the dependency packages."
        exit 1
    fi


}
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
CURRENT_DIR_NAME=$(dirname "$SCRIPT_DIR")
monitorName=$(basename "$CURRENT_DIR_NAME")
TARGET_PY_FILE="${CURRENT_DIR_NAME}/$monitorName.py"

# Check if the Python file exists
if [ ! -f "$TARGET_PY_FILE" ]; then
    echo "Error: Python script '$TARGET_PY_FILE' not found in the expected directory."
    exit 1
fi

# Add Python shebang line to the top of the Python file
sed -i "1s|^.*$|#!$PYTHON_PATH|" "$TARGET_PY_FILE"


package="psycopg2-binary"

if ! $PYTHON_CMD -c "import psycopg2" &> /dev/null; then
    echo "Info: Package 'psycopg2' is not installed. Attempting installation..."
    pip_check
    Install_pakages
    if $PIP_CMD install "$package" &> /dev/null; then
        echo "Package '$package' installed successfully."
    else
        echo "Error: Failed to install the package '$package'."
        exit 1
    fi
else
    echo "Package '$package' is already installed."
fi

