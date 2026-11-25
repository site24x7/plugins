#!/bin/bash
# Installs or upgrades the Site24x7 PostgreSQL plugin (version 2) for the Site24x7 Linux agent.
#
# Upgrading keeps the existing postgres.cfg (all monitors and their encrypted
# credentials) and the plugin's state; only postgres.py and the README are replaced.
#
# Usage: bash Site24x7PostgresPluginInstaller.sh [--from-dir DIR]
#   --from-dir DIR   install postgres.py, postgres.cfg and README.md from a local
#                    folder instead of downloading them (offline / air-gapped hosts)

func_exit() {
    tput sgr0 2>/dev/null
    exit 0
}
trap func_exit SIGINT SIGTSTP

plugin=postgres
agent_dir=/opt/site24x7/monagent
agent_path_change=false
base_url="https://raw.githubusercontent.com/site24x7/plugins/master/$plugin"
from_dir=""
mode="install"          # install | upgrade

if [ "$1" = "--from-dir" ] && [ -n "$2" ]; then
    from_dir="$2"
fi

color() { tput setaf "$1" 2>/dev/null; }
reset() { tput sgr0 2>/dev/null; }

error_handler() {
    if [ "$1" -ne 0 ]; then
        color 1
        echo "------------Error Occurred------------"
        echo "$2"
        reset
        echo "------------Process Exited------------"
        exit 1
    fi
}

agent_check() {
    for i in 0 1 2; do
        if [ -x "$agent_dir/bin/monagent" ] && "$agent_dir/bin/monagent" status 2>/dev/null | grep -Eq "Site24x7 (monitoring|full-stack) agent service"; then
            return
        fi
        agent_path_change=true
        color 3
        [ "$i" -eq 0 ] && echo "The Site24x7 Linux agent was not found in $agent_dir."
        read -r -p "Enter the directory where the Site24x7 Linux agent is installed: " agent_dir
        reset
    done
    echo "The Site24x7 Linux agent is required. Install it and run this installer again."
    exit 1
}

prerequisites() {
    color 3; echo "------------Prerequisites------------"; reset
    echo
    echo "  1. Python 3.6 or later on this server."
    echo "  2. A PostgreSQL user for monitoring with the $(tput bold 2>/dev/null)pg_monitor$(reset) role, on every node of the cluster with the same password:"
    echo "       CREATE USER site24x7 WITH PASSWORD '<password>';"
    echo "       GRANT pg_monitor TO site24x7;"
    echo "  3. A pg_hba.conf entry that lets this user connect from this server."
    echo
    color 3; read -r -p "Continue with the installation? (y or n): " ans; reset
    if [ -n "$ans" ] && [ "$ans" != "y" ] && [ "$ans" != "Y" ]; then
        echo "Process exited."
        exit 0
    fi
}

fetch() {
    # fetch <file> <destination-dir>
    if [ -n "$from_dir" ]; then
        cp "$from_dir/$1" "$2/$1"
        error_handler $? "Could not copy $from_dir/$1"
    elif command -v wget >/dev/null 2>&1; then
        wget -q -O "$2/$1" "$base_url/$1"
        error_handler $? "Could not download $base_url/$1"
    else
        curl -fsSL -o "$2/$1" "$base_url/$1"
        error_handler $? "Could not download $base_url/$1"
    fi
    echo "  $1"
}

check_existing() {
    if [ -f "$plugin_dir/$plugin/$plugin.cfg" ]; then
        echo "The $plugin plugin is already installed in $plugin_dir/$plugin."
        color 3
        read -r -p "Upgrade it and keep the existing configuration and monitors? (y or n): " ans
        reset
        if [ -z "$ans" ] || [ "$ans" = "y" ] || [ "$ans" = "Y" ]; then
            mode="upgrade"
        else
            echo "Process exited. Nothing was changed."
            exit 0
        fi
    fi
}

download() {
    color 3; echo; echo "------------Getting the plugin files------------"; reset
    rm -rf "$temp_dir"
    mkdir -p "$temp_dir"
    error_handler $? "Could not create $temp_dir"
    fetch "$plugin.py" "$temp_dir"
    fetch "README.md" "$temp_dir"
    if [ "$mode" = "install" ]; then
        fetch "$plugin.cfg" "$temp_dir"
    fi
}

install_driver() {
    # The Full-Stack Linux agent runs plugins in its own Python (use_agent_python=1),
    # which already bundles psycopg2: nothing to install.
    if ls -d "$agent_dir"/lib/lib/psycopg2 >/dev/null 2>&1; then
        echo "The agent's own Python already includes psycopg2."
        return
    fi
    if "$python" -c "import psycopg2" >/dev/null 2>&1; then
        echo "The psycopg2 module is already installed."
        return
    fi
    color 3; echo; echo "------------Installing the psycopg2 module------------"; reset
    echo "The plugin needs psycopg2. It will be installed with: $python -m pip install psycopg2-binary"
    read -r -p "Install it now? (y or n): " ans
    if [ -z "$ans" ] || [ "$ans" = "y" ] || [ "$ans" = "Y" ]; then
        "$python" -m pip install psycopg2-binary
        error_handler $? "psycopg2-binary could not be installed. Install it manually and run the installer again."
    else
        echo "Install psycopg2 before the plugin can collect data: $python -m pip install psycopg2-binary"
    fi
}

