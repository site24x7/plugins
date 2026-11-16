#!/usr/bin/python3

import time
import psutil
import socket
import json
import argparse
from psutil import cpu_count

def monitor_port_metrics(port, duration):
    num_cores = psutil.cpu_count()
    start_time = time.time()
    end_time = start_time + duration

    metrics = {
        "plugin_version": 1,
        "heartbeat_required": True,
        "Connection Latency": None,
        "Cpu Usage": 0,
        "Memory Usage": 0,
        "Active Connections": 0,
        "Connection Rate": 0,
        "Port Status Text": "closed",
        "Processes Count": 0,
        "Throughput Sent": 0, 
        "Throughput Received": 0,  
        "units":{
            "Connection Latency":"ms",
            "Cpu Usage":"%",
            "Memory Usage":"mb",
            "Throughput Sent": "bytes",
            "Throughput Received": "bytes"
        }
    }

    connections_established = 0

    initial_io = psutil.net_io_counters()

    while time.time() < end_time:
        latency_start = time.time()
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                if s.connect_ex(('localhost', port)) == 0:
                    metrics["Connection Latency"] = (time.time() - latency_start)*1000
                    connections_established += 1
                    metrics["Port Status Text"] = "open"
        except Exception as e:
            metrics["Port Status Text"] = "closed"
            metrics["status"] = 0
            metrics["msg"] = f"Error: {str(e)}"
            break

    # Update Port Status
    if metrics["Port Status Text"] == "open":
        metrics["Port Status"] = 1
    else:
        metrics["Port Status"] = 0

    processes = set() 
    for conn in psutil.net_connections(kind='inet'):
        if conn.laddr.port == port and conn.status == 'LISTEN':
            try:
                process = psutil.Process(conn.pid)
                processes.add(conn.pid)
                metrics["Cpu Usage"] += process.cpu_percent(interval=0.1) / num_cores                    
                metrics["Memory Usage"] += process.memory_info().rss / (1024 * 1024)
            except Exception:
                pass

    metrics["Processes Count"] = len(processes)

    metrics["Active Connections"] = sum(
        1 for conn in psutil.net_connections(kind='inet') if conn.laddr.port == port
    )

    final_io = psutil.net_io_counters()

    metrics["Throughput Sent"] = final_io.bytes_sent - initial_io.bytes_sent
    metrics["Throughput Received"] = final_io.bytes_recv - initial_io.bytes_recv

    metrics["Connection Rate"] = connections_established / duration

    if metrics["Port Status Text"] == "closed":
        metrics["status"] = 0
        metrics["msg"] = "Port is closed"

    return metrics

def main():
    parser = argparse.ArgumentParser(description="Monitor a port and gather metrics.")
    parser.add_argument("--port", type=int, required=True, help="The port number to monitor")
    
    args = parser.parse_args()
    port_to_monitor = args.port

    monitor_duration = 5

    metrics = monitor_port_metrics(port_to_monitor, monitor_duration)

    print(json.dumps(metrics, indent=4))

if __name__ == "__main__":
    main()
