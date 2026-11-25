#!/usr/bin/python3
"""
Site24x7 PostgreSQL plugin, version 2.

Monitors the PostgreSQL server at --host/--port. Every metric comes from a
declarative catalogue (QUERIES, TABLES, RATES below): each entry is one SQL
statement, the PostgreSQL versions it applies to, and the metrics its columns
become. A small engine runs the catalogue, so adding a metric is one entry and
never a new branch of code.

Rules the engine enforces:
  * A failed or inapplicable query removes its metrics instead of reporting 0.
    The only fixed values are the safe stand-ins in truthful_zeros().
  * `status` is 0 only when the server cannot be monitored at all (driver
    missing, connection or authentication failure, unsupported version).
  * Rates and deltas come from the previous poll of the same server process.
    On a monitor's first poll they are measured over RATE_SAMPLE_S seconds.
"""

import argparse
import hashlib
import json
import math
import os
import re
import time

try:
    import psycopg2
    HAVE_PSYCOPG2 = True
except ImportError:
    psycopg2 = None
    HAVE_PSYCOPG2 = False


PLUGIN_VERSION = 2
HEARTBEAT = True

VERSION_FLOOR = (9, 6)
CONNECT_TIMEOUT_S = 10
STATEMENT_TIMEOUT_MS = 5000
CYCLE_BUDGET_S = 40.0          # the agent kills a plugin after 50 s
RATE_MIN_INTERVAL_S = 0.5
RATE_MAX_INTERVAL_S = 3600.0
LONG_QUERY_S = 300

# Site24x7 platform limits
MAX_TABLES = 10
MAX_COLUMNS = 15
MAX_ROWS = 25
MAX_STRING_COLS = 5            # including `name`
MAX_NAME_CHARS = 520
MAX_STRING_CHARS = 100
MAX_METRICS = 200
MAX_MSG_CHARS = 180

RESERVED_KEYS = {
    "plugin_version", "heartbeat_required", "status", "msg", "units",
    "tabs", "s247config", "applog",
}

PLUGIN_DIR = os.path.dirname(os.path.abspath(__file__))
STATE_DIR = os.path.join(PLUGIN_DIR, ".state")

DRIVER_MISSING_MSG = (
    "psycopg2 module not installed. Install it for the agent's Python: "
    "pip3 install psycopg2-binary"
)

# Node roles reported in `Node Role`.
ROLE_PRIMARY = "primary"
ROLE_STANDBY = "standby"

# Which kind of node a query applies to.
ANY, PRIMARY, STANDBY = "any", "primary", "standby"


# =============================================================================
# 1. CATALOGUE
# =============================================================================

class M(object):
    """One metric produced by one column of a query."""

    def __init__(self, name, unit="", tab="", kind=int):
        self.name = name
        self.unit = unit
        self.tab = tab
        self.kind = kind          # int, float or str


class Variant(object):
    """The SQL used from PostgreSQL `min_ver` upward, and the metrics its columns map to."""

    def __init__(self, min_ver, sql, fields):
        self.min_ver = min_ver
        self.sql = sql
        self.fields = fields


class Query(object):
    """A single-row query. The highest variant the server satisfies is used."""

    def __init__(self, key, variants, role=ANY, when=None):
        self.key = key
        self.variants = sorted(variants, key=lambda v: v.min_ver, reverse=True)
        self.role = role
        self.when = when          # optional callable(node) -> bool

    def pick(self, version):
        for v in self.variants:
            if version >= v.min_ver:
                return v
        return None


class Table(object):
    """A multi-row query whose rows become a Site24x7 child table."""

    def __init__(self, name, tab, variants, units, role=ANY, when=None, optional=False):
        self.name = name
        self.tab = tab
        self.variants = sorted(variants, key=lambda v: v[0], reverse=True)
        self.units = units        # column -> unit, also fixes column order and types
        self.role = role
        self.when = when
        self.optional = optional  # True: a failure leaves the table out silently

    def pick(self, version):
        for min_ver, sql in self.variants:
            if version >= min_ver:
                return sql
        return None


class Rate(object):
    """A per-second rate (or a per-poll delta) of a cumulative counter metric."""

    def __init__(self, name, source, unit, tab, delta=False, scale=1.0):
        self.name = name
        self.source = source
        self.unit = unit
        self.tab = tab
        self.delta = delta        # True: change since the previous poll, not per second
        self.scale = scale


# Summary plus these 8 tabs all fit on one line of the Site24x7 console.
TAB_ORDER = [
    "Cluster",
    "Replication",
    "Activity",
    "Transactions and Sessions",
    "DB and IO stats",
    "Vacuum and Wraparound",
    "WAL and Archiving",
    "BG Writer",
]
SUMMARY = ""                      # metrics with no tab chart on the built-in Summary tab

# Counters that only grow since the server started. The plugin reads them to compute
# the "Per Sec" and "New ..." metrics, but does not send them: a lifetime total is a
# rising line, and its rate or per-poll change is what people watch and alert on.
HIDDEN_COUNTERS = {
    "Total Rows Inserted", "Total Rows Updated", "Total Rows Deleted", "Total Rows Fetched",
    "Total Rows Returned", "Total Block Reads", "Total Temp Data", "Sequential Scans",
    "Index Scans", "WAL Written", "Total Deadlocks", "Total Conflicts", "Checkpoints Req",
    "Archive Failed Count", "Checksum Failures", "WAL Buffers Full",
}

# pg_stat_activity filter for client sessions, excluding this plugin's own session.
_CLIENTS_10 = "backend_type = 'client backend' AND pid <> pg_backend_pid()"
_CLIENTS_96 = "datname IS NOT NULL AND pid <> pg_backend_pid()"


def _activity_sql(clients):
    return (
        "SELECT count(*) FILTER (WHERE state = 'active'),"
        " count(*) FILTER (WHERE state = 'active' AND wait_event IS NOT NULL),"
        " count(*) FILTER (WHERE state = 'idle'),"
        " count(*) FILTER (WHERE state LIKE 'idle in transaction%%'),"
        " count(*) FILTER (WHERE xact_start IS NOT NULL),"
        " coalesce(max(extract(epoch FROM now() - xact_start)), 0)::bigint,"
        " count(*) FILTER (WHERE state = 'active' AND now() - query_start > interval '%d seconds'),"
        " count(*) FILTER (WHERE cardinality(pg_blocking_pids(pid)) > 0)"
        " FROM pg_stat_activity WHERE %s" % (LONG_QUERY_S, clients)
    )


_ACTIVITY_FIELDS = [
    M("Active Queries", "queries", "Activity"),
    M("Active Waiting Queries", "queries", "Activity"),
    M("Idle Connections", "connections", "Activity"),
    M("Transactions Idle In Transaction", "transactions", "Transactions and Sessions"),
    M("Transactions Open", "transactions", "Transactions and Sessions"),
    M("Longest Transaction", "s", "Activity"),
    M("Long Running Queries", "queries", "Activity"),
    M("Blocked Sessions", "sessions", "Activity"),
]

