#!/usr/bin/python
import json
import argparse
import subprocess
import sys

PLUGIN_VERSION = 1
HEARTBEAT = True

METRIC_UNITS = {
    'speed': 'Mbps',
    'uptime': 's',
    'downtime': 's',
    'obstructions': 'count',
    'dish_state': '',
    'latency': 'ms',
    'downlink_throughput_bps': 'bps',
    'uplink_throughput_bps': 'bps',
    'ping_latency_ms': 'ms',
    'ping_drop_rate': '%',
    'power_watts': 'W',
    'snr_good': 'dB'
}

def run_starlink_grpc_json(starlink_grpc_path='starlink_grpc', dish_address='localhost'):
    try:
        proc = subprocess.run(
            [starlink_grpc_path, 'dish_stats', '--address', dish_address, '--json'],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10, check=True)
        return json.loads(proc.stdout.decode())
    except Exception as e:
        raise Exception("Failed to run starlink_grpc: {}".format(e))

def get_metrics(data):
    metrics = {}
    metrics['speed'] = data.get('download_throughput_bps', 0) / 125000 if 'download_throughput_bps' in data else 0  
    metrics['uptime'] = int(data.get('uptime', 0))
    metrics['downtime'] = int(data.get('total_downtime', 0)) if 'total_downtime' in data else int(data.get('downtime', 0))
    metrics['obstructions'] = int(data.get('obstruction_stats', {}).get('fraction_obstructed', 0) * 100) if 'obstruction_stats' in data else 0
    metrics['dish_state'] = str(data.get('state', 'unknown'))
    metrics['latency'] = float(data.get('latency_ms', 0)) if 'latency_ms' in data else 0
    metrics['downlink_throughput_bps'] = int(data.get('download_throughput_bps', 0))
    metrics['uplink_throughput_bps'] = int(data.get('upload_throughput_bps', 0))
    metrics['ping_latency_ms'] = float(data.get('ping_latency_ms', 0)) if 'ping_latency_ms' in data else 0
    metrics['ping_drop_rate'] = float(data.get('ping_drop_rate', 0)) * 100 if 'ping_drop_rate' in data else 0
    metrics['power_watts'] = float(data.get('power_watts', 0)) if 'power_watts' in data else 0
    metrics['snr_good'] = float(data.get('snr', 0)) if 'snr' in data else 0
    return metrics

def main():
    parser = argparse.ArgumentParser(description='Monitor Starlink Dish Metrics for Site24x7')
    parser.add_argument('--starlink_grpc_path', help='Path to starlink_grpc binary', type=str, default='starlink_grpc')
    parser.add_argument('--dish_address', help='Address of the dish service (default: localhost)', type=str, default='localhost')
    args = parser.parse_args()

    output = {
        "plugin_version": PLUGIN_VERSION,
        "heartbeat_required": HEARTBEAT
    }

    try:
        dish_data = run_starlink_grpc_json(args.starlink_grpc_path, args.dish_address)
        metrics = get_metrics(dish_data)
        output.update(metrics)
        output["units"] = METRIC_UNITS
    except Exception as e:
        output["status"] = 0
        output["msg"] = str(e)

    print(json.dumps(output, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()
