import json
import time
import requests
import urllib3
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

PLUGIN_VERSION = 1
HEARTBEAT      = "true"

WEAVIATE_READY_URI   = "/v1/.well-known/ready"
WEAVIATE_META_URI    = "/v1/meta"
WEAVIATE_SCHEMA_URI  = "/v1/schema"
WEAVIATE_NODES_URI   = "/v1/nodes?output=verbose"
WEAVIATE_GRAPHQL_URI = "/v1/graphql"

METRICS_UNITS = {
    "GraphQL Response Time": "ms",
    "Memory Usage"         : "MB",
    "Virtual Memory"       : "MB",
    "Heap Alloc"           : "MB",
    "Heap Sys"             : "MB",
    "CPU Seconds"          : "s",
    "Open File Descriptors": "fds",
    "Max File Descriptors" : "fds",
    "Goroutines"           : "goroutines",
    "OS Threads"           : "threads",
    "GC Pause Duration"    : "ms",
    "Heap Objects"         : "objects",
    "Object Count"         : "objects",
    "Shard Count"          : "shards",
    "Collection Count"     : "collections",
    "Node Count"           : "nodes",
}

TABS = {
    "Collections": {
        "order": 1,
        "tablist": [
            "Collection Details",
        ]
    },
    "Nodes": {
        "order": 2,
        "tablist": [
            "Node Details",
            "Shard Details",
        ]
    },
}


def clean_quotes(value):
    if not value:
        return value
    value_str = str(value).strip()
    if (value_str.startswith('"') and value_str.endswith('"')) or \
       (value_str.startswith("'") and value_str.endswith("'")):
        return value_str[1:-1]
    return value_str


def bytes_to_mb(value):
    try:
        return round(float(value) / (1024 * 1024), 2)
    except Exception:
        return 0


def makeAPICall(endpoint_uri, data):
    try:
        url     = WEAVIATE_SERVER + endpoint_uri
        headers = {}
        if WEAVIATE_API_KEY:
            headers["Authorization"] = f"Bearer {WEAVIATE_API_KEY}"

        response = requests.get(url, headers=headers, verify=WEAVIATE_SSL_VERIFY)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        error_msg = f"API Error [{endpoint_uri}]: {str(e)}"
        data["msg"]    = data["msg"] + " | " + error_msg if "msg" in data else error_msg
        data["status"] = 0
        return {}


def parsePrometheus(raw_text):
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


def fetchPrometheusMetrics(data):
    try:
        url      = f"http://{WEAVIATE_HOST}:{WEAVIATE_METRICS_PORT}/metrics"
        response = requests.get(url)
        response.raise_for_status()
        return parsePrometheus(response.text)
    except Exception as e:
        error_msg = f"Prometheus Error: {str(e)}"
        data["msg"] = data["msg"] + " | " + error_msg if "msg" in data else error_msg
        return {}


def getResponseTime(data):
    try:
        url     = WEAVIATE_SERVER + WEAVIATE_READY_URI
        headers = {}
        if WEAVIATE_API_KEY:
            headers["Authorization"] = f"Bearer {WEAVIATE_API_KEY}"
        response = requests.get(url, headers=headers, verify=WEAVIATE_SSL_VERIFY)

        if response.status_code != 200:
            data["status"] = 0
            data["msg"]    = "Weaviate is not ready"
            return False

    except Exception as e:
        data["status"] = 0
        data["msg"]    = f"Connection Error: {str(e)}"
        return False

    return True


def getGraphQLResponseTime(data):
    try:
        url     = WEAVIATE_SERVER + WEAVIATE_GRAPHQL_URI
        headers = {"Content-Type": "application/json"}
        if WEAVIATE_API_KEY:
            headers["Authorization"] = f"Bearer {WEAVIATE_API_KEY}"

        start    = time.time()
        response = requests.post(
            url,
            json={"query": "{ Get { } }"},
            headers=headers,
            verify=WEAVIATE_SSL_VERIFY,
        )
        elapsed = round((time.time() - start) * 1000, 2)
        data["GraphQL Response Time"] = elapsed if response.status_code == 200 else -1

    except Exception as e:
        data["GraphQL Response Time"] = -1
        error_msg = f"GraphQL Error: {str(e)}"
        data["msg"] = data["msg"] + " | " + error_msg if "msg" in data else error_msg


def getMeta(data):
    meta = makeAPICall(WEAVIATE_META_URI, data)
    if meta:
        data["Weaviate Version"] = meta.get("version", "-")


def getCollections(data):
    schema  = makeAPICall(WEAVIATE_SCHEMA_URI, data)
    classes = (schema or {}).get("classes", []) or []

    data["Collection Count"]   = len(classes)
    collection_details = []
    for cls in classes:
        cls_name = cls.get("class")
        if cls_name:
            collection_details.append({
                "name"       : cls_name,
                "Vectorizer" : cls.get("vectorizer", "-"),
                "Description": cls.get("description", "-"),
            })
    data["Collection Details"] = collection_details if collection_details else [{"name": "-", "Vectorizer": "-", "Description": "-"}]


