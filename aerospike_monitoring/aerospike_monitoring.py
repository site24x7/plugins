#!/usr/bin/python3
import json

PLUGIN_VERSION = 1
HEARTBEAT = True

HOSTNAME = 'localhost'
PORT = '3000'
TLS_ENABLE = 'false'
TLS_NAME = 'None'
CAFILE = 'None'
SSL_VERIFY = 'false'
USERNAME = 'None'
PASSWORD = 'None'

METRICS_UNITS = {
    'Cluster Clock Skew': 'min',
    'Process CPU': '%',
    'Heap Efficiency': '%',
    'Heap Allocated': 'MB',
    'Heap Active': 'MB',
    'Heap Mapped': 'MB',
    'Nodes': {
        'Process CPU': '%',
        'Heap Efficiency': '%',
    },
    'Namespaces': {
        'Data Used': '%',
        'Data Avail': '%',
    }
}

summary_metrics = {
    'client_connections': 'Client Connections',
    'cluster_size': 'Cluster Size',
    'rw_in_progress': 'Read Write In Progress',
    'process_cpu_pct': 'Process CPU',
    'cluster_generation': 'Cluster Generation',
    'cluster_clock_skew_ms': 'Cluster Clock Skew',
    'long_queries_active': 'Long Queries Active',
}

tab_metrics = {
    'System Performance': {
        'heap_efficiency_pct': 'Heap Efficiency',
        'heap_allocated_kbytes': 'Heap Allocated',
        'heap_active_kbytes': 'Heap Active',
        'heap_mapped_kbytes': 'Heap Mapped',
        'threads_pool_active': 'Threads Pool Active',
        'threads_detached': 'Threads Detached',
        'threads_joinable': 'Threads Joinable',
    },
    'Connections': {
        'client_connections_opened': 'Client Connections Opened',
        'client_connections_closed': 'Client Connections Closed',
        'admin_connections': 'Admin Connections',
        'admin_connections_opened': 'Admin Connections Opened',
        'admin_connections_closed': 'Admin Connections Closed',
        'heartbeat_connections': 'Heartbeat Connections',
        'heartbeat_connections_opened': 'Heartbeat Connections Opened',
        'heartbeat_connections_closed': 'Heartbeat Connections Closed',
        'fabric_connections': 'Fabric Connections',
        'fabric_connections_opened': 'Fabric Connections Opened',
        'fabric_connections_closed': 'Fabric Connections Closed',
    },
    'Operations': {
        'batch_index_complete': 'Batch Index Complete',
        'batch_index_error': 'Batch Index Error',
        'batch_index_timeout': 'Batch Index Timeout',
        'proxy_in_progress': 'Proxy In Progress',
        'objects': 'Objects',
        'tombstones': 'Tombstones',
        'migrate_partitions_remaining': 'Migrate Partitions Remaining',
        'demarshal_error': 'Demarshal Error',
        'early_tsvc_client_error': 'Early Transaction Service Error',
        'reaped_fds': 'Reaped File Descriptors',
        'info_complete': 'Info Requests Complete',
        'fabric_rw_recv_rate': 'Fabric Read Write Receive Rate',
        'fabric_rw_send_rate': 'Fabric Read Write Send Rate',
        'deprecated_requests': 'Deprecated Requests',
        'tree_gc_queue': 'Tree GC Queue',
    },
}

config_metrics = {
    'threads_pool_total': ('Threads Pool Total', 'threads'),
    'uptime': ('Uptime', 'Minutes'),
    'cluster_key': ('Cluster Key', ''),
    'time_since_rebalance': ('Time Since Rebalance', 'Minutes'),
    'cluster_clock_skew_stop_writes_sec': ('Cluster Clock Skew Stop Writes', 'Minutes'),
}

node_child_metrics = {
    'client_connections': 'Client Connections',
    'process_cpu_pct': 'Process CPU',
    'heap_efficiency_pct': 'Heap Efficiency',
    'rw_in_progress': 'Read Write In Progress',
    'objects': 'Objects',
    'tombstones': 'Tombstones',
    'batch_index_error': 'Batch Index Error',
    'migrate_partitions_remaining': 'Migrate Partitions Remaining',
    'long_queries_active': 'Long Queries Active',
    'demarshal_error': 'Demarshal Error',
}

