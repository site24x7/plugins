#!/usr/bin/python
'''
Created on 04-May-2018

@author: giri
'''
import socket
import json

PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

SERVER = "127.0.0.1"
PORT = 5432
result_json = {}
result_json["plugin_version"] = PLUGIN_VERSION
result_json["heartbeat_required"] = HEARTBEAT
result_json["status"] = 1

def sdp_postgres_port_monitor():
	try:
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		result = sock.connect_ex((SERVER, PORT))
		if result == 0:
			result_json["POSTGRES_PORT_STATUS"] = 1
		else:
			result_json["POSTGRES_PORT_STATUS"] = 0

	except Exception as e:
		result_json["status"] = 0
		result_json["msg"] = e

sdp_postgres_port_monitor()
print(json.dumps(result_json))