QUERIES = [
    Query("server", [Variant((9, 6),
        "SELECT current_setting('server_version'),"
        " floor(extract(epoch FROM now() - pg_postmaster_start_time()))::bigint,"
        " current_setting('max_connections')::int,"
        " (SELECT count(*) FROM pg_database WHERE datname NOT IN ('template0', 'template1')),"
        " (SELECT count(*) FROM pg_stat_all_tables)",
        [M("Server Version", tab="Activity", kind=str),
         M("Uptime", "s", SUMMARY),
         M("Max Connections", "connections", "Activity"),
         M("Database Count", "databases", "DB and IO stats"),
         M("Table Count", "tables", "DB and IO stats")])]),

    Query("activity", [
        Variant((10, 0), _activity_sql(_CLIENTS_10), _ACTIVITY_FIELDS),
        Variant((9, 6), _activity_sql(_CLIENTS_96), _ACTIVITY_FIELDS)]),

    Query("database_totals", [Variant((9, 6),
        "SELECT sum(numbackends), sum(xact_commit), sum(xact_rollback), sum(conflicts),"
        " sum(deadlocks), sum(tup_inserted), sum(tup_updated), sum(tup_deleted),"
        " sum(tup_fetched), sum(tup_returned), sum(blks_read), sum(blks_hit),"
        " sum(temp_files), round(sum(temp_bytes) / 1048576.0, 2)"
        " FROM pg_stat_database",
        [M("Active Connections", "connections", SUMMARY),
         M("Total Commits", "transactions", "Transactions and Sessions"),
         M("Total Rollbacks", "transactions", "Transactions and Sessions"),
         M("Total Conflicts", "conflicts", "Transactions and Sessions"),
         M("Total Deadlocks", "deadlocks", "Transactions and Sessions"),
         M("Total Rows Inserted", "rows", "DB and IO stats"),
         M("Total Rows Updated", "rows", "DB and IO stats"),
         M("Total Rows Deleted", "rows", "DB and IO stats"),
         M("Total Rows Fetched", "rows", "DB and IO stats"),
         M("Total Rows Returned", "rows", "DB and IO stats"),
         M("Total Block Reads", "blocks", "DB and IO stats"),
         M("Total Block Hits", "blocks", "DB and IO stats"),
         M("Total Temp Files", "files", "DB and IO stats"),
         M("Total Temp Data", "MB", "DB and IO stats", float)])]),

    Query("sessions", [Variant((14, 0),
        "SELECT sum(sessions), sum(sessions_abandoned), sum(sessions_fatal), sum(sessions_killed)"
        " FROM pg_stat_database",
        [M("Total Sessions", "sessions", "Transactions and Sessions"),
         M("Total Sessions Abandoned", "sessions", "Transactions and Sessions"),
         M("Total Sessions Fatal", "sessions", "Transactions and Sessions"),
         M("Total Sessions Killed", "sessions", "Transactions and Sessions")])]),

    Query("bgwriter", [
        Variant((17, 0),
            "SELECT c.num_timed, c.num_requested, c.write_time, c.sync_time, c.buffers_written,"
            " b.buffers_clean, b.maxwritten_clean, b.buffers_alloc"
            " FROM pg_stat_checkpointer c, pg_stat_bgwriter b",
            [M("Checkpoints Timed", "checkpoints", "BG Writer"),
             M("Checkpoints Req", "checkpoints", "BG Writer"),
             M("Checkpoint Write Time", "ms", "BG Writer", float),
             M("Checkpoint Sync Time", "ms", "BG Writer", float),
             M("Buffers Checkpoint", "buffers", "BG Writer"),
             M("Buffers Clean", "buffers", "BG Writer"),
             M("Maxwritten Clean", "times", "BG Writer"),
             M("Buffers Alloc", "buffers", "BG Writer")]),
        Variant((9, 6),
            "SELECT checkpoints_timed, checkpoints_req, checkpoint_write_time, checkpoint_sync_time,"
            " buffers_checkpoint, buffers_clean, maxwritten_clean, buffers_alloc,"
            " buffers_backend, buffers_backend_fsync FROM pg_stat_bgwriter",
            [M("Checkpoints Timed", "checkpoints", "BG Writer"),
             M("Checkpoints Req", "checkpoints", "BG Writer"),
             M("Checkpoint Write Time", "ms", "BG Writer", float),
             M("Checkpoint Sync Time", "ms", "BG Writer", float),
             M("Buffers Checkpoint", "buffers", "BG Writer"),
             M("Buffers Clean", "buffers", "BG Writer"),
             M("Maxwritten Clean", "times", "BG Writer"),
             M("Buffers Alloc", "buffers", "BG Writer"),
             M("Buffers Backend", "buffers", "BG Writer"),
             M("Buffers Backend Fsync", "fsyncs", "BG Writer")])]),

    Query("locks", [Variant((9, 6),
        "SELECT count(*), count(*) FILTER (WHERE NOT granted) FROM pg_locks"
        " WHERE pid IS DISTINCT FROM pg_backend_pid()",
        [M("Locks Count", "locks", "Activity"),
         M("Waiting Locks", "locks", "Activity")])]),

    Query("table_stats", [Variant((9, 6),
        # with no user tables these counts are truly 0, so they are coalesced
        "SELECT (SELECT coalesce(sum(idx_scan), 0) FROM pg_stat_user_indexes),"
        " coalesce(sum(seq_scan), 0), coalesce(sum(n_dead_tup), 0), coalesce(sum(n_live_tup), 0),"
        " count(*) FILTER (WHERE coalesce(last_vacuum, last_autovacuum) IS NULL AND n_live_tup > 0),"
        " floor(extract(epoch FROM now() - min(greatest(last_vacuum, last_autovacuum))))::bigint"
        " FROM pg_stat_user_tables",
        [M("Index Scans", "scans", "DB and IO stats"),
         M("Sequential Scans", "scans", "DB and IO stats"),
         M("Dead Tuples", "rows", "Vacuum and Wraparound"),
         M("Live Tuples", "rows", "Vacuum and Wraparound"),
         M("Tables Never Vacuumed", "tables", "Vacuum and Wraparound"),
         M("Oldest Table Vacuum Age", "s", "Vacuum and Wraparound")])]),

    Query("index_hit", [Variant((9, 6),
        "SELECT CASE WHEN coalesce(sum(idx_blks_hit) + sum(idx_blks_read), 0) = 0 THEN NULL"
        " ELSE round(100.0 * sum(idx_blks_hit) / (sum(idx_blks_hit) + sum(idx_blks_read)), 2) END"
        " FROM pg_statio_user_tables",
        [M("Index Hit Percent", "%", "DB and IO stats", float)])]),

    Query("wraparound", [Variant((9, 6),
        "SELECT max(age(datfrozenxid)), max(mxid_age(datminmxid)),"
        " round(100.0 * max(age(datfrozenxid)) / current_setting('autovacuum_freeze_max_age')::numeric, 2)"
        " FROM pg_database WHERE datallowconn",
        [M("Max XID Age", "transactions", "Vacuum and Wraparound"),
         M("Max Multixact Age", "multixacts", "Vacuum and Wraparound"),
         M("XID Wraparound Percent", "%", "Vacuum and Wraparound", float)])]),

    Query("database_size", [Variant((9, 6),
        "SELECT round(sum(CASE WHEN has_database_privilege(oid, 'CONNECT')"
        " THEN pg_database_size(oid) ELSE 0 END) / 1048576.0, 2)"
        " FROM pg_database WHERE datallowconn",
        [M("Total Database Size", "MB", "DB and IO stats", float)])]),

    Query("checksums", [Variant((12, 0),
        # failures detected; 0 when none were (or checksums are off and none can be)
        "SELECT coalesce(sum(checksum_failures), 0) FROM pg_stat_database",
        [M("Checksum Failures", "failures", "DB and IO stats")])]),

    Query("wal_position", [
        Variant((10, 0),
            "SELECT round(pg_wal_lsn_diff(pg_current_wal_lsn(), '0/0') / 1048576.0, 2)",
            [M("WAL Written", "MB", "WAL and Archiving", float)]),
        Variant((9, 6),
            "SELECT round(pg_xlog_location_diff(pg_current_xlog_location(), '0/0') / 1048576.0, 2)",
            [M("WAL Written", "MB", "WAL and Archiving", float)])],
        role=PRIMARY),

    Query("wal_stats", [Variant((14, 0),
        "SELECT wal_buffers_full FROM pg_stat_wal",
        [M("WAL Buffers Full", "times", "WAL and Archiving")])]),

    Query("wal_directory", [Variant((10, 0),
        "SELECT count(*), round(coalesce(sum(size), 0) / 1048576.0, 2) FROM pg_ls_waldir()",
        [M("WAL Files", "files", "WAL and Archiving"),
         M("WAL Directory Size", "MB", "WAL and Archiving", float)])]),

    Query("archiver", [Variant((9, 6),
        "SELECT archived_count, failed_count,"
        " floor(extract(epoch FROM now() - last_archived_time))::bigint,"
        " CASE WHEN last_failed_time IS NOT NULL AND (last_archived_time IS NULL"
        " OR last_failed_time > last_archived_time) THEN 1 ELSE 0 END"
        " FROM pg_stat_archiver",
        [M("Archived Count", "files", "WAL and Archiving"),
         M("Archive Failed Count", "files", "WAL and Archiving"),
         M("Last Archive Age", "s", "WAL and Archiving"),
         M("Archiving Failing", "flag", "WAL and Archiving")])],
        when=lambda node: node.settings.get("archive_mode", "off") != "off"),

    # Its own query: listing the archive status directory needs pg_monitor, and without
    # that role only this metric should be missing, not every archive metric.
    Query("archive_ready", [Variant((12, 0),
        "SELECT count(*) FROM pg_ls_archive_statusdir() WHERE name LIKE '%.ready'",
        [M("Archive Ready Files", "files", "WAL and Archiving")])],
        when=lambda node: node.settings.get("archive_mode", "off") != "off"),

    Query("wal_receiver", [
        Variant((10, 0),
            "SELECT (SELECT count(*) FROM pg_stat_wal_receiver WHERE status = 'streaming'),"
            " CASE WHEN pg_last_wal_receive_lsn() = pg_last_wal_replay_lsn() THEN 0"
            " ELSE floor(extract(epoch FROM now() - pg_last_xact_replay_timestamp()))::bigint END,"
            " round(pg_wal_lsn_diff(pg_last_wal_receive_lsn(), pg_last_wal_replay_lsn()) / 1048576.0, 2),"
            " (SELECT floor(extract(epoch FROM now() - max(last_msg_receipt_time)))::bigint"
            " FROM pg_stat_wal_receiver)",
            [M("WAL Receiver Connected", "flag", "Replication"),
             M("Replay Lag", "s", "Replication"),
             M("Replay Backlog", "MB", "Replication", float),
             M("Last WAL Message Age", "s", "Replication")]),
        Variant((9, 6),
            "SELECT (SELECT count(*) FROM pg_stat_wal_receiver WHERE status = 'streaming'),"
            " CASE WHEN pg_last_xlog_receive_location() = pg_last_xlog_replay_location() THEN 0"
            " ELSE floor(extract(epoch FROM now() - pg_last_xact_replay_timestamp()))::bigint END,"
            " round(pg_xlog_location_diff(pg_last_xlog_receive_location(),"
            " pg_last_xlog_replay_location()) / 1048576.0, 2),"
            " (SELECT floor(extract(epoch FROM now() - max(last_msg_receipt_time)))::bigint"
            " FROM pg_stat_wal_receiver)",
            [M("WAL Receiver Connected", "flag", "Replication"),
             M("Replay Lag", "s", "Replication"),
             M("Replay Backlog", "MB", "Replication", float),
             M("Last WAL Message Age", "s", "Replication")])],
        role=STANDBY),

    Query("timeline", [
        Variant((10, 0),
            "SELECT ('x' || substr(pg_walfile_name(pg_current_wal_lsn()), 1, 8))::bit(32)::int",
            [M("Timeline", "timeline", "Cluster")]),
        Variant((9, 6),
            "SELECT ('x' || substr(pg_xlogfile_name(pg_current_xlog_location()), 1, 8))::bit(32)::int",
            [M("Timeline", "timeline", "Cluster")])],
        role=PRIMARY),

    Query("timeline_standby", [Variant((9, 6),
        "SELECT received_tli FROM pg_stat_wal_receiver",
        [M("Timeline", "timeline", "Cluster")])],
        role=STANDBY),

    Query("slots", [
        Variant((10, 0),
            "SELECT count(*), count(*) FILTER (WHERE NOT active),"
            " round(coalesce(max(pg_wal_lsn_diff(CASE WHEN pg_is_in_recovery()"
            " THEN pg_last_wal_receive_lsn() ELSE pg_current_wal_lsn() END, restart_lsn)), 0)"
            " / 1048576.0, 2)"
            " FROM pg_replication_slots",
            [M("Replication Slots", "slots", "Replication"),
             M("Inactive Replication Slots", "slots", "Replication"),
             M("Max Slot Retained WAL", "MB", "Replication", float)])],
        # Reported on every node: the template only registers metrics that have a value,
        # so a standby-registered template must carry them too. Note that HA managers
        # (Patroni) keep idle slots on standbys on purpose; see the README.
        ),

    Query("subscriptions", [
        Variant((15, 0),
            "SELECT count(*), count(s.pid),"
            " floor(extract(epoch FROM now() - max(s.last_msg_receipt_time)))::bigint,"
            " (SELECT coalesce(sum(apply_error_count), 0) FROM pg_stat_subscription_stats),"
            " (SELECT coalesce(sum(sync_error_count), 0) FROM pg_stat_subscription_stats)"
            " FROM pg_subscription sub LEFT JOIN pg_stat_subscription s"
            " ON s.subid = sub.oid AND s.relid IS NULL",
            [M("Subscriptions", "subscriptions", "Replication"),
             M("Active Subscriptions", "subscriptions", "Replication"),
             M("Last Subscription Message Age", "s", "Replication"),
             M("Subscription Apply Errors", "errors", "Replication"),
             M("Subscription Sync Errors", "errors", "Replication")]),
        Variant((10, 0),
            "SELECT count(*), count(s.pid),"
            " floor(extract(epoch FROM now() - max(s.last_msg_receipt_time)))::bigint"
            " FROM pg_subscription sub LEFT JOIN pg_stat_subscription s"
            " ON s.subid = sub.oid AND s.relid IS NULL",
            [M("Subscriptions", "subscriptions", "Replication"),
             M("Active Subscriptions", "subscriptions", "Replication"),
             M("Last Subscription Message Age", "s", "Replication")])]),
]

RATES = [
    Rate("Transactions Per Sec", "Total Commits", "transactions", SUMMARY),
    Rate("Rollbacks Per Sec", "Total Rollbacks", "transactions", "Transactions and Sessions"),
    Rate("Rows Inserted Per Sec", "Total Rows Inserted", "rows", "DB and IO stats"),
    Rate("Rows Updated Per Sec", "Total Rows Updated", "rows", "DB and IO stats"),
    Rate("Rows Deleted Per Sec", "Total Rows Deleted", "rows", "DB and IO stats"),
    Rate("Rows Fetched Per Sec", "Total Rows Fetched", "rows", "DB and IO stats"),
    Rate("Rows Returned Per Sec", "Total Rows Returned", "rows", "DB and IO stats"),
    Rate("Block Reads Per Sec", "Total Block Reads", "blocks", "DB and IO stats"),
    Rate("Sequential Scans Per Sec", "Sequential Scans", "scans", "DB and IO stats"),
    Rate("Index Scans Per Sec", "Index Scans", "scans", "DB and IO stats"),
    Rate("Temp Data Per Sec", "Total Temp Data", "MB", "DB and IO stats"),
    Rate("WAL Generated Per Sec", "WAL Written", "MB", "WAL and Archiving"),
    Rate("New Deadlocks", "Total Deadlocks", "deadlocks", "Transactions and Sessions", delta=True),
    Rate("New Conflicts", "Total Conflicts", "conflicts", "Transactions and Sessions", delta=True),
    Rate("New Requested Checkpoints", "Checkpoints Req", "checkpoints", "BG Writer", delta=True),
    Rate("New Archive Failures", "Archive Failed Count", "files", "WAL and Archiving", delta=True),
    Rate("New Checksum Failures", "Checksum Failures", "failures", "DB and IO stats", delta=True),
    Rate("New WAL Buffers Full", "WAL Buffers Full", "times", "WAL and Archiving", delta=True),
]

# Metrics computed in derive_metrics() rather than read from a query.
DERIVED = [
    M("Node Role", tab="Activity", kind=str),
    M("Connection Utilization", "%", SUMMARY, float),
    M("Buffer Cache Hit Percent", "%", SUMMARY, float),
    M("Collection Time", "ms", SUMMARY),
    M("Failed Queries", "queries", SUMMARY),
    M("Permission Gaps", "queries", SUMMARY),
    # Cluster layer (built in section 6 from the discovered nodes)
    M("Cluster Type", tab="Cluster", kind=str),
    M("Cluster Health", "status", SUMMARY),
    M("Health Code", "code", "Cluster"),
    M("Health Reason", tab="Cluster", kind=str),
    M("Primary Node", tab="Cluster", kind=str),
    M("Nodes Total", "nodes", "Cluster"),
    M("Nodes Up", "nodes", SUMMARY),
    M("Nodes Down", "nodes", "Cluster"),
    M("Standbys Streaming", "nodes", "Cluster"),
    M("Sync Standbys", "nodes", "Cluster"),
    M("Max Standby Replay Lag", "s", "Replication", float),
    M("Max Standby Backlog", "MB", "Replication", float),
    M("Last Failover Age", "s", "Cluster"),
    M("Failovers 24h", "failovers", "Cluster"),
]

