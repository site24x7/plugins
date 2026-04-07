#!/usr/bin/python3
# -*- coding: utf-8 -*-
### PostgreSQL Cluster Monitoring Plugin for Site24x7
### Comprehensive cluster-level metrics: replication, WAL, slots, recovery, connections, conflicts
### 
### Language : Python
### Tested in Ubuntu

import psycopg2
import json

# Cluster-level monitoring uses 'postgres' database (hardcoded for cluster scope)
CLUSTER_DB = 'postgres'           # Cluster monitoring uses default postgres DB
USERNAME = 'postgres'             # Change the username here
PASSWORD = 'postgres'             # Change the authentication method
HOSTNAME = 'localhost'            # Change this value if it is a remote host
PORT = 5433                       # Change the port number (5432 by default)

PLUGIN_VERSION = 8
HEARTBEAT = True

tabs = {
    "tabs": {
        "Cluster Nodes": {
            "order": "1",
            "tablist": [
                "Cluster Nodes"        
            ]
        },
        "Replication": {
            "order": "2",
            "tablist": [
                "Replication Lag",
                "Write Lag",
                "Flush Lag",
                "Replay Lag",
                "Replication Slot Count",
                "Active Replication Slots",
                "Inactive Replication Slots",
                "Slot Lag",
                "Physical Slots",
                "Logical Slots"
            ]
        },
        "Archiving": {
            "order": "3",
            "tablist": [
                "Archive Status Success",
                "Archive Status Failed",
                "Last Archived WAL File",
                "Archive Ready Files Count"
            ]
        },
        "Write Ahead Log": {
            "order": "4",
            "tablist": [
                "Current WAL LSN",
                "WAL Insert LSN",
                "WAL Flush LSN",
                "WAL Files Count",
                "WAL Total Size"
            ]
        },
        "Checkpoint": {
            "order": "5",
            "tablist": [
                "Checkpoints Timed",
                "Checkpoints Requested",
                "Checkpoint Write",
                "Checkpoint Sync",
                "Buffers Checkpoint"
            ]
        },
        "BGWriter": {
            "order": "6",
            "tablist": [
                "Buffers Clean",
                "Buffers Backend Direct Writes",
                "Buffers Allocated",
                "Maxwritten Clean"
            ]
        },
        "Standby/Receiver": {
            "order": "7",
            "tablist": [
                "WAL Receiver Status",
                "Last Received LSN",
                "Last Replayed LSN",
                "Replay Lag Time",
                "Receive Apply Lag"
            ]
        },
        "Connections": {
            "order": "8",
            "tablist": [
                "Active Connections",
                "Available Connections",
                "Connection Utilization Percent"
            ]
        },
        "Recovery & Conflicts": {
            "order": "9",
            "tablist": [
                "Recovery Conflicts Total",
                "Conflicts Tablespace",
                "Conflicts Lock",
                "Conflicts Snapshot",
                "Conflicts Buffer Pin",
                "Conflicts Deadlock",
                "Oldest Running Transaction Age"
            ]
        }
    }
}

units = {
    "Replication Lag": "s",
    "Write Lag": "s",
    "Flush Lag": "s",
    "Replay Lag": "s",
    "Slot Lag": "MB",
    "Receive Apply Lag": "s",
    "Replay Lag Time": "s",
    "Active Connections": "connections",
    "Connection Utilization Percent": "%",
    "WAL Total Size": "MB",
    "Current WAL LSN": "MB",
    "WAL Insert LSN": "MB",
    "WAL Flush LSN": "MB",
    "Checkpoint Write": "minutes",
    "Checkpoint Sync": "minutes",
    "Oldest Running Transaction Age": "s",
    "Cluster Nodes": {
        "Port": "port",
        "Node Role": "",  
        "State": "",     
        "Sync State": "" 
    }
}


