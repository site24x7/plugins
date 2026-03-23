#!/usr/bin/python3
import json
import os
import warnings
warnings.filterwarnings("ignore")

PLUGIN_VERSION = 1
HEARTBEAT = True

METRICS_UNITS = {
    # Global Cache / Interconnect
    "GC CR Block Received Per Second":          "count",
    "GC Current Block Received Per Second":     "count",
    "GC Average CR Get Time":                  "sec",
    "GC Average Current Get Time":             "sec",
    "Global Cache Blocks Lost":                 "count",
    "Global Cache Blocks Corrupted":            "count",
    "GC CR Blocks Served Total":           "count",
    "GC Current Blocks Served Total":      "count",
    "GC CR Block Received Total":               "count",
    "GC Current Block Received Total":          "count",
    "Global Cache Average Block Receive Time": "sec",
    "Global Cache Block Access Latency":       "sec",
    "Global Cache Service Utilization":         "count",
    "Interconnect Bytes Received Per Second":   "mb",
    "Interconnect Bytes Sent Per Second":       "mb",
    # GC Wait Analysis
    "GC CR Request Avg Wait Time":             "sec",
    "GC Current Request Avg Wait Time":        "sec",
    "GC CR Block Busy Avg Wait Time":          "sec",
    "GC Current Block Busy Avg Wait Time":     "sec",
    "GC Buffer Busy Acquire Avg Wait Time":    "sec",
    "GC Buffer Busy Release Avg Wait Time":    "sec",
    "GC CR Request Wait Count":                 "count",
    "GC Current Request Wait Count":            "count",
    "GC CR Block Busy Wait Count":              "count",
    "GC Current Block Busy Wait Count":         "count",
    "GC Buffer Busy Acquire Wait Count":        "count",
    "GC Buffer Busy Release Wait Count":        "count",
    # Cluster identity
    "cluster_name":                              "",
    # RAC Node Health
    "Active RAC Nodes":                         "count",
    "RAC Nodes Down":                           "count"
}