# Child tables built by the cluster layer: name -> (tab, column units). The column
# order here is the order rows are built in; "" marks a string column.
CLUSTER_TABLES = {
    "Nodes": ("Cluster", {
        "role": "", "state": "", "address": "", "status": "flag", "reachable": "flag",
        "replay_lag_s": "s", "backlog_mb": "MB", "timeline": "timeline",
        "conn_pct": "%", "uptime_s": "s", "longest_query_s": "s",
        "last_msg_age_s": "s", "last_seen_s": "s"}),
    "Replication_Links": ("Replication", {
        "state": "", "sync_state": "", "client_addr": "", "sent_lag_mb": "MB",
        "write_lag_mb": "MB", "flush_lag_mb": "MB", "replay_lag_mb": "MB",
        "write_lag_s": "s", "flush_lag_s": "s", "replay_lag_s": "s"}),
    "Events": ("Cluster", {
        "event": "", "node": "", "old_role": "", "new_role": "", "age_s": "s"}),
}

# Health Code values: what the plugin alone can know about the cluster.
HEALTH_OK, HEALTH_NODE_DOWN, HEALTH_NO_PRIMARY, HEALTH_SPLIT_BRAIN = 0, 1, 2, 3
HEALTH_MANAGER_DISAGREES = 4
HEALTH_SEVERITY = {HEALTH_OK: 0, HEALTH_NODE_DOWN: 1, HEALTH_NO_PRIMARY: 2,
                   HEALTH_SPLIT_BRAIN: 2, HEALTH_MANAGER_DISAGREES: 1}

NODE_FORGET_S = 24 * 3600      # a missing node is reported for a day, then dropped
PROBE_TIMEOUT_S = 3
MAX_EVENTS = MAX_ROWS

TABLES = [
    Table("Stats_per_DB", "DB and IO stats", [((9, 6),
        "SELECT d.datname AS name, s.numbackends AS active_connections,"
        " round(CASE WHEN has_database_privilege(d.oid, 'CONNECT')"
        " THEN pg_database_size(d.oid) END / 1048576.0, 2) AS size_in_mb,"  # not readable: left blank, not 0
        " s.tup_inserted AS rows_inserted, s.tup_updated AS rows_updated,"
        " s.tup_deleted AS rows_deleted, s.tup_fetched AS rows_fetched,"
        " s.tup_returned AS rows_returned, s.blks_read AS block_reads, s.blks_hit AS block_hits,"
        " CASE WHEN s.blks_hit + s.blks_read = 0 THEN NULL"
        " ELSE round(100.0 * s.blks_hit / (s.blks_hit + s.blks_read), 2) END AS cache_hit_percent,"
        " s.deadlocks AS deadlocks, s.temp_files AS temp_files"
        " FROM pg_database d JOIN pg_stat_database s ON d.oid = s.datid"
        " WHERE d.datname NOT IN ('template0', 'template1')"
        " ORDER BY size_in_mb DESC NULLS LAST, d.datname")],
        {"active_connections": "connections", "size_in_mb": "MB", "rows_inserted": "rows",
         "rows_updated": "rows", "rows_deleted": "rows", "rows_fetched": "rows",
         "rows_returned": "rows", "block_reads": "blocks", "block_hits": "blocks",
         "cache_hit_percent": "%", "deadlocks": "deadlocks", "temp_files": "files"}),

    Table("Transactions_and_Sessions_per_Database", "Transactions and Sessions", [
        ((14, 0),
         "SELECT datname AS name, xact_commit AS commits, xact_rollback AS rollbacks,"
         " conflicts, sessions, sessions_abandoned, sessions_fatal, sessions_killed,"
         " round(session_time::numeric, 2) AS session_time,"
         " round(active_time::numeric, 2) AS sessions_active_time,"
         " round(idle_in_transaction_time::numeric, 2) AS session_idle_in_transaction_time"
         " FROM pg_stat_database WHERE datname IS NOT NULL"
         " AND datname NOT IN ('template0', 'template1') ORDER BY xact_commit DESC, datname"),
        ((9, 6),
         "SELECT datname AS name, xact_commit AS commits, xact_rollback AS rollbacks, conflicts"
         " FROM pg_stat_database WHERE datname IS NOT NULL"
         " AND datname NOT IN ('template0', 'template1') ORDER BY xact_commit DESC, datname")],
        {"commits": "transactions", "rollbacks": "transactions", "conflicts": "conflicts",
         "sessions": "sessions", "sessions_abandoned": "sessions", "sessions_fatal": "sessions",
         "sessions_killed": "sessions", "session_time": "ms", "sessions_active_time": "ms",
         "session_idle_in_transaction_time": "ms"}),

    Table("Wait_Events", "Activity", [
        ((10, 0),
         "SELECT coalesce(wait_event_type, 'CPU') || ':' || coalesce(wait_event, 'running') AS name,"
         " count(*) AS sessions FROM pg_stat_activity WHERE state = 'active' AND " + _CLIENTS_10 +
         " GROUP BY 1 ORDER BY 2 DESC, 1"),
        ((9, 6),
         "SELECT coalesce(wait_event_type, 'CPU') || ':' || coalesce(wait_event, 'running') AS name,"
         " count(*) AS sessions FROM pg_stat_activity WHERE state = 'active' AND " + _CLIENTS_96 +
         " GROUP BY 1 ORDER BY 2 DESC, 1")],
        {"sessions": "sessions"}),

    Table("Replication_Slots", "Replication", [
        ((14, 0),
         "SELECT s.slot_name AS name, s.slot_type, s.active::int AS active,"
         " round(coalesce(pg_wal_lsn_diff(CASE WHEN pg_is_in_recovery()"
         " THEN pg_last_wal_receive_lsn() ELSE pg_current_wal_lsn() END, s.restart_lsn), 0)"
         " / 1048576.0, 2) AS retained_mb, coalesce(s.wal_status, 'unknown') AS wal_status,"
         " age(s.catalog_xmin) AS catalog_xmin_age,"
         " round(coalesce(st.spill_bytes, 0) / 1048576.0, 2) AS spill_mb"
         " FROM pg_replication_slots s LEFT JOIN pg_stat_replication_slots st USING (slot_name)"
         " ORDER BY retained_mb DESC, s.slot_name"),
        ((13, 0),
         "SELECT slot_name AS name, slot_type, active::int AS active,"
         " round(coalesce(pg_wal_lsn_diff(CASE WHEN pg_is_in_recovery()"
         " THEN pg_last_wal_receive_lsn() ELSE pg_current_wal_lsn() END, restart_lsn), 0)"
         " / 1048576.0, 2) AS retained_mb, coalesce(wal_status, 'unknown') AS wal_status"
         " FROM pg_replication_slots ORDER BY retained_mb DESC, slot_name"),
        ((10, 0),
         "SELECT slot_name AS name, slot_type, active::int AS active,"
         " round(coalesce(pg_wal_lsn_diff(CASE WHEN pg_is_in_recovery()"
         " THEN pg_last_wal_receive_lsn() ELSE pg_current_wal_lsn() END, restart_lsn), 0)"
         " / 1048576.0, 2) AS retained_mb"
         " FROM pg_replication_slots ORDER BY retained_mb DESC, slot_name")],
        {"slot_type": "", "active": "flag", "retained_mb": "MB", "wal_status": "",
         "catalog_xmin_age": "transactions", "spill_mb": "MB"}),

    # Only when pg_stat_statements is installed in the monitored database.
    Table("Top_Queries", "Activity", [
        ((13, 0),
         "SELECT queryid::text AS name, calls, round(total_exec_time::numeric, 2) AS total_time_ms,"
         " round(mean_exec_time::numeric, 2) AS mean_time_ms, rows,"
         " left(regexp_replace(query, '\\s+', ' ', 'g'), 100) AS query"
         " FROM pg_stat_statements WHERE queryid IS NOT NULL"
         " ORDER BY total_exec_time DESC LIMIT 10"),
        ((9, 6),
         "SELECT queryid::text AS name, calls, round(total_time::numeric, 2) AS total_time_ms,"
         " round(mean_time::numeric, 2) AS mean_time_ms, rows,"
         " left(regexp_replace(query, '\\s+', ' ', 'g'), 100) AS query"
         " FROM pg_stat_statements WHERE queryid IS NOT NULL"
         " ORDER BY total_time DESC LIMIT 10")],
        {"calls": "calls", "total_time_ms": "ms", "mean_time_ms": "ms", "rows": "rows", "query": ""},
        # installed but not in shared_preload_libraries, the view raises an error on
        # every read: that is the extension's setup, not a collection failure
        when=lambda node: node.settings.get("pg_stat_statements"), optional=True),
]

# Per-database tables Site24x7 discovers as child items (as in version 1).
CHILD_DISCOVERY = ["Transactions_and_Sessions_per_Database", "Stats_per_DB"]


def all_metric_defs():
    """Every metric the plugin sends, in a stable order, without duplicates."""
    seen = {}
    for q in QUERIES:
        for v in q.variants:
            for f in v.fields:
                seen.setdefault(f.name, f)
    for r in RATES:
        seen.setdefault(r.name, M(r.name, r.unit, r.tab, float))
    for d in DERIVED:
        seen.setdefault(d.name, d)
    return [m for m in seen.values() if m.name not in HIDDEN_COUNTERS]


def build_tabs_and_units():
    """`tabs` and `units` generated from the catalogue, so they cannot drift apart."""
    tabs = {}
    for i, name in enumerate(TAB_ORDER, start=1):
        tabs[name] = {"order": str(i), "tablist": []}
    units = {}
    for t in TABLES:
        tabs[t.tab]["tablist"].append(t.name)
        units[t.name] = {c: u for c, u in t.units.items() if u}
    for name, (tab, cols) in CLUSTER_TABLES.items():
        tabs[tab]["tablist"].append(name)
        units[name] = {c: u for c, u in cols.items() if u}
    for m in all_metric_defs():
        if m.tab:
            tabs[m.tab]["tablist"].append(m.name)
        if m.kind is not str and m.unit:
            units[m.name] = m.unit
    return tabs, units


# =============================================================================
# 2. HELPERS
# =============================================================================

def clean_quotes(value):
    """cfg values may arrive wrapped in quotes (host="localhost")."""
    if value is None:
        return value
    s = str(value).strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    return s


def parse_bool(value, default=True):
    if value is None or str(value).strip() == "":
        return default
    return str(clean_quotes(value)).strip().lower() in ("1", "true", "yes", "on")


def to_number(value, kind):
    """Converts a database value to int/float/str; returns None for NULL or non-finite."""
    if value is None:
        return None
    if kind is str:
        return str(value)[:MAX_STRING_CHARS]
    try:
        num = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(num) or math.isinf(num):
        return None
    return int(round(num)) if kind is int else round(num, 4)


def table_cell(value):
    if value is None:
        return None
    if isinstance(value, bool):
        return int(value)
    if isinstance(value, (int, float)):
        return value if not (isinstance(value, float) and (math.isnan(value) or math.isinf(value))) else None
    try:
        num = float(value)
        return int(num) if num.is_integer() and "." not in str(value) else round(num, 4)
    except (TypeError, ValueError):
        return str(value)[:MAX_STRING_CHARS]


def safe_row_name(value):
    return re.sub(r"[^A-Za-z0-9_.:-]", "_", str(value))[:MAX_NAME_CHARS] or "unknown"


def scrub(text):
    """Keeps passwords and connection strings out of anything shown to the user."""
    text = re.sub(r"(password\s*=\s*)\S+", r"\1***", str(text), flags=re.IGNORECASE)
    return " ".join(text.split())


# =============================================================================
# 3. CONNECTION
# =============================================================================

