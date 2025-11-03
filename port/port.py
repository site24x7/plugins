#!/usr/bin/python3
import json
import os
import sys
import time
import socket
import argparse

PLUGIN_VERSION = "1"
HEARTBEAT = "true"

plugin_rs = {}
metric_units = {
    "Connection Latency": "ms",
    "Cpu Usage": "%",
    "Memory Usage": "mb",
    "Throughput Sent": "bytes",
    "Throughput Received": "bytes"
}
plugin_rs['plugin_version'] = PLUGIN_VERSION
plugin_rs['heartbeat_required'] = HEARTBEAT

try:
    plugin_script_path = os.path.dirname(os.path.realpath(__file__))
    sys.path.insert(0, plugin_script_path)

    try:
        import psutil
    except Exception as e:
        plugin_rs['status'] = 0
        plugin_rs['msg'] = f"psutil module not installed or failed to load: {str(e)}"
        print(json.dumps(plugin_rs, indent=4))
        sys.exit(1)

    # -------------------------------
    # Argument Parsing (instead of cfg file)
    # -------------------------------
    parser = argparse.ArgumentParser(description="Monitor a port and gather metrics.")
    parser.add_argument("--port", type=int, required=True, help="The port number to monitor")
    parser.add_argument("--duration", type=int, default=5, help="Duration to monitor in seconds (default: 5)")
    args = parser.parse_args()

    port_to_monitor = args.port
    duration = args.duration
    # -------------------------------

    # Metrics dictionary
    metrics = {
        "plugin_version": PLUGIN_VERSION,
        "heartbeat_required": HEARTBEAT,
        "units": metric_units,
        "Connection Latency": 0,
        "Cpu Usage": 0,
        "Memory Usage": 0,
        "Active Connections": 0,
        "Connection Rate": 0,
        "Port Status Text": "closed",
        "Processes Count": 0,
        "Throughput Sent": 0,
        "Throughput Received": 0,
    }

    connections_established = 0
    initial_io = psutil.net_io_counters()

    start_time = time.time()
    end_time = start_time + duration

    while time.time() < end_time:
        latency_start = time.time()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if s.connect_ex(('localhost', port_to_monitor)) == 0:
                    metrics["Connection Latency"] = (time.time() - latency_start) * 1000
                    connections_established += 1
                    metrics["Port Status Text"] = "open"
        except Exception:
            metrics["Port Status Text"] = "closed"

    # Update Port Status
    metrics["Port Status"] = 1 if metrics["Port Status Text"] == "open" else 0

    # Processes info
    num_cores = psutil.cpu_count()
    processes = set()
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port_to_monitor and conn.status == 'LISTEN':
            try:
                process = psutil.Process(conn.pid)
                processes.add(conn.pid)
                metrics["Cpu Usage"] += process.cpu_percent(interval=0.1) / num_cores
                metrics["Memory Usage"] += process.memory_info().rss / (1024 * 1024)
            except Exception:
                pass

    metrics["Processes Count"] = len(processes)
    metrics["Active Connections"] = sum(
        1 for conn in psutil.net_connections(kind='inet') if conn.laddr.port == port_to_monitor
    )

    final_io = psutil.net_io_counters()
    metrics["Throughput Sent"] = final_io.bytes_sent - initial_io.bytes_sent
    metrics["Throughput Received"] = final_io.bytes_recv - initial_io.bytes_recv
    metrics["Connection Rate"] = connections_established / duration

    if metrics["Port Status Text"] == "closed":
        metrics["msg"] = "Port is closed"
    else:
        metrics["msg"] = "Port is open"

    plugin_rs.update(metrics)

except Exception as e:
    plugin_rs['status'] = 0
    plugin_rs['msg'] = str(e)

print(json.dumps(plugin_rs, indent=4))
