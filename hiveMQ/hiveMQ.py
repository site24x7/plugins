#!/usr/bin/python3
import json
import subprocess
import argparse


PLUGIN_VERSION = 1
HEARTBEAT = True

class HiveMQ:

    def __init__(self, args):
        self.maindata = {
            'plugin_version': PLUGIN_VERSION,
            'heartbeat_required': HEARTBEAT
        }
        self.hivemq_host = args.hivemq_host
        self.hivemq_jmx_port = args.hivemq_jmx_port

    def execute_command(self, cmd, need_out=False):
        try:
            if not isinstance(cmd, list):
                cmd = cmd.split()
            result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            if result.returncode != 0:
                return False
            if need_out:
                return result.stdout
            return True
        except Exception as e:
            return False

    def metriccollector(self):
        try:
            import jmxquery as jmx
            from jmxquery import JMXQuery, JMXConnection
            jmxConnection = JMXConnection(f"service:jmx:rmi:///jndi/rmi://{self.hivemq_host}:{self.hivemq_jmx_port}/jmxrmi")

            metric_queries = {
                    "Shared Subscription Cache Hit Rate": "metrics:name=com.hivemq.cache.shared-subscription.averageLoadPenalty",
                    "Shared Subscription Cache Eviction Count": "metrics:name=com.hivemq.cache.shared-subscription.evictionCount",
                    "Shared Subscription Cache Miss Count": "metrics:name=com.hivemq.cache.shared-subscription.missCount",
                    "Shared Subscription Cache Total Load Time": "metrics:name=com.hivemq.cache.shared-subscription.totalLoadTime",
                    "Licensed CPU Cores": "metrics:name=com.hivemq.cpu-cores.licensed",
                    "Used CPU Cores": "metrics:name=com.hivemq.cpu-cores.used",
                    "Publish Service Publishes": "metrics:name=com.hivemq.extensions.services.publish-service-publishes",
                    "Publish Service Publishes to Client": "metrics:name=com.hivemq.extensions.services.publish-service-publishes-to-client",
                    "Rate Limit Exceeded Count": "metrics:name=com.hivemq.extensions.services.rate-limit-exceeded.count",
                    "Keep Alive Disconnect Count": "metrics:name=com.hivemq.keep-alive.disconnect.count",
                    "Dropped Messages Total": "metrics:name=com.hivemq.messages.dropped.count",
                    "Dropped Messages - Queue Full": "metrics:name=com.hivemq.messages.dropped.queue-full.count",
                    "Dropped Messages - QoS 0 Memory Exceeded": "metrics:name=com.hivemq.messages.dropped.qos-0-memory-exceeded.count",
                    "Dropped Messages - Internal Error": "metrics:name=com.hivemq.messages.dropped.internal-error.count",
                    "Expired Messages Count": "metrics:name=com.hivemq.messages.expired-messages",
                    "Incoming CONNECT Messages": "metrics:name=com.hivemq.messages.incoming.connect.count",
                    "Incoming PINGREQ Messages": "metrics:name=com.hivemq.messages.incoming.pingreq.count",
                    "Incoming SUBSCRIBE Messages": "metrics:name=com.hivemq.messages.incoming.subscribe.count",
                    "Incoming UNSUBSCRIBE Messages": "metrics:name=com.hivemq.messages.incoming.unsubscribe.count",
                    "Incoming PUBLISH Messages": "metrics:name=com.hivemq.messages.incoming.publish.count",
                    "Incoming Total Message Count": "metrics:name=com.hivemq.messages.incoming.total.count",
                    "Outgoing CONNACK Messages": "metrics:name=com.hivemq.messages.outgoing.connack.count",
                    "Outgoing PINGRESP Messages": "metrics:name=com.hivemq.messages.outgoing.pingresp.count",
                    "Outgoing PUBACK Messages": "metrics:name=com.hivemq.messages.outgoing.puback.count",
                    "Outgoing PUBCOMP Messages": "metrics:name=com.hivemq.messages.outgoing.pubcomp.count",
                    "Outgoing PUBREL Messages": "metrics:name=com.hivemq.messages.outgoing.pubrel.count",
                    "Outgoing DISCONNECT Messages": "metrics:name=com.hivemq.messages.outgoing.disconnect.count",
                    "Outgoing Total Message Count": "metrics:name=com.hivemq.messages.outgoing.total.count",
                    "Cluster Name Request Retry Count": "metrics:name=com.hivemq.cluster.name-request.retry.count",
                    "MQTT 3 CONNECT Count": "metrics:name=com.hivemq.messages.incoming.connect.mqtt3.count",
                    "MQTT 5 CONNECT Count": "metrics:name=com.hivemq.messages.incoming.connect.mqtt5.count",
                    "Active Session": "metrics:name=com.hivemq.sessions.persistent.active",
                    "Subscriptions Count": "metrics:name=com.hivemq.subscriptions.overall.current",
                    "Bytes Received Per Second": "metrics:name=com.hivemq.networking.bytes.read.current",
                    "Bytes Sent Per Second": "metrics:name=com.hivemq.networking.bytes.write.current",
                    "Total Bytes Received": "metrics:name=com.hivemq.networking.bytes.read.total",
                    "Total Bytes Sent": "metrics:name=com.hivemq.networking.bytes.write.total",
                    "Connection Closures Total": "metrics:name=com.hivemq.networking.connections-closed.total.count",
                    "System Memory Free": "metrics:name=com.hivemq.system.os.global.memory.available",
                    "System Memory Total": "metrics:name=com.hivemq.system.os.global.memory.total",
                    "System CPU Load": "metrics:name=com.hivemq.system.process-cpu.load",
                    "JVM Heap Memory Used": "metrics:name=com.hivemq.jvm.memory.heap.used",
                    "JVM Heap Memory Max": "metrics:name=com.hivemq.jvm.memory.heap.max",
                    "JVM Non-Heap Memory Used": "metrics:name=com.hivemq.jvm.memory.non-heap.used",
                    "JVM Non-Heap Memory Committed": "metrics:name=com.hivemq.jvm.memory.non-heap.committed",
                    "JVM Thread Count": "metrics:name=com.hivemq.jvm.threads.count",
                    "JVM Thread Peak": "metrics:name=com.hivemq.jvm.threads.peak.count",
                    "JVM Thread Daemon": "metrics:name=com.hivemq.jvm.threads.daemon.count",
                    }


            for metric_name, query in metric_queries.items():
                jmxQuery = [JMXQuery(query)]
                try:
                    metric_result = jmxConnection.query(jmxQuery)
                    if metric_result:
                        self.maindata[metric_name] = metric_result[0].value
                except Exception as inner_e:
                    self.maindata['msg'] = f"Error calling JMX: {str(inner_e)}"
                    self.maindata['status'] = 0
                    return self.maindata

        except Exception as e:
            self.maindata['msg'] = str(e)
            self.maindata['status'] = 0
            return self.maindata

        self.maindata['tabs'] = {
            'Message Traffic': {
                'order': 1,
                'tablist': [
                    "Publish Service Publishes",
                    "Publish Service Publishes to Client",
                    "Dropped Messages Total",
                    "Dropped Messages - Queue Full",
                    "Dropped Messages - QoS 0 Memory Exceeded",
                    "Dropped Messages - Internal Error",
                    "Expired Messages Count",
                    "Incoming CONNECT Messages",
                    "Incoming PINGREQ Messages",
                    "Incoming SUBSCRIBE Messages",
                    "Incoming UNSUBSCRIBE Messages",
                    "Incoming PUBLISH Messages",
                    "Incoming Total Message Count",
                    "Outgoing CONNACK Messages",
                    "Outgoing PINGRESP Messages",
                    "Outgoing PUBACK Messages",
                    "Outgoing PUBCOMP Messages",
                    "Outgoing PUBREL Messages",
                    "Outgoing DISCONNECT Messages",
                    "Outgoing Total Message Count",
                    "MQTT 3 CONNECT Count",
                    "MQTT 5 CONNECT Count"
                    ]
            },
            'System': {
                'order': 2,
                'tablist': [
                    "Licensed CPU Cores",
                    "Used CPU Cores",
                    "System Memory Total",
                ]
            },
            'Connections': {
                'order': 3,
                'tablist': [
                    "Keep Alive Disconnect Count",
                    "Connection Closures Total",
                    "Active Session",
                    "Subscriptions Count",
                    "Bytes Received Per Second",
                    "Total Bytes Sent"
                ]
            },
            'JVM': {
                'order': 4,
                'tablist': [
                    "JVM Heap Memory Used",
                    "JVM Heap Memory Max",
                    "JVM Non-Heap Memory Used",
                    "JVM Non-Heap Memory Committed",
                    "JVM Thread Count",
                    "JVM Thread Peak",
                    "JVM Thread Daemon",
                ]
            }
        }

        self.maindata['units']={
            "Shared Subscription Cache Hit Rate": "hits/second",
            "Shared Subscription Cache Eviction Count": "count",
            "Shared Subscription Cache Miss Count": "count",
            "Shared Subscription Cache Total Load Time": "microseconds",
            "Licensed CPU Cores": "count",
            "Used CPU Cores": "count",
            "Publish Service Publishes": "count",
            "Publish Service Publishes to Client": "count",
            "Rate Limit Exceeded Count": "count",
            "Keep Alive Disconnect Count": "count",
            "Dropped Messages Total": "count",
            "Dropped Messages - Queue Full": "count",
            "Dropped Messages - QoS 0 Memory Exceeded": "count",
            "Dropped Messages - Internal Error": "count",
            "Expired Messages Count": "count",
            "Incoming CONNECT Messages": "count",
            "Incoming PINGREQ Messages": "count",
            "Incoming SUBSCRIBE Messages": "count",
            "Incoming UNSUBSCRIBE Messages": "count",
            "Incoming PUBLISH Messages": "count",
            "Incoming Total Message Count": "count",
            "Outgoing CONNACK Messages": "count",
            "Outgoing PINGRESP Messages": "count",
            "Outgoing PUBACK Messages": "count",
            "Outgoing PUBCOMP Messages": "count",
            "Outgoing PUBREL Messages": "count",
            "Outgoing DISCONNECT Messages": "count",
            "Outgoing Total Message Count": "count",
            "Cluster Name Request Retry Count": "count",
            "MQTT 3 CONNECT Count": "count",
            "MQTT 5 CONNECT Count": "count",
            "Active Session": "count",
            "Subscriptions Count": "count",
            "Bytes Received Per Second": "bytes/second",
            "Bytes Sent Per Second": "bytes/second",
            "Total Bytes Received": "bytes",
            "Total Bytes Sent": "bytes",
            "Connection Closures Total": "count",
            "System Memory Free": "bytes",
            "System Memory Total": "bytes",
            "System CPU Load": "ratio",
            "JVM Heap Memory Used": "bytes",
            "JVM Heap Memory Max": "bytes",
            "JVM Non-Heap Memory Used": "bytes",
            "JVM Non-Heap Memory Committed": "bytes",
            "JVM Thread Count": "count",
            "JVM Thread Peak": "count",
            "JVM Thread Daemon": "count"
        }
        return self.maindata


if __name__ == "__main__":
    hivemq_host = "localhost"
    hivemq_jmx_port = "9010"

    parser = argparse.ArgumentParser()
    parser.add_argument('--hivemq_host', help='host name to access the HiveMQ JMX metrics', default=hivemq_host)
    parser.add_argument('--hivemq_jmx_port', help='JMX port for HiveMQ', default=hivemq_jmx_port)
    args = parser.parse_args()

    obj = HiveMQ(args)
    result = obj.metriccollector()
    print(json.dumps(result))