class Node(object):
    """One PostgreSQL server connection with per-query failure isolation."""

    def __init__(self, host, port, user, password, dbname, sslmode="", sslrootcert="",
                 sslcert="", sslkey="", connect_timeout=CONNECT_TIMEOUT_S):
        self.host = host
        self.port = int(port)
        self.user = user
        self.password = password
        self.dbname = dbname
        self.sslmode = sslmode
        self.sslrootcert = sslrootcert
        self.sslcert = sslcert
        self.sslkey = sslkey
        self.connect_timeout = connect_timeout
        self.conn = None
        self.version = (0, 0)
        self.is_recovery = False
        self.settings = {}
        self.identity = ""
        self.error = ""
        self.auth_failed = False
        self.failures = []      # real query failures
        self.denied = []        # objects this user may not read (permission gaps)

    @property
    def role(self):
        return ROLE_STANDBY if self.is_recovery else ROLE_PRIMARY

    def connect(self):
        kwargs = {
            "host": self.host, "port": self.port, "user": self.user, "dbname": self.dbname,
            "connect_timeout": self.connect_timeout,
            "application_name": "site24x7_postgres",
            "options": "-c statement_timeout=%d -c lock_timeout=2000"
                       " -c default_transaction_read_only=on" % STATEMENT_TIMEOUT_MS,
        }
        if self.password:
            kwargs["password"] = self.password
        for key in ("sslmode", "sslrootcert", "sslcert", "sslkey"):
            if getattr(self, key):
                kwargs[key] = getattr(self, key)
        try:
            try:
                self.conn = psycopg2.connect(**kwargs)
            except Exception as e:
                # Connection poolers (PgBouncer) refuse the "options" startup parameter.
                # Every query this plugin runs is a read, so retrying without it is safe.
                if "options" not in str(e).lower():
                    raise
                kwargs.pop("options")
                self.conn = psycopg2.connect(**kwargs)
            self.conn.autocommit = True
        except Exception as e:
            text = str(e)
            self.auth_failed = getattr(e, "pgcode", None) in ("28000", "28P01") or \
                "authentication failed" in text.lower()
            self.error = scrub(text)
            return False
        num = getattr(self.conn, "server_version", 0) or 0
        # 10+: 160004 -> (16, 4); before 10: 90624 -> (9, 6)
        self.version = (num // 10000, num % 10000) if num >= 100000 else (num // 10000, (num // 100) % 100)
        row = self.query_one(
            "SELECT pg_is_in_recovery(), current_setting('archive_mode'),"
            " pg_postmaster_start_time()::text,"
            " (SELECT count(*) FROM pg_extension WHERE extname = 'pg_stat_statements')")
        if row:
            self.is_recovery = bool(row[0])
            self.settings["archive_mode"] = row[1]
            self.identity = "%s:%s|%s" % (self.host, self.port, row[2])
            self.settings["pg_stat_statements"] = bool(row[3]) if len(row) > 3 else False
        return True

    def record_failure(self, exc):
        """Sorts a query error into a permission gap (the user chose not to grant a role)
        or a real failure. Only real failures are collection problems."""
        text = str(exc).splitlines()[0] if str(exc) else type(exc).__name__
        if getattr(exc, "pgcode", None) == "42501" or "permission denied" in text.lower():
            what = re.sub(r"(?i)^.*permission denied (for )?", "", text).strip() or text
            self.denied.append(scrub(what))
        else:
            self.failures.append(scrub(text))

    def query_all(self, sql, with_columns=False):
        """Rows of `sql` (with column names first if asked), or None if it failed."""
        if self.conn is None:
            return None
        cur = None
        try:
            cur = self.conn.cursor()
            cur.execute("/* site24x7 */ " + sql)
            rows = cur.fetchall()
            return ([d[0] for d in cur.description], rows) if with_columns else rows
        except Exception as e:
            self.record_failure(e)
            return None
        finally:
            if cur is not None:
                try:
                    cur.close()
                except Exception:
                    pass

    def query_one(self, sql):
        rows = self.query_all(sql)
        if rows is None:
            return None
        return rows[0] if rows else ()

    def close(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception:
                pass
            self.conn = None


# =============================================================================
# 4. STATE (previous counters, for rates)
# =============================================================================

def state_path(host, port, dbname):
    key = "%s:%s/%s" % (host, port, dbname)
    return os.path.join(STATE_DIR, hashlib.sha1(key.encode("utf-8")).hexdigest()[:16] + ".json")


def load_state(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, dict) else {}
    except (OSError, ValueError):
        return {}


def save_state(path, state):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            json.dump(state, fh)
        os.replace(tmp, path)
        return True
    except OSError:
        return False


# =============================================================================
# 5. COLLECTION
# =============================================================================

def applies(entry, node):
    if entry.role == PRIMARY and node.is_recovery:
        return False
    if entry.role == STANDBY and not node.is_recovery:
        return False
    return entry.when is None or bool(entry.when(node))


def collect_metrics(node, deadline, only=None):
    """Runs every applicable single-row query (or only the keys in `only`, in that
    order); returns {metric: value}."""
    out = {}
    queries = QUERIES if only is None else [q for k in only for q in QUERIES if q.key == k]
    for q in queries:
        if time.time() > deadline:
            node.failures.append("cycle time budget exhausted before '%s'" % q.key)
            break
        if not applies(q, node):
            continue
        variant = q.pick(node.version)
        if variant is None:
            continue
        row = node.query_one(variant.sql)
        if not row:
            continue
        for field, value in zip(variant.fields, row):
            num = to_number(value, field.kind)
            if num is not None:
                out[field.name] = num
    return out


def collect_tables(node, deadline):
    """Runs every applicable table query; returns {table: [rows]}, at most MAX_ROWS each."""
    out = {}
    for t in TABLES:
        if time.time() > deadline:
            node.failures.append("cycle time budget exhausted before '%s'" % t.name)
            break
        if not applies(t, node):
            continue
        sql = t.pick(node.version)
        before, denied_before = len(node.failures), len(node.denied)
        result = node.query_all(sql, with_columns=True) if sql else None
        if result is None and t.optional:
            del node.failures[before:]
            del node.denied[denied_before:]
        if result is None:
            continue
        cols, rows = result
        table_rows = []
        seen = set()
        for r in rows:
            row = {}
            for c, v in zip(cols, r):
                if c == "name":
                    row["name"] = safe_row_name(v)
                else:
                    cell = table_cell(v)
                    if cell is not None:
                        row[c] = cell
            if row.get("name") and row["name"] not in seen:
                seen.add(row["name"])
                table_rows.append(row)
            if len(table_rows) >= MAX_ROWS:
                break
        out[t.name] = table_rows
    return out


def compute_rates(metrics, prev, now, identity):
    """Rates and deltas from the previous sample of the same server process."""
    out = {}
    prev_counters = prev.get("counters") or {}
    dt = now - float(prev.get("ts") or 0)
    if prev.get("identity") != identity or not RATE_MIN_INTERVAL_S <= dt <= RATE_MAX_INTERVAL_S:
        return out
    for r in RATES:
        cur = metrics.get(r.source)
        old = prev_counters.get(r.source)
        if cur is None or old is None:
            continue
        diff = float(cur) - float(old)
        if diff < 0:          # statistics were reset; skip one poll
            continue
        out[r.name] = int(diff) if r.delta else round(diff * r.scale / dt, 2)
    return out


RATE_SAMPLE_S = 5.0          # 2 s was measured 75% off under load; 5 s within ~10%


def sampled_rates(node, deadline):
    """Real rates on a monitor's first poll, when there is no previous sample: reads
    the rate counters twice, RATE_SAMPLE_S apart.

    Site24x7 builds the template only from metrics that have a value when a monitor
    registers, so without this no rate metric would ever be registered. The counter
    queries run back to back, with `database_totals` last in the first reading and
    first in the second, so only one of the plugin's own statements (one commit)
    falls between its two readings; that commit is taken off.
    Returns (rates, second_reading, time_of_second_reading)."""
    sources = {r.source for r in RATES}
    keys = [q.key for q in QUERIES if q.key != "database_totals"
            and any(f.name in sources for v in q.variants for f in v.fields)]
    if time.time() + RATE_SAMPLE_S + 5 > deadline:
        return {}, {}, time.time()
    first = collect_metrics(node, deadline, only=keys + ["database_totals"])
    t_first = time.time()
    time.sleep(RATE_SAMPLE_S)
    second = collect_metrics(node, deadline, only=["database_totals"] + keys)
    t_second = time.time()
    counters = {k: v for k, v in first.items() if k in sources}
    if "Total Commits" in counters and "Total Commits" in second:
        counters["Total Commits"] = min(counters["Total Commits"] + 1, second["Total Commits"])
    prev = {"ts": t_first, "identity": node.identity, "counters": counters}
    return compute_rates(second, prev, t_second, node.identity), second, t_second


def truthful_zeros(node, metrics):
    """Values that are genuinely 0 for this node rather than unknown, so the metric is
    sent (and registered in the template) instead of left out.

    A value is filled only where there is nothing to measure. Where something should
    have been measured and was not (a standby with no WAL receiver, archiving on but
    nothing archived yet, a disabled subscription, a table never vacuumed), the value
    is unknown and stays out, so "age above X" alerts are never silenced by a fake 0."""
    zeros = {}
    if node.settings.get("archive_mode", "off") == "off":
        # nothing is archived, so nothing has been archived, failed or is waiting
        zeros.update({"Archived Count": 0, "Archive Failed Count": 0, "Archiving Failing": 0,
                      "Archive Ready Files": 0, "New Archive Failures": 0, "Last Archive Age": 0})
    if not node.is_recovery:
        # a primary replays nothing and receives WAL from no one
        zeros.update({"Replay Lag": 0, "Replay Backlog": 0.0, "WAL Receiver Connected": 0,
                      "Last WAL Message Age": 0})
    else:
        # a standby generates no WAL of its own
        zeros.update({"WAL Generated Per Sec": 0.0, "WAL Written": 0.0})
    if not metrics.get("Subscriptions"):
        zeros["Last Subscription Message Age"] = 0      # no subscription, nothing to wait for
    if not metrics.get("Tables Never Vacuumed"):
        zeros["Oldest Table Vacuum Age"] = 0            # no table with rows awaits a first vacuum
    zeros["Index Hit Percent"] = 100.0                  # no index reads: no misses, never a fake 0 %
    return {k: v for k, v in zeros.items() if k not in metrics}


def derive_metrics(node, metrics):
    out = {"Node Role": node.role}
    conns, max_conns = metrics.get("Active Connections"), metrics.get("Max Connections")
    if conns is not None and max_conns:
        out["Connection Utilization"] = round(100.0 * conns / max_conns, 2)
    hits, reads = metrics.get("Total Block Hits"), metrics.get("Total Block Reads")
    if hits is not None and reads is not None and hits + reads > 0:
        out["Buffer Cache Hit Percent"] = round(100.0 * hits / (hits + reads), 2)
    return out


# =============================================================================
# 6. CLUSTER LAYER
#
# An adapter answers two questions for one kind of cluster: "is this my kind?"
# and "which nodes exist?". The first adapter that recognises the seed wins.
# Whatever an adapter claims, a node's role is taken from pg_is_in_recovery()
# whenever the plugin can connect to it.
# =============================================================================

LOOPBACK = ("localhost", "127.0.0.1", "::1", "")


def parse_address_map(raw):
    """'10.0.0.5:5432=127.0.0.1:5441,pg2=127.0.0.1:5442' -> {source: target}."""
    out = {}
    for pair in str(raw or "").split(","):
        if "=" in pair:
            src, dst = pair.split("=", 1)
            if src.strip() and dst.strip():
                out[src.strip()] = dst.strip()
    return out


def map_address(host, port, address_map):
    """Translates an address as the cluster reports it into one the agent can reach."""
    target = address_map.get("%s:%s" % (host, port)) or address_map.get(str(host))
    if not target:
        return host, port
    if ":" in target:
        h, p = target.rsplit(":", 1)
        try:
            return h, int(p)
        except ValueError:
            return h, port
    return target, port


def node_row(name, role, state, status, address="", **extra):
    row = {"name": safe_row_name(name), "role": role, "state": state,
           "status": 1 if status else 0, "address": address[:MAX_STRING_CHARS],
           "reachable": 0}
    row.update({k: v for k, v in extra.items() if v is not None})
    return row


def seed_name(seed):
    """A node is named by its address, never by its role, so a promotion or a
    demotion keeps the same name (and its history) in the Nodes table."""
    row = seed.query_one("SELECT host(inet_server_addr())")
    if row and row[0] and row[0] not in LOOPBACK:
        return row[0]
    # Names are never DNS-resolved: some resolvers answer unknown names with a public IP.
    return seed.host if seed.host not in LOOPBACK else "local"


def own_application_name(seed):
    """The application_name this standby's WAL receiver presents to its primary."""
    row = seed.query_one(
        "SELECT coalesce(substring(conninfo FROM 'application_name=([^ ]+)'),"
        " nullif(current_setting('cluster_name'), ''), 'walreceiver')"
        " FROM pg_stat_wal_receiver")
    return row[0] if row else ""


def upstream_of(seed):
    """(host, port, streaming) of the primary a standby replicates from, or None."""
    if seed.version >= (11, 0):
        row = seed.query_one("SELECT sender_host, sender_port, status = 'streaming'"
                             " FROM pg_stat_wal_receiver")
    else:
        row = seed.query_one(
            "SELECT substring(conninfo FROM 'host=([^ ]+)'),"
            " coalesce(substring(conninfo FROM 'port=([0-9]+)'), '5432'), status = 'streaming'"
            " FROM pg_stat_wal_receiver")
    if not row or not row[0]:
        return None
    try:
        return str(row[0]), int(row[1] or 5432), bool(row[2])
    except (TypeError, ValueError):
        return None


def replication_view(primary, by_app_name=False, logical=False):
    """The primary's pg_stat_replication rows: one dict per attached standby.

    Logical walsenders (subscribers, not standbys) are excluded unless `logical`.
    `by_app_name` names rows by application_name, which Patroni sets to the member name."""
    if primary.version >= (10, 0):
        kind = "" if logical else (
            " WHERE pid NOT IN (SELECT active_pid FROM pg_replication_slots"
            " WHERE slot_type = 'logical' AND active_pid IS NOT NULL)")
        sql = ("SELECT application_name, coalesce(host(client_addr), ''), state, sync_state,"
               " round(pg_wal_lsn_diff(pg_current_wal_lsn(), sent_lsn) / 1048576.0, 2),"
               " round(pg_wal_lsn_diff(pg_current_wal_lsn(), write_lsn) / 1048576.0, 2),"
               " round(pg_wal_lsn_diff(pg_current_wal_lsn(), flush_lsn) / 1048576.0, 2),"
               " round(pg_wal_lsn_diff(pg_current_wal_lsn(), replay_lsn) / 1048576.0, 2),"
               " extract(epoch FROM write_lag), extract(epoch FROM flush_lag),"
               " extract(epoch FROM replay_lag), current_setting('port')"
               " FROM pg_stat_replication" + kind + " ORDER BY application_name")
    else:
        sql = ("SELECT application_name, coalesce(host(client_addr), ''), state, sync_state,"
               " round(pg_xlog_location_diff(pg_current_xlog_location(), sent_location) / 1048576.0, 2),"
               " round(pg_xlog_location_diff(pg_current_xlog_location(), write_location) / 1048576.0, 2),"
               " round(pg_xlog_location_diff(pg_current_xlog_location(), flush_location) / 1048576.0, 2),"
               " round(pg_xlog_location_diff(pg_current_xlog_location(), replay_location) / 1048576.0, 2),"
               " NULL, NULL, NULL, current_setting('port')"
               " FROM pg_stat_replication ORDER BY application_name")
    rows = primary.query_all(sql)
    if rows is None:
        return None
    links, used = [], set()
    for r in rows:
        app, addr = str(r[0] or "").strip(), str(r[1] or "")
        meaningful_app = app if app and app != "walreceiver" else ""
        name = (meaningful_app or addr) if by_app_name else (addr or meaningful_app or "standby")
        if name in used:
            name = "%s-%d" % (name, len(used) + 1)
        used.add(name)
        replay_mb = to_number(r[7], float)
        replay_s = to_number(r[10], float)
        if replay_s is None and replay_mb == 0:
            replay_s = 0.0          # caught up and idle: PostgreSQL reports NULL lag
        links.append({
            "name": safe_row_name(name), "app": app, "client_addr": addr,
            "port": to_number(r[11], int) or 5432,
            "state": str(r[2] or "unknown"),
            # 'quorum' (ANY n) standbys are synchronous candidates too
            "sync_state": str(r[3] or "async"),
            "sent_lag_mb": to_number(r[4], float), "write_lag_mb": to_number(r[5], float),
            "flush_lag_mb": to_number(r[6], float), "replay_lag_mb": replay_mb,
            "write_lag_s": to_number(r[8], float), "flush_lag_s": to_number(r[9], float),
            "replay_lag_s": replay_s,
        })
    return links


def quiet_query(node, sql, all_rows=False):
    """A probe query whose failure is expected on most servers and is not a collection error."""
    before, denied_before = len(node.failures), len(node.denied)
    result = node.query_all(sql) if all_rows else node.query_one(sql)
    del node.failures[before:]
    del node.denied[denied_before:]
    return result


def preloaded(seed, library):
    """True if the server loads `library`. Reading shared_preload_libraries needs
    pg_read_all_settings; without it, an installed extension of that name counts."""
    row = quiet_query(seed, "SELECT current_setting('shared_preload_libraries')")
    if row and library in str(row[0]):
        return True
    ext = quiet_query(seed, "SELECT count(*) FROM pg_extension WHERE extname = '%s'" % library)
    return bool(ext and ext[0])


def metadata_node(seed, ctx, dbname):
    """A connection to the same server for metadata kept in another database
    (repmgr keeps it in `repmgr`, pg_auto_failover in `pg_auto_failover`)."""
    if seed.dbname == dbname:
        return seed, False
    node = ctx["connect"](seed.host, seed.port, dbname)
    return node, node is not None


def fetch_json(host, port, path, scheme="http", verify=True, timeout=PROBE_TIMEOUT_S,
               cafile="", certfile="", keyfile="", username="", password=""):
    """GET a JSON document from a cluster manager's REST API (Patroni).

    HTTPS certificates are verified (against `cafile` if given) unless the user
    explicitly turned that off. `certfile`/`keyfile` present a client certificate,
    for Patroni's `verify_client: required`. `username`/`password` send basic auth,
    for a proxy in front of the API; Patroni itself never asks for it on reads."""
    import base64
    import ssl
    import urllib.request
    context = None
    try:
        if scheme == "https":   # inside the try: a bad cert path falls back to SQL discovery
            context = ssl.create_default_context(cafile=cafile or None)
            if not verify:
                context.check_hostname = False
                context.verify_mode = ssl.CERT_NONE
            if certfile:
                context.load_cert_chain(certfile, keyfile or None)
        url = "%s://%s:%s%s" % (scheme, host, port, path)
        request = urllib.request.Request(url)
        if username:
            token = base64.b64encode(("%s:%s" % (username, password)).encode("utf-8")).decode("ascii")
            request.add_header("Authorization", "Basic " + token)
        with urllib.request.urlopen(request, timeout=timeout, context=context) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except Exception:
        return None


def address_matches(row_host, row_port, seed, seed_addr):
    return (str(row_host) in (seed.host, seed_addr) and int(row_port) == seed.port) or \
        (seed_addr and str(row_host) == seed_addr)


def registry_rows(seed, ctx, members):
    """Rows for nodes listed by a cluster manager: (name, host, port, claimed_role, state, alive, extra)."""
    seed_addr_row = quiet_query(seed, "SELECT coalesce(host(inet_server_addr()), '')")
    seed_addr = seed_addr_row[0] if seed_addr_row else ""
    rows, seed_seen = [], False
    for name, host, port, role, state, alive, extra in members:
        mhost, mport = map_address(host, port, ctx["address_map"])
        if not seed_seen and (address_matches(host, port, seed, seed_addr)
                              or (mhost, mport) == (seed.host, seed.port)):
            row = seed_row(seed, ctx, name=name)
            row["state"] = state
            seed_seen = True
            if role in (ROLE_PRIMARY, ROLE_STANDBY):
                row["_claimed"] = role
            else:
                row["role"] = role
        else:
            row = node_row(name, role, state, alive, address="%s:%s" % (mhost, mport))
            row["_probe"] = (mhost, mport)
            if role in (ROLE_PRIMARY, ROLE_STANDBY):
                row["_claimed"] = role
        row.update({k: v for k, v in extra.items() if v is not None})
        rows.append(row)
    return rows


class PatroniAdapter(object):
    """Patroni's REST API lists every member, including stopped ones. Used only when
    `patroni_port` is configured."""
    name = "patroni"
    single_writer = True

    def detect(self, seed, ctx):
        port = ctx["args"].get("patroni_port")
        if not port:
            return False
        host, rport = map_address(seed.host, port, ctx["address_map"])
        a = ctx["args"]
        ctx["patroni"] = fetch_json(host, rport, "/cluster", a.get("patroni_scheme", "http"),
                                    a.get("patroni_verify", True),
                                    cafile=a.get("patroni_cafile", ""),
                                    certfile=a.get("patroni_certfile", ""),
                                    keyfile=a.get("patroni_keyfile", ""),
                                    username=a.get("patroni_username", ""),
                                    password=a.get("patroni_password", ""))
        return bool(ctx["patroni"] and ctx["patroni"].get("members"))

    def nodes(self, seed, ctx):
        members, leader = [], ""
        for m in ctx["patroni"]["members"]:
            role = ROLE_PRIMARY if m.get("role") in ("leader", "master") else ROLE_STANDBY
            state = str(m.get("state") or "unknown")
            if role == ROLE_PRIMARY:
                leader = m.get("name", "")
            lag = m.get("lag")
            members.append((m.get("name") or m.get("host"), m.get("host"), int(m.get("port") or 5432),
                            role, state, state in ("running", "streaming", "in archive recovery"),
                            {"timeline": to_number(m.get("timeline"), int),
                             "backlog_mb": round(lag / 1048576.0, 2) if isinstance(lag, (int, float)) else None}))
        rows = registry_rows(seed, ctx, members)
        links = None
        lrow = next((r for r in rows if r["name"] == leader), None)
        if lrow is not None:
            lnode = seed if "_probe" not in lrow else ctx["connect"](*lrow["_probe"])
            if lnode is not None:
                try:
                    links = replication_view(lnode, by_app_name=True)
                finally:
                    if lnode is not seed:
                        lnode.close()
        apply_link_lag(rows, links)
        return ClusterView(nodes=rows, links=links, primary_name=leader)


class RepmgrAdapter(object):
    """repmgr's node registry (repmgr.nodes), read from the `repmgr` database."""
    name = "repmgr"
    single_writer = True

    def detect(self, seed, ctx):
        return preloaded(seed, "repmgr")

    def nodes(self, seed, ctx):
        meta, opened = metadata_node(seed, ctx, "repmgr")
        if meta is None:
            return StreamingAdapter().nodes(seed, ctx)
        try:
            reg = quiet_query(meta, "SELECT node_name, conninfo, type, active FROM repmgr.nodes"
                                    " ORDER BY node_id", all_rows=True)
        finally:
            if opened:
                meta.close()
        if not reg:
            return StreamingAdapter().nodes(seed, ctx)
        members = []
        for name, conninfo, ntype, active in reg:
            host = re.search(r"host=(\S+)", str(conninfo or ""))
            port = re.search(r"port=(\d+)", str(conninfo or ""))
            role = {"primary": ROLE_PRIMARY, "standby": ROLE_STANDBY}.get(ntype, ntype)
            # a conninfo without port= means libpq's default, 5432 (not the seed's port)
            members.append((name, host.group(1) if host else name, int(port.group(1)) if port else 5432,
                            role, "active" if active else "inactive", bool(active), {}))
        rows = registry_rows(seed, ctx, members)
        primary = next((r["name"] for r in rows if r.get("_claimed", r["role"]) == ROLE_PRIMARY), "")
        links = None
        prow = next((r for r in rows if r["name"] == primary), None)
        if prow is not None:
            # a standby seed reads the links from the registry's primary
            pnode = seed if "_probe" not in prow else ctx["connect"](*prow["_probe"])
            if pnode is not None:
                try:
                    if not pnode.is_recovery:
                        links = replication_view(pnode)
                finally:
                    if pnode is not seed:
                        pnode.close()
        apply_link_lag(rows, links)
        return ClusterView(nodes=rows, links=links, primary_name=primary)


def apply_link_lag(rows, links):
    """Copies replay lag from the primary's replication links onto the standby rows.
    A link matches a row by name or by application_name (repmgr and Patroni set it to
    the node name)."""
    for r in rows:
        if r["role"] != ROLE_STANDBY:
            continue
        link = next((l for l in links or [] if r["name"] in (l["name"], l.get("app"))), None)
        if link:
            r["replay_lag_s"] = link["replay_lag_s"]
            r["backlog_mb"] = link["replay_lag_mb"]


class AutoFailoverMonitorAdapter(object):
    """pg_auto_failover, when the configured address is its monitor node. (Pointed at a
    data node, the streaming adapter finds the pair instead.)"""
    name = "pg_auto_failover"
    single_writer = True

    def detect(self, seed, ctx):
        return preloaded(seed, "pgautofailover")

    def nodes(self, seed, ctx):
        meta, opened = metadata_node(seed, ctx, "pg_auto_failover")
        reg = None
        if meta is not None:
            try:
                # goalstate is what the monitor has decided; reportedstate can be stale
                # for a crashed node. health is the monitor's own check (1 = healthy).
                reg = quiet_query(meta, "SELECT nodename, nodehost, nodeport, goalstate, health"
                                        " FROM pgautofailover.node ORDER BY nodeid", all_rows=True)
            finally:
                if opened:
                    meta.close()
        monitor = seed_row(seed, ctx)
        monitor["role"] = "monitor"
        members = []
        for name, host, port, goal, health in reg or []:
            role = ROLE_PRIMARY if goal in ("primary", "single", "wait_primary") else ROLE_STANDBY
            members.append((name, host, int(port), role, str(goal), health == 1, {}))
        rows = [monitor] + [r for r in registry_rows(seed, ctx, members) if r["name"] != monitor["name"]]
        primary = next((r["name"] for r in rows if r.get("_claimed") == ROLE_PRIMARY), "")
        return ClusterView(nodes=rows, primary_name=primary)


class CitusAdapter(object):
    """Citus: a coordinator plus workers, each its own primary (pg_dist_node)."""
    name = "citus"
    single_writer = False

    def detect(self, seed, ctx):
        row = seed.query_one("SELECT count(*) FROM pg_extension WHERE extname = 'citus'")
        return bool(row and row[0])

    def nodes(self, seed, ctx):
        reg = quiet_query(seed, "SELECT nodename, nodeport, groupid, noderole, isactive"
                                " FROM pg_dist_node ORDER BY groupid, nodename", all_rows=True) or []
        members = [(n, n, int(p), "coordinator" if g == 0 else
                    ("worker" if r == "primary" else "worker standby"),
                    "active" if a else "inactive", bool(a), {}) for n, p, g, r, a in reg]
        rows = registry_rows(seed, ctx, members)
        if not any("_probe" not in r for r in rows):      # the coordinator is not registered
            coord = seed_row(seed, ctx)
            coord["role"] = "coordinator"
            rows.insert(0, coord)
        return ClusterView(nodes=rows, primary_name=rows[0]["name"])


class PgpoolAdapter(object):
    """pgpool-II: the configured address is the pool; SHOW POOL_NODES lists the backends.
    The probe fails on plain PostgreSQL, so it is retried at most once a day."""
    name = "pgpool"
    single_writer = True

    def detect(self, seed, ctx):
        memo = ctx["prev_cluster"].get("pgpool_checked", 0)
        if not ctx["prev_cluster"].get("pgpool") and ctx["now"] - memo < 86400:
            return False
        ctx["state_extra"]["pgpool_checked"] = ctx["now"]
        if seed.conn is None:
            return False
        try:
            cur = seed.conn.cursor()
            cur.execute("SHOW POOL_NODES")
            cols = [d[0] for d in cur.description]
            ctx["pool_nodes"] = [dict(zip(cols, r)) for r in cur.fetchall()]
            cur.close()
        except Exception:
            ctx["pool_nodes"] = None
        ctx["state_extra"]["pgpool"] = bool(ctx["pool_nodes"])
        return bool(ctx["pool_nodes"])

    def nodes(self, seed, ctx):
        members = []
        for n in ctx["pool_nodes"]:
            role = ROLE_PRIMARY if str(n.get("role", "")).lower() in ("primary", "master") else ROLE_STANDBY
            state = str(n.get("status", "unknown"))
            members.append(("%s:%s" % (n.get("hostname"), n.get("port")), n.get("hostname"),
                            int(n.get("port") or 5432), role, state, state in ("up", "waiting"), {}))
        rows = []
        for name, host, port, role, state, alive, _ in members:
            mhost, mport = map_address(host, port, ctx["address_map"])
            row = node_row(name, role, state, alive, address="%s:%s" % (mhost, mport))
            row["_probe"], row["_claimed"] = (mhost, mport), role
            rows.append(row)
        primary = next((r["name"] for r in rows if r["_claimed"] == ROLE_PRIMARY), "")
        return ClusterView(nodes=rows, primary_name=primary)


class LogicalAdapter(object):
    """Logical replication between writable nodes: native publications/subscriptions,
    and the extensions built on logical decoding (pglogical, Spock, BDR/PGD). Every
    node is a writer; peers are found from the logical walsenders and subscriptions."""
    name = "logical"
    single_writer = False
    EXTENSIONS = ("bdr", "spock", "pglogical")

    def detect(self, seed, ctx):
        if seed.is_recovery or seed.version < (10, 0):
            return False
        row = seed.query_one(
            "SELECT (SELECT count(*) FROM pg_subscription),"
            " (SELECT count(*) FROM pg_replication_slots WHERE slot_type = 'logical' AND active),"
            " (SELECT string_agg(extname, ',') FROM pg_extension WHERE extname IN ('bdr', 'spock', 'pglogical'))")
        if not row:
            return False
        ctx["logical_ext"] = (row[2] or "").split(",")[0]
        # both directions present, or an extension that is multi-writer by design
        return bool((row[0] and row[1]) or ctx["logical_ext"])

    def nodes(self, seed, ctx):
        peers = quiet_query(seed,
            "SELECT DISTINCT host(r.client_addr) FROM pg_stat_replication r"
            " JOIN pg_replication_slots s ON s.active_pid = r.pid"
            " WHERE s.slot_type = 'logical' AND r.client_addr IS NOT NULL", all_rows=True) or []
        port_row = seed.query_one("SELECT current_setting('port')")
        port = int(port_row[0]) if port_row else seed.port
        me = seed_row(seed, ctx)
        me["role"] = "writer"
        rows = [me]
        for (addr,) in peers:
            if addr == me["name"]:
                continue
            host, mport = map_address(addr, port, ctx["address_map"])
            row = node_row(addr, "writer", "replicating", True, address="%s:%s" % (host, mport))
            row["_probe"] = (host, mport)
            rows.append(row)
        return ClusterView(nodes=rows, links=replication_view(seed, logical=True))


class StandaloneAdapter(object):
    name = "standalone"
    single_writer = True

    def detect(self, seed, ctx):
        return True

    def nodes(self, seed, ctx):
        return ClusterView(nodes=[seed_row(seed, ctx)], primary_name=seed_name(seed))


class StreamingAdapter(object):
    """Plain streaming replication, and anything built on it (CloudNativePG, Stolon,
    keepalived, managed services). Nodes come from the primary's pg_stat_replication;
    a standby seed is followed to its primary first."""
    name = "streaming"
    single_writer = True

    def detect(self, seed, ctx):
        if seed.is_recovery:
            return upstream_of(seed) is not None or bool(ctx["remembered"])
        links = replication_view(seed)
        return bool(links) or bool(ctx["remembered"])

    def nodes(self, seed, ctx):
        if not seed.is_recovery:
            return self.from_primary(seed, seed, ctx)
        up = upstream_of(seed)
        if up is None:
            return ClusterView(nodes=[seed_row(seed, ctx)], primary_name="")
        host, port = map_address(up[0], up[1], ctx["address_map"])
        primary = ctx["connect"](host, port)
        if primary is not None and not primary.is_recovery:
            try:
                return self.from_primary(primary, seed, ctx)
            finally:
                primary.close()
        if primary is not None:
            primary.close()
        # Primary not reachable from here. A streaming WAL receiver proves it is alive.
        label = up[0]
        rows = [seed_row(seed, ctx),
                node_row(label, ROLE_PRIMARY, "up" if up[2] else "unreachable", up[2],
                         address="%s:%s" % (host, port))]
        return ClusterView(nodes=rows, primary_name=label if up[2] else "")

    def from_primary(self, primary, seed, ctx, primary_label=None):
        links = replication_view(primary)
        p_label = primary_label or seed_name(primary)
        if primary is seed:
            p_row = seed_row(seed, ctx, name=p_label)
        else:
            p_row = node_row(p_label, ROLE_PRIMARY, "up", True,
                             address="%s:%s" % (primary.host, primary.port), reachable=1)
            p_row["_fp"] = node_fingerprint(primary)
        rows = [p_row]
        seed_app = own_application_name(seed) if seed.is_recovery else ""
        seed_addr = ""
        if seed.is_recovery:
            r = seed.query_one("SELECT coalesce(host(inet_server_addr()), '')")
            seed_addr = r[0] if r else ""
        for link in links or []:
            is_seed = seed.is_recovery and (
                (seed_app and seed_app != "walreceiver" and link["app"] == seed_app)
                or (seed_addr and link["client_addr"] == seed_addr)
                or len(links) == 1)
            if is_seed:
                row = seed_row(seed, ctx, name=link["name"])
                row["state"] = link["state"]
            else:
                host, port = map_address(link["client_addr"], link["port"], ctx["address_map"])
                row = node_row(link["name"], ROLE_STANDBY, link["state"],
                               link["state"] == "streaming", address="%s:%s" % (host, port))
                row["_probe"] = (host, port)
            row["replay_lag_s"] = link["replay_lag_s"]
            row["backlog_mb"] = link["replay_lag_mb"]
            row["_sync"] = link["sync_state"]
            rows.append({k: v for k, v in row.items() if v is not None})
        return ClusterView(nodes=rows, links=links, primary_name=p_row["name"])


# Most specific first; Standalone always matches.
ADAPTERS = [PatroniAdapter(), RepmgrAdapter(), AutoFailoverMonitorAdapter(), CitusAdapter(),
            PgpoolAdapter(), LogicalAdapter(), StreamingAdapter(), StandaloneAdapter()]


class ClusterView(object):
    def __init__(self, nodes, links=None, primary_name=""):
        self.nodes = nodes
        self.links = links
        self.primary_name = primary_name


def node_fingerprint(node):
    """The server's postmaster start time: identical for every name it is reached by."""
    identity = getattr(node, "identity", "") or ""
    return identity.split("|", 1)[1] if "|" in identity else ""


def seed_row(seed, ctx, name=None):
    m = ctx["metrics"]
    row = node_row(
        name or seed_name(seed), seed.role, "up", True,
        address="%s:%s" % (seed.host, seed.port), reachable=1,
        conn_pct=m.get("Connection Utilization"), uptime_s=m.get("Uptime"),
        longest_query_s=m.get("Longest Transaction"), timeline=m.get("Timeline"),
        replay_lag_s=m.get("Replay Lag"), backlog_mb=m.get("Replay Backlog"),
        last_msg_age_s=m.get("Last WAL Message Age"))
    row["_fp"] = node_fingerprint(seed)
    return row


PROBE_SQL = (
    "SELECT pg_is_in_recovery(),"
    " round(100.0 * (SELECT count(*) FROM pg_stat_activity WHERE datname IS NOT NULL)"
    " / current_setting('max_connections')::int, 2),"
    " floor(extract(epoch FROM now() - pg_postmaster_start_time()))::bigint,"
    " (SELECT coalesce(floor(max(extract(epoch FROM now() - xact_start))), 0)::bigint"
    " FROM pg_stat_activity WHERE datname IS NOT NULL AND pid <> pg_backend_pid()),"
    " (SELECT floor(extract(epoch FROM now() - max(last_msg_receipt_time)))::bigint"
    " FROM pg_stat_wal_receiver),"
    " pg_postmaster_start_time()::text")   # fingerprint: the same server under two names


def probe_nodes(rows, ctx, deadline):
    """One light query per non-seed node, in parallel. Fills role from the node itself."""
    import threading
    targets = [r for r in rows if "_probe" in r]

    def work(row):
        host, port = row["_probe"]
        node = ctx["connect"](host, port)
        if node is None:
            return
        try:
            res = node.query_one(PROBE_SQL)
            row["reachable"] = 1
            row["status"] = 1
            # A cluster manager's own state is kept as reported (pgpool may say "down"
            # for a node that is up but detached from the pool); only states the plugin
            # inferred itself are corrected.
            if row["state"] in ("down", "unreachable") and "_claimed" not in row:
                row["state"] = "up"
            if res:
                if row["role"] in (ROLE_PRIMARY, ROLE_STANDBY):   # PostgreSQL decides, not the registry
                    row["role"] = ROLE_STANDBY if res[0] else ROLE_PRIMARY
                if len(res) > 5 and res[5]:
                    row["_fp"] = str(res[5])
                for key, val in zip(("conn_pct", "uptime_s", "longest_query_s", "last_msg_age_s"), res[1:5]):
                    num = to_number(val, float if key == "conn_pct" else int)
                    if num is not None:
                        row[key] = num
        finally:
            node.close()

    threads = [threading.Thread(target=work, args=(r,), daemon=True) for r in targets]
    for t in threads:
        t.start()
    for t in threads:
        t.join(max(0.0, deadline - time.time()))


def merge_remembered(rows, prev_nodes, now):
    """Adds nodes seen in earlier polls but missing now. Returns names to forget."""
    present = {r["name"] for r in rows}
    addresses = {r.get("address") for r in rows if r.get("address")}
    forgotten = []
    for name, info in sorted(prev_nodes.items()):
        if name in present:
            continue
        if info.get("address") and info["address"] in addresses:
            continue    # the same server, now listed under another name: drop the old name
        age = now - float(info.get("last_seen") or 0)
        if age > NODE_FORGET_S:
            forgotten.append(name)
            continue
        address = info.get("address", "")
        row = node_row(name, info.get("role", ROLE_STANDBY),
                       "not streaming" if info.get("role") != ROLE_PRIMARY else "down",
                       False, address=address, last_seen_s=int(age))
        host, _, port = address.rpartition(":")
        if host and port.isdigit():
            row["_probe"] = (host, int(port))   # it may be up but detached, or a second primary
        rows.append(row)
    return forgotten


def fill_links_from_primary(view, seed, ctx):
    """Adapters that read a registry (pgpool, pg_auto_failover) know the nodes but not
    the replication links. Ask the primary itself, so standby counts and lag are real."""
    primary = next((r for r in view.nodes if r["role"] == ROLE_PRIMARY and r["status"]), None)
    if primary is None:
        return
    if "_probe" not in primary:
        node = seed if not seed.is_recovery else None
    else:
        node = ctx["connect"](*primary["_probe"])
    if node is None:
        return
    try:
        if not node.is_recovery:
            view.links = replication_view(node)
            apply_link_lag(view.nodes, view.links)
    finally:
        if node is not seed:
            node.close()


def dedupe_nodes(rows):
    """Removes a remembered row that turned out to be a server already listed under
    another name (same postmaster start time). Without this, one primary known by a
    hostname yesterday and by its IP today looks like a split brain."""
    seen, out = {}, []
    for r in sorted(rows, key=lambda r: "last_seen_s" in r):   # live rows before remembered ones
        fp = r.get("_fp")
        if fp and fp in seen:
            continue
        if fp:
            seen[fp] = r["name"]
        out.append(r)
    rows[:] = [r for r in rows if r in out]


def detect_events(rows, prev_nodes, forgotten, now):
    """Role and availability changes since the previous poll."""
    events = []
    if not prev_nodes:
        return events
    for r in rows:
        old = prev_nodes.get(r["name"])
        if old is None:
            events.append(("joined", r["name"], "", r["role"]))
            continue
        if old.get("role") != r["role"] and r["status"]:
            kind = "promoted" if r["role"] == ROLE_PRIMARY else "demoted"
            events.append((kind, r["name"], old.get("role", ""), r["role"]))
        if old.get("status", 1) and not r["status"]:
            events.append(("down", r["name"], old.get("role", ""), r["role"]))
        elif not old.get("status", 1) and r["status"]:
            events.append(("recovered", r["name"], old.get("role", ""), r["role"]))
    for name in forgotten:
        events.append(("removed", name, prev_nodes[name].get("role", ""), ""))
    return [{"ts": now, "event": e[0], "node": e[1], "old_role": e[2], "new_role": e[3]}
            for e in events]


def evaluate_health(rows, cluster_type, single_writer=True):
    up = [r for r in rows if r["status"]]
    primaries = [r for r in up if r["role"] == ROLE_PRIMARY]
    clustered = cluster_type != "standalone" and single_writer
    if clustered and len(primaries) > 1:
        return HEALTH_SPLIT_BRAIN, "split brain: %s are all writable" % ", ".join(
            r["name"] for r in primaries)
    if clustered and not primaries:
        return HEALTH_NO_PRIMARY, "no reachable primary"
    disagree = [r["name"] for r in rows if r.get("_claimed") and r.get("reachable")
                and r["_claimed"] != r["role"]]
    if disagree:
        return HEALTH_MANAGER_DISAGREES, "cluster manager role differs from PostgreSQL on: %s" % (
            ", ".join(disagree))
    down_nodes = [r["name"] for r in rows if not r["status"] or r["state"] == "not streaming"]
    if down_nodes:
        return HEALTH_NODE_DOWN, "%d node(s) down or not streaming: %s" % (
            len(down_nodes), ", ".join(down_nodes))
    return HEALTH_OK, "%d of %d nodes up" % (len(up), len(rows))


def cluster_metrics(view, cluster_type, history, now, single_writer=True, since=None):
    rows = view.nodes
    code, reason = evaluate_health(rows, cluster_type, single_writer)
    standbys = [r for r in rows if r["role"] == ROLE_STANDBY]
    out = {
        "Cluster Type": cluster_type,
        "Health Code": code,
        "Cluster Health": HEALTH_SEVERITY[code],
        "Health Reason": reason[:MAX_STRING_CHARS],
        "Nodes Total": len(rows),
        "Nodes Up": len([r for r in rows if r["status"]]),
        "Nodes Down": len([r for r in rows if not r["status"]]),
    }
    if view.primary_name:
        out["Primary Node"] = view.primary_name
    links = view.links if view.links is not None else ([] if not standbys else None)
    if links is not None:          # with no standbys at all, 0 streaming is the truth
        out["Standbys Streaming"] = len([l for l in links if l["state"] == "streaming"])
        out["Sync Standbys"] = len([l for l in links if l["sync_state"] in ("sync", "quorum")])
    lags = [r["replay_lag_s"] for r in standbys if r.get("replay_lag_s") is not None]
    backlogs = [r["backlog_mb"] for r in standbys if r.get("backlog_mb") is not None]
    if not lags and view.links:     # node names didn't match link names: use the links
        lags = [l["replay_lag_s"] for l in view.links if l.get("replay_lag_s") is not None]
        backlogs = [l["replay_lag_mb"] for l in view.links if l.get("replay_lag_mb") is not None]
    if lags or not standbys:       # no standby means no standby is behind
        out["Max Standby Replay Lag"] = max(lags) if lags else 0.0
    if backlogs or not standbys:
        out["Max Standby Backlog"] = max(backlogs) if backlogs else 0.0
    promotions = [e["ts"] for e in history if e["event"] == "promoted"]
    if promotions:
        out["Last Failover Age"] = int(now - max(promotions))
    elif since is not None:
        # no failover seen since monitoring began: report that time, a true lower bound
        # ("no failover for at least this long"), never 0, which would read as "just now"
        out["Last Failover Age"] = int(now - since)
    out["Failovers 24h"] = len([t for t in promotions if now - t <= 86400])
    return out


def event_rows(history, now):
    rows = []
    for e in sorted(history, key=lambda e: e["ts"], reverse=True)[:MAX_EVENTS]:
        stamp = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime(e["ts"]))
        rows.append({"name": safe_row_name("%s_%s_%s" % (stamp, e["node"], e["event"])),
                     "event": e["event"], "node": e["node"][:MAX_STRING_CHARS],
                     "old_role": e["old_role"] or "-", "new_role": e["new_role"] or "-",
                     "age_s": int(now - e["ts"])})
    return rows


def link_rows(links):
    cols = CLUSTER_TABLES["Replication_Links"][1]
    return [{k: v for k, v in l.items() if (k == "name" or k in cols) and v is not None}
            for l in (links or [])][:MAX_ROWS]


def public_rows(rows):
    cols = CLUSTER_TABLES["Nodes"][1]
    out = [{k: v for k, v in r.items() if (k == "name" or k in cols) and v is not None} for r in rows]
    # down nodes first, so a large cluster never hides a failure past the row limit
    out.sort(key=lambda r: (r["status"], r["role"] != ROLE_PRIMARY, r["name"]))
    return out[:MAX_ROWS]


def discover_cluster(seed, ctx):
    """Runs the first adapter that recognises the seed."""
    adapter = next(a for a in ADAPTERS if a.detect(seed, ctx))
    label = adapter.name
    if label == "logical" and ctx.get("logical_ext"):
        label = ctx["logical_ext"]          # pglogical, spock or bdr
    return adapter, label, adapter.nodes(seed, ctx)


# =============================================================================
# 7. EVENTS LOG
# =============================================================================

LOG_MAX_BYTES = 1024 * 1024
LOG_BACKUPS = 3


def log_path(args):
    """The events log always lives in the plugin folder; only the file name is configurable."""
    name = os.path.basename(args.get("log_file_path") or "") or "postgres_events.log"
    return os.path.join(PLUGIN_DIR, name)


def write_events_log(path, events, cluster_id):
    if not events:
        return
    try:
        if os.path.exists(path) and os.path.getsize(path) > LOG_MAX_BYTES:
            for i in range(LOG_BACKUPS - 1, 0, -1):
                if os.path.exists("%s.%d" % (path, i)):
                    os.replace("%s.%d" % (path, i), "%s.%d" % (path, i + 1))
            os.replace(path, path + ".1")
        with open(path, "a", encoding="utf-8") as fh:
            for e in events:
                fh.write("%s cluster=%s node=%s event=%s role=%s->%s\n" % (
                    time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(e["ts"])), cluster_id,
                    e["node"], e["event"], e["old_role"] or "-", e["new_role"] or "-"))
    except OSError:
        pass


