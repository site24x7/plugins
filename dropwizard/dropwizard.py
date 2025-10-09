#!/usr/bin/env python3

import urllib.request
import json
import argparse
import time
import configparser
import os

PLUGIN_VERSION = 1
HEARTBEAT = True

DEFAULT_PROTOCOL = "http"
DEFAULT_HOST = "localhost"
DEFAULT_PORT = "8081"
DEFAULT_TIMEOUT = 30

# -------------------------------
#  TIMER METRICS (Requests, Connections)
# -------------------------------
TIMERS_MAP = {
    "io.dropwizard.jetty.MutableServletContextHandler.requests": "Total Requests",
    "io.dropwizard.jetty.MutableServletContextHandler.get-requests": "Get Requests",
    "io.dropwizard.jetty.MutableServletContextHandler.post-requests": "Post Requests",
    "io.dropwizard.jetty.MutableServletContextHandler.put-requests": "Put Requests",
    "io.dropwizard.jetty.MutableServletContextHandler.delete-requests": "Delete Requests",
    "org.eclipse.jetty.server.HttpConnectionFactory.8080.connections": "Connections at 8080",
    "org.eclipse.jetty.server.HttpConnectionFactory.8081.connections": "Connections at 8081",
    "org.eclipse.jetty.server.HttpConnectionFactory.8443.connections": "Connections at 8443",
    "org.eclipse.jetty.server.HttpConnectionFactory.8444.connections": "Connections at 8444",
}

# -------------------------------
#  METER METRICS (Logs, Status Codes, Health)
# -------------------------------
METERS_MAP = {
    # Log-related
    "ch.qos.logback.core.Appender.all": "Log Count",
    "ch.qos.logback.core.Appender.debug": "Debug Logs",
    "ch.qos.logback.core.Appender.error": "Error Logs",
    "ch.qos.logback.core.Appender.info": "Info Logs",
    "ch.qos.logback.core.Appender.trace": "Trace Logs",
    "ch.qos.logback.core.Appender.warn": "Warn Logs",

    # Response Codes
    "io.dropwizard.jetty.MutableServletContextHandler.1xx-responses": "1xx Responses",
    "io.dropwizard.jetty.MutableServletContextHandler.2xx-responses": "2xx Responses",
    "io.dropwizard.jetty.MutableServletContextHandler.3xx-responses": "3xx Responses",
    "io.dropwizard.jetty.MutableServletContextHandler.4xx-responses": "4xx Responses",
    "io.dropwizard.jetty.MutableServletContextHandler.5xx-responses": "5xx Responses",

    # Health Check metrics
    "TimeBoundHealthCheck-pool.created": "HealthCheck Pool Created",
    "TimeBoundHealthCheck-pool.terminated": "HealthCheck Pool Terminated",
}