class OracleRAC:

    def __init__(self, args):
        self.maindata = {}
        self.maindata['plugin_version'] = PLUGIN_VERSION
        self.maindata['heartbeat_required'] = HEARTBEAT
        self.maindata['units'] = METRICS_UNITS
        self.username = args.username
        self.password = args.password
        self.sid = args.sid
        self.hostname = args.hostname
        self.port = args.port
        self.tls = str(args.tls).lower() if args.tls is not None else "false"
        self.wallet_location = args.wallet_location
        self.oracle_home = args.oracle_home

    # ------------------------------------------------------------------ #
    #  Connection helpers                                                  #
    # ------------------------------------------------------------------ #

    def connect(self, dsn):
        try:
            import oracledb
            if self.oracle_home and self.oracle_home != "None" and os.path.exists(self.oracle_home):
                try:
                    oracledb.init_oracle_client(lib_dir=self.oracle_home)
                except Exception:
                    pass
            self.conn = oracledb.connect(user=self.username, password=self.password, dsn=dsn)
            self.c = self.conn.cursor()
            return (True, "Connected")
        except Exception as e:
            self.conn = None
            self.c = None
            return (False, str(e))

    def close_connection(self):
        try:
            if hasattr(self, 'c') and self.c:
                self.c.close()
            if hasattr(self, 'conn') and self.conn:
                self.conn.close()
        except Exception:
            pass

    # ------------------------------------------------------------------ #
    #  Cluster name + RAC tag                                              #
    # ------------------------------------------------------------------ #

    def fetch_cluster_info(self):
        queried_data = {}
        cluster_name = ""
        node_name = self.hostname

        try:
            self.c.execute("""
                SELECT value
                FROM v$parameter
                WHERE name = 'cluster_database'
            """)
            row = self.c.fetchone()
            is_rac = bool(row and str(row[0]).strip().upper() in ["TRUE", "YES", "1"])
            if not is_rac:
                return queried_data
        except Exception:
            return queried_data

        try:
            self.c.execute("""
                SELECT value
                FROM v$parameter
                WHERE name = 'db_unique_name'
            """)
            row = self.c.fetchone()
            if row and row[0]:
                cluster_name = str(row[0]).strip()
        except Exception:
            pass

        if not cluster_name:
            try:
                self.c.execute("""
                    SELECT name
                    FROM v$database
                """)
                row = self.c.fetchone()
                if row and row[0]:
                    cluster_name = str(row[0]).strip()
            except Exception:
                pass

        try:
            self.c.execute("""
                SELECT host_name
                FROM v$instance
            """)
            row = self.c.fetchone()
            if row and row[0]:
                node_name = row[0]
        except Exception:
            pass

        if cluster_name:
            queried_data["cluster_name"] = cluster_name
            queried_data["tags"] = "ORACLE_RAC_CLUSTER:{},ORACLE_RAC_NODE:{}".format(
                cluster_name,
                node_name
            )
        return queried_data
    # ------------------------------------------------------------------ #
    #  RAC metric collectors                                               #
    # ------------------------------------------------------------------ #

    def execute_sysmetric_bulk(self):
        queried_data = {
            "GC CR Block Received Per Second": 0,
            "GC Current Block Received Per Second": 0,
            "GC Average CR Get Time": 0,
            "GC Average Current Get Time": 0,
            "Global Cache Blocks Lost": 0,
            "Global Cache Blocks Corrupted": 0,
            "GC CR Blocks Served Total": 0,
            "GC Current Blocks Served Total": 0,
        }

        sysmetric_map = {
            "GC CR Blocks Received Per Second": "GC CR Block Received Per Second",
            "GC Current Blocks Received Per Second": "GC Current Block Received Per Second",
            "Global Cache Average CR Get Time": "GC Average CR Get Time",
            "Global Cache Average Current Get Time": "GC Average Current Get Time",
        }

        metric_list = "','".join(sysmetric_map.keys())
        query = f"""
            SELECT metric_name, AVG(value)
            FROM gv$sysmetric
            WHERE metric_name IN ('{metric_list}')
            GROUP BY metric_name
        """
        try:
            self.c.execute(query)
            for metric_name, value in self.c:
                if metric_name in ["Global Cache Average CR Get Time", "Global Cache Average Current Get Time"]:
                    queried_data[sysmetric_map[metric_name]] = round(float(value) / 1000, 4) if value is not None else 0
                else:
                    queried_data[sysmetric_map[metric_name]] = round(float(value), 4) if value is not None else 0
        except Exception as e:
            queried_data["status"] = 0
            queried_data["msg"] = str(e)

        return queried_data

    def execute_sysstat_bulk(self):
        """
        Cumulative stats from GV$SYSSTAT — summed across all RAC instances.
        """
        queried_data = {}
        sysstat_map = {
            "gc cr blocks received":      "GC CR Block Received Total",
            "gc current blocks received": "GC Current Block Received Total",
            "gc cr blocks served":        "GC CR Blocks Served Total",
            "gc current blocks served":   "GC Current Blocks Served Total",
        }
        stat_list = "','".join(sysstat_map.keys())
        query = f"""
            SELECT LOWER(n.name), SUM(s.value)
            FROM GV$SYSSTAT s
            JOIN GV$STATNAME n
              ON s.statistic# = n.statistic# AND s.inst_id = n.inst_id
            WHERE LOWER(n.name) IN ('{stat_list}')
            GROUP BY LOWER(n.name)
        """
        try:
            self.c.execute(query)
            raw = {}
            for row in self.c:
                stat_name, value = row
                raw[stat_name] = value if value is not None else 0

            for oracle_name, metric_name in sysstat_map.items():
                if oracle_name in raw and not metric_name.startswith("_"):
                    queried_data[metric_name] = raw[oracle_name]

        except Exception as e:
            queried_data['status'] = 0
            queried_data['msg'] = str(e)
        return queried_data

    def execute_gc_wait_metrics(self):
        queried_data = {
            "GC CR Request Avg Wait Time": 0,
            "GC Current Request Avg Wait Time": 0,
            "GC CR Block Busy Avg Wait Time": 0,
            "GC Current Block Busy Avg Wait Time": 0,
            "GC Buffer Busy Acquire Avg Wait Time": 0,
            "GC Buffer Busy Release Avg Wait Time": 0,
            "GC CR Request Wait Count": 0,
            "GC Current Request Wait Count": 0,
            "GC CR Block Busy Wait Count": 0,
            "GC Current Block Busy Wait Count": 0,
            "GC Buffer Busy Acquire Wait Count": 0,
            "GC Buffer Busy Release Wait Count": 0,
        }

        event_map = {
            "gc cr request": ("GC CR Request Avg Wait Time", "GC CR Request Wait Count"),
            "gc current request": ("GC Current Request Avg Wait Time", "GC Current Request Wait Count"),
            "gc cr block busy": ("GC CR Block Busy Avg Wait Time", "GC CR Block Busy Wait Count"),
            "gc current block busy": ("GC Current Block Busy Avg Wait Time", "GC Current Block Busy Wait Count"),
            "gc buffer busy acquire": ("GC Buffer Busy Acquire Avg Wait Time", "GC Buffer Busy Acquire Wait Count"),
            "gc buffer busy release": ("GC Buffer Busy Release Avg Wait Time", "GC Buffer Busy Release Wait Count"),
        }

        query = f"""
            SELECT LOWER(event), SUM(total_waits), SUM(time_waited_micro)
            FROM GV$SYSTEM_EVENT
            WHERE wait_class='Cluster'
            GROUP BY LOWER(event)

        """
        try:
            self.c.execute(query)
            for row in self.c:
                event_name, total_waits, time_waited_ms = row
                if event_name in event_map:
                    avg_metric, count_metric = event_map[event_name]
                    total_waits = total_waits or 0
                    time_waited_ms = float(time_waited_ms) if time_waited_ms else 0
                    queried_data[avg_metric] = round((time_waited_ms / total_waits) / 1000000, 4) if total_waits > 0 else 0
                    queried_data[count_metric] = total_waits
        except Exception as e:
            queried_data["status"] = 0
            queried_data["msg"] = str(e)
        return queried_data
   
    def execute_interconnect_metrics(self):
        queried_data = {}
        try:
            self.c.execute("""
                SELECT metric_name, AVG(value)
                FROM gv$sysmetric
                WHERE metric_name IN (
                    'Interconnect Bytes Received Per Second',
                    'Interconnect Bytes Sent Per Second'
                )
                GROUP BY metric_name
            """)
            recv = 0
            sent = 0
            for metric_name, value in self.c:
                if metric_name == 'Interconnect Bytes Received Per Second':
                    recv = float(value) if value else 0
                elif metric_name == 'Interconnect Bytes Sent Per Second':
                    sent = float(value) if value else 0

            queried_data["Interconnect Bytes Received Per Second"] = round(recv / (1024 * 1024), 2)
            queried_data["Interconnect Bytes Sent Per Second"] = round(sent / (1024 * 1024), 2)

        except Exception:
            queried_data["Interconnect Bytes Received Per Second"] = 0
            queried_data["Interconnect Bytes Sent Per Second"] = 0

        return queried_data
   

    def execute_rac_node_metrics(self):
        """
        RAC node health: active nodes, nodes down, and per-instance details.
        """
        queried_data = {}
        try:
            self.c.execute("""
                SELECT inst_id, instance_name, host_name, status, instance_number
                FROM GV$INSTANCE
                ORDER BY inst_id
            """)
            rows = self.c.fetchall()

            active    = 0
            down      = 0
            node_list = []
            for row in rows:
                inst_id, inst_name, host_name, status, inst_num = row
                node_list.append({
                    "name":            inst_name,
                    "Instance_Number": inst_num,
                    "Host_Name":       host_name,
                    "Status":          status
                })
                if status == "OPEN":
                    active += 1
                else:
                    down += 1

            queried_data["Active RAC Nodes"] = active
            queried_data["RAC Nodes Down"]   = down
            queried_data["RAC_Node_Details"] = node_list
        except Exception as e:
            queried_data['status'] = 0
            queried_data['msg']    = str(e)
        return queried_data
   
    def execute_global_cache_service_metrics(self):
        """
        Global Cache Average Block Receive Time, Block Access Latency,
        and Global Cache Service Utilization — all from GV$ views.
        """
        queried_data = {}
        try:
            self.c.execute("""
                SELECT METRIC_NAME, AVG(VALUE)
                FROM GV$SYSMETRIC
                WHERE METRIC_NAME IN (
                    'Global Cache Average CR Get Time',
                    'Global Cache Average Current Get Time'
                )
                GROUP BY METRIC_NAME
            """)
            cr_time   = 0
            curr_time = 0
            cnt       = 0
            for row in self.c:
                metric_name, value = row
                value = float(value) if value else 0
                if metric_name == "Global Cache Average CR Get Time":
                    cr_time = value
                    cnt += 1
                elif metric_name == "Global Cache Average Current Get Time":
                    curr_time = value
                    cnt += 1

            avg_receive_time = (
                round(((cr_time + curr_time) / 2) / 1000, 4) if cnt == 2 else round((cr_time or curr_time) / 1000, 4)
            )
            queried_data["Global Cache Average Block Receive Time"] = avg_receive_time
            queried_data["Global Cache Block Access Latency"] = round(cr_time/1000,4)

            # Total GC blocks received across all instances
            self.c.execute("""
                SELECT NVL(SUM(value), 0)
                                FROM GV$SYSSTAT s
                                JOIN GV$STATNAME n
                                    ON s.statistic# = n.statistic# AND s.inst_id = n.inst_id
                                WHERE LOWER(n.name) IN ('gc cr blocks received', 'gc current blocks received')
            """)
            row = self.c.fetchone()
            queried_data["Global Cache Service Utilization"] = row[0] if row else 0

        except Exception as e:
            queried_data['status'] = 0
            queried_data['msg']    = str(e)
        return queried_data

    # ------------------------------------------------------------------ #
    #  Main collector                                                      #
    # ------------------------------------------------------------------ #

    def metriccollector(self):
        if self.tls == "true":
            dsn = (
                f"(DESCRIPTION="
                f"(ADDRESS=(PROTOCOL=tcps)(HOST={self.hostname})(PORT={self.port}))"
                f"(CONNECT_DATA=(SERVICE_NAME={self.sid}))"
                f"(SECURITY=(MY_WALLET_DIRECTORY={self.wallet_location})))"
            )
        else:
            dsn = f"{self.hostname}:{self.port}/{self.sid}"

        status, msg = self.connect(dsn)
        if not status:
            self.maindata['status'] = 0
            self.maindata['msg'] = msg
            self.close_connection()
            return self.maindata

        # Set tabs early so they are always sent
        self.maindata['tabs'] = {
            "Global Cache": {
                "order": 1,
                "tablist": [
                    "GC CR Block Received Per Second",
                    "GC Current Block Received Per Second",
                    "GC Average CR Get Time",
                    "GC Average Current Get Time",
                    "Global Cache Blocks Lost",
                    "Global Cache Blocks Corrupted",
                    "GC CR Blocks Served Total",
                    "GC Current Blocks Served Total",
                    "GC CR Block Received Total",
                    "GC Current Block Received Total",
                    "Global Cache Average Block Receive Time",
                    "Global Cache Block Access Latency",
                    "Global Cache Service Utilization"
                ]
            },
            "GC Wait Analysis": {
                "order": 2,
                "tablist": [
                    "GC CR Request Avg Wait Time",
                    "GC Current Request Avg Wait Time",
                    "GC CR Block Busy Avg Wait Time",
                    "GC Current Block Busy Avg Wait Time",
                    "GC Buffer Busy Acquire Avg Wait Time",
                    "GC Buffer Busy Release Avg Wait Time",
                    "GC CR Request Wait Count",
                    "GC Current Request Wait Count",
                    "GC CR Block Busy Wait Count",
                    "GC Current Block Busy Wait Count",
                    "GC Buffer Busy Acquire Wait Count",
                    "GC Buffer Busy Release Wait Count"
                ]
            },
        }

        self.maindata['s247config'] = {
            "childdiscovery": [
                "RAC_Node_Details"
            ]
        }

        collectors = [
            self.fetch_cluster_info,
            self.execute_rac_node_metrics,        # Active RAC Nodes
            self.execute_sysmetric_bulk,          # GC metrics
            self.execute_sysstat_bulk,
            self.execute_gc_wait_metrics,
            self.execute_interconnect_metrics,
            self.execute_global_cache_service_metrics,
        ]

        error_messages = []

        for collector in collectors:
            try:
                result = collector()
                if result:
                    if result.get("status") == 0 and result.get("msg"):
                        error_messages.append(result["msg"])
                        result.pop("status", None)
                        result.pop("msg", None)
                    self.maindata.update(result)
            except Exception as e:
                error_messages.append(str(e))

        if error_messages:
            self.maindata["msg"] = "; ".join(error_messages)

        self.close_connection()
        return self.maindata