# =============================================================================
# 8. OUTPUT
# =============================================================================

def base_payload(args):
    tabs, units = build_tabs_and_units()
    return {
        "plugin_version": args.get("plugin_version", PLUGIN_VERSION),
        "heartbeat_required": args.get("heartbeat", HEARTBEAT),
        "status": 1,
        "tabs": tabs,
        "units": units,
        "s247config": {"childdiscovery": list(CHILD_DISCOVERY)},
    }


def finalize(payload):
    """Drops tab and unit entries for anything not emitted this poll.

    The repository rules require every `units` key to exist in the data. Declaring
    unsent metrics would not help either: Site24x7 builds the template only from
    metrics that carry a value, which is why truthful_zeros() and
    sampled_rates() exist."""
    emitted = {k for k in payload if k not in RESERVED_KEYS}
    for tab in payload.get("tabs", {}).values():
        tab["tablist"] = [m for m in tab["tablist"] if m in emitted]
    payload["tabs"] = {k: v for k, v in payload.get("tabs", {}).items() if v["tablist"]}
    payload["units"] = {k: v for k, v in payload.get("units", {}).items() if k in emitted}
    if "msg" in payload:
        payload["msg"] = str(payload["msg"])[:MAX_MSG_CHARS]
    return payload


def validate_output(payload):
    """Site24x7 platform limits, checked on every poll. Returns a list of violations."""
    problems = []
    if payload.get("status") not in (0, 1):
        problems.append("status must be 0 or 1")
    tables = {k: v for k, v in payload.items()
              if k not in RESERVED_KEYS and isinstance(v, list)}
    metrics = {k: v for k, v in payload.items()
               if k not in RESERVED_KEYS and not isinstance(v, list)}
    if len(tables) > MAX_TABLES:
        problems.append("%d tables > %d" % (len(tables), MAX_TABLES))
    if len(metrics) > MAX_METRICS:
        problems.append("%d metrics > %d" % (len(metrics), MAX_METRICS))
    for name, rows in tables.items():
        if len(rows) > MAX_ROWS:
            problems.append("%s: %d rows > %d" % (name, len(rows), MAX_ROWS))
        for row in rows:
            if "name" not in row:
                problems.append("%s: row without name" % name)
            if len(row) > MAX_COLUMNS:
                problems.append("%s: %d columns > %d" % (name, len(row), MAX_COLUMNS))
            strings = [c for c, v in row.items() if isinstance(v, str)]
            if len(strings) > MAX_STRING_COLS:
                problems.append("%s: %d string columns > %d" % (name, len(strings), MAX_STRING_COLS))
            for c, v in row.items():
                limit = MAX_NAME_CHARS if c == "name" else MAX_STRING_CHARS
                if isinstance(v, str) and len(v) > limit:
                    problems.append("%s.%s longer than %d" % (name, c, limit))
    for name, value in metrics.items():
        if isinstance(value, str) and len(value) > MAX_STRING_CHARS:
            problems.append("%s longer than %d" % (name, MAX_STRING_CHARS))
        if isinstance(value, float) and (math.isnan(value) or math.isinf(value)):
            problems.append("%s is not finite" % name)
    units = payload.get("units", {})
    for tab, content in payload.get("tabs", {}).items():
        for item in content.get("tablist", []):
            if item in payload and not isinstance(payload[item], (str, list)) and item not in units:
                problems.append("%s has no unit" % item)
    return problems