# -------------------------------
#  GAUGE METRICS (JVM, Memory, Jetty)
# -------------------------------
GAUGES_MAP = {
    # JVM - Threads, Classloader
    "jvm.attribute.uptime": "JVM Uptime",
    "jvm.threads.count": "Threads Count",
    "jvm.threads.runnable.count": "Threads Runnable Count",
    "jvm.classloader.loaded": "Classloader Loaded",
    "jvm.classloader.unloaded": "Classloader Unloaded",
    "jvm.filedescriptor": "File Descriptor Ratio",

    # JVM - Memory (Heap, Non-Heap, Total)
    "jvm.memory.heap.used": "Heap Used",
    "jvm.memory.heap.max": "Heap Max",
    "jvm.memory.non-heap.used": "Non-Heap Used",
    "jvm.memory.non-heap.max": "Non-Heap Max",
    "jvm.memory.total.max": "Max Memory",
    "jvm.memory.total.used": "Used Memory",
    "jvm.memory.total.committed": "Memory Total Committed",

    # JVM - Memory Pools
    "jvm.memory.pools.Metaspace.used": "Metaspace Used",
    "jvm.memory.pools.Compressed-Class-Space.used": "Compressed Class Space Used",
    "jvm.memory.pools.Code-Cache.used": "Code Cache Used",
    "jvm.memory.pools.G1-Eden-Space.used": "G1 Eden Space Used",
    "jvm.memory.pools.G1-Old-Gen.used": "G1 Old Gen Used",
    "jvm.memory.pools.G1-Survivor-Space.used": "G1 Survivor Space Used",

    # JVM - Garbage Collection
    "jvm.gc.G1-Young-Generation.count": "GC G1 Young Generation Count",
    "jvm.gc.G1-Young-Generation.time": "GC G1 Young Generation Time",
    "jvm.gc.G1-Old-Generation.count": "GC G1 Old Generation Count",
    "jvm.gc.G1-Old-Generation.time": "GC G1 Old Generation Time",
    "jvm.gc.G1-Concurrent-GC.count": "GC G1 Concurrent GC Count",
    "jvm.gc.G1-Concurrent-GC.time": "GC G1 Concurrent GC Time",

    # Jetty Thread Pools (DW)
    "org.eclipse.jetty.util.thread.QueuedThreadPool.dw.size": "Jetty DW Pool Size",
    "org.eclipse.jetty.util.thread.QueuedThreadPool.dw.utilization": "Jetty DW Utilization",
    "org.eclipse.jetty.util.thread.QueuedThreadPool.dw.utilization-max": "Jetty DW Utilization Max",
    "org.eclipse.jetty.util.thread.QueuedThreadPool.dw.jobs": "Jetty DW Jobs",
    "org.eclipse.jetty.util.thread.QueuedThreadPool.dw.jobs-queue-utilization": "Jetty DW Queue Utilization",

    # Jetty Thread Pools (DW Admin)
    "org.eclipse.jetty.util.thread.QueuedThreadPool.dw-admin.size": "Jetty DW Admin Pool Size",
    "org.eclipse.jetty.util.thread.QueuedThreadPool.dw-admin.utilization": "Jetty DW Admin Utilization",
    "org.eclipse.jetty.util.thread.QueuedThreadPool.dw-admin.utilization-max": "Jetty DW Admin Utilization Max",
    "org.eclipse.jetty.util.thread.QueuedThreadPool.dw-admin.jobs": "Jetty DW Admin Jobs",
    "org.eclipse.jetty.util.thread.QueuedThreadPool.dw-admin.jobs-queue-utilization": "Jetty DW Admin Queue Utilization",

    # Jetty - Active requests / dispatches
    "io.dropwizard.jetty.MutableServletContextHandler.active-requests": "Active Requests",
    "io.dropwizard.jetty.MutableServletContextHandler.active-dispatches": "Active Dispatches",
    "io.dropwizard.jetty.MutableServletContextHandler.active-suspended": "Active Suspended",
}

# -------------------------------
# UNITS
# -------------------------------
METRIC_UNITS = {
    "Connections at 8080": "connections",
    "Connections at 8081": "connections",
    "Connections at 8443": "connections",
    "Connections at 8444": "connections",
    "JVM Uptime": "ms",
    "Threads Count": "units",
    "Threads Runnable Count": "units",
    "File Descriptor Ratio": "ratio",
    "Heap Used": "MB",
    "Heap Max": "MB",
    "Non-Heap Used": "MB",
    "Non-Heap Max": "MB",
    "Max Memory": "MB",
    "Used Memory": "MB",
    "Memory Total Committed": "MB",
    "Metaspace Used": "MB",
    "Compressed Class Space Used": "MB",
    "Code Cache Used": "MB",
    "G1 Eden Space Used": "MB",
    "G1 Old Gen Used": "MB",
    "G1 Survivor Space Used": "MB",
}

# -------------------------------
# Helper Functions
# -------------------------------
def to_mb(v):
    try:
        return round(float(v) / (1024.0 * 1024.0), 2)
    except Exception:
        return v


def load_config(cfg_path="dropwiz.cfg"):
    cfg = {}
    parser = configparser.ConfigParser()
    if os.path.exists(cfg_path):
        parser.read(cfg_path)
        if "dw" in parser:
            sec = parser["dw"]
            cfg["protocol"] = sec.get("protocol", DEFAULT_PROTOCOL)
            cfg["host"] = sec.get("host", DEFAULT_HOST)
            cfg["port"] = sec.get("port", DEFAULT_PORT)
            cfg["timeout"] = sec.getint("timeout", DEFAULT_TIMEOUT)
    return cfg


def fetch_metrics(url, timeout):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req, timeout=timeout) as res:
        return json.loads(res.read().decode())