find_python() {
    python=$(command -v python3)
    if [ -z "$python" ]; then
        error_handler 1 "Python 3 was not found. Install Python 3.6 or later and run the installer again."
    fi
    sed -i "1s|^.*|#!$python|" "$temp_dir/$plugin.py"
    error_handler $? "Could not set the Python path in $plugin.py"
    echo "Using $("$python" --version 2>&1) at $python"
}

get_plugin_data() {
    color 3; echo; echo "------------Connection details------------"; reset
    echo " Press Enter to keep a default. The password is encrypted by the agent and is not stored in Site24x7."
    echo " For a cluster, give any one node, a VIP, a DNS name or a proxy write port; the other nodes are found automatically."
    echo
    read -r -p "  PostgreSQL host (default: localhost): " pg_host
    read -r -p "  PostgreSQL port (default: 5432): " pg_port
    read -r -p "  Username of the user with pg_monitor (default: None): " pg_user
    read -r -s -p "  Password of that user (default: None): " pg_password
    echo
    read -r -p "  Database (default: postgres): " pg_db
    read -r -p "  Patroni REST API port, only if this is a Patroni cluster (default: none): " patroni_port
    pg_host=${pg_host:-localhost}
    pg_port=${pg_port:-5432}
    pg_user=${pg_user:-None}
    pg_password=${pg_password:-None}
    pg_db=${pg_db:-postgres}
}

escape() { printf '%s' "$1" | sed -e 's/[\\&|]/\\&/g'; }

add_conf() {
    cfg="$temp_dir/$plugin.cfg"
    sed -i "s|^host=.*|host=\"$(escape "$pg_host")\"|" "$cfg" &&
    sed -i "s|^port=.*|port=\"$(escape "$pg_port")\"|" "$cfg" &&
    sed -i "s|^username=.*|username=\"$(escape "$pg_user")\"|" "$cfg" &&
    sed -i "s|^password=.*|password=\"$(escape "$pg_password")\"|" "$cfg" &&
    sed -i "s|^db=.*|db=\"$(escape "$pg_db")\"|" "$cfg"
    error_handler $? "Could not write $cfg"
    if [ -n "$patroni_port" ]; then
        sed -i "s|^patroni_port=.*|patroni_port=\"$(escape "$patroni_port")\"|" "$cfg"
    fi
}

check_plugin_execution() {
    output=$("$python" "$temp_dir/$plugin.py" --host "$pg_host" --port "$pg_port" \
             --username "$pg_user" --password "$pg_password" --db "$pg_db" 2>&1)
    if [ $? -ne 0 ] || grep -q '"status": 0' <<< "$output"; then
        color 1
        echo "------------The test run failed------------"
        grep -E '"msg"' <<< "$output"
        reset
        exit 1
    fi
    if ! grep -qE '"Server Version"|"Active Connections"' <<< "$output"; then
        error_handler 1 "The test run returned no metrics. Check the connection details."
    fi
    color 2
    echo "------------Test run successful------------"
    grep -E '"(Server Version|Node Role|Cluster Type|Nodes Up)": [^[{]' <<< "$output"
    reset
}

move_plugin() {
    if [ "$mode" = "upgrade" ]; then
        # replace only the code and README; keep postgres.cfg, .state/ and logs
        cp "$temp_dir/$plugin.py" "$plugin_dir/$plugin/$plugin.py" &&
        cp "$temp_dir/README.md" "$plugin_dir/$plugin/README.md"
        error_handler $? "Could not update $plugin_dir/$plugin"
        rm -rf "$temp_dir"
    else
        mkdir -p "$plugin_dir" && mv "$temp_dir" "$plugin_dir/$plugin"
        error_handler $? "Could not move the plugin to $plugin_dir"
    fi
    echo "Completed."
}

restart_agent() {
    color 3; read -r -p "Restart the Site24x7 Linux agent now? (y or n): " ans; reset
    if [ -z "$ans" ] || [ "$ans" = "y" ] || [ "$ans" = "Y" ]; then
        "$agent_dir/bin/monagent" restart
        error_handler $? "Could not restart the agent"
    fi
    if $agent_path_change; then
        echo "If the agent runs as a non-root user, give it access to the plugin folder, for example:"
        echo "  chown -R site24x7-agent:site24x7-group $plugin_dir/$plugin"
    fi
}

echo
echo "Site24x7 PostgreSQL plugin installer (version 2)"
echo
agent_check
temp_dir="$agent_dir/temp/plugins/$plugin"
plugin_dir="$agent_dir/plugins"
prerequisites
check_existing
download
find_python
install_driver
if [ "$mode" = "install" ]; then
    get_plugin_data
    add_conf
    check_plugin_execution
else
    # an upgrade has no plain-text credentials to test with (the agent encrypted them)
    "$python" -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" "$temp_dir/$plugin.py"
    error_handler $? "The downloaded $plugin.py is not valid Python."
    echo "Existing configuration kept: $plugin_dir/$plugin/$plugin.cfg"
fi
color 3; echo; echo "------------Installing into $plugin_dir/$plugin------------"; reset
move_plugin
color 2
if [ "$mode" = "upgrade" ]; then echo "------------Plugin upgraded successfully------------"
else echo "------------Plugin installed successfully------------"; fi
reset
restart_agent