def down(payload, message):
    payload["status"] = 0
    payload["msg"] = message
    return finalize(payload)


# =============================================================================
# 9. ENTRY POINTS
# =============================================================================

def resolve_args(param):
    """Normalises cfg/CLI parameters. Unknown keys are ignored."""
    p = {k: clean_quotes(v) for k, v in (param or {}).items()}
    p = {k: ("" if v == "None" else v) for k, v in p.items()}   # cfg placeholder
    try:
        port = int(p.get("port") or 5432)
    except ValueError:
        port = 5432
    try:
        timeout = int(p.get("timeout") or CONNECT_TIMEOUT_S)
    except ValueError:
        timeout = CONNECT_TIMEOUT_S
    try:
        plugin_version = int(p.get("plugin_version") or PLUGIN_VERSION)
    except ValueError:
        plugin_version = PLUGIN_VERSION
    try:
        patroni_port = int(p.get("patroni_port") or 0)
    except ValueError:
        patroni_port = 0
    return {
        "host": p.get("host") or "localhost",
        "port": port if 0 < port < 65536 else 5432,
        "username": p.get("username") or "postgres",
        "password": p.get("password") or "",
        "db": p.get("db") or "postgres",
        "sslmode": p.get("sslmode") or "",
        "sslrootcert": p.get("sslrootcert") or "",
        "sslcert": p.get("sslcert") or "",
        "sslkey": p.get("sslkey") or "",
        "timeout": min(max(timeout, 1), 30),
        "plugin_version": plugin_version,
        "heartbeat": parse_bool(p.get("heartbeat"), HEARTBEAT),
        "address_map": parse_address_map(p.get("address_map")),
        "patroni_port": patroni_port if 0 < patroni_port < 65536 else 0,
        "patroni_scheme": "https" if str(p.get("patroni_scheme") or "").lower() == "https" else "http",
        "patroni_verify": parse_bool(p.get("patroni_verify"), True),
        "patroni_cafile": p.get("patroni_cafile") or "",
        "patroni_certfile": p.get("patroni_certfile") or "",
        "patroni_keyfile": p.get("patroni_keyfile") or "",
        "patroni_username": p.get("patroni_username") or "",
        "patroni_password": p.get("patroni_password") or "",
        "logs_enabled": parse_bool(p.get("logs_enabled"), False),
        "log_type_name": p.get("log_type_name") or "PostgreSQL Cluster Events",
        "log_file_path": p.get("log_file_path") or "",
    }