# -------------------------------
# Main Plugin
# -------------------------------
class DropwizardPlugin:
    def __init__(self, protocol, host, port, timeout):
        self.url = f"{protocol}://{host}:{port}/metrics"
        self.timeout = timeout

    def collect(self):
        out = {
            "plugin_version": PLUGIN_VERSION,
            "heartbeat_required": HEARTBEAT,
            "units": METRIC_UNITS,
            "collected_at": int(time.time()),
        }

        try:
            payload = fetch_metrics(self.url, self.timeout)
        except Exception as e:
            out["error"] = f"Failed to fetch metrics: {e}"
            out["error_details"] = repr(e)
            return out

        # TIMERS
        timers = payload.get("timers", {}) if isinstance(payload, dict) else {}
        for src, name in TIMERS_MAP.items():
            val = timers.get(src, {}).get("count", 0)
            out[name] = val

        # METERS
        meters = payload.get("meters", {}) if isinstance(payload, dict) else {}
        for src, name in METERS_MAP.items():
            val = meters.get(src, {}).get("count", 0)
            out[name] = val

        # GAUGES
        gauges = payload.get("gauges", {}) if isinstance(payload, dict) else {}
        for src, name in GAUGES_MAP.items():
            val = gauges.get(src, {}).get("value")
            if METRIC_UNITS.get(name) == "MB" and isinstance(val, (int, float)):
                val = to_mb(val)
            out[name] = val if val is not None else 0

        # -------------------------------
        # Tabs
        # -------------------------------
        connection_tab = [
            "Total Requests", "Get Requests", "Post Requests", "Put Requests", "Delete Requests",
            "Connections at 8080", "Connections at 8081", "Connections at 8443", "Connections at 8444"
        ]
        events_tab = [
            "Log Count", "Debug Logs", "Error Logs", "Info Logs", "Trace Logs", "Warn Logs",
            "1xx Responses", "2xx Responses", "3xx Responses", "4xx Responses", "5xx Responses"
        ]
        jvm_tab = [
            "JVM Uptime", "Threads Count", "Threads Runnable Count",
            "Classloader Loaded", "Classloader Unloaded", "File Descriptor Ratio",
            "GC G1 Young Generation Count", "GC G1 Young Generation Time",
            "GC G1 Old Generation Count", "GC G1 Old Generation Time",
            "GC G1 Concurrent GC Count", "GC G1 Concurrent GC Time"
        ]
        memory_tab = [
            "Heap Used", "Heap Max", "Non-Heap Used", "Non-Heap Max",
            "Max Memory", "Used Memory", "Memory Total Committed",
            "Metaspace Used", "Compressed Class Space Used", "Code Cache Used",
            "G1 Eden Space Used", "G1 Old Gen Used", "G1 Survivor Space Used"
        ]
        jetty_tab = [
            "Jetty DW Pool Size", "Jetty DW Utilization", "Jetty DW Utilization Max",
            "Jetty DW Jobs", "Jetty DW Queue Utilization",
            "Jetty DW Admin Pool Size", "Jetty DW Admin Utilization",
            "Jetty DW Admin Utilization Max", "Jetty DW Admin Jobs",
            "Jetty DW Admin Queue Utilization",
            "Active Requests", "Active Dispatches", "Active Suspended"
        ]

        out["tabs"] = {
            "Connection": {"order": 1, "tablist": connection_tab},
            "Events": {"order": 2, "tablist": events_tab},
            "JVM": {"order": 3, "tablist": jvm_tab},
            "Memory": {"order": 4, "tablist": memory_tab},
            "Jetty": {"order": 5, "tablist": jetty_tab},
        }

        return out


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--protocol", default=None)
    p.add_argument("--host", default=None)
    p.add_argument("--port", default=None)
    p.add_argument("--timeout", type=int, default=None)
    return p.parse_args()


def main():
    cfg = load_config()
    args = parse_args()
    protocol = args.protocol or cfg.get("protocol") or DEFAULT_PROTOCOL
    host = args.host or cfg.get("host") or DEFAULT_HOST
    port = args.port or cfg.get("port") or DEFAULT_PORT
    timeout = args.timeout or cfg.get("timeout") or DEFAULT_TIMEOUT

    plugin = DropwizardPlugin(protocol, host, port, timeout)
    print(json.dumps(plugin.collect(), indent=2, sort_keys=False, default=str))


if __name__ == "__main__":
    main()
