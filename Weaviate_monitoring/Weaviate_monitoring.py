import json
import time
import sys
import os
import tempfile




# Initialize variables securely
SSL_VERIFY = True

PLUGIN_VERSION = 1
HEARTBEAT = "true"

# Base units definition to ensure Site24x7 always has a schema to read
UNITS = {
    "Response Time": "ms",
    "GraphQL Response Time": "ms",
    "CPU Percent": "%",
    "Memory Usage": "MB",
    "Batch Duration": "ms",
    "Batch Delete Duration": "ms",
    "Object Duration": "ms",
    "Segment Size": "MB",
    "Bloom Filter Duration": "ms",
    "Duration": "ms",
    "Maintenance": "ms",
    "Startup Duration": "ms",
}

TABS = {
    "Vector Index": {
        "order": 1,
        "tablist": [
            "Operations",
            "Size",
            "Duration",
            "Maintenance",
            "Tombstones",
            "Tombstone Threads",
        ]
    },
    "LSM Storage": {
        "order": 2,
        "tablist": [
            "Active Segments",
            "Segment Count",
            "Segment Size",
            "Bloom Filter Duration",
        ]
    },
    "Cluster Topology": {
        "order": 3,
        "tablist": [
            "Collection Count",
            "Object Count",
            "Collection Details",
            "Node Details",
            "Total Shard Count",
            "Shard Details"
        ]
    }
}

def get_error_payload(error_message):
    """Returns a valid JSON payload even if the script crashes completely."""
    return {
        "plugin_version": PLUGIN_VERSION,
        "heartbeat_required": HEARTBEAT,
        "status": 0,
        "msg": error_message,
        "units": UNITS
    }

# Safely attempt to import requests to catch Local System environment issues
try:
    import requests
except ImportError:
    print(json.dumps(get_error_payload("Python 'requests' module not found. Install globally using Admin PowerShell: python -m pip install requests")))
    sys.exit(0)

REQUEST_TIMEOUT = 5

def auth_headers():
    if WEAVIATE_API_KEY:
        return {"Authorization": f"Bearer {WEAVIATE_API_KEY}"}
    return {}