class pgsql():
    def __init__(self, host_name, port, username, password):
        self._conn = None
        self._uname = username
        self._pwd = password
        self._hostname = host_name
        self._port = port
        self._results = {}
        self._msg = ""

    def main(self):
        try:
            self._results.setdefault('plugin_version', PLUGIN_VERSION)
            self._results.setdefault('heartbeat_required', HEARTBEAT)

            self._conn = psycopg2.connect(
                dbname=CLUSTER_DB,
                user=self._uname,
                password=self._pwd,
                host=self._hostname,
                port=self._port
            )

            self.metricCollector()
            cluster_name = self._results.get("Cluster Name", "unknown")
            self._results['tags'] = f"PG_CLUSTER:{cluster_name},PG_NODE:{self._hostname}"

        except ImportError as e:
            self._results.setdefault('status', 0)
            self._results.setdefault('msg',
                "psycopg2 Module Not Installed\nDependency missing: 'psycopg2' Python client library\n"
                "Install with command:\n\npip3 install psycopg2-binary\n")
        except Exception as e:
            self._results.setdefault('status', 0)
            self._results.setdefault('msg', str(e))
        finally:
            if self._conn:
                self._conn.close()
            self._results.update(tabs)
            self._results["units"] = units
            if self._msg != "":
                self._results["msg"] = self._msg
            return self._results

    def metricCollector(self):
        cur = self._conn.cursor()

        self._init_metrics()

        cur.execute("SHOW cluster_name;")
        row = cur.fetchone()
        cluster_name = row[0] if row else ""

        if not cluster_name or str(cluster_name).strip() == "":
            cluster_name = "unnamed_cluster"

        self._results["Cluster Name"] = cluster_name
        node_role = "Unknown"
        is_standby = None

        try:
            # === NODE STATUS & BASIC INFO ===
            cur.execute("SELECT pg_is_in_recovery();")
            is_standby = cur.fetchone()[0]
            node_role = "Standby" if is_standby else "Primary"
            if node_role == "Primary":
                self._results["WAL Receiver Status"] = "N/A"
            self._results["Node Role"] = node_role
            self._results["Is In Recovery"] = "Yes" if is_standby else "No"

            cur.execute("SELECT version();")
            version = cur.fetchone()[0]
            self._results["PostgreSQL Version"] = version.split(',')[0]

            cur.execute("SELECT pg_backend_pid();")
            server_pid = cur.fetchone()[0]
            self._results["Server PID"] = f"PID-{server_pid}"

            cur.execute("SELECT EXTRACT(EPOCH FROM (now() - pg_postmaster_start_time()))::BIGINT;")
            uptime = cur.fetchone()[0]
            if uptime:
                hours = int(uptime // 3600)
                minutes = int((uptime % 3600) // 60)
                seconds = int(uptime % 60)
                self._results["Server Uptime"] = f"{hours}h {minutes}m {seconds}s"
            else:
                self._results["Server Uptime"] = "0h 0m 0s"

            cur.execute("SELECT timeline_id FROM pg_control_checkpoint();")
            timeline_id = cur.fetchone()[0]
            self._results["Timeline ID"] = int(timeline_id or 0)

        except Exception as e:
            self._msg += f",Node_Status:{str(e)}"
            self._conn.rollback()

        # === REPLICATION HEALTH (Primary) ===
        if node_role == "Primary":
            self._collect_primary_replication(cur)

        # === WAL RECEIVER (Standby) ===
        if node_role == "Standby":
            self._collect_standby_replication(cur)

        # === REPLICATION SLOTS ===
        self._collect_replication_slots(cur)

        # === WAL & ARCHIVING ===
        self._collect_wal_metrics(cur)

        # === CHECKPOINT & BGWRITER ===
        self._collect_bgwriter_metrics(cur)

        # === CONNECTIONS ===
        self._collect_connection_metrics(cur)

        # === RECOVERY CONFLICTS ===
        self._collect_recovery_conflicts(cur)

        # === CLUSTER NODES TABLE ===
        self._collect_cluster_nodes(cur)

        cur.close()

    def _init_metrics(self):
        """Initialize all metrics with proper types"""
        textual = {
            "Cluster Name": "",
            "Cluster Status": "Unknown",
            "Is In Recovery": "Unknown",
            "Last Archived WAL File": "No WAL archived yet",
            "Node Role": "Unknown",
            "PostgreSQL Version": "Unknown",
            "Replication State": "Unknown",
            "Server PID": "PID-0",
            "Server Uptime": "0h 0m 0s",
            "Sync State": "Unknown",
            "WAL Receiver Status": "stopped",
            "Max Connections": "0 connections",
            "Timeline ID": 0,
            "Superuser Reserved Connections": "0 connections"
        }

        integers = {
            "Replica Count": 0,
            "Replication Lag": 0,
            "Write Lag": 0,
            "Flush Lag": 0,
            "Replay Lag": 0,
            "Replication Slot Count": 0,
            "Active Replication Slots": 0,
            "Inactive Replication Slots": 0,
            "Physical Slots": 0,
            "Logical Slots": 0,
            "Replay Lag Time": 0,
            "Receive Apply Lag": 0,
            "Available Connections": 0,
            "Active Connections": 0,
            "Connection Utilization Percent": 0,
            "Recovery Conflicts Total": 0,
            "Conflicts Tablespace": 0,
            "Conflicts Lock": 0,
            "Conflicts Snapshot": 0,
            "Conflicts Buffer Pin": 0,
            "Conflicts Deadlock": 0,
            "Oldest Running Transaction Age": 0,
            "WAL Files Count": 0,
            "Archive Status Success": 0,
            "Archive Status Failed": 0,
            "Archive Ready Files Count": 0,
            "Checkpoints Timed": 0,
            "Checkpoints Requested": 0,
            "Buffers Checkpoint": 0,
            "Buffers Clean": 0,
            "Buffers Backend Direct Writes": 0,
            "Buffers Allocated": 0,
            "Maxwritten Clean": 0
        }

        floats = {
            "Current WAL LSN": 0.0,
            "WAL Insert LSN": 0.0,
            "WAL Flush LSN": 0.0,
            "WAL Total Size": 0.0,
            "Last Received LSN": 0.0,
            "Last Replayed LSN": 0.0,
            "Checkpoint Write": 0.0,
            "Checkpoint Sync": 0.0,
            "Slot Lag": 0.0
        }

        # Default empty table — required so Site24x7 registers the template
        self._results["Cluster Nodes"] = []

        self._results.update(textual)
        self._results.update(integers)
        self._results.update(floats)

    def _collect_primary_replication(self, cur):
        """Collect replication metrics from primary node"""
        try:
            cur.execute("""
                SELECT 
                    COUNT(*) as replica_count,
                    CASE 
                        WHEN COUNT(*) = 0 THEN 'No replicas'
                        WHEN COUNT(*) = COUNT(*) FILTER (WHERE state = 'streaming') THEN 'All streaming'
                        ELSE 'Partial streaming'
                    END as replication_state,
                    COALESCE(EXTRACT(EPOCH FROM MAX(replay_lag))::INT, 0) as max_replay_lag_s,
                    COALESCE(EXTRACT(EPOCH FROM MAX(write_lag))::INT, 0) as max_write_lag_s,
                    COALESCE(EXTRACT(EPOCH FROM MAX(flush_lag))::INT, 0) as max_flush_lag_s,
                    COALESCE(MAX(CASE WHEN sync_state = 'sync' THEN 'Sync' ELSE 'Async' END), 'N/A') as sync_state
                FROM pg_stat_replication;
            """)
            result = cur.fetchone()
            if result:
                replica_count = int(result[0]) if result[0] else 0
                self._results["Replica Count"] = replica_count
                self._results["Replication State"] = result[1]
                self._results["Replication Lag"] = int(result[2]) if result[2] else 0
                self._results["Replay Lag"] = int(result[2]) if result[2] else 0
                self._results["Write Lag"] = int(result[3]) if result[3] else 0
                self._results["Flush Lag"] = int(result[4]) if result[4] else 0
                self._results["Sync State"] = result[5]

                if replica_count == 0:
                    self._results["Cluster Status"] = "Degraded"
                elif result[1] == "All streaming":
                    self._results["Cluster Status"] = "Healthy"
                else:
                    self._results["Cluster Status"] = "Warning"
        except Exception as e:
            self._msg += f",Primary_Replication:{str(e)}"
            self._conn.rollback()

    def _collect_standby_replication(self, cur):
        """Collect replication metrics from standby node"""
        wal_status = "n/a"

        try:
            cur.execute("""
                SELECT COALESCE(status, 'N/A') as wal_receiver_status
                FROM pg_stat_wal_receiver;
            """)
            result = cur.fetchone()
            if result and result[0]:
                wal_status = str(result[0]).strip().lower()
            self._results["WAL Receiver Status"] = wal_status
        except Exception as e:
            self._msg += f",Standby_WAL_Receiver:{str(e)}"
            self._conn.rollback()

        try:
            cur.execute("""
                SELECT 
                    COALESCE(ROUND(pg_wal_lsn_diff(pg_last_wal_replay_lsn(), '0/0') / 1024.0 / 1024.0, 2), 0);
            """)
            result = cur.fetchone()
            if result:
                self._results["Last Replayed LSN"] = float(result[0]) if result[0] else 0

            cur.execute("""
                SELECT COALESCE(ROUND(pg_wal_lsn_diff(pg_last_wal_receive_lsn(), '0/0') / 1024.0 / 1024.0, 2), 0);
            """)
            recv = cur.fetchone()
            self._results["Last Received LSN"] = float(recv[0]) if recv and recv[0] else 0
        except Exception as e:
            self._msg += f",Standby_LSN:{str(e)}"
            self._conn.rollback()

        try:
            cur.execute("""
                SELECT COALESCE(EXTRACT(EPOCH FROM (now() - pg_last_xact_replay_timestamp()))::BIGINT, 0);
            """)
            result = cur.fetchone()
            if result:
                self._results["Replay Lag Time"] = int(result[0]) if result[0] else 0
        except Exception as e:
            self._msg += f",Standby_ReplayLag:{str(e)}"
            self._conn.rollback()

        try:
            cur.execute("""
                SELECT COALESCE(EXTRACT(EPOCH FROM (now() - latest_end_time))::BIGINT, 0)
                FROM pg_stat_wal_receiver;
            """)
            result = cur.fetchone()
            if result:
                self._results["Receive Apply Lag"] = int(result[0]) if result[0] else 0
        except Exception as e:
            self._msg += f",Standby_ReceiveApplyLag:{str(e)}"
            self._conn.rollback()

        last_received_lsn = self._results.get("Last Received LSN", 0)
        last_replayed_lsn = self._results.get("Last Replayed LSN", 0)

        if wal_status == "streaming":
            self._results["Replication State"] = "Streaming"
            self._results["Cluster Status"] = "Healthy"
        elif last_received_lsn > 0 or last_replayed_lsn > 0:
            self._results["WAL Receiver Status"] = "replay_only"
            self._results["Replication State"] = "Receiving/Replayed"
            self._results["Cluster Status"] = "Warning"
        else:
            self._results["Replication State"] = "Not Streaming"
            self._results["Cluster Status"] = "Degraded"

    def _collect_replication_slots(self, cur):
        """Collect replication slot metrics"""
        try:
            cur.execute("""
                SELECT 
                    COUNT(*) as total_slots,
                    COUNT(*) FILTER (WHERE active) as active_slots,
                    COUNT(*) FILTER (WHERE NOT active) as inactive_slots,
                    COUNT(*) FILTER (WHERE slot_type = 'physical') as physical_slots,
                    COUNT(*) FILTER (WHERE slot_type = 'logical') as logical_slots
                FROM pg_replication_slots;
            """)
            result = cur.fetchone()
            if result:
                self._results["Replication Slot Count"] = int(result[0]) if result[0] else 0
                self._results["Active Replication Slots"] = int(result[1]) if result[1] else 0
                self._results["Inactive Replication Slots"] = int(result[2]) if result[2] else 0
                self._results["Physical Slots"] = int(result[3]) if result[3] else 0
                self._results["Logical Slots"] = int(result[4]) if result[4] else 0
        except Exception as e:
            self._msg += f",Replication_Slots_Count:{str(e)}"
            self._conn.rollback()

        try:
            cur.execute("""
                SELECT 
                    COALESCE(MAX(pg_wal_lsn_diff(
                        CASE 
                            WHEN pg_is_in_recovery() THEN pg_last_wal_replay_lsn()
                            ELSE pg_current_wal_lsn()
                        END,
                        restart_lsn
                    ))::BIGINT, 0)
                FROM pg_replication_slots
                WHERE restart_lsn IS NOT NULL;
            """)
            result = cur.fetchone()
            if result:
                self._results["Slot Lag"] = round(float(result[0]) / (1024.0 * 1024.0), 2) if result[0] else 0.0
        except Exception as e:
            self._msg += f",Replication_Slot_Lag:{str(e)}"
            self._conn.rollback()

    def _collect_wal_metrics(self, cur):
        """Collect WAL and archiving metrics"""
        try:
            cur.execute("""
                SELECT 
                    ROUND(pg_wal_lsn_diff(pg_current_wal_lsn(), '0/0') / 1024.0 / 1024.0, 2),
                    ROUND(pg_wal_lsn_diff(pg_current_wal_insert_lsn(), '0/0') / 1024.0 / 1024.0, 2),
                    ROUND(pg_wal_lsn_diff(pg_current_wal_flush_lsn(), '0/0') / 1024.0 / 1024.0, 2);
            """)
            result = cur.fetchone()
            if result:
                self._results["Current WAL LSN"] = float(result[0]) if result[0] else 0.0
                self._results["WAL Insert LSN"] = float(result[1]) if result[1] else 0.0
                self._results["WAL Flush LSN"] = float(result[2]) if result[2] else 0.0
        except Exception as e:
            self._conn.rollback()
            self._results["Current WAL LSN"] = 0.0
            self._results["WAL Insert LSN"] = 0.0
            self._results["WAL Flush LSN"] = 0.0

        try:
            cur.execute("""
                SELECT 
                    COUNT(*) as wal_files_count,
                    COALESCE(ROUND(SUM(size) / 1024.0 / 1024.0, 2), 0) as total_size_mb
                FROM pg_ls_waldir();
            """)
            result = cur.fetchone()
            if result:
                self._results["WAL Files Count"] = int(result[0]) if result[0] else 0
                self._results["WAL Total Size"] = float(result[1]) if result[1] else 0.0
        except Exception as e:
            self._results["WAL Files Count"] = 0
            self._results["WAL Total Size"] = 0.0
            self._conn.rollback()

        try:
            cur.execute("""
                SELECT 
                    COALESCE(archived_count, 0),
                    COALESCE(failed_count, 0),
                    COALESCE(last_archived_wal, '0')
                FROM pg_stat_archiver;
            """)
            result = cur.fetchone()
            if result:
                self._results["Archive Status Success"] = int(result[0]) if result[0] else 0
                self._results["Archive Status Failed"] = int(result[1]) if result[1] else 0
                self._results["Last Archived WAL File"] = result[2] if result[2] and result[2] != '0' else "No WAL archived yet"
        except Exception as e:
            self._msg += f",Archiver_Stats:{str(e)}"
            self._conn.rollback()

        try:
            cur.execute("""
                SELECT COUNT(*) FROM pg_ls_archive_statusdir() WHERE name LIKE '%.ready';
            """)
            result = cur.fetchone()
            if result:
                self._results["Archive Ready Files Count"] = int(result[0]) if result[0] else 0
        except Exception as e:
            self._results["Archive Ready Files Count"] = 0
            self._conn.rollback()

    def _collect_bgwriter_metrics(self, cur):
        """Collect checkpoint and background writer metrics"""
        try:
            cur.execute("""
                SELECT 
                    COALESCE(buffers_clean, 0),
                    COALESCE(buffers_alloc, 0),
                    COALESCE(maxwritten_clean, 0)
                FROM pg_stat_bgwriter;
            """)
            result = cur.fetchone()
            if result:
                self._results["Buffers Clean"] = int(result[0]) if result[0] else 0
                self._results["Buffers Allocated"] = int(result[1]) if result[1] else 0
                self._results["Maxwritten Clean"] = int(result[2]) if result[2] else 0
                self._results["Buffers Backend Direct Writes"] = 0  
        except Exception as e:
            self._msg += f",BGWriter_BufferStats:{str(e)}"
            self._conn.rollback()

        try:
            cur.execute("""
                SELECT 
                    COALESCE(num_timed, 0),
                    COALESCE(num_requested, 0),
                    COALESCE(write_time, 0),
                    COALESCE(sync_time, 0),
                    COALESCE(buffers_written, 0)
                FROM pg_stat_checkpointer;
            """)
            result = cur.fetchone()
            if result:
                self._results["Checkpoints Timed"] = int(result[0]) if result[0] else 0
                self._results["Checkpoints Requested"] = int(result[1]) if result[1] else 0
                self._results["Checkpoint Write"] = round(float(result[2]) / 60000, 2) if result[2] else 0.0
                self._results["Checkpoint Sync"] = round(float(result[3]) / 60000, 2) if result[3] else 0.0
                self._results["Buffers Checkpoint"] = int(result[4]) if result[4] else 0
        except Exception as e:
            self._msg += f",BGWriter_Checkpoints:{str(e)}"
            self._conn.rollback()

    def _collect_connection_metrics(self, cur):
        """Collect connection and utilization metrics"""
        try:
            cur.execute("""
                SELECT 
                    (SELECT count(*) FROM pg_stat_activity) as active_connections,
                    (SELECT setting::INT FROM pg_settings WHERE name = 'max_connections') as max_connections,
                    (SELECT setting::INT FROM pg_settings WHERE name = 'superuser_reserved_connections') as superuser_reserved;
            """)
            result = cur.fetchone()
            if result:
                active = int(result[0]) if result[0] else 0
                max_conn = int(result[1]) if result[1] else 0
                reserved = int(result[2]) if result[2] else 0
                available = max_conn - reserved - active
                util_percent = round((active / max_conn) * 100, 2) if max_conn > 0 else 0

                self._results["Active Connections"] = active
                self._results["Max Connections"] = f"{max_conn} connections"
                self._results["Superuser Reserved Connections"] = f"{reserved} connections"
                self._results["Available Connections"] = max(0, available)
                self._results["Connection Utilization Percent"] = util_percent
        except Exception as e:
            self._msg += f",Connections:{str(e)}"
            self._conn.rollback()

    def _collect_recovery_conflicts(self, cur):
        """Collect recovery conflicts and failover indicators"""
        try:
            cur.execute("""
                SELECT 
                    COALESCE(SUM(confl_tablespace), 0),
                    COALESCE(SUM(confl_lock), 0),
                    COALESCE(SUM(confl_snapshot), 0),
                    COALESCE(SUM(confl_bufferpin), 0),
                    COALESCE(SUM(confl_deadlock), 0),
                    COALESCE(SUM(confl_tablespace) + SUM(confl_lock) + SUM(confl_snapshot) +
                              SUM(confl_bufferpin) + SUM(confl_deadlock), 0)
                FROM pg_stat_database_conflicts;
            """)
            result = cur.fetchone()
            if result:
                self._results["Conflicts Tablespace"] = int(result[0]) if result[0] else 0
                self._results["Conflicts Lock"] = int(result[1]) if result[1] else 0
                self._results["Conflicts Snapshot"] = int(result[2]) if result[2] else 0
                self._results["Conflicts Buffer Pin"] = int(result[3]) if result[3] else 0
                self._results["Conflicts Deadlock"] = int(result[4]) if result[4] else 0
                self._results["Recovery Conflicts Total"] = int(result[5]) if result[5] else 0
        except Exception as e:
            self._msg += f",Recovery_Conflicts:{str(e)}"
            self._conn.rollback()

        try:
            cur.execute("""
                SELECT COALESCE(MAX(EXTRACT(EPOCH FROM now() - xact_start))::BIGINT, 0)
                FROM pg_stat_activity
                WHERE state <> 'idle' AND xact_start IS NOT NULL;
            """)
            result = cur.fetchone()
            if result:
                self._results["Oldest Running Transaction Age"] = int(result[0]) if result[0] else 0
        except Exception as e:
            pass

    def _collect_cluster_nodes(self, cur):
        """
        Collect cluster node details as a Site24x7-compatible tabular array.

        Site24x7 table rules:
          - Each row must have a "name" key (string, reserved keyword, case-sensitive)
          - ALL other column values must be NUMERIC (int or float)
          - Non-numeric values in non-name columns are NOT supported
          - Max 25 rows per table

Encoding legend:
  Node Role  -> 1 = Primary,            0 = Standby
  State      -> 1 = Active / Streaming,  0 = Not Streaming / Unknown
  Sync State -> 2 = Sync,  1 = N/A (Primary has no sync state),  0 = Async
        """
        try:
            node_list = []

            # -- Primary node --
            cur.execute("SELECT inet_server_addr(), inet_server_port()")
            primary = cur.fetchone()

            if primary:
                host = str(primary[0]) if primary[0] else "localhost"
                port = int(primary[1]) if primary[1] else 0
                node_list.append({
                    "name": f"primary_{host}", 
                    "Port": port,
                    "Node Role": 1,           
                    "State": 1,                 
                    "Sync State": 1             
                })

            # -- Standby nodes from pg_stat_replication --
            cur.execute("""
                SELECT 
                    application_name,
                    COALESCE(client_hostname, client_addr::text),
                    client_port,
                    state,
                    sync_state
                FROM pg_stat_replication
            """)
            rows = cur.fetchall()

            for row in rows:
                app_name = row[0] if row[0] else "standby"
                host = str(row[1]) if row[1] else "unknown"
                port = int(row[2]) if row[2] else 0
                state_str = str(row[3]).lower() if row[3] else ""
                sync_str = str(row[4]).lower() if row[4] else ""

                state_val = 1 if state_str == "streaming" else 0

                if sync_str == "sync":
                    sync_val = 2
                elif sync_str == "async":
                    sync_val = 0
                else:
                    sync_val = 1  

                node_list.append({
                    "name": f"{app_name}_{host}",  
                    "Port": port,
                    "Node Role": 0,            
                    "State": state_val,
                    "Sync State": sync_val
                })

            self._results["Cluster Nodes"] = node_list

        except Exception as e:
            self._msg += f",Cluster_Nodes:{str(e)}"
            self._conn.rollback()


def clean_quotes(value):
    if not value:
        return value
    value_str = str(value)
    if value_str.startswith('"') and value_str.endswith('"'):
        return value_str[1:-1]
    elif value_str.startswith("'") and value_str.endswith("'"):
        return value_str[1:-1]
    return value_str


def run(param):
    host_name = clean_quotes(param.get("host")) if param and param.get("host") else "localhost"
    port = clean_quotes(param.get("port")) if param and param.get("port") else "5432"
    username = clean_quotes(param.get("username")) if param and param.get("username") else "postgres"
    password = clean_quotes(param.get("password")) if param and param.get("password") else "postgres"

    psql_instance = pgsql(host_name, port, username, password)
    result = psql_instance.main()
    return result


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', help='Host to be monitored', nargs='?', default=HOSTNAME)
    parser.add_argument('--port', help='port number', type=int, nargs='?', default=PORT)
    parser.add_argument('--username', help='user name', nargs='?', default=USERNAME)
    parser.add_argument('--password', help='password', nargs='?', default=PASSWORD)
    args = parser.parse_args()

    host_name = args.host
    port = str(args.port)
    username = args.username
    password = args.password

    psql = pgsql(host_name, port, username, password)
    results = psql.main()
    print(results)
