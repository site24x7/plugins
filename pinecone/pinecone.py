#!/usr/bin/python3
import json
import time
import socket
import sys
import os
from concurrent.futures import ThreadPoolExecutor, as_completed, TimeoutError as FuturesTimeoutError

try:
    import requests
    _REQUESTS_IMPORT_ERROR = None
except Exception as _import_err:
    requests = None
    _REQUESTS_IMPORT_ERROR = str(_import_err)

socket.setdefaulttimeout(15)

PLUGIN_VERSION = 1
HEARTBEAT = "true"

PINECONE_LIST_INDEXES_URL = "https://api.pinecone.io/indexes"
PINECONE_PROMETHEUS_DISCOVERY_URL = "https://api.pinecone.io/prometheus/projects/{project_id}/metrics/discovery"

METRICS_UNITS = {

    "Database Available": "count",
    "HTTP Status": "count",
    "Total Indexes": "count",
    "Indexes Ready": "count",
    "Indexes Not Ready": "count",
    "Number Of Indexes Monitored": "count",

    "Total Vectors Stored": "count",
    "Total Namespaces": "count",
    "Largest Index Vector Count": "count",
    "Smallest Index Vector Count": "count",
    "Average Vector Count Per Index": "count",
    "Indexes With Zero Vectors": "count",

    "Serverless Indexes": "count",
    "Pod Based Indexes": "count",
    "Average Dimension Across Indexes": "count",
    "Unique Regions In Use": "count",
    "Unique Cloud Providers In Use": "count",

    "Average Index Fullness Percent": "percent",
    "Maximum Index Fullness Percent": "percent",

    "Indexes With Embedding Configured": "count",
    "Indexes With Deletion Protection Enabled": "count",

    "Indexes That Failed To Respond": "count",

    "Telemetry Available": "count",
    "Total Upsert Requests": "count",
    "Average Upsert Latency Milliseconds": "ms",
    "Total Read Units Consumed": "count",
    "Total Write Units Consumed": "count",
    "Average CPU Usage Percent": "percent",

    "Telemetry Vector Count": "count",
    "Telemetry Index Fullness Percent": "percent",

    "Total Data Plane Requests": "count",
    "Total Data Plane Errors": "count",
    "Data Plane Error Rate Percent": "percent",
    "Request Latency Min Milliseconds": "ms",
    "Request Latency Max Milliseconds": "ms",
    "Request Latency Avg Milliseconds": "ms",
    "Request Latency P50 Milliseconds": "ms",
    "Request Latency P90 Milliseconds": "ms",
    "Request Latency P95 Milliseconds": "ms",
    "Request Latency P99 Milliseconds": "ms",
    "Request Latency P999 Milliseconds": "ms",
    "Request Latency Sample Count": "count",

    "Query Requests": "count",
    "Fetch Requests": "count",
    "Update Requests": "count",
    "Delete Requests": "count",
    "List Requests": "count",
    "Query Requests Duration Milliseconds": "ms",
    "Fetch Requests Duration Milliseconds": "ms",
    "Update Requests Duration Milliseconds": "ms",
    "Delete Requests Duration Milliseconds": "ms",
    "Upsert Requests Duration Milliseconds": "ms",
    "List Requests Duration Milliseconds": "ms",
    "Total Storage Size Bytes": "bytes",
    "Total Records (Telemetry)": "count",


    "Indexes": {
        "Vector Count": "count",
        "Dimension": "count",
        "Index Fullness": "percent",
        "Ready Status": "count",
        "Is Serverless": "count",
        "Has Embedding Configured": "count",
        "Telemetry Vector Count": "count",
        "Telemetry Index Fullness Percent": "percent"
    }
}