namespace_num_metrics = {
    'objects': 'Objects',
    'master_objects': 'Master Objects',
    'dead_partitions': 'Dead Partitions',
    'unavailable_partitions': 'Unavailable Partitions',
    'client_read_error': 'Client Read Error',
    'client_write_error': 'Client Write Error',
    'client_delete_error': 'Client Delete Error',
    'client_udf_error': 'Client UDF Error',
    'expired_objects': 'Expired Objects',
    'data_used_pct': 'Data Used',
    'data_avail_pct': 'Data Avail',
    'pi_query_aggr_error': 'Primary Index Query Aggregation Error',
}

namespace_bool_metrics = {
    'stop_writes': 'Stop Writes',
    'clock_skew_stop_writes': 'Clock Skew Stop Writes',
}

cluster_bool_metrics = {
    'cluster_integrity': 'Cluster Integrity',
    'cluster_is_member': 'Cluster Is Member',
    'migrate_allowed': 'Migrate Allowed',
    'failed_best_practices': 'Failed Best Practices',
}


def is_true(value):
    return str(value).strip().lower() in ['true', 'yes', '1']


def is_none(value):
    return value is None or str(value).strip().lower() in ['none', '']


def parse_response(response):
    result = {}
    for item in response.split(';'):
        if '=' in item:
            key, value = item.split('=', 1)
            result[key.strip()] = value.strip()
    return result


def safe_int(value, default=-1):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default


