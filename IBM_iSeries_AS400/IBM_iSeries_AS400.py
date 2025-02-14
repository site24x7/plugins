#!/usr/bin/python3

import os, json
import subprocess
from pathlib import Path

# Configuration
PLUGIN_VERSION = "1"
HEARTBEAT_REQUIRED = "true"

HOST = "localhost"
USERNAME = "test"
PASSWORD = "test"
JAVA_HOME = "/usr/bin"

def run_java_plugin(host, username, password, java_home):
    
    PLUGIN_PATH = os.path.dirname(os.path.abspath(__file__))
    CLASS_PATH = os.pathsep.join([
        str(Path(PLUGIN_PATH) / "json-20140107.jar"),
        str(Path(PLUGIN_PATH) / "jt400.jar")
    ])

    # Compile Java class
    compile_command = [
        JAVA_HOME + "/javac",
        "-cp", CLASS_PATH,
        "-d", PLUGIN_PATH,
        str(Path(PLUGIN_PATH) / "As400DataCollector.java")
    ]

    try:
        # Execute compilation
        subprocess.run(compile_command, check=True)

        # Run Java program
        java_command = [
            java_home + "/java",
            "-cp", os.pathsep.join([CLASS_PATH, PLUGIN_PATH]),
            "As400DataCollector",
            PLUGIN_VERSION,
            HEARTBEAT_REQUIRED,
            host,
            username,
            password
        ]

        result = subprocess.run(
            java_command,
            capture_output=True,
            text=True,
            check=True
        )

        print(result.stdout.strip())

    except Exception as e:
        print(json.dumps({
            "plugin_version": PLUGIN_VERSION,
            "heartbeat_required": HEARTBEAT_REQUIRED,
            "msg": str(e),
            "status": 0
        }))



if __name__=="__main__":
    

    import argparse
    parser=argparse.ArgumentParser()

    parser.add_argument('--host', help='Host ip or domain of the as400 server', nargs='?', default=HOST)
    parser.add_argument('--username', help='username', nargs='?', default=USERNAME)
    parser.add_argument('--password', help='password', nargs='?', default=PASSWORD)
    parser.add_argument('--java_path', help='Path to java', nargs='?', default=JAVA_HOME)

    args=parser.parse_args()
    run_java_plugin(args.host, args.username, args.password, args.java_path)
