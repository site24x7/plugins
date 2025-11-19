
import json
import requests
import urllib3
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PLUGIN_VERSION=1
HEARTBEAT="true"

RABBITMQ_API_URI="/api/overview"
RABBITMQ_NODES_URI="/api/nodes"
RABBITMQ_QUEUES_URI="/api/queues"

METRICS_UNITS={
    'Node Uptime':'minutes',
    'IO Read Avg Time':'ms',
    'IO Write Avg Time':'ms', 
    'IO Sync Avg Time':'ms',
    'IO Seek Avg Time':'ms',
    'IO Read Bytes':'bytes',
    'IO Write Bytes':'bytes',
    'Total Garbage Collection Bytes Reclaimed':'bytes',
    'Memory Usage Rate':'bytes/s',
    'Garbage Collection Rate':'gc/s',
    'Context Switch Rate':'switches/s',
    'Connections Created Rate':'conn/s',
    'Connections Closed Rate':'conn/s',
    'IO Read Count Rate':'ops/s',
    'IO Read Bytes Rate':'bytes/s',
    'IO Read Avg Time Rate':'ms/s',
    'IO Write Count Rate':'ops/s',
    'IO Write Bytes Rate':'bytes/s', 
    'IO Write Avg Time Rate':'ms/s',
    'IO Sync Count Rate':'ops/s',
    'IO Sync Avg Time Rate':'ms/s',
    'IO Seek Count Rate':'ops/s',
    'IO Seek Avg Time Rate':'ms/s',
    'IO Reopen Count Rate':'ops/s',
    'File Descriptor Usage Rate':'fd/s',
    'Socket Usage Rate':'sockets/s',
    'GC Bytes Reclaimed Rate':'bytes/s',
    'Mnesia RAM Transaction Rate':'tx/s',
    'Mnesia Disk Transaction Rate':'tx/s',
    'Message Store Read Rate':'ops/s',
    'Message Store Write Rate':'ops/s',
    'Queue Index Read Rate':'ops/s',
    'Queue Index Write Rate':'ops/s',
    'Total Messages Rate':'msg/s',
    'Total Messages Ready Rate':'msg/s',
    'Total Messages Unacknowledged Rate':'msg/s'
}

TABS={
        "Queues": {
            "order": 1,
            "tablist": [
                "Queues",
                "Queues Declared",
                "Queues Created",
                "Queues Deleted",
                "Total Queues"
            ]
        },
        "I/O Operations": {
            "order": 2,
            "tablist": [
                "IO Read Avg Time",
                "IO Read Bytes",
                "IO Read Count",
                "IO Sync Avg Time",
                "IO Sync Count",
                "IO Write Avg Time",
                "IO Write Bytes",
                "IO Write Count",
                "IO Seek Count",
                "IO Seek Avg Time",
                "IO Reopen Count"
            ]
        },
        "Storage Operations": {
            "order": 3,
            "tablist": [
                "Mnesia RAM Transaction Count",
                "Mnesia Disk Transaction Count",
                "Message Store Read Count",
                "Message Store Write Count",
                "Queue Index Read Count",
                "Queue Index Write Count"
            ]
        },
        "Erlang VM": {
            "order": 4,
            "tablist": [
                "Total Garbage Collection Count",
                "Total Garbage Collection Bytes Reclaimed",
                "Context Switches",
                "ErLang Processes Used",
                "ErLang Processes Total",
                "ErLang Processes Remaining",
                "File Descriptor Used",
                "File Descriptor Total",
                "File Descriptor Remaining",
                "Sockets Used",
                "Run Queue"
            ]
        },
        "Performance Rates": {
            "order": 5,
            "tablist": [
                "Memory Usage Rate",
                "Garbage Collection Rate", 
                "Context Switch Rate",
                "Connections Created Rate",
                "Connections Closed Rate",
                "IO Read Count Rate",
                "IO Read Bytes Rate",
                "IO Read Avg Time Rate",
                "IO Write Count Rate", 
                "IO Write Bytes Rate",
                "IO Write Avg Time Rate",
                "IO Sync Count Rate",
                "IO Sync Avg Time Rate",
                "IO Seek Count Rate",
                "IO Seek Avg Time Rate",
                "IO Reopen Count Rate",
                "File Descriptor Usage Rate",
                "Socket Usage Rate",
                "GC Bytes Reclaimed Rate",
                "Mnesia RAM Transaction Rate",
                "Mnesia Disk Transaction Rate",
                "Message Store Read Rate",
                "Message Store Write Rate",
                "Queue Index Read Rate",
                "Queue Index Write Rate"
            ]
        }
    }