TABS = {
    "Health Snapshot": {
        "order": 1,
        "tablist": [
            "Database Available",
            "HTTP Status",
            "Total Indexes",
            "Indexes Ready",
            "Indexes Not Ready",
            "Number Of Indexes Monitored"
        ]
    },
    "Capacity": {
        "order": 2,
        "tablist": [
            "Total Vectors Stored",
            "Total Namespaces",
            "Largest Index Vector Count",
            "Largest Index Name",
            "Smallest Index Vector Count",
            "Smallest Index Name",
            "Average Vector Count Per Index",
            "Indexes With Zero Vectors"
        ]
    },
    "Configuration": {
        "order": 3,
        "tablist": [
            "Serverless Indexes",
            "Pod Based Indexes",
            "Average Dimension Across Indexes",
            "Unique Regions In Use",
            "Regions In Use",
            "Unique Cloud Providers In Use",
            "Cloud Providers In Use"
        ]
    },
    "Fullness": {
        "order": 4,
        "tablist": [
            "Average Index Fullness Percent",
            "Maximum Index Fullness Percent"
        ]
    },
    "Embedding And Security": {
        "order": 5,
        "tablist": [
            "Indexes With Embedding Configured",
            "Embedding Models In Use",
            "Indexes With Deletion Protection Enabled"
        ]
    },
    "Performance And Reliability": {
        "order": 6,
        "tablist": [
            "Total Scan Time Seconds",
            "Average Index Response Time Seconds",
            "Indexes That Failed To Respond"
        ]
    },
    "Telemetry": {
        "order": 7,
        "tablist": [
            "Telemetry Available",
            "Total Upsert Requests",
            "Average Upsert Latency Milliseconds",
            "Total Read Units Consumed",
            "Total Write Units Consumed",
            "Average CPU Usage Percent",
            "Total Data Plane Requests",
            "Total Data Plane Errors",
            "Data Plane Error Rate Percent",
            "Total Storage Size Bytes",
            "Total Records (Telemetry)",
            "Telemetry Vector Count"
        ]
    },
    "Serverless Operations": {
        "order": 8,
        "tablist": [
            "Query Requests",
            "Fetch Requests",
            "Update Requests",
            "Delete Requests",
            "List Requests",
            "Query Requests Duration Milliseconds",
            "Fetch Requests Duration Milliseconds",
            "Update Requests Duration Milliseconds",
            "Delete Requests Duration Milliseconds",
            "Upsert Requests Duration Milliseconds",
            "List Requests Duration Milliseconds"
        ]
    },
    "Latency": {
        "order": 9,
        "tablist": [
            "Request Latency Min Milliseconds",
            "Request Latency Max Milliseconds",
            "Request Latency Avg Milliseconds",
            "Request Latency P50 Milliseconds",
            "Request Latency P90 Milliseconds",
            "Request Latency P95 Milliseconds",
            "Request Latency P99 Milliseconds",
            "Request Latency P999 Milliseconds",
            "Request Latency Sample Count"
        ]
    },
    "Indexes": {
        "order": 10,
        "tablist": [
            "Indexes"
        ]
    }
}


