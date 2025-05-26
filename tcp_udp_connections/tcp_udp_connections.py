import subprocess
import json

PLUGIN_VERSION = "1"
HEARTBEAT = "true"

METRIC_UNITS = {
    'TCP_Listening_Ports': 'count',
    'TCP_Packets_Received': 'count',
    'TCP_Packets_Sent': 'count',
    'TCP_Retransmissions': 'count',
    'UDP_Listening_Ports': 'count',
    'UDP_Datagrams_Received': 'count',
    'UDP_Datagrams_Sent': 'count',
    'UDP_Packet_Loss': 'count',
    'UDP_Dropped_Packets': 'count',
}

class datacollector:
    def __init__(self):
        self.data = {
            'plugin_version': PLUGIN_VERSION,
            'heartbeat_required': HEARTBEAT
        }

    def run_cmd(self, cmd):
        return subprocess.check_output(cmd, shell=True).decode()

    def parse_proc_net_snmp(self, protocol):
        metrics = {}
        try:
            with open("/proc/net/snmp", "r") as f:
                lines = f.readlines()
            for i in range(len(lines)):
                if lines[i].startswith(protocol):
                    keys = lines[i].strip().split()[1:]
                    values = lines[i + 1].strip().split()[1:]
                    metrics = dict(zip(keys, map(int, values)))
                    break
        except Exception as e:
            pass
        return metrics

    def metricCollector(self):
        try:
            # TCP Listening Ports
            tcp_listen = int(self.run_cmd("netstat -lt | grep -v 'Active' | wc -l"))
            self.data["TCP_Listening_Ports"] = tcp_listen

            # UDP Listening Ports
            udp_listen = int(self.run_cmd("netstat -lu | grep -v 'Active' | wc -l"))
            self.data["UDP_Listening_Ports"] = udp_listen

            # TCP Metrics
            tcp_metrics = self.parse_proc_net_snmp("Tcp")
            self.data["TCP_Packets_Received"] = tcp_metrics.get("InSegs", 0)
            self.data["TCP_Packets_Sent"] = tcp_metrics.get("OutSegs", 0)
            self.data["TCP_Retransmissions"] = tcp_metrics.get("RetransSegs", 0)

            # UDP Metrics
            udp_metrics = self.parse_proc_net_snmp("Udp")
            self.data["UDP_Datagrams_Received"] = udp_metrics.get("InDatagrams", 0)
            self.data["UDP_Datagrams_Sent"] = udp_metrics.get("OutDatagrams", 0)
            self.data["UDP_Packet_Loss"] = udp_metrics.get("InErrors", 0)
            self.data["UDP_Dropped_Packets"] = udp_metrics.get("RcvbufErrors", 0) + udp_metrics.get("SndbufErrors", 0)

        except Exception as e:
            self.data["status"] = 0
            self.data["msg"] = str(e)

        self.data['units'] = METRIC_UNITS
        return self.data
    
def run(param=None):
    update = datacollector()
    result = update.metricCollector()
    return result
            

if __name__ == "__main__":
    update = datacollector()
    result = update.metricCollector()
    print(json.dumps(result, indent=4, sort_keys=True))
