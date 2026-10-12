import json
import time
import requests

PLUGIN_VERSION = 1
HEARTBEAT      = "true"

PINECONE_API_BASE   = "https://api.pinecone.io"
PINECONE_INDEXES_URI = "/indexes"

METRICS_UNITS = {
    "Index Count"                  : "indexes",
    "Ready Indexes"                : "indexes",
    "Not Ready Indexes"            : "indexes",
    "Total Vectors"                : "vectors",
    "Total Namespaces"             : "namespaces",
    "Average Vectors Per Index"    : "vectors",
    "Indexes With Zero Vectors"    : "indexes",
    "Serverless Indexes"           : "indexes",
    "Pod Based Indexes"            : "indexes",
    "Average Dimension"            : "dimensions",
    "Unique Regions"               : "regions",
    "Unique Cloud Providers"       : "providers",
    "Average Index Fullness"       : "percent",
    "Maximum Index Fullness"       : "percent",
    "Indexes Failed To Respond"    : "indexes",
    "Active Imports"               : "imports",
    "Completed Imports"            : "imports",
    "Failed Imports"               : "imports",
    "Cancelled Imports"            : "imports",
}

TABS = {
    "Indexes": {
        "order": 1,
        "tablist": [
            "Index Details",
        ]
    },
    "Namespaces": {
        "order": 2,
        "tablist": [
            "Namespace Details",
        ]
    }
}


def clean_quotes(value):
    if not value:
        return value
    value_str = str(value).strip()
    if (value_str.startswith('"') and value_str.endswith('"')) or \
       (value_str.startswith("'") and value_str.endswith("'")):
        return value_str[1:-1]
    return value_str


def makeAPICall(url, data, method="GET"):
    try:
        headers = {
            "Api-Key"                : PINECONE_API_KEY,
            "Content-Type"           : "application/json",
            "X-Pinecone-Api-Version" : PINECONE_API_VERSION,
        }
        if method == "POST":
            response = requests.post(url, headers=headers, json={}, verify=True)
        else:
            response = requests.get(url, headers=headers, verify=True)
        response.raise_for_status()
        return response.json()

    except Exception as e:
        error_msg = f"API Error: {str(e)}"
        data["msg"]    = data["msg"] + " | " + error_msg if "msg" in data else error_msg
        data["status"] = 0
        return None


def getIndexStats(host, data):
    clean_host = host.strip().rstrip("/")
    if not clean_host.startswith("http://") and not clean_host.startswith("https://"):
        clean_host = "https://" + clean_host
    url = clean_host + "/describe_index_stats"
    try:
        headers = {
            "Api-Key"                : PINECONE_API_KEY,
            "Content-Type"           : "application/json",
            "X-Pinecone-Api-Version" : PINECONE_API_VERSION,
        }
        response = requests.post(url, headers=headers, json={}, verify=True)
        response.raise_for_status()
        return response.json()
    except Exception:
        return None


def getImportStatusCounts(host):
    clean_host = host.strip().rstrip("/")
    if not clean_host.startswith("http://") and not clean_host.startswith("https://"):
        clean_host = "https://" + clean_host
    url = clean_host + "/bulk/imports"
    headers = {
        "Api-Key"                : PINECONE_API_KEY,
        "Content-Type"           : "application/json",
        "X-Pinecone-Api-Version" : PINECONE_API_VERSION,
    }
    counts = {"active": 0, "completed": 0, "failed": 0, "cancelled": 0}
    try:
        next_token = None
        while True:
            page_url = url
            if next_token:
                page_url = url + "?paginationToken=" + next_token
            response = requests.get(page_url, headers=headers, verify=True)
            response.raise_for_status()
            body = response.json()
            for job in body.get("data", []) or []:
                status = str(job.get("status", "")).lower()
                if status in ("pending", "inprogress"):
                    counts["active"] += 1
                elif status == "completed":
                    counts["completed"] += 1
                elif status == "failed":
                    counts["failed"] += 1
                elif status == "cancelled":
                    counts["cancelled"] += 1
            next_token = (body.get("pagination", {}) or {}).get("next")
            if not next_token:
                break
    except Exception:
        return None
    return counts