def metricCollector():
    data = {}
    data['plugin_version'] = PLUGIN_VERSION
    data['heartbeat_required'] = HEARTBEAT
    data['units'] = METRICS_UNITS
    data['s247config'] = {
        'childdiscovery': [
            'Queues'
        ]
    }
    data['tabs'] = TABS
    
    overview_success = getOverview(data)
    
    if not overview_success:
        return data
    
    getNodes(data)   
    getQueues(data)
    return data


def convertBytesToMB(v):
    try:
        byte_s = float(v)
        return byte_s / 1000 / 1000
    except Exception as e:
        return -1

def makeAPICall(endpoint_uri, data):
    try:
        url = RABBITMQ_SERVER + endpoint_uri
        
        if RABBITMQ_USERNAME and RABBITMQ_PASSWORD:
            auth = HTTPBasicAuth(RABBITMQ_USERNAME, RABBITMQ_PASSWORD)
        else:
            auth = None
            
        response = requests.get(url, auth=auth, timeout=10, verify=RABBITMQ_SSL_VERIFY)
        response.raise_for_status()
        
        return response.json()
        
    except Exception as e:
        data['status'] = 0
        error_msg = f"API Error [{endpoint_uri}]: {str(e)}"
        if 'msg' in data:
            data['msg'] = data['msg'] + " | " + error_msg
        else:
            data['msg'] = error_msg
        return {}  

def getOverview(data):
    try:
        rabbit_dict = makeAPICall(RABBITMQ_API_URI, data)
        
        if not rabbit_dict:
            return False
        
        data['Node Name'] = rabbit_dict.get('node', '-')
        data['Rates Mode'] = rabbit_dict.get('rates_mode', '-')
        data['Total Consumers'] = rabbit_dict.get('object_totals', {}).get('consumers', -1)
        data['Total Exchanges'] = rabbit_dict.get('object_totals', {}).get('exchanges', -1)
        data['Total Channels'] = rabbit_dict.get('object_totals', {}).get('channels', -1)
        data['Total Connections'] = rabbit_dict.get('object_totals', {}).get('connections', -1)
        data['Total Messages Ready'] = rabbit_dict.get('queue_totals', {}).get('messages_ready', -1)
        data['Total Messages Unacknowledged'] = rabbit_dict.get('queue_totals', {}).get('messages_unacknowledged', -1)
        data['Total Messages'] = rabbit_dict.get('queue_totals', {}).get('messages', -1)
        data['Total Messages Rate'] = rabbit_dict.get('queue_totals', {}).get('messages_details', {}).get('rate', -1)
        data['Total Messages Ready Rate'] = rabbit_dict.get('queue_totals', {}).get('messages_ready_details', {}).get('rate', -1)
        data['Total Messages Unacknowledged Rate'] = rabbit_dict.get('queue_totals', {}).get('messages_unacknowledged_details', {}).get('rate', -1)
        
        return True 

    except Exception as e:
        data['status'] = 0
        error_msg = f"Overview Error: {str(e)}"
        if 'msg' in data:
            data['msg'] = data['msg'] + " | " + error_msg
        else:
            data['msg'] = error_msg
        return False
    