# ------------------------------------------------------------------ #
#  Helpers                                                            #
# ------------------------------------------------------------------ #

def clean_quotes(value):
    if not value:
        return value
    value_str = str(value)
    if (value_str.startswith('"') and value_str.endswith('"')) or \
       (value_str.startswith("'") and value_str.endswith("'")):
        return value_str[1:-1]
    return value_str


def run(param):
    hostname        = clean_quotes(param.get("hostname"))        or "localhost"
    port            = clean_quotes(param.get("port"))            or "1521"
    sid             = clean_quotes(param.get("sid"))             or "ORCL"
    username        = clean_quotes(param.get("username"))        or "None"
    password        = clean_quotes(param.get("password"))        or "None"
    tls             = clean_quotes(param.get("tls"))             or "false"
    wallet_location = clean_quotes(param.get("wallet_location")) or "None"
    oracle_home     = clean_quotes(param.get("oracle_home"))     or None

    if oracle_home in ["None", "", "null"]:
        oracle_home = None

    class Args:
        pass

    args = Args()
    args.hostname        = hostname
    args.port            = port
    args.sid             = sid
    args.username        = username
    args.password        = password
    args.tls             = tls
    args.wallet_location = wallet_location
    args.oracle_home     = oracle_home

    return OracleRAC(args).metriccollector()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Oracle RAC Monitoring Plugin")
    parser.add_argument('--hostname',        default="localhost")
    parser.add_argument('--port',            default="1521")
    parser.add_argument('--sid',             default="ORCL")
    parser.add_argument('--username',        default="ORACLE_USER")
    parser.add_argument('--password',        default="ORACLE_USER")
    parser.add_argument('--tls',             default="False")
    parser.add_argument('--wallet_location', default=None)
    parser.add_argument('--oracle_home',     default=None)

    args = parser.parse_args()

    if args.oracle_home and os.path.exists(args.oracle_home):
        os.environ['ORACLE_HOME'] = args.oracle_home

    result = OracleRAC(args).metriccollector()
    print(json.dumps(result, default=str))
