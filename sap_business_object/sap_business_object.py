import requests
import xml.etree.ElementTree as ET
import json
import argparse
import time

# Default parameters
DEFAULT_PARAMS = {
    "plugin_version": 1,
    "heartbeat_required": True
}

def fetch_logon_token(host, port, username, password):
    logon_url = f"http://{host}:{port}/biprws/logon/long"
    headers = {
        "Accept": "application/xml",
        "Content-Type": "application/xml"
    }
    data = f'''<attrs xmlns="http://www.sap.com/rws/bip">
        <attr name="userName" type="string">{username}</attr>
        <attr name="password" type="string">{password}</attr>
        <attr name="auth" type="string" possibilities="secEnterprise,secLDAP,secWinAD,secSAPR3">secEnterprise</attr>
    </attrs>'''

    try:
        response = requests.post(logon_url, headers=headers, data=data)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            logon_token = root.find('.//{http://www.sap.com/rws/bip}attr[@name="logonToken"]')
            if logon_token is not None:
                return logon_token.text
            else:
                raise Exception("Logon Token not found in the response.")
        else:
            raise Exception(f"Failed to log in: {response.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Connection Error: {str(e)}")

def safe_int(value):
    try:
        return int(value)
    except (ValueError, TypeError):
        return None

def fetch_data(host, port, url_path, logon_token, data_type):
    url = f"http://{host}:{port}/{url_path}"
    headers = {
        "Content-Type": "application/xml",
        "Accept": "application/xml",
        "X-SAP-LogonToken": logon_token
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            data = []
            namespaces = {
                'atom': 'http://www.w3.org/2005/Atom',
                'bip': 'http://www.sap.com/rws/bip'
            }
            for entry in root.findall('.//atom:entry', namespaces):
                item_data = {}
                attrs = entry.find('.//atom:content/bip:attrs', namespaces)
                if attrs is not None:
                    for attr in attrs.findall('.//bip:attr', namespaces):
                        name = attr.get("name")
                        value = attr.text
                        if data_type == 'users':
                            if name == "name":
                                item_data["name"] = value
                            elif name == "ownerid":
                                item_data["ownerid"] = value
                            elif name == "parentid":
                                item_data["parentid"] = value
                        elif data_type == 'folders':
                            if name == "name":
                                item_data["name"] = value
                            elif name == "id":
                                item_data["folder_id"] = safe_int(value)
                            elif name == "ownerid":
                                item_data["owner_id"] = value
                        elif data_type == 'servers':
                            if name == "kind":
                                item_data["name"] = value
                            elif name == "status_type":
                                item_data["status"] = 1 if value == "Running" else 0
                            elif name == "disabled":
                                item_data["enabled"] = 1 if value == "Enabled" else 0
                            elif name == "server_process_id":
                                item_data["server_process_id"] = safe_int(value)
                            elif name == "id":
                                item_data["server_id"] = safe_int(value)
                            elif name == "parent_id":
                                item_data["parent_id"] = safe_int(value)
                data.append(item_data)
            return data
        else:
            raise Exception(f"Failed to fetch {data_type}: {response.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Connection Error: {str(e)}")

def fetch_connection(logon_token, host, port):
    url = f"http://{host}:{port}/biprws/raylight/v1/connections"
    headers = {
        "Accept": "application/xml",
        "Content-Type": "application/xml",
        "X-SAP-LogonToken": logon_token
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            root = ET.fromstring(response.text)
            connections = []
            for conn in root.findall('.//connection'):
                connection_data = {
                    "name": conn.find('name').text,
                    "connection_id": safe_int(conn.find('id').text),
                    "connection_folder_id": safe_int(conn.find('folderId').text)
                }
                connections.append(connection_data)
            return {"connections": connections, "TotalNoOfConnections": len(connections)}
        else:
            raise Exception(f"Failed to fetch connections: {response.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Connection Error: {str(e)}")

def parse_jobs(xml_response):
    namespaces = {
        'atom': 'http://www.w3.org/2005/Atom',
        'bip': 'http://www.sap.com/rws/bip'
    }
    root = ET.fromstring(xml_response)
    metrics = {
        "TotalJobsWarning": 0,
        "TotalFailedJobs": 0,
        "TotalJobs": 0,
        "TotalJobsRunning": 0,
        "TotalJobsExpired": 0,
        "TotalJobsPending": 0,
        "TotalJobsSuccess": 0
    }

    for entry in root.findall('.//atom:entry', namespaces):
        attrs = entry.find('.//atom:content/bip:attrs', namespaces)
        if attrs is not None:
            status_type = None
            count = 0
            for attr in attrs.findall('.//bip:attr', namespaces):
                name = attr.get("name")
                value = attr.text
                if name == "status_type":
                    status_type = value
                elif name == "count":
                    count = safe_int(value)

            if status_type == "Warning":
                metrics["TotalJobsWarning"] = count
            elif status_type == "Failed":
                metrics["TotalFailedJobs"] = count
            elif status_type == "Total":
                metrics["TotalJobs"] = count
            elif status_type == "Running":
                metrics["TotalJobsRunning"] = count
            elif status_type == "Expired":
                metrics["TotalJobsExpired"] = count
            elif status_type == "Pending":
                metrics["TotalJobsPending"] = count
            elif status_type == "Success":
                metrics["TotalJobsSuccess"] = count

    return metrics

def fetch_jobs(logon_token, host, port):
    url = f"http://{host}:{port}/biprws/bionbi/job/"
    headers = {
        "Accept": "application/xml",
        "Content-Type": "application/xml",
        "X-SAP-LogonToken": logon_token
    }
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return parse_jobs(response.text)
        else:
            raise Exception(f"Failed to fetch jobs: {response.status_code}")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Connection Error: {str(e)}")


def fetch_users(host, port, logon_token):
    return fetch_data(host, port, "biprws/v1/users", logon_token, 'users')

def fetch_folders(host, port, logon_token):
    return fetch_data(host, port, "biprws/v1/folders", logon_token, 'folders')

def fetch_servers(host, port, logon_token):
    return fetch_data(host, port, "biprws/bionbi/server/list/", logon_token, 'servers')

def fetch_publications(host, port, logon_token):
    headers = {
        "Accept": "application/xml",
        "Content-Type": "application/xml",
        "X-SAP-LogonToken": logon_token
    }
    base_url = f"http://{host}:{port}/biprws/v1/publications"
    publications = []
    
    try:
        url = base_url
        while url:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                root = ET.fromstring(response.text)
                namespaces = {'atom': 'http://www.w3.org/2005/Atom', 'bip': 'http://www.sap.com/rws/bip'}
                
                # Collect publication data
                for entry in root.findall('.//atom:entry', namespaces):
                    publication = {}
                    attrs = entry.find('.//atom:content/bip:attrs', namespaces)
                    if attrs is not None:
                        for attr in attrs.findall('.//bip:attr', namespaces):
                            name = attr.get("name")
                            value = attr.text
                            if name == "name":
                                publication["name"] = value
                            elif name == "id":
                                publication["publication_id"] = int(value)
                            elif name == "parentid":
                                publication["publication_folder_id"] = int(value)
                    publications.append(publication)
                
                # Check for next page
                next_link = root.find('.//atom:link[@rel="next"]', namespaces)
                url = next_link.get('href') if next_link is not None else None
            else:
                raise Exception(f"Failed to fetch publications: {response.status_code}")
        
        # Process results
        result = {
            "publications": publications,
            "TotalNoOfPublications": len(publications)
        }
        return result
    except requests.exceptions.RequestException as e:
        raise Exception(f"Connection Error: {str(e)}")

def calculate_server_metrics(servers):
    metrics = {
        "TotalNoOfServers": len(servers),
        "TotalNoOfRunningServers": sum(1 for server in servers if server["status"] == 1),
        "TotalNoOfStoppedServers": sum(1 for server in servers if server["status"] == 0),
        "TotalNoOfEnabledServers": sum(1 for server in servers if server["enabled"] == 1),
        "TotalNoOfDisabledServers": sum(1 for server in servers if server["enabled"] == 0)
    }
    return metrics

def check_bi_launchpad_availability(host, port):
    launchpad_url = f"http://{host}:{port}/BOE/BI"
    try:
        start_time = time.time()
        response = requests.get(launchpad_url, timeout=10)
        response_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        if response.status_code == 200:
            return {"BILaunchpadAvailability": "Available", "BILaunchpadResponseTimeMS": round(response_time)}
        else:
            return {"BILaunchpadAvailability": "Unavailable", "BILaunchpadAvailability": 0}
    except requests.exceptions.RequestException:
        return {"BILaunchpadAvailability": "Unavailable", "BILaunchpadAvailability": 0}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='SAP BIP host', default='localhost')
    parser.add_argument('--port', help='SAP BIP port', default='6405')
    parser.add_argument('--username', help='SAP BIP username', default='Administrator')
    parser.add_argument('--password', help='SAP BIP password', default='Admin123')
    args = parser.parse_args()

    try:
        launchpad_status = check_bi_launchpad_availability(args.host, args.port)
        logon_token = fetch_logon_token(args.host, args.port, args.username, args.password)
        users = fetch_users(args.host, args.port, logon_token)
        folders = fetch_folders(args.host, args.port, logon_token)
        servers = fetch_servers(args.host, args.port, logon_token)
        connections = fetch_connection(logon_token, args.host, args.port)

        jobs_metrics = fetch_jobs(logon_token, args.host, args.port)
        
        publications_data = fetch_publications(args.host, args.port, logon_token)
        
        server_metrics = calculate_server_metrics(servers)
        total_no_of_users = len(users)
        total_no_of_folders = len(folders)

        data = {
            **DEFAULT_PARAMS,
            **launchpad_status,
            **server_metrics,
            **connections,
            **jobs_metrics,
            **publications_data,
            "TotalNoOfUsers": total_no_of_users,
            "TotalNoOfFolders": total_no_of_folders,
            "users": users,
            "folders": folders,
            "servers": servers
        }
        data['tabs'] = {
                        'Servers': {
                            'order': 1,
                            'tablist': [
                                "servers",
                                "TotalNoOfServers",
                                "TotalNoOfRunningServers",
                                "TotalNoOfStoppedServers",
                                "TotalNoOfEnabledServers",
                                "TotalNoOfDisabledServers"
                            ]
                        },
                        'Connections': {
                            'order': 2,
                            'tablist': [
                                "connections",
                                "TotalNoOfConnections",

                            ]
                        },
                        'Jobs': {
                            'order': 3,
                            'tablist': [
                                "TotalJobsWarning",
                                "TotalFailedJobs",
                                "TotalJobs",
                                "TotalJobsRunning",
                                "TotalJobsExpired",
                                "TotalJobsPending",
                                "TotalJobsSuccess"
                            ]
                        },
                        'Publications': {
                            'order': 4,
                            'tablist': [
                                "publications",
                                "TotalNoOfPublications",

                            ]
                        }
                        
                    }
        print(json.dumps(data))
    except Exception as e:
        error_response = {
            **DEFAULT_PARAMS,
            "status": 0,
            "msg": str(e)
        }
        print(json.dumps(error_response))

if __name__ == "__main__":
    main()
    