def getNodes(data):
    try:
        current_node = data.get('Node Name', '')
        
        if not current_node or current_node == '-':
            error_msg = "Node name not available"
            if 'msg' in data:
                data['msg'] = data['msg'] + " | " + error_msg
            else:
                data['msg'] = error_msg
            return
        
        node_endpoint = f"{RABBITMQ_NODES_URI}/{current_node}"
        nodes_dict = makeAPICall(node_endpoint, data)
        
        if not nodes_dict:
            error_msg = f"Node '{current_node}' not found in cluster"
            if 'msg' in data:
                data['msg'] = data['msg'] + " | " + error_msg
            else:
                data['msg'] = error_msg
            nodes_dict = None
    
        data['File Descriptor Used'] = nodes_dict.get('fd_used', -1) if nodes_dict else -1
        data['Run Queue'] = nodes_dict.get('run_queue', -1) if nodes_dict else -1
        data['Sockets Used'] = nodes_dict.get('sockets_used', -1) if nodes_dict else -1
        data['ErLang Processes Used'] = nodes_dict.get('proc_used', -1) if nodes_dict else -1
        data['File Descriptor Total'] = nodes_dict.get('fd_total', -1) if nodes_dict else -1
        data['ErLang Processes Total'] = nodes_dict.get('proc_total', -1) if nodes_dict else -1
        fd_used = nodes_dict.get('fd_used', -1) if nodes_dict else -1
        fd_total = nodes_dict.get('fd_total', -1) if nodes_dict else -1
        data['File Descriptor Remaining'] = fd_total - fd_used if (fd_used != -1 and fd_total != -1) else -1
        proc_used = nodes_dict.get('proc_used', -1) if nodes_dict else -1
        proc_total = nodes_dict.get('proc_total', -1) if nodes_dict else -1
        data['ErLang Processes Remaining'] = proc_total - proc_used if (proc_used != -1 and proc_total != -1) else -1
        uptime_ms = nodes_dict.get('uptime', -1) if nodes_dict else -1
        data['Node Uptime'] = round(uptime_ms / 60000, 2) if uptime_ms != -1 else -1
        partitions = nodes_dict.get('partitions', []) if nodes_dict else []
        data['Partitions'] = len(partitions) if partitions else 0
        data['IO Read Count'] = nodes_dict.get('io_read_count', -1) if nodes_dict else -1
        data['IO Write Count'] = nodes_dict.get('io_write_count', -1) if nodes_dict else -1
        data['IO Sync Count'] = nodes_dict.get('io_sync_count', -1) if nodes_dict else -1
        data['IO Seek Count'] = nodes_dict.get('io_seek_count', -1) if nodes_dict else -1
        data['IO Reopen Count'] = nodes_dict.get('io_reopen_count', -1) if nodes_dict else -1
        data['IO Read Bytes'] = nodes_dict.get('io_read_bytes', -1) if nodes_dict else -1
        data['IO Write Bytes'] = nodes_dict.get('io_write_bytes', -1) if nodes_dict else -1
        data['IO Read Avg Time'] = nodes_dict.get('io_read_avg_time', -1) if nodes_dict else -1
        data['IO Write Avg Time'] = nodes_dict.get('io_write_avg_time', -1) if nodes_dict else -1
        data['IO Sync Avg Time'] = nodes_dict.get('io_sync_avg_time', -1) if nodes_dict else -1
        data['IO Seek Avg Time'] = nodes_dict.get('io_seek_avg_time', -1) if nodes_dict else -1
        data['Mnesia RAM Transaction Count'] = nodes_dict.get('mnesia_ram_tx_count', -1) if nodes_dict else -1
        data['Mnesia Disk Transaction Count'] = nodes_dict.get('mnesia_disk_tx_count', -1) if nodes_dict else -1
        data['Message Store Read Count'] = nodes_dict.get('msg_store_read_count', -1) if nodes_dict else -1
        data['Message Store Write Count'] = nodes_dict.get('msg_store_write_count', -1) if nodes_dict else -1
        data['Queue Index Read Count'] = nodes_dict.get('queue_index_read_count', -1) if nodes_dict else -1
        data['Queue Index Write Count'] = nodes_dict.get('queue_index_write_count', -1) if nodes_dict else -1
        data['Total Garbage Collection Count'] = nodes_dict.get('gc_num', -1) if nodes_dict else -1
        data['Total Garbage Collection Bytes Reclaimed'] = nodes_dict.get('gc_bytes_reclaimed', -1) if nodes_dict else -1
        data['Context Switches'] = nodes_dict.get('context_switches', -1) if nodes_dict else -1
        data['Connections Created'] = nodes_dict.get('connection_created', -1) if nodes_dict else -1
        data['Connections Closed'] = nodes_dict.get('connection_closed', -1) if nodes_dict else -1
        data['Channels Created'] = nodes_dict.get('channel_created', -1) if nodes_dict else -1
        data['Channels Closed'] = nodes_dict.get('channel_closed', -1) if nodes_dict else -1
        data['Queues Declared'] = nodes_dict.get('queue_declared', -1) if nodes_dict else -1
        data['Queues Created'] = nodes_dict.get('queue_created', -1) if nodes_dict else -1
        data['Queues Deleted'] = nodes_dict.get('queue_deleted', -1) if nodes_dict else -1
        data['Memory Usage Rate'] = nodes_dict.get('mem_used_details', {}).get('rate', -1) if nodes_dict else -1
        data['Garbage Collection Rate'] = nodes_dict.get('gc_num_details', {}).get('rate', -1) if nodes_dict else -1
        data['Context Switch Rate'] = nodes_dict.get('context_switches_details', {}).get('rate', -1) if nodes_dict else -1
        data['Connections Created Rate'] = nodes_dict.get('connection_created_details', {}).get('rate', -1) if nodes_dict else -1
        data['Connections Closed Rate'] = nodes_dict.get('connection_closed_details', {}).get('rate', -1) if nodes_dict else -1
        data['IO Read Count Rate'] = nodes_dict.get('io_read_count_details', {}).get('rate', -1) if nodes_dict else -1
        data['IO Read Bytes Rate'] = nodes_dict.get('io_read_bytes_details', {}).get('rate', -1) if nodes_dict else -1
        data['IO Read Avg Time Rate'] = nodes_dict.get('io_read_avg_time_details', {}).get('rate', -1) if nodes_dict else -1
        data['IO Write Count Rate'] = nodes_dict.get('io_write_count_details', {}).get('rate', -1) if nodes_dict else -1
        data['IO Write Bytes Rate'] = nodes_dict.get('io_write_bytes_details', {}).get('rate', -1) if nodes_dict else -1
        data['IO Write Avg Time Rate'] = nodes_dict.get('io_write_avg_time_details', {}).get('rate', -1) if nodes_dict else -1
        data['IO Sync Count Rate'] = nodes_dict.get('io_sync_count_details', {}).get('rate', -1) if nodes_dict else -1
        data['IO Sync Avg Time Rate'] = nodes_dict.get('io_sync_avg_time_details', {}).get('rate', -1) if nodes_dict else -1
        data['IO Seek Count Rate'] = nodes_dict.get('io_seek_count_details', {}).get('rate', -1) if nodes_dict else -1
        data['IO Seek Avg Time Rate'] = nodes_dict.get('io_seek_avg_time_details', {}).get('rate', -1) if nodes_dict else -1
        data['IO Reopen Count Rate'] = nodes_dict.get('io_reopen_count_details', {}).get('rate', -1) if nodes_dict else -1
        data['Mnesia RAM Transaction Rate'] = nodes_dict.get('mnesia_ram_tx_count_details', {}).get('rate', -1) if nodes_dict else -1
        data['Mnesia Disk Transaction Rate'] = nodes_dict.get('mnesia_disk_tx_count_details', {}).get('rate', -1) if nodes_dict else -1
        data['Message Store Read Rate'] = nodes_dict.get('msg_store_read_count_details', {}).get('rate', -1) if nodes_dict else -1
        data['Message Store Write Rate'] = nodes_dict.get('msg_store_write_count_details', {}).get('rate', -1) if nodes_dict else -1
        data['Queue Index Read Rate'] = nodes_dict.get('queue_index_read_count_details', {}).get('rate', -1) if nodes_dict else -1
        data['Queue Index Write Rate'] = nodes_dict.get('queue_index_write_count_details', {}).get('rate', -1) if nodes_dict else -1
        data['GC Bytes Reclaimed Rate'] = nodes_dict.get('gc_bytes_reclaimed_details', {}).get('rate', -1) if nodes_dict else -1
        data['File Descriptor Usage Rate'] = nodes_dict.get('fd_used_details', {}).get('rate', -1) if nodes_dict else -1
        data['Socket Usage Rate'] = nodes_dict.get('sockets_used_details', {}).get('rate', -1) if nodes_dict else -1
            
    except Exception as e:
        error_msg = f"Nodes Error: {str(e)}"
        if 'msg' in data:
            data['msg'] = data['msg'] + " | " + error_msg
        else:
            data['msg'] = error_msg