class Aerospike:

    def __init__(self, args):
        self.maindata = {}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required'] = HEARTBEAT
        self.maindata['units'] = METRICS_UNITS

        self.hostname = args.hostname
        self.port = int(args.port)
        self.tls_enable = args.tls_enable
        self.tls_name = args.tls_name
        self.cafile = args.cafile
        self.ssl_verify = args.ssl_verify
        self.username = args.username
        self.password = args.password

        if is_none(self.username):
            self.username = None
        if is_none(self.password):
            self.password = None

    def connect(self):
        import aerospike

        if is_true(self.tls_enable):
            tls_config = {'enable': True}

            if is_true(self.ssl_verify):
                if not is_none(self.cafile):
                    tls_config['cafile'] = self.cafile

            if not is_none(self.tls_name):
                hosts = (self.hostname, self.port, self.tls_name)
            else:
                hosts = (self.hostname, self.port)

            config = {
                'hosts': [hosts],
                'tls': tls_config
            }
        else:
            hosts = (self.hostname, self.port)
            config = {
                'hosts': [hosts]
            }

        if self.username and self.password:
            config['user'] = self.username
            config['password'] = self.password

        client = aerospike.client(config).connect()
        return client

    def collect_server_metrics(self, client):
        try:
            stats_data = client.info_all("statistics")

            for node, (err, res) in stats_data.items():
                if res is not None:
                    parsed = parse_response(res)

                    for raw, display in summary_metrics.items():
                        self.maindata[display] = safe_int(parsed.get(raw))

                    for tab_name, metrics_map in tab_metrics.items():
                        for raw, display in metrics_map.items():
                            self.maindata[display] = safe_int(parsed.get(raw))

                    clock_skew = self.maindata.get('Cluster Clock Skew', -1)
                    if clock_skew >= 0:
                        self.maindata['Cluster Clock Skew'] = round(clock_skew / 60000, 2)

                    for key in ['Heap Allocated', 'Heap Active', 'Heap Mapped']:
                        val = self.maindata.get(key, -1)
                        if val >= 0:
                            self.maindata[key] = round(val / 1024, 2)

                    for raw, (display, unit) in config_metrics.items():
                        val = parsed.get(raw)
                        if val is not None:
                            if unit == 'Minutes':
                                self.maindata[display] = f"{round(int(val) / 60, 2)} {unit}"
                            elif unit:
                                self.maindata[display] = f"{val} {unit}"
                            else:
                                self.maindata[display] = val
                        else:
                            self.maindata[display] = '-'

                    for raw, display in cluster_bool_metrics.items():
                        val = parsed.get(raw)
                        self.maindata[display] = val if val in ['true', 'false'] else '-'

                    break

            return stats_data

        except Exception as e:
            self.maindata['msg'] = str(e)
            self.maindata['status'] = 0
            return None

    def collect_node_metrics(self, client, stats_data):
        try:
            if not stats_data:
                return

            node_addr_map = {}
            try:
                svc_data = client.info_all("service")
                for node_id, (err, res) in svc_data.items():
                    if res:
                        node_addr_map[node_id] = res.strip()
            except Exception:
                pass

            node_list = []
            for node_id, (err, res) in stats_data.items():
                node_name = node_addr_map.get(node_id, f"{self.hostname}:{self.port}")
                node_name = node_name.replace('.', '_').replace(':', '_')
                if res is not None:
                    parsed = parse_response(res)
                    node_entry = {'name': node_name}

                    for raw, display in node_child_metrics.items():
                        node_entry[display] = safe_int(parsed.get(raw))

                    node_list.append(node_entry)
                else:
                    node_entry = {'name': node_name}
                    for raw, display in node_child_metrics.items():
                        node_entry[display] = -1
                    node_list.append(node_entry)

            if node_list:
                self.maindata['Nodes'] = node_list

        except Exception as e:
            self.maindata['msg'] = str(e)
            self.maindata['status'] = 0

    def collect_namespace_metrics(self, client):
        try:
            ns_data = client.info_all("namespaces")
            namespaces = set()
            for node, (err, res) in ns_data.items():
                if res:
                    for ns in res.strip().split(';'):
                        ns = ns.strip()
                        if ns:
                            namespaces.add(ns)

            namespace_list = []
            for ns in sorted(namespaces):
                try:
                    ns_stats = client.info_all(f"namespace/{ns}")
                    for node, (err, res) in ns_stats.items():
                        if res is not None:
                            parsed = parse_response(res)
                            ns_entry = {'name': ns}

                            for raw, display in namespace_num_metrics.items():
                                ns_entry[display] = safe_int(parsed.get(raw))

                            for raw, display in namespace_bool_metrics.items():
                                val = parsed.get(raw)
                                ns_entry[display] = val if val in ['true', 'false'] else '-'

                            namespace_list.append(ns_entry)
                            break

                except Exception:
                    ns_entry = {'name': ns}
                    for raw, display in namespace_num_metrics.items():
                        ns_entry[display] = -1
                    for raw, display in namespace_bool_metrics.items():
                        ns_entry[display] = '-'
                    namespace_list.append(ns_entry)

            if namespace_list:
                self.maindata['Namespaces'] = namespace_list

        except Exception as e:
            self.maindata['msg'] = str(e)
            self.maindata['status'] = 0

    def metriccollector(self):
        try:
            import aerospike
        except Exception as e:
            self.maindata['msg'] = str(e)
            self.maindata['status'] = 0
            return self.maindata

        try:
            client = self.connect()

            try:
                stats_data = self.collect_server_metrics(client)
                self.collect_node_metrics(client, stats_data)
                self.collect_namespace_metrics(client)
            finally:
                client.close()

        except Exception as e:
            self.maindata['msg'] = str(e)
            self.maindata['status'] = 0

        self.maindata['tabs'] = {
            'Nodes': {
                'order': 1,
                'tablist': ['Nodes']
            },
            'Namespaces': {
                'order': 2,
                'tablist': ['Namespaces']
            },
            'System Performance': {
                'order': 3,
                'tablist': list(tab_metrics['System Performance'].values())
            },
            'Connections': {
                'order': 4,
                'tablist': list(tab_metrics['Connections'].values())
            },
            'Operations': {
                'order': 5,
                'tablist': list(tab_metrics['Operations'].values())
            },
        }

        self.maindata['s247config'] = {
            'childdiscovery': ['Nodes', 'Namespaces']
        }

        return self.maindata


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', help='Hostname of Aerospike', default=HOSTNAME)
    parser.add_argument('--port', help='Port number for Aerospike', default=PORT)
    parser.add_argument('--tls_enable', help='Enable TLS (true/false/yes/no)', default=TLS_ENABLE)
    parser.add_argument('--tls_name', help='TLS name of Aerospike', default=TLS_NAME)
    parser.add_argument('--cafile', help='CA file path for TLS', default=CAFILE)
    parser.add_argument('--ssl_verify', help='Verify SSL certificate (true/false/yes/no)', default=SSL_VERIFY)
    parser.add_argument('--username', help='Username for Aerospike', default=USERNAME)
    parser.add_argument('--password', help='Password for Aerospike', default=PASSWORD)
    args = parser.parse_args()

    obj = Aerospike(args)
    result = obj.metriccollector()
    print(json.dumps(result, indent=4))
