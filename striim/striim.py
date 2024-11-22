#!/usr/bin/python3
import json
import requests

PLUGIN_VERSION = 1
HEARTBEAT = True
METRICS_UNITS = {}

class Striim:

    def __init__(self, args):
        self.maindata = {}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required'] = HEARTBEAT
        self.maindata['units'] = METRICS_UNITS
        self.host = args.host
        self.port = args.port
        self.token = args.token

    def metriccollector(self):
        url = f"http://{self.host}:{self.port}/health?token={self.token}"

        try:
            response = requests.get(url)
            response.raise_for_status()
            response_data = response.json()

            result = {
                'plugin_version': PLUGIN_VERSION,
                'heartbeat_required': HEARTBEAT,
                'appHealthMap': [],
                'serverHealthMap': [],
            }

            app_health_map = response_data["healthRecords"][0].get("appHealthMap", {})
            for app_name, app_data in app_health_map.items():
                rate_value = app_data.get("rate", 0)
                result['appHealthMap'].append({
                    "name": app_name,
                    "Throughput_Per_Second": rate_value
                })

            server_health_map = response_data["healthRecords"][0].get("serverHealthMap", {})
            for server_name, server_data in server_health_map.items():
                memory_in_gb = round(server_data.get("memory", 0) / (1024**3), 2)

                cpu_in_percentage = float(server_data.get("cpu", "0").replace("%", ""))

                elasticsearch_free_in_gb = float(server_data.get("elasticsearchFree", "0GB").replace("GB", ""))

                disk_free_in_percentage = float(server_data.get("diskFree", "/: 0%").split(": ")[1].replace("%", ""))

                result['serverHealthMap'].append({
                    "name": server_name,
                    "MemoryInGB": memory_in_gb,
                    "CpuInPercentage": cpu_in_percentage,
                    "EleasticSearchFreeInGB": elasticsearch_free_in_gb,
                    "DiskFreeInPercentage": disk_free_in_percentage
                })

            target_health_map = response_data["healthRecords"][0].get("targetHealthMap", {})
            filtered_targets = []

            for target_name, target_data in target_health_map.items():
                if "System$" not in target_name:
                    if target_data.get("lagEnd2End") and target_data["lagEnd2End"].get("data"):
                        lee_value = target_data["lagEnd2End"]["data"][0].get("lee", 0) 
                    else:
                        lee_value = 0
                    result[f"{target_name}-Data_Latency"] = lee_value
                    filtered_targets.append(f"{target_name}-Data_Latency")
                    METRICS_UNITS[f"{target_name}-Data_Latency"] = "ms"

            tabs = {
                "App Health Map": {
                    "order": 1,
                    "tablist": ['appHealthMap']
                },
                "Server Health Map": {
                    "order": 2,
                    "tablist": ['serverHealthMap']
                },
                "Target Health Map": {
                    "order": 3,
                    "tablist": filtered_targets 
                }
            }

            result['tabs'] = tabs
            result['units'] = METRICS_UNITS

            return result

        except requests.exceptions.HTTPError as http_err:
            return {"error": f"HTTP error occurred: {http_err}"}
        except Exception as err:
            return {"error": f"Other error occurred: {err}"}


if __name__ == "__main__":

    host = "localhost"
    port = 9080
    api_token = "token"

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Striim host', default=host)
    parser.add_argument('--port', help='Striim port', default=port)
    parser.add_argument('--token', help='Striim access token', default=api_token)

    args = parser.parse_args()

    obj = Striim(args)

    result = obj.metriccollector()
    print(json.dumps(result, indent=4))