def getQueues(data):
    data['Queues'] = []
    data['Total Queues'] = 0
    default_queue = {
        'name': '-',
        'Vhost': '-',
        'Consumers': -1,
        'Messages': -1,
        'Messages_Ready': -1,
        'Messages_Unacknowledged': -1,
        'Messages_Persistent': -1,
        'Messages_Rate': -1,
        'Messages_Ready_Rate': -1,
        'Messages_Unacknowledged_Rate': -1
    }
    
    try:
        queues_list = makeAPICall(RABBITMQ_QUEUES_URI, data)
        
        if not queues_list:
            data['Total Queues'] = 0
            data['Queues'].append(default_queue)
            return
        
        current_node = data.get('Node Name', '')
        
        node_queues = [q for q in queues_list if q.get('node', '') == current_node]
        
        data['Total Queues'] = len(node_queues)
        
        if not node_queues:
            data['Queues'].append(default_queue)
            return
        
        for queue in node_queues:
            queue_data = {
                'name': queue.get('name', 'unknown'),
                'Vhost': queue.get('vhost', '/'),
                'Consumers': queue.get('consumers', -1),
                'Messages': queue.get('messages', -1),
                'Messages_Ready': queue.get('messages_ready', -1),
                'Messages_Unacknowledged': queue.get('messages_unacknowledged', -1),
                'Messages_Persistent': queue.get('messages_persistent', -1),
                'Messages_Rate': queue.get('messages_details', {}).get('rate', -1),
                'Messages_Ready_Rate': queue.get('messages_ready_details', {}).get('rate', -1),
                'Messages_Unacknowledged_Rate': queue.get('messages_unacknowledged_details', {}).get('rate', -1)
            }
            
            data['Queues'].append(queue_data)
            
    except Exception as e:
        error_msg = f"Queues Error: {str(e)}"
        if 'msg' in data:
            data['msg'] = data['msg'] + " | " + error_msg
        else:
            data['msg'] = error_msg
        data['Total Queues'] = -1
        data['Queues'].append(default_queue)