def getIndexes(data):
    body = makeAPICall(PINECONE_API_BASE + PINECONE_INDEXES_URI, data)
    if body is None:
        return

    indexes = body.get("indexes", []) or []

    ready_count        = 0
    not_ready_count    = 0
    serverless_count   = 0
    pod_count          = 0
    total_vectors      = 0
    total_namespaces   = 0
    zero_vector_count  = 0
    failed_count       = 0
    dimensions         = []
    fullness_values    = []
    regions_seen       = set()
    clouds_seen        = set()
    index_details      = []
    namespace_details  = []
    active_imports     = 0
    completed_imports  = 0
    failed_imports     = 0
    cancelled_imports  = 0

    for idx in indexes:
        name   = idx.get("name", "unknown")
        host   = idx.get("host", "")
        status = idx.get("status", {}) or {}
        spec   = idx.get("spec", {}) or {}
        ready  = bool(status.get("ready", False))

        if ready:
            ready_count += 1
        else:
            not_ready_count += 1

        serverless = spec.get("serverless", {}) or {}
        pod        = spec.get("pod", {}) or {}

        if serverless:
            serverless_count += 1
            if serverless.get("region"):
                regions_seen.add(serverless.get("region"))
            if serverless.get("cloud"):
                clouds_seen.add(serverless.get("cloud"))
        elif pod:
            pod_count += 1
            if pod.get("environment"):
                regions_seen.add(pod.get("environment"))

        dimension      = idx.get("dimension", 0) or 0
        vector_type    = idx.get("vector_type", "-") or "-"
        vector_count   = 0
        index_fullness = 0

        if host:
            stats = getIndexStats(host, data)
            if stats is not None:
                vector_count   = stats.get("totalVectorCount", 0) or 0
                dimension      = stats.get("dimension", dimension) or dimension
                index_fullness = round((stats.get("indexFullness", 0) or 0) * 100, 4)
                vector_type    = stats.get("vectorType", vector_type) or vector_type
                namespaces     = stats.get("namespaces", {}) or {}
                total_namespaces += len(namespaces)
                for ns_name, ns_info in namespaces.items():
                    ns_label = ns_name if ns_name else "(default)"
                    namespace_details.append({
                        "name"        : "{}_{}".format(name, ns_label),
                        "Index"       : name,
                        "Namespace"   : ns_label,
                        "Vector_Count": (ns_info or {}).get("vectorCount", 0) or 0,
                    })
            else:
                failed_count += 1
        else:
            failed_count += 1

        if host and serverless:
            import_counts = getImportStatusCounts(host)
            if import_counts is not None:
                active_imports    += import_counts["active"]
                completed_imports += import_counts["completed"]
                failed_imports    += import_counts["failed"]
                cancelled_imports += import_counts["cancelled"]

        total_vectors += vector_count
        if dimension:
            dimensions.append(dimension)
        fullness_values.append(index_fullness)
        if vector_count == 0:
            zero_vector_count += 1

        index_details.append({
            "name"         : name,
            "Vector_Count" : vector_count,
            "Dimension"    : dimension,
            "Index_Fullness": index_fullness,
            "Metric"       : idx.get("metric", "-"),
            "Vector_Type"  : vector_type,
            "Cloud"        : serverless.get("cloud", "-") if serverless else "-",
            "Region"       : serverless.get("region", "-") if serverless else pod.get("environment", "-"),
            "Ready_Status" : "Ready" if ready else "Not Ready",
        })

    count = len(indexes)

    data["Index Count"]               = count
    data["Ready Indexes"]             = ready_count
    data["Not Ready Indexes"]         = not_ready_count
    data["Total Vectors"]             = total_vectors
    data["Total Namespaces"]          = total_namespaces
    data["Average Vectors Per Index"] = round(total_vectors / count, 2) if count else 0
    data["Indexes With Zero Vectors"] = zero_vector_count
    data["Serverless Indexes"]        = serverless_count
    data["Pod Based Indexes"]         = pod_count
    data["Average Dimension"]         = round(sum(dimensions) / len(dimensions), 2) if dimensions else 0
    data["Unique Regions"]            = len(regions_seen)
    data["Unique Cloud Providers"]    = len(clouds_seen)
    data["Average Index Fullness"]    = round(sum(fullness_values) / len(fullness_values), 4) if fullness_values else 0
    data["Maximum Index Fullness"]    = max(fullness_values) if fullness_values else 0
    data["Indexes Failed To Respond"] = failed_count
    data["Active Imports"]            = active_imports
    data["Completed Imports"]         = completed_imports
    data["Failed Imports"]            = failed_imports
    data["Cancelled Imports"]         = cancelled_imports
    data["Index Details"]             = index_details if index_details else [{
        "name": "-", "Vector_Count": 0, "Dimension": 0, "Index_Fullness": 0,
        "Metric": "-", "Vector_Type": "-", "Cloud": "-", "Region": "-", "Ready_Status": "-",
    }]
    data["Namespace Details"]         = namespace_details if namespace_details else [{
        "name": "-", "Index": "-", "Namespace": "-", "Vector_Count": 0,
    }]


def metricCollector():
    data = {}
    data["plugin_version"]     = PLUGIN_VERSION
    data["heartbeat_required"] = HEARTBEAT
    data["units"]              = METRICS_UNITS
    data["tabs"]               = TABS

    if not PINECONE_API_KEY:
        data["status"] = 0
        data["msg"]    = "Pinecone API key is not configured"
        return data

    getIndexes(data)

    return data


def run(param):
    global PINECONE_API_KEY, PINECONE_API_VERSION

    PINECONE_API_KEY     = clean_quotes(param.get("api_key", ""))
    PINECONE_API_VERSION = clean_quotes(param.get("api_version", "2025-10")) or "2025-10"

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
    parser.add_argument("--api_key",     help="Pinecone API Key",                  default="")
    parser.add_argument("--api_version", help="Pinecone API Version header",       default="2025-10")
    args = parser.parse_args()

    PINECONE_API_KEY     = args.api_key
    PINECONE_API_VERSION = args.api_version

    print(json.dumps(metricCollector(), indent=2))