def make_connector(args, deadline):
    """Opens a short-timeout connection to another cluster node, or returns None."""
    def connect(host, port, dbname=None):
        if time.time() > deadline:
            return None
        n = Node(host, port, args["username"], args["password"], dbname or args["db"], args["sslmode"],
                 args["sslrootcert"], args["sslcert"], args["sslkey"],
                 min(PROBE_TIMEOUT_S, args["timeout"]))
        return n if n.connect() else None
    return connect


def cluster_identity(seed):
    """The cluster's system identifier, if this user may read it (PG 10+)."""
    if seed.version < (10, 0):
        return ""
    before, denied_before = len(seed.failures), len(seed.denied)
    row = seed.query_one("SELECT system_identifier::text FROM pg_control_system()")
    del seed.failures[before:]          # optional: not a collection failure
    del seed.denied[denied_before:]
    return row[0] if row else ""


def collect_cluster(seed, metrics, prev, args, deadline, now):
    """The cluster layer: metrics, child tables and the new cluster state."""
    prev_cluster = prev.get("cluster") or {}
    sysid = cluster_identity(seed)
    if sysid and prev_cluster.get("sysid") and prev_cluster["sysid"] != sysid:
        prev_cluster = {}               # the address now reaches a different cluster
    prev_nodes = prev_cluster.get("nodes") or {}
    ctx = {"metrics": metrics, "address_map": args["address_map"], "args": args,
           "connect": make_connector(args, deadline), "now": now,
           "prev_cluster": prev_cluster, "state_extra": {},
           # Remembered nodes keep a cluster "a cluster" while its standbys are away.
           # A standalone server's state holds only itself, which is not evidence of one.
           "remembered": [] if prev_cluster.get("type", "standalone") == "standalone"
                         else [n for n in prev_nodes if prev_nodes[n].get("role")]}
    for key in ("pgpool", "pgpool_checked"):
        if key in prev_cluster:
            ctx["state_extra"][key] = prev_cluster[key]
    adapter, cluster_type, view = discover_cluster(seed, ctx)
    forgotten = merge_remembered(view.nodes, prev_nodes, now)
    probe_nodes(view.nodes, ctx, deadline)
    dedupe_nodes(view.nodes)
    if view.links is None and adapter.single_writer:
        fill_links_from_primary(view, seed, ctx)
    events = detect_events(view.nodes, prev_nodes, forgotten, now)
    history = [e for e in (prev_cluster.get("events") or []) if now - e.get("ts", 0) <= 7 * 86400]
    history = (history + events)[-MAX_EVENTS:]

    nodes_state = {}
    for r in view.nodes:
        old = prev_nodes.get(r["name"], {})
        nodes_state[r["name"]] = {
            "role": r["role"], "status": r["status"], "address": r.get("address", ""),
            "last_seen": now if r["status"] else old.get("last_seen", now)}
    since = float(prev_cluster.get("since") or now)
    out = cluster_metrics(view, cluster_type, history, now, adapter.single_writer, since)
    tables = {"Nodes": public_rows(view.nodes), "Events": event_rows(history, now)}
    if view.links is not None:
        tables["Replication_Links"] = link_rows(view.links)
    state = {"sysid": sysid, "type": cluster_type, "nodes": nodes_state, "events": history,
             "since": since}
    state.update(ctx["state_extra"])
    return out, tables, events, state