def clean_quotes(value):
    if not value:
        return value
    
    value_str = str(value)
    
    if value_str.startswith('"') and value_str.endswith('"'):
        return value_str[1:-1]
    
    elif value_str.startswith("'") and value_str.endswith("'"):
        return value_str[1:-1]
    
    return value_str

def run(param):
    global RABBITMQ_HOST, RABBITMQ_PORT, RABBITMQ_USERNAME, RABBITMQ_PASSWORD, RABBITMQ_SERVER, RABBITMQ_SSL_VERIFY

    host = clean_quotes(param.get("host", "localhost"))
    port = clean_quotes(param.get("port", "15672"))
    username = clean_quotes(param.get("username", "guest"))
    password = clean_quotes(param.get("password", "guest"))
    ssl_enabled = clean_quotes(param.get("ssl", "false")).lower() == "true"
    insecure = clean_quotes(param.get("insecure", "false")).lower() == "true"

    RABBITMQ_HOST = host
    RABBITMQ_PORT = port
    RABBITMQ_USERNAME = username if username != "None" else None
    RABBITMQ_PASSWORD = password if password != "None" else None
    
    
    protocol = "https" if ssl_enabled else "http"
    RABBITMQ_SERVER = f"{protocol}://{RABBITMQ_HOST}:{RABBITMQ_PORT}"
    
    
    RABBITMQ_SSL_VERIFY = not insecure
    
    try:
        result = metricCollector()
        return result
    except Exception as e:
        return {
            'status': 0,
            'msg': f"Plugin Error: {str(e)}",
            'plugin_version': PLUGIN_VERSION,
            'heartbeat_required': HEARTBEAT
        }


if __name__ == "__main__":
    
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--host',help="Host Name",nargs='?',default='localhost')
    parser.add_argument('--port',help="Port",nargs='?',default="15672")
    parser.add_argument('--username',help="Username",default="guest")
    parser.add_argument('--password',help="Password",default="guest")
    parser.add_argument('--ssl',help="Use SSL/HTTPS",default="false")
    parser.add_argument('--insecure',help="Skip SSL certificate verification",default="false")

    args=parser.parse_args()
    
    RABBITMQ_HOST=args.host
    RABBITMQ_PORT=args.port
    RABBITMQ_USERNAME=args.username
    RABBITMQ_PASSWORD=args.password
    
    ssl_enabled = args.ssl.lower() == "true"
    insecure = args.insecure.lower() == "true"
    protocol = "https" if ssl_enabled else "http"
    RABBITMQ_SERVER = f"{protocol}://{RABBITMQ_HOST}:{RABBITMQ_PORT}"
    RABBITMQ_SSL_VERIFY = not insecure

    print(json.dumps(metricCollector()))