def getNodes(data):
    nodes_resp   = makeAPICall(WEAVIATE_NODES_URI, data)
    nodes        = (nodes_resp or {}).get("nodes", []) or []

    total_objects = 0
    total_shards  = 0
    node_details  = []
    shard_details = []

    for node in nodes:
        stats       = node.get("stats") or {}
        node_name   = node.get("name", "unknown")
        obj_count   = stats.get("objectCount", 0) or 0
        shard_count = stats.get("shardCount", 0) or 0

        total_objects += obj_count
        total_shards  += shard_count

        node_details.append({
            "name"        : node_name,
            "Object_Count": obj_count,
            "Shard_Count" : shard_count,
            "Node Status" : node.get("status", "-"),
        })

        for shard in node.get("shards", []) or []:
            shard_name = shard.get("name")
            if not shard_name:
                continue
            cls_name = shard.get("class", "Unknown")
            shard_details.append({
                "name"        : f"{cls_name} / {shard_name} ({node_name})",
                "Object_Count": shard.get("objectCount", 0) or 0,
            })

    data["Node Count"]    = len(nodes)
    data["Object Count"]  = total_objects
    data["Shard Count"]   = total_shards
    data["Node Details"]  = node_details  if node_details  else [{"name": "-", "Object_Count": 0, "Shard_Count": 0, "Node Status": "-"}]
    data["Shard Details"] = shard_details if shard_details else [{"name": "-", "Object_Count": 0}]


def getPrometheusMetrics(data):
    totals = fetchPrometheusMetrics(data)
    if not totals:
        return

    data["Memory Usage"]          = bytes_to_mb(totals.get("process_resident_memory_bytes", 0))
    data["Virtual Memory"]        = bytes_to_mb(totals.get("process_virtual_memory_bytes", 0))
    data["Heap Alloc"]            = bytes_to_mb(totals.get("go_memstats_heap_alloc_bytes", 0))
    data["Heap Sys"]              = bytes_to_mb(totals.get("go_memstats_heap_sys_bytes", 0))
    data["Heap Objects"]          = int(totals.get("go_memstats_heap_objects", 0))
    data["CPU Seconds"]           = round(totals.get("process_cpu_seconds_total", 0), 4)
    data["Open File Descriptors"] = int(totals.get("process_open_fds", 0))
    data["Max File Descriptors"]  = int(totals.get("process_max_fds", 0))
    data["Goroutines"]            = int(totals.get("go_goroutines", 0))
    data["OS Threads"]            = int(totals.get("go_threads", 0))
    data["GC Pause Duration"]     = round(totals.get("go_gc_duration_seconds_sum", 0) * 1000, 4)


def metricCollector():
    data = {}
    data["plugin_version"]     = PLUGIN_VERSION
    data["heartbeat_required"] = HEARTBEAT
    data["units"]              = METRICS_UNITS
    data["tabs"]               = TABS

    ready = getResponseTime(data)
    if not ready:
        return data

    getMeta(data)
    getGraphQLResponseTime(data)
    getCollections(data)
    getNodes(data)
    getPrometheusMetrics(data)

    data.pop("status", None)

    return data


def run(param):
    global WEAVIATE_HOST, WEAVIATE_PORT, WEAVIATE_METRICS_PORT
    global WEAVIATE_API_KEY, WEAVIATE_SERVER, WEAVIATE_SSL_VERIFY

    WEAVIATE_HOST         = clean_quotes(param.get("host", "localhost"))
    WEAVIATE_PORT         = clean_quotes(param.get("port", "8080"))
    WEAVIATE_METRICS_PORT = clean_quotes(param.get("metrics_port", "2112"))
    WEAVIATE_API_KEY      = clean_quotes(param.get("api_key", ""))

    ssl_enabled         = clean_quotes(param.get("ssl", "false")).lower() == "true"
    insecure            = clean_quotes(param.get("insecure", "false")).lower() == "true"
    protocol            = "https" if ssl_enabled else "http"
    WEAVIATE_SERVER     = f"{protocol}://{WEAVIATE_HOST}:{WEAVIATE_PORT}"
    WEAVIATE_SSL_VERIFY = not insecure

    try:
        return metricCollector()
    except Exception as e:
        return {
            "status"            : 0,
            "msg"               : f"Plugin Error: {str(e)}",
            "plugin_version"    : PLUGIN_VERSION,
            "heartbeat_required": HEARTBEAT,
        }


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--host",         help="Weaviate Host",                  nargs="?", default="localhost")
    parser.add_argument("--port",         help="Weaviate REST API Port",         nargs="?", default="8080")
    parser.add_argument("--metrics_port", help="Weaviate Prometheus Metrics Port",nargs="?", default="2112")
    parser.add_argument("--api_key",      help="API Key (if auth enabled)",                  default="")
    parser.add_argument("--ssl",          help="Use SSL/HTTPS (true/false)",                 default="false")
    parser.add_argument("--insecure",     help="Skip SSL certificate verification",          default="false")
    args = parser.parse_args()

    WEAVIATE_HOST         = args.host
    WEAVIATE_PORT         = args.port
    WEAVIATE_METRICS_PORT = args.metrics_port
    WEAVIATE_API_KEY      = args.api_key

    ssl_enabled         = args.ssl.lower() == "true"
    insecure            = args.insecure.lower() == "true"
    protocol            = "https" if ssl_enabled else "http"
    WEAVIATE_SERVER     = f"{protocol}://{WEAVIATE_HOST}:{WEAVIATE_PORT}"
    WEAVIATE_SSL_VERIFY = not insecure

    print(json.dumps(metricCollector(), indent=2))
