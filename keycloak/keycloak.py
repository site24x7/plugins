#!/usr/bin/python3
import json
import requests

PLUGIN_VERSION = 1
HEARTBEAT = True
METRICS_UNITS = {}

class KeycloakServerInfo:

    def __init__(self, args):
        self.maindata = {
            'plugin_version': PLUGIN_VERSION,
            'heartbeat_required': HEARTBEAT,
            'units': METRICS_UNITS
        }
        self.host = args.host
        self.port = args.port
        self.username = args.username
        self.password = args.password
        self.client_id = args.client_id

    def metriccollector(self):
        token_url = f"http://{self.host}:{self.port}/realms/master/protocol/openid-connect/token"
        token_data = {
            'grant_type': 'password',
            'client_id': self.client_id,
            'username': self.username,
            'password': self.password
        }

        try:
            token_response = requests.post(token_url, data=token_data)
            token_response.raise_for_status()
            access_token = token_response.json().get('access_token')

            server_info_url = f"http://{self.host}:{self.port}/admin/serverinfo"
            headers = {'Authorization': f'Bearer {access_token}', 'Content-Type': 'application/json'}
            server_info_response = requests.get(server_info_url, headers=headers)
            server_info_response.raise_for_status()

            server_info = server_info_response.json()
            system_info = server_info.get('systemInfo', {})
            memory_info = server_info.get('memoryInfo', {})

            keycloak_version = system_info.pop("version", None)
            uptime = system_info.pop("uptime", None)

            total_gb = memory_info.get("total", 0) / (1024 ** 3)
            used_gb = memory_info.get("used", 0) / (1024 ** 3)
            free_gb = memory_info.get("free", 0) / (1024 ** 3)

            memory_info_formatted = {
                "Total_Memory": round(total_gb, 2),
                "Used_Memory": round(used_gb, 2),
                "Free_Memory": round(free_gb, 2),
                "Free_Memory_Percentage": memory_info.get("freePercentage", 0),
                "Total_Formated_Memory": round(memory_info.get("total", 0) / (1024 ** 2), 0),
                "Used_Formated_Memory": round(memory_info.get("used", 0) / (1024 ** 2), 0),
                "Free_Formated_Memory": round(memory_info.get("free", 0) / (1024 ** 2), 0)
            }

            units = {
                "Total_Memory": "GB",
                "Used_Memory": "GB",
                "Free_Memory": "GB",
                "Free_Memory_Percentage": "%",
                "Total_Formated_Memory": "MB",
                "Used_Formated_Memory": "MB",
                "Free_Formated_Memory": "MB"
            }

            # Prepare result with flattened system_info and memory_info keys in the tabs
            result = {
                'plugin_version': PLUGIN_VERSION,
                'heartbeat_required': HEARTBEAT,
                'keycloak_version': keycloak_version,
                'Server_Uptime' : uptime,
                'units': units
            }
            
            # Add memory_info values to the result directly
            result.update(memory_info_formatted)

            return result

        except requests.exceptions.HTTPError as http_err:
            return {
                "plugin_version": PLUGIN_VERSION,
                "heartbeat_required": HEARTBEAT,
                "status": 0,
                "msg": f"HTTP error occurred: {http_err}"
            }
        except Exception as err:
            return {
                "plugin_version": PLUGIN_VERSION,
                "heartbeat_required": HEARTBEAT,
                "status": 0,
                "msg": f"Other error occurred: {err}"
            }

if __name__ == "__main__":
    host = "localhost"
    port = 8080
    username = "admin"
    password = "admin"
    client_id = "admin-cli"

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Keycloak host', default=host)
    parser.add_argument('--port', help='Keycloak port', default=port)
    parser.add_argument('--username', help='Keycloak username', default=username)
    parser.add_argument('--password', help='Keycloak password', default=password)
    parser.add_argument('--client_id', help='Keycloak client ID', default=client_id)

    args = parser.parse_args()

    obj = KeycloakServerInfo(args)
    result = obj.metriccollector()
    print(json.dumps(result, indent=4))
