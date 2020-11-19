# The following piece of code has to be added in the main function of mysql.py to read the configuration from mysql.cfg file

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--host', help="mysql host",type=str)
parser.add_argument('--port', help ="mysql port",type=str)
parser.add_argument('--username', help='mysql username', type=str)
parser.add_argument('--password', help='mysql password', type=str)

args = parser.parse_args()

if args.host:
    MYSQL_HOST = args.host
if args.port:
    MYSQL_PORT = args.port
if args.username:
    MYSQL_USERNAME = args.username
if args.password:
    MYSQL_PASSWORD = args.password