def fetch_json(url):
    try:
        response = requests.get(url, headers=auth_headers(), verify=globals().get("SSL_VERIFY", True), timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json()
    except (requests.exceptions.RequestException, ValueError):
        return None

def fetch_text(url):
    try:
        response = requests.get(url, headers=auth_headers(), verify=globals().get("SSL_VERIFY", True), timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException:
        return None

def timed_get(url):
    try:
        start = time.time()
        response = requests.get(url, headers=auth_headers(), verify=globals().get("SSL_VERIFY", True), timeout=REQUEST_TIMEOUT)
        elapsed_ms = round((time.time() - start) * 1000, 2)
        return response.status_code == 200, elapsed_ms
    except requests.exceptions.RequestException:
        return False, 0

def timed_post(url, body):
    try:
        start = time.time()
        response = requests.post(url, json=body, headers=auth_headers(), verify=globals().get("SSL_VERIFY", True), timeout=REQUEST_TIMEOUT)
        elapsed_ms = round((time.time() - start) * 1000, 2)
        return response.status_code == 200, elapsed_ms
    except requests.exceptions.RequestException:
        return False, 0

def parse_prometheus(raw_text):
    totals = {}
    if not raw_text:
        return totals
    for line in raw_text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        parts = line.rsplit(" ", 1)
        if len(parts) != 2:
            continue
        name_with_labels, value_str = parts
        name = name_with_labels.split("{")[0]
        if name.endswith("_bucket"):
            continue
        try:
            value = float(value_str)
        except ValueError:
            continue
        totals[name] = totals.get(name, 0.0) + value
    return totals

def get_metric(totals, exact_name):
    return totals.get(exact_name, 0.0)

def bytes_to_mb(value):
    if not value: return 0
    return round(value / (1024 * 1024), 2)

def to_number(value):
    return value if isinstance(value, (int, float)) else 0

def build_collection_details(schema):
    classes = (schema or {}).get("classes", []) or []
    details = []
    for cls in classes:
        cls_name = cls.get("class")
        if cls_name:
            vectorizer = cls.get("vectorizer", "-")
            # Site24x7 tables only allow string values in 'name'
            details.append({
                "name": f"{cls_name} (vectorizer: {vectorizer})"
            })
    return details

def build_node_and_shard_details(nodes_data):
    nodes = (nodes_data or {}).get("nodes", []) or []
    node_details, shard_details = [], []
    for node in nodes:
        stats = node.get("stats") or {}
        node_name = node.get("name")
        if not node_name: 
            continue
            
        node_details.append({
            "name": node_name,
            "Shard_Count": to_number(stats.get("shardCount")),
            "Object_Count": to_number(stats.get("objectCount"))
        })
        
        for shard in node.get("shards", []) or []:
            shard_name = shard.get("name")
            if not shard_name: 
                continue
            
            cls_name = shard.get("class", "Unknown")
            # Combine class, shard name, and node into the 'name' field
            shard_details.append({
                "name": f"{cls_name} / {shard_name} ({node_name})",
                "Object_Count": to_number(shard.get("objectCount"))
            })
            
    return node_details, shard_details
CPU_STATE_FILE = os.path.join(tempfile.gettempdir(), "weaviate_cpu_state.json")

def get_cpu_utilization_percent(current_cpu_seconds, cores=1):
    """
    Converts a cumulative Prometheus counter (process_cpu_seconds_total)
    into an instantaneous CPU utilization percentage, by comparing it
    against the value from the previous plugin run.
    """
    now = time.time()
    previous_time = None
    previous_cpu = None

    try:
        with open(CPU_STATE_FILE, "r") as f:
            state = json.load(f)
            previous_time = state.get("timestamp")
            previous_cpu = state.get("cpu_seconds")
    except (FileNotFoundError, ValueError, OSError):
        pass

    try:
        with open(CPU_STATE_FILE, "w") as f:
            json.dump({"timestamp": now, "cpu_seconds": current_cpu_seconds}, f)
    except OSError:
        pass

    if previous_time is None or previous_cpu is None:
        return 0  # first run — no prior data point to diff against

    delta_time = now - previous_time
    delta_cpu = current_cpu_seconds - previous_cpu

    if delta_cpu < 0 or delta_time <= 0:
        return 0  # counter reset (process restarted) or no time elapsed

    cores = cores if cores and cores > 0 else 1
    return round(((delta_cpu / delta_time) * 100) / cores, 2)

def metricCollector():
    ready_ok, response_time_ms = timed_get(f"{WEAVIATE_SERVER}/v1/.well-known/ready")
    _, graphql_time_ms = timed_post(f"{WEAVIATE_SERVER}/v1/graphql", {"query": "{ __schema { queryType { name } } }"})
    raw_metrics = fetch_text(WEAVIATE_METRICS_URL)
    totals = parse_prometheus(raw_metrics)
    cpu_seconds = get_metric(totals, "process_cpu_seconds_total")
    cpu_percent = get_cpu_utilization_percent(cpu_seconds, cores=os.cpu_count() or 1)
    schema = fetch_json(f"{WEAVIATE_SERVER}/v1/schema")
    nodes_data = fetch_json(f"{WEAVIATE_SERVER}/v1/nodes?output=verbose")
    nodes = (nodes_data or {}).get("nodes", []) or []
    
    object_count = sum(to_number((n.get("stats") or {}).get("objectCount")) for n in nodes)
    shard_count = sum(to_number((n.get("stats") or {}).get("shardCount")) for n in nodes)
    collection_count = len((schema or {}).get("classes", []) or [])
    node_details, shard_details = build_node_and_shard_details(nodes_data)
    collection_details = build_collection_details(schema)

    return {
        "plugin_version": PLUGIN_VERSION,
        "heartbeat_required": HEARTBEAT,
        "status": 1 if ready_ok else 0,
        "Response Time": response_time_ms,
        "GraphQL Response Time": graphql_time_ms,
        "CPU Percent": cpu_percent,
        "Memory Usage": bytes_to_mb(get_metric(totals, "process_resident_memory_bytes")),
        "Requests Total": get_metric(totals, "requests_total"),
        "Open File Descriptors": get_metric(totals, "process_open_fds"),
        "Collection Count": collection_count,
        "Object Count": object_count,
        "Node Count": len(nodes),
        "Total Shard Count": shard_count,
        "Batch Duration": get_metric(totals, "batch_durations_ms_sum"),
        "Batch Delete Duration": get_metric(totals, "batch_delete_durations_ms_sum"),
        "Object Duration": get_metric(totals, "objects_durations_ms_sum"),
        #LSM params
        "Active Segments": get_metric(totals, "lsm_active_segments"),
        "Segment Count": get_metric(totals, "lsm_segment_count"),
        "Segment Size": bytes_to_mb(get_metric(totals, "lsm_segment_size")),
        "Bloom Filter Duration": get_metric(totals, "lsm_bloom_filter_duration_ms_sum"),
        #Vector Index parameters
        "Size": get_metric(totals, "vector_index_size"),
        "Tombstones": get_metric(totals, "vector_index_tombstones"),
        "Tombstone Threads": get_metric(totals, "vector_index_tombstone_cleanup_threads"),
        "Operations": get_metric(totals, "vector_index_operations"),
        "Duration": get_metric(totals, "vector_index_durations_ms_sum"),
        "Maintenance": get_metric(totals, "vector_index_maintenance_durations_ms_sum"),
        #Ends here
        "Async Operations Running": get_metric(totals, "async_operations_running"),
        "Startup Duration": get_metric(totals, "startup_durations_ms_sum"),
        "Collection Details": collection_details,
        "Node Details": node_details,
        "Shard Details": shard_details,
        "units": UNITS,
        "tabs": TABS,
    }

def run(param):
    global WEAVIATE_HOST, WEAVIATE_PORT, WEAVIATE_METRICS_PORT, WEAVIATE_API_KEY, WEAVIATE_SERVER, WEAVIATE_METRICS_URL
    global SSL_VERIFY

    try:
        WEAVIATE_HOST = param.get("host", "localhost")
        WEAVIATE_PORT = param.get("port", "8080")
        WEAVIATE_METRICS_PORT = param.get("metrics_port", "2112")
        WEAVIATE_API_KEY = param.get("api_key", "")
        ssl_enabled = str(param.get("ssl", "false")).lower() == "true"

        verify_val = param.get("ssl_verify", "true")
        if verify_val.lower() == "true": SSL_VERIFY = True
        elif verify_val.lower() == "false": SSL_VERIFY = False
        else: SSL_VERIFY = verify_val 

        protocol = "https" if ssl_enabled else "http"
        WEAVIATE_SERVER = f"{protocol}://{WEAVIATE_HOST}:{WEAVIATE_PORT}"
        WEAVIATE_METRICS_URL = f"http://{WEAVIATE_HOST}:{WEAVIATE_METRICS_PORT}/metrics"

        return metricCollector()
    except Exception as e:
        return get_error_payload(f"Plugin Execution Error: {str(e)}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help="Host Name", nargs='?', default='localhost')
    parser.add_argument('--port', help="REST API Port", nargs='?', default="8080")
    parser.add_argument('--metrics_port', help="Prometheus Metrics Port", nargs='?', default="2112")
    parser.add_argument('--api_key', help="API Key (if authentication is enabled)", default="")
    parser.add_argument('--ssl', help="Use SSL/HTTPS", default="false")
    parser.add_argument('--ssl_verify', help="SSL Verification", default="true")
    args = parser.parse_args()

    print(json.dumps(run(vars(args))))