def permission_note(denied, prev_denied):
    """Text about permission gaps, shown only when they change: on a monitor's first poll
    (registration), when a new gap appears, or when gaps are fixed. A user who chose not
    to grant pg_monitor is told once, not on every poll; the Permission Gaps metric
    carries the count every poll for anyone who wants to alert on it."""
    if prev_denied is not None and sorted(prev_denied) == denied:
        return ""
    if denied:
        return "Not readable by this user: %s. Grant pg_monitor to include them (shown once)." % (
            ", ".join(denied))
    if prev_denied:
        return "Permission gaps resolved: all metrics are readable now."
    return ""


def error_payload(exc):
    """What the agent receives if the plugin itself fails: always valid output."""
    return {"plugin_version": PLUGIN_VERSION, "heartbeat_required": HEARTBEAT,
            "status": 0, "msg": scrub("plugin error: %s" % exc)[:MAX_MSG_CHARS]}


def run(param):
    """Collects one poll. `param` is the cfg section as a dict; returns the payload.

    The Linux agent imports this module and calls run() itself, so the guard against
    an unexpected error lives here and not only in __main__."""
    try:
        return collect(param)
    except Exception as exc:
        return error_payload(exc)


def collect(param):
    t0 = time.time()
    args = resolve_args(param)
    payload = base_payload(args)
    if not HAVE_PSYCOPG2:
        return down(payload, DRIVER_MISSING_MSG)

    node = Node(args["host"], args["port"], args["username"], args["password"], args["db"],
                args["sslmode"], args["sslrootcert"], args["sslcert"], args["sslkey"],
                args["timeout"])
    if not node.connect():
        reason = "authentication failed for user %s" % args["username"] if node.auth_failed \
            else "cannot connect to %s:%s (%s)" % (args["host"], args["port"], node.error)
        if not (param or {}).get("host"):
            reason = "no configuration received from agent; " + reason
        return down(payload, reason)

    path = state_path(args["host"], args["port"], args["db"])
    prev = load_state(path)
    deadline = t0 + CYCLE_BUDGET_S
    cluster_out, cluster_tables, events, cluster_state = {}, {}, [], prev.get("cluster") or {}
    try:
        if node.version < VERSION_FLOOR:
            return down(payload, "PostgreSQL %d.%d is not supported; version %d.%d or later is required"
                        % (node.version + VERSION_FLOOR))
        metrics = collect_metrics(node, deadline)
        tables = collect_tables(node, deadline)
        sample_ts = t0
        rates = compute_rates(metrics, prev, t0, node.identity)
        if not rates:                   # first poll of this server process
            rates, second, sample_ts = sampled_rates(node, deadline)
            metrics.update(second)
        metrics.update(rates)
        filled = truthful_zeros(node, metrics)
        metrics.update(filled)
        metrics.update(derive_metrics(node, metrics))
        try:
            cluster_out, cluster_tables, events, cluster_state = collect_cluster(
                node, metrics, prev, args, deadline, t0)
        except Exception as exc:        # never lose node metrics to a cluster-layer fault
            node.failures.append(scrub("cluster discovery: %s" % exc))
    finally:
        node.close()

    save_state(path, {
        "ts": sample_ts, "identity": node.identity,
        # pre-declared values are not counters: a standby's 0 "WAL Written" must not turn
        # into a fake WAL spike after it is promoted
        "counters": {r.source: metrics[r.source] for r in RATES
                     if r.source in metrics and r.source not in filled},
        "cluster": cluster_state,
        "denied": sorted(set(node.denied)),
    })
    if args["logs_enabled"]:
        write_events_log(log_path(args), events, cluster_state.get("sysid") or
                         "%s:%s" % (args["host"], args["port"]))
        payload["applog"] = {"logs_enabled": True, "log_type_name": args["log_type_name"],
                             "log_file_path": log_path(args)}

    metrics.update(cluster_out)
    metrics["Failed Queries"] = len(node.failures)
    denied = sorted(set(node.denied))
    metrics["Permission Gaps"] = len(denied)
    metrics["Collection Time"] = int((time.time() - t0) * 1000)
    payload.update({k: v for k, v in metrics.items() if k not in HIDDEN_COUNTERS})
    payload.update(tables)
    payload.update(cluster_tables)
    if node.failures:
        payload["msg"] = "%d queries failed: %s" % (len(node.failures), node.failures[0])
    else:
        note = permission_note(denied, prev.get("denied"))
        if note:
            payload["msg"] = note
    payload = finalize(payload)
    problems = validate_output(payload)
    if problems:
        note = "schema: " + problems[0]
        payload["msg"] = (payload.get("msg", "") + " | " + note).strip(" |")[:MAX_MSG_CHARS]
    return payload


def parse_cli(argv=None):
    parser = argparse.ArgumentParser(description="Site24x7 PostgreSQL plugin")
    parser.add_argument("--host", default="")
    parser.add_argument("--port", default="5432")
    parser.add_argument("--username", default="postgres")
    parser.add_argument("--password", default="")
    parser.add_argument("--db", default="postgres")
    parser.add_argument("--sslmode", default="")
    parser.add_argument("--sslrootcert", default="")
    parser.add_argument("--sslcert", default="")
    parser.add_argument("--sslkey", default="")
    parser.add_argument("--timeout", default=str(CONNECT_TIMEOUT_S))
    parser.add_argument("--plugin_version", default=str(PLUGIN_VERSION))
    parser.add_argument("--heartbeat", default="true")
    parser.add_argument("--address_map", default="")
    parser.add_argument("--patroni_port", default="")
    parser.add_argument("--patroni_scheme", default="http")
    parser.add_argument("--patroni_verify", default="true")
    for opt in ("patroni_cafile", "patroni_certfile", "patroni_keyfile",
                "patroni_username", "patroni_password"):
        parser.add_argument("--" + opt, default="")
    parser.add_argument("--logs_enabled", default="false")
    parser.add_argument("--log_type_name", default="")
    parser.add_argument("--log_file_path", default="")
    return vars(parser.parse_args(argv))


if __name__ == "__main__":
    try:
        result = run(parse_cli())
    except Exception as exc:  # argument parsing: the agent must still receive valid JSON
        result = error_payload(exc)
    print(json.dumps(result, indent=4, sort_keys=True))
