#!/usr/bin/python3
import requests
import json
import argparse

PLUGIN_VERSION = "1"
HEARTBEAT = "true"

data = {}

endpoints = [
    "wp-json/wp-site-health/v1/tests/background-updates",
    "wp-json/wp-site-health/v1/tests/loopback-requests",
    "wp-json/wp-site-health/v1/tests/https-status",
    "wp-json/wp-site-health/v1/tests/dotorg-communication",
    "wp-json/wp-site-health/v1/tests/authorization-header"
]

status_mapping = {
    "good": 1,
    "recommended": 2,
    "critical": 3
}

def metricCollector(url, username, application_password):
    for endpoint in endpoints:
        full_url = f"{url}/{endpoint}"
        
        try:
            response = requests.get(full_url, auth=(username, application_password))
            
            if response.status_code == 200:
                result = response.json()
                
                test_name = result.get('test')
                status = result.get('status')
                
                if test_name and status:
                    key = test_name.replace('_', '-') + "_status"
                    data[key] = status
                    
                    numeric_status = status_mapping.get(status, -1)  
                    data[test_name.replace('_', '-')] = numeric_status
            else:
                data['msg'] = f"Failed to fetch {full_url}, Status code: {response.status_code}"
                data['status'] = 0
        except requests.exceptions.RequestException as e:
            data['msg'] = f"Request failed for {full_url}: {str(e)}"
            data['status'] = 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--url', help="REST API url", default="https://localhost/wordpress/")
    parser.add_argument('--username', help="WordPress Username", default="wordpress_username")
    parser.add_argument('--application_password', help="Application Password for Authentication", default="application_password")
    args = parser.parse_args()

    metricCollector(args.url, args.username, args.application_password)

    data['plugin_version'] = PLUGIN_VERSION
    data['heartbeat_required'] = HEARTBEAT
    
    print(json.dumps(data))