class pinecone:

    def __init__(self, args):

        self.maindata = {}
        self.maindata["plugin_version"] = PLUGIN_VERSION
        self.maindata["heartbeat_required"] = HEARTBEAT
        self.maindata["displayname"] = "Pinecone Monitor"
        self.maindata["units"] = METRICS_UNITS
        self.maindata["tabs"] = TABS
        self.maindata["s247config"] = {
            "childdiscovery": [
                "Indexes"
            ]
        }

        self.logsenabled = args.logs_enabled
        self.logtypename = args.log_type_name
        self.logfilepath = args.log_file_path

        self.api_key = self.clean_quotes(args.api_key)
        self.api_version = self.clean_quotes(args.api_version) or "2025-10"
        self.project_id = self.clean_quotes(args.project_id) or None

        self.headers = {
            "Api-Key": self.api_key,
            "Content-Type": "application/json",
            "X-Pinecone-Api-Version": self.api_version
        }

    def clean_quotes(self, value):
        if not value:
            return value
        value_str = str(value).strip()
        if value_str.startswith('"') and value_str.endswith('"'):
            return value_str[1:-1]
        if value_str.startswith("'") and value_str.endswith("'"):
            return value_str[1:-1]
        return value_str

    def mask_key_hint(self, api_key_raw):
        if not api_key_raw:
            return "api_key is empty/not configured"
        key = self.clean_quotes(api_key_raw)
        if key.lower() in ("your-pinecone-api-key", "none", ""):
            return "api_key looks like the placeholder value - set your real key in the cfg"
        return "api_key configured (len=%d, ends with '%s') - verify this matches a key from the correct Pinecone project" % (len(key), key[-4:])

    def request(self, method, url, data, payload=None, timeout=10, critical=True):
        response = None
        data["_transient"] = False
        try:
            if method == "POST":
                response = requests.post(url, headers=self.headers, json=payload if payload else {}, timeout=timeout)
            else:
                response = requests.get(url, headers=self.headers, timeout=timeout)
            response.raise_for_status()

        except requests.exceptions.HTTPError as err:
            if not critical:
                return None
            data["status"] = 0
            msg = "HTTP Error: " + str(err)
            if response is not None and response.status_code in (401, 403):
                msg += " | " + self.mask_key_hint(self.headers.get("Api-Key"))
            data["msg"] = msg
            return None

        except requests.exceptions.ConnectionError as err:
            data["_transient"] = True
            if not critical:
                return None
            data["status"] = 0
            data["msg"] = "Connection Error: " + str(err)
            return None

        except requests.exceptions.Timeout as err:
            data["_transient"] = True
            if not critical:
                return None
            data["status"] = 0
            data["msg"] = "Timeout Error: " + str(err)
            return None

        except Exception as err:
            if not critical:
                return None
            data["status"] = 0
            data["msg"] = str(err)
            return None

        return response

    def get_index_stats(self, host, data):
        clean_host = host.strip().rstrip("/")
        if not clean_host.startswith("http://") and not clean_host.startswith("https://"):
            clean_host = "https://" + clean_host
        url = clean_host + "/describe_index_stats"

        response = self.request("POST", url, data, payload={}, timeout=6, critical=False)
        if response is not None:
            return response

        time.sleep(0.5)
        return self.request("POST", url, data, payload={}, timeout=6, critical=False)

    def parse_prometheus_text(self, text):
        result = {}
        if not text:
            return result

        for line in text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            try:
                if "{" in line and "}" in line:
                    name_part, rest = line.split("{", 1)
                    labels_part, value_part = rest.rsplit("}", 1)
                    metric_name = name_part.strip()
                    value = float(value_part.strip().split()[0])

                    labels = {}
                    for pair in labels_part.split(","):
                        if "=" in pair:
                            k, v = pair.split("=", 1)
                            labels[k.strip()] = v.strip().strip('"')
                else:
                    parts = line.rsplit(None, 1)
                    if len(parts) != 2:
                        continue
                    metric_name = parts[0].strip()
                    value = float(parts[1].strip())
                    labels = {}

                result.setdefault(metric_name, []).append((labels, value))

            except (ValueError, IndexError):
                continue

        return result

    def fetch_telemetry(self, data, timeout=6, overall_budget=10):
        if not self.project_id:
            return None

        try:
            discovery_url = PINECONE_PROMETHEUS_DISCOVERY_URL.format(project_id=self.project_id)
            discovery_headers = {
                "Authorization": "Bearer " + self.api_key
            }

            discovery_response = requests.get(discovery_url, headers=discovery_headers, timeout=timeout)
            discovery_response.raise_for_status()
            targets_config = discovery_response.json()

            target_urls = []
            if isinstance(targets_config, list):
                for group in targets_config:
                    for target in group.get("targets", []):
                        target_url = target if target.startswith("http") else "https://" + target
                        target_urls.append(target_url)

            if not target_urls:
                return None

            target_urls = target_urls[:25]
            per_target_timeout = min(timeout, 5)

            def _fetch_one_target(target_url):
                try:
                    metrics_response = requests.get(
                        target_url if target_url.endswith("/metrics") else target_url.rstrip("/") + "/metrics",
                        headers=discovery_headers,
                        timeout=per_target_timeout,
                    )
                    metrics_response.raise_for_status()
                    return self.parse_prometheus_text(metrics_response.text)
                except Exception:
                    return None

            combined_metrics = {}
            max_workers = min(10, len(target_urls))
            executor = ThreadPoolExecutor(max_workers=max_workers)
            try:
                futures = [executor.submit(_fetch_one_target, url) for url in target_urls]
                try:
                    for future in as_completed(futures, timeout=overall_budget):
                        parsed = future.result()
                        if parsed:
                            for name, samples in parsed.items():
                                combined_metrics.setdefault(name, []).extend(samples)
                except FuturesTimeoutError:
                    pass
            finally:
                executor.shutdown(wait=False)

            return combined_metrics if combined_metrics else None

        except Exception:
            return None

    def collect_index_stats(self, indexes, data):
        stats_by_name = {}
        max_workers = min(10, len(indexes)) if indexes else 1
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_name = {}
            for idx in indexes:
                host = idx.get("host", "")
                name = idx.get("name", "unknown")
                if host:
                    idx_start = time.perf_counter()
                    future = executor.submit(self.get_index_stats, host, data)
                    future_to_name[future] = (name, idx_start)

            for future in as_completed(future_to_name):
                name, idx_start = future_to_name[future]
                idx_elapsed_sec = round(time.perf_counter() - idx_start, 2)
                try:
                    stats_by_name[name] = (future.result(), idx_elapsed_sec)
                except Exception:
                    stats_by_name[name] = (None, idx_elapsed_sec)

        return stats_by_name

    def build_index_rows(self, indexes, stats_by_name, data):
        indexes_ready = 0
        indexes_not_ready = 0
        serverless_count = 0
        pod_count = 0
        total_vectors_all = 0
        total_namespaces_all = 0
        largest_index_name = ""
        largest_index_vectors = 0
        smallest_index_name = ""
        smallest_index_vectors = None
        response_times_sec = []
        index_rows = []
        stats_failed_count = 0

        dimensions = []
        fullness_values = []
        indexes_with_zero_vectors = 0

        regions_seen = set()
        cloud_providers_seen = set()
        embedding_models_seen = set()
        deletion_protection_count = 0
        embedding_configured_count = 0

        for idx in indexes:

            index_name = idx.get("name", "unknown")
            host = idx.get("host", "")
            status = idx.get("status", {})
            ready = bool(status.get("ready", False))
            spec = idx.get("spec", {})

            if ready:
                indexes_ready += 1
            else:
                indexes_not_ready += 1

            serverless = spec.get("serverless", {})
            pod = spec.get("pod", {})
            is_serverless = bool(serverless)

            if serverless:
                serverless_count += 1
                region = serverless.get("region")
                cloud = serverless.get("cloud")
                if region:
                    regions_seen.add(region)
                if cloud:
                    cloud_providers_seen.add(cloud)
            elif pod:
                pod_count += 1
                env = pod.get("environment")
                if env:
                    regions_seen.add(env)

            has_deletion_protection = idx.get("deletion_protection") == "enabled"
            if has_deletion_protection:
                deletion_protection_count += 1

            embed = idx.get("embed", {}) or {}
            has_embedding = bool(embed)
            if embed:
                embedding_configured_count += 1
                model = embed.get("model")
                if model:
                    embedding_models_seen.add(model)

            vector_count = 0
            dimension = idx.get("dimension", 0)
            index_fullness = 0
            namespace_count_this_index = 0

            if host:
                stats_response, idx_elapsed_sec = stats_by_name.get(index_name, (None, 0))

                if stats_response is not None:
                    response_times_sec.append(idx_elapsed_sec)
                    stats_data = stats_response.json()
                    vector_count = stats_data.get("totalVectorCount", 0)
                    dimension = stats_data.get("dimension", dimension)
                    index_fullness = round(stats_data.get("indexFullness", 0) * 100, 4)
                    namespace_count_this_index = len(stats_data.get("namespaces", {}))
                    total_namespaces_all += namespace_count_this_index
                else:
                    stats_failed_count += 1
            else:
                stats_failed_count += 1

            total_vectors_all += vector_count

            if dimension:
                dimensions.append(dimension)
            fullness_values.append(index_fullness)

            if vector_count == 0:
                indexes_with_zero_vectors += 1

            if vector_count > largest_index_vectors:
                largest_index_vectors = vector_count
                largest_index_name = index_name

            if smallest_index_vectors is None or vector_count < smallest_index_vectors:
                smallest_index_vectors = vector_count
                smallest_index_name = index_name

            if len(index_rows) < 25:
                index_rows.append({
                    "name": index_name,
                    "Vector Count": vector_count,
                    "Dimension": dimension,
                    "Index Fullness": index_fullness,
                    "Ready Status": int(ready),
                    "Is Serverless": int(is_serverless),
                    "Has Embedding Configured": int(has_embedding),
                    "Telemetry Vector Count": 0,
                    "Telemetry Index Fullness Percent": 0,
                })

        count = len(indexes)

        data["Indexes Ready"] = indexes_ready
        data["Indexes Not Ready"] = indexes_not_ready
        data["Serverless Indexes"] = serverless_count
        data["Pod Based Indexes"] = pod_count
        data["Total Vectors Stored"] = total_vectors_all
        data["Total Namespaces"] = total_namespaces_all
        data["Largest Index Vector Count"] = largest_index_vectors
        data["Largest Index Name"] = largest_index_name if largest_index_name else "None"
        data["Smallest Index Vector Count"] = smallest_index_vectors if smallest_index_vectors is not None else 0
        data["Smallest Index Name"] = smallest_index_name if smallest_index_name else "None"

        data["Average Vector Count Per Index"] = round(total_vectors_all / count, 2) if count else 0
        data["Indexes With Zero Vectors"] = indexes_with_zero_vectors

        data["Average Dimension Across Indexes"] = round(sum(dimensions) / len(dimensions), 2) if dimensions else 0

        data["Average Index Fullness Percent"] = round(sum(fullness_values) / len(fullness_values), 4) if fullness_values else 0
        data["Maximum Index Fullness Percent"] = max(fullness_values) if fullness_values else 0

        data["Unique Regions In Use"] = len(regions_seen)
        data["Regions In Use"] = ", ".join(sorted(regions_seen)) if regions_seen else "None"
        data["Unique Cloud Providers In Use"] = len(cloud_providers_seen)
        data["Cloud Providers In Use"] = ", ".join(sorted(cloud_providers_seen)) if cloud_providers_seen else "None"

        data["Indexes With Embedding Configured"] = embedding_configured_count
        data["Embedding Models In Use"] = ", ".join(sorted(embedding_models_seen)) if embedding_models_seen else "None"
        data["Indexes With Deletion Protection Enabled"] = deletion_protection_count

        data["Indexes That Failed To Respond"] = stats_failed_count

        data["Average Index Response Time Seconds"] = round(sum(response_times_sec) / len(response_times_sec), 2) if response_times_sec else 0

        return index_rows, count

    def ingest_telemetry(self, data, index_rows):
        if not self.project_id:
            return

        try:
            telemetry = self.fetch_telemetry(data)
            if not telemetry:
                return

            data["Telemetry Available"] = 1

            upsert_counts = telemetry.get("pinecone_db_op_upsert_count", [])
            data["Total Upsert Requests"] = int(sum(v for _, v in upsert_counts))

            upsert_duration_sum = sum(v for _, v in telemetry.get("pinecone_db_op_upsert_duration_sum", []))
            upsert_count_total = sum(v for _, v in upsert_counts)
            if upsert_count_total > 0:
                data["Average Upsert Latency Milliseconds"] = round((upsert_duration_sum / upsert_count_total) * 1000, 2)
            data["Upsert Requests Duration Milliseconds"] = round(upsert_duration_sum, 2)

            read_units = telemetry.get("pinecone_db_read_unit_count", [])
            data["Total Read Units Consumed"] = int(sum(v for _, v in read_units))

            write_units = telemetry.get("pinecone_db_write_unit_count", [])
            data["Total Write Units Consumed"] = int(sum(v for _, v in write_units))

            cpu_samples = telemetry.get("pinecone_db_drn_cpu_usage_percent", [])
            if cpu_samples:
                data["Average CPU Usage Percent"] = round(sum(v for _, v in cpu_samples) / len(cpu_samples), 2)

            vector_count_samples = telemetry.get("pinecone_vector_count", [])
            data["Telemetry Vector Count"] = int(sum(v for _, v in vector_count_samples))

            fullness_samples = telemetry.get("pinecone_index_fullness", [])
            if fullness_samples:
                data["Telemetry Index Fullness Percent"] = round(
                    (sum(v for _, v in fullness_samples) / len(fullness_samples)) * 100, 4
                )

            vector_by_index = {}
            for labels, value in vector_count_samples:
                idx_label = labels.get("index_name") or labels.get("index")
                if idx_label:
                    vector_by_index[idx_label] = vector_by_index.get(idx_label, 0) + value

            fullness_by_index = {}
            for labels, value in fullness_samples:
                idx_label = labels.get("index_name") or labels.get("index")
                if idx_label:
                    fullness_by_index[idx_label] = value

            if vector_by_index or fullness_by_index:
                for row in index_rows:
                    row_name = row.get("name")
                    if row_name in vector_by_index:
                        row["Telemetry Vector Count"] = int(vector_by_index[row_name])
                    if row_name in fullness_by_index:
                        row["Telemetry Index Fullness Percent"] = round(fullness_by_index[row_name] * 100, 4)

            request_count_samples = telemetry.get("pinecone_request_count_total", [])
            data["Total Data Plane Requests"] = int(sum(v for _, v in request_count_samples))

            request_error_samples = telemetry.get("pinecone_request_error_count_total", [])
            data["Total Data Plane Errors"] = int(sum(v for _, v in request_error_samples))

            if data["Total Data Plane Requests"] > 0:
                data["Data Plane Error Rate Percent"] = round(
                    (data["Total Data Plane Errors"] / data["Total Data Plane Requests"]) * 100, 4
                )

            latency_field_map = {
                "pinecone_request_latency_seconds_min": "Request Latency Min Milliseconds",
                "pinecone_request_latency_seconds_max": "Request Latency Max Milliseconds",
                "pinecone_request_latency_seconds_avg": "Request Latency Avg Milliseconds",
                "pinecone_request_latency_seconds_50percentile": "Request Latency P50 Milliseconds",
                "pinecone_request_latency_seconds_90percentile": "Request Latency P90 Milliseconds",
                "pinecone_request_latency_seconds_95percentile": "Request Latency P95 Milliseconds",
                "pinecone_request_latency_seconds_99percentile": "Request Latency P99 Milliseconds",
                "pinecone_request_latency_seconds_99.9percentile": "Request Latency P999 Milliseconds",
            }
            for metric_name, field_name in latency_field_map.items():
                samples = telemetry.get(metric_name, [])
                if samples:
                    avg_seconds = sum(v for _, v in samples) / len(samples)
                    data[field_name] = round(avg_seconds * 1000, 4)

            latency_count_samples = telemetry.get("pinecone_request_latency_seconds_count", [])
            data["Request Latency Sample Count"] = int(sum(v for _, v in latency_count_samples))

            op_count_field_map = {
                "pinecone_db_op_query_count": "Query Requests",
                "pinecone_db_op_fetch_count": "Fetch Requests",
                "pinecone_db_op_update_count": "Update Requests",
                "pinecone_db_op_delete_count": "Delete Requests",
                "pinecone_db_op_list_count": "List Requests",
            }
            for metric_name, field_name in op_count_field_map.items():
                data[field_name] = int(sum(v for _, v in telemetry.get(metric_name, [])))

            op_duration_field_map = {
                "pinecone_db_op_query_duration_sum": "Query Requests Duration Milliseconds",
                "pinecone_db_op_fetch_duration_sum": "Fetch Requests Duration Milliseconds",
                "pinecone_db_op_update_duration_sum": "Update Requests Duration Milliseconds",
                "pinecone_db_op_delete_duration_sum": "Delete Requests Duration Milliseconds",
                "pinecone_db_op_list_duration_sum": "List Requests Duration Milliseconds",
            }
            for metric_name, field_name in op_duration_field_map.items():
                data[field_name] = round(sum(v for _, v in telemetry.get(metric_name, [])), 2)

            storage_samples = telemetry.get("pinecone_db_storage_size_bytes", [])
            data["Total Storage Size Bytes"] = int(sum(v for _, v in storage_samples))

            record_samples = telemetry.get("pinecone_db_record_total", [])
            data["Total Records (Telemetry)"] = int(sum(v for _, v in record_samples))

        except Exception:
            pass

    def metriccollector(self):
        data = self.maindata

        data["Telemetry Available"] = 0
        data["Total Upsert Requests"] = 0
        data["Average Upsert Latency Milliseconds"] = 0
        data["Total Read Units Consumed"] = 0
        data["Total Write Units Consumed"] = 0
        data["Average CPU Usage Percent"] = 0
        data["Telemetry Vector Count"] = 0
        data["Telemetry Index Fullness Percent"] = 0
        data["Total Data Plane Requests"] = 0
        data["Total Data Plane Errors"] = 0
        data["Data Plane Error Rate Percent"] = 0
        data["Request Latency Min Milliseconds"] = 0
        data["Request Latency Max Milliseconds"] = 0
        data["Request Latency Avg Milliseconds"] = 0
        data["Request Latency P50 Milliseconds"] = 0
        data["Request Latency P90 Milliseconds"] = 0
        data["Request Latency P95 Milliseconds"] = 0
        data["Request Latency P99 Milliseconds"] = 0
        data["Request Latency P999 Milliseconds"] = 0
        data["Request Latency Sample Count"] = 0
        data["Query Requests"] = 0
        data["Fetch Requests"] = 0
        data["Update Requests"] = 0
        data["Delete Requests"] = 0
        data["List Requests"] = 0
        data["Query Requests Duration Milliseconds"] = 0
        data["Fetch Requests Duration Milliseconds"] = 0
        data["Update Requests Duration Milliseconds"] = 0
        data["Delete Requests Duration Milliseconds"] = 0
        data["Upsert Requests Duration Milliseconds"] = 0
        data["List Requests Duration Milliseconds"] = 0
        data["Total Storage Size Bytes"] = 0
        data["Total Records (Telemetry)"] = 0

        try:

            start_time = time.perf_counter()

            list_response = None
            list_attempts = 2
            for _attempt in range(list_attempts):
                list_response = self.request("GET", PINECONE_LIST_INDEXES_URL, data, timeout=6, critical=True)
                if list_response is not None:
                    break
                if not data.get("_transient"):
                    break
                if _attempt < list_attempts - 1:
                    data.pop("status", None)
                    data.pop("msg", None)
                    time.sleep(1)

            if list_response is None:
                data.pop("_transient", None)
                return data

            list_body = list_response.json()
            indexes = list_body.get("indexes", [])

            data["Database Available"] = 1
            data["HTTP Status"] = list_response.status_code
            data["Total Indexes"] = len(indexes)

            stats_by_name = self.collect_index_stats(indexes, data)
            index_rows, count = self.build_index_rows(indexes, stats_by_name, data)

            data["Indexes"] = index_rows
            data["Number Of Indexes Monitored"] = len(index_rows)

            self.ingest_telemetry(data, index_rows)

            data["Total Scan Time Seconds"] = round(time.perf_counter() - start_time, 2)

            data["status"] = 1
            data["msg"] = "No indexes found in this project." if count == 0 else "Metrics collected successfully for %d index(es)." % count

        except Exception as err:
            data["status"] = 0
            data["msg"] = str(err)

        data.pop("_transient", None)
        return data


if __name__ == "__main__":

    try:

        import argparse

        parser = argparse.ArgumentParser()
        parser.add_argument("--logs_enabled", default="False")
        parser.add_argument("--log_type_name", nargs="?", default=None)
        parser.add_argument("--log_file_path", nargs="?", default=None)
        parser.add_argument("--api_key", nargs="?", default=None)
        parser.add_argument("--api_version", nargs="?", default="2025-10")
        parser.add_argument("--project_id", nargs="?", default=None,
                             help="Optional. Only needed for the Telemetry tab (Prometheus metrics) - "
                                  "requires a Standard or Enterprise Pinecone plan. Leave unset to skip it.")

        args, _unknown = parser.parse_known_args()

        if requests is None:
            print(json.dumps({
                "plugin_version": PLUGIN_VERSION,
                "heartbeat_required": HEARTBEAT,
                "displayname": "Pinecone Monitor",
                "status": 0,
                "msg": "The 'requests' Python library is not installed/importable in this environment ("
                       + str(_REQUESTS_IMPORT_ERROR)
                       + "). Run: pip install requests  using the same Python interpreter the Site24x7 agent invokes."
            }, indent=4))

        elif not args.api_key:
            print(json.dumps({
                "plugin_version": PLUGIN_VERSION,
                "heartbeat_required": HEARTBEAT,
                "displayname": "Pinecone Monitor",
                "status": 0,
                "msg": "Missing required plugin parameter: api_key. Check that the .cfg file on the agent has this key set."
            }, indent=4))

        else:
            obj = pinecone(args)

            executor = ThreadPoolExecutor(max_workers=1)
            future = executor.submit(obj.metriccollector)
            try:
                result = future.result(timeout=30)
                print(json.dumps(result, indent=4))
                sys.stdout.flush()
            except FuturesTimeoutError:
                print(json.dumps({
                    "plugin_version": PLUGIN_VERSION,
                    "heartbeat_required": HEARTBEAT,
                    "displayname": "Pinecone Monitor",
                    "status": 0,
                    "msg": "Pinecone API call did not respond within 30 seconds - check network connectivity or Pinecone service status."
                }, indent=4))
                sys.stdout.flush()
                os._exit(0)

    except SystemExit:
        print(json.dumps({
            "plugin_version": PLUGIN_VERSION,
            "heartbeat_required": HEARTBEAT,
            "displayname": "Pinecone Monitor",
            "status": 0,
            "msg": "Argument parsing failed - check the parameters configured in the .cfg file."
        }, indent=4))
        sys.stdout.flush()

    except Exception as top_level_err:
        print(json.dumps({
            "plugin_version": PLUGIN_VERSION,
            "heartbeat_required": HEARTBEAT,
            "displayname": "Pinecone Monitor",
            "status": 0,
            "msg": "Unexpected top-level error: " + str(top_level_err)
        }, indent=4))
        sys.stdout.flush()
