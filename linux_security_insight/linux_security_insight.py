#!/usr/bin/python3
import json
import subprocess
import shutil
import re
import pwd
import grp
import os
from datetime import datetime, timedelta

PLUGIN_VERSION = "1"
HEARTBEAT = "true"

maindata = {
    "plugin_version": PLUGIN_VERSION,
    "heartbeat_required": HEARTBEAT
}


class LinuxInsightMonitor:

    def run_command(self, cmd, timeout=10):
        try:
            output = subprocess.check_output(
                cmd,
                shell=True,
                stderr=subprocess.DEVNULL,
                universal_newlines=True,
                timeout=timeout,
            )
            return output.strip()
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, Exception):
            return ""

    def detect_firewall_cmd(self):
        """Auto-detects firewall command for any distro"""
        if shutil.which("firewall-cmd"):
            return "firewall-cmd"
        elif shutil.which("ufw"):
            # Prefer iptables if UFW is installed but inactive
            status_line = self.run_command("ufw status | head -n 1")
            if status_line and "inactive" not in status_line.lower():
                return "ufw"
            if shutil.which("iptables"):
                return "iptables"
        elif shutil.which("iptables"):
            return "iptables"
        elif shutil.which("nft"):
            return "nft"
        return None

    def get_firewall_status(self):
        fw_cmd = self.detect_firewall_cmd()
        status = "Unknown"
        numeric_status = 0
        if fw_cmd == "firewall-cmd":
            status = self.run_command("firewall-cmd --state") or "inactive"
        elif fw_cmd == "ufw":
            status = self.run_command("ufw status | grep -i 'Status' | awk '{print $2}'") or "inactive"
        elif fw_cmd == "iptables":
            status = "active" if self.run_command("iptables -L") else "inactive"
        elif fw_cmd == "nft":
            status = "active" if self.run_command("nft list ruleset") else "inactive"

        if status.lower().strip() in ["active", "running", "enabled"]:
            numeric_status = 1

        maindata["Firewall_Status"] = status
        maindata["firewall_status_numeric"] = numeric_status

    def get_firewall_info(self):
        """
        Collect firewall rules and details in a single pass per backend.

        Populates:
          - Firewall_Rules (sampled, up to 10)
          - Firewall_Default_Policies
          - firewall_total_rules
          - firewall_active_zones / ufw_status_verbose (when applicable)
        """
        fw_cmd = self.detect_firewall_cmd()
        rules = []
        default_policies = []
        total_rules = 0

        if not fw_cmd:
            maindata["Firewall_Rules"] = [{
                "Rule": "-",
                "Rule_Status": "-",
                "name": "Rule1"
            }]
            maindata["Firewall_Default_Policies"] = [{
                "Chain": "-",
                "Policy": "-",
                "Packets": "-",
                "Bytes": "-",
                "name": "Chain1"
            }]
            maindata["firewall_total_rules"] = 0
            return

        # Treat both native iptables and UFW (which is built on top of iptables)
        # as iptables backends for purposes of rule counters. For UFW, prefer
        # the ufw-specific user input chain to focus on user rules:
        #   iptables -nvL ufw-user-input
        # If that chain is not available or returns nothing, fall back to the
        # full filter table. This way we always get pkts/bytes counters.
        if fw_cmd in ("iptables", "ufw"):
            if fw_cmd == "ufw":
                output = self.run_command("iptables -nvL ufw-user-input")
                if not output:
                    output = self.run_command("iptables -L -n -v")
            else:
                output = self.run_command("iptables -L -n -v")

            if output:
                lines = output.splitlines()
                chain_index = 1
                rule_index = 1
                for line in lines:
                    clean = line.strip()
                    if not clean:
                        continue

                    chain_match = re.match(
                        r"Chain\s+(\S+)\s+\(policy\s+(\S+)(?:\s+(\d+)\s+packets,\s+(\d+)\s+bytes)?",
                        clean
                    )
                    if chain_match:
                        packets = chain_match.group(3) if chain_match.group(3) else "-"
                        bytes_count = chain_match.group(4) if chain_match.group(4) else "-"
                        default_policies.append({
                            "Chain": chain_match.group(1),
                            "Policy": chain_match.group(2),
                            "Packets": packets,
                            "Bytes": bytes_count,
                            "name": "Chain{}".format(chain_index)
                        })
                        chain_index += 1
                        continue

                    if clean.lower().startswith(("chain", "target")):
                        continue

                    if rule_index <= 10:
                        parts = clean.split()
                        if len(parts) >= 2 and parts[0].lower() == "pkts" and parts[1].lower() == "bytes":
                            # header line inside the chain; skip it
                            continue
                        packets = parts[0] if parts else "-"
                        bytes_count = parts[1] if len(parts) > 1 else "-"

                        # For native iptables we can skip completely idle rules to
                        # reduce noise. For UFW we still want to list the rules even
                        # if they have not yet seen any packets.
                        if fw_cmd == "iptables":
                            if packets == "0" and bytes_count == "0":
                                total_rules += 1
                                continue

                        # Derive a more descriptive rule name:
                        # Try to capture destination or source port first
                        port_match = re.search(r"dpt:(\d+)", clean)
                        if not port_match:
                            port_match = re.search(r"sport:(\d+)", clean)
                        port = port_match.group(1) if port_match else None

                        # iptables -L -n -v format (typical):
                        # pkts bytes target prot opt in out source destination ...
                        target = parts[2] if len(parts) > 2 else "-"
                        proto_raw = parts[3] if len(parts) > 3 else "-"
                        # Normalize protocol: iptables may show numeric proto (6,17,...)
                        # when using -n; map common numbers to names for readability.
                        proto = proto_raw.lower()
                        if proto.isdigit():
                            proto_map = {
                                "6": "tcp",
                                "17": "udp",
                                "1": "icmp"
                            }
                            proto = proto_map.get(proto, proto)
                        # For display purposes we only need something concise like:
                        # "ACCEPT tcp 22" or "DROP tcp"
                        if port:
                            rule_name = "{} {} {}".format(target, proto, port)
                        else:
                            rule_name = "{} {}".format(target, proto)

                        # If we still didn't get anything meaningful
                        # (i.e., the constructed name is effectively empty or just dashes),
                        # skip adding this rule to the sample list but still count it.
                        if not rule_name.strip() or rule_name.strip("- ") == "":
                            total_rules += 1
                            continue

                        # Derive rule_status primarily from the iptables target,
                        # falling back to simple text heuristics if needed.
                        rule_status = "unknown"
                        upper_target = target.upper()
                        if upper_target in ("ACCEPT", "ALLOW"):
                            rule_status = "allow"
                        elif upper_target in ("DROP", "REJECT", "DENY"):
                            rule_status = "deny"
                        else:
                            lower_line = clean.lower()
                            if any(x in lower_line for x in ["allow", "accept", "permit"]):
                                rule_status = "allow"
                            elif any(x in lower_line for x in ["deny", "drop", "reject", "block"]):
                                rule_status = "deny"
                            elif "active" in lower_line:
                                rule_status = "active"
                            elif "inactive" in lower_line or "disabled" in lower_line:
                                rule_status = "inactive"

                        rules.append({
                            "Rule": rule_name,
                            "Rule_Status": rule_status,
                            "Packets": packets,
                            "Bytes": bytes_count,
                            "name": "Rule{}".format(rule_index)
                        })
                        rule_index += 1
                        total_rules += 1
                    else:
                        total_rules += 1

        elif fw_cmd == "firewall-cmd":
            # firewalld backend: focus on the default zone, and extract allowed
            # services and ports from `firewall-cmd --list-all`.
            output = self.run_command("firewall-cmd --list-all")
            lines = output.splitlines()
            zone_name = "-"
            services = []
            ports_list = []

            for line in lines:
                clean_line = line.strip()
                if not clean_line:
                    continue

                # First non-empty line is typically "<zone> (active)"
                if zone_name == "-" and "(" in clean_line:
                    zone_name = clean_line.split()[0]
                    continue

                lower_line = clean_line.lower()

                if lower_line.startswith("services:"):
                    # Example: "services: ssh dhcpv6-client"
                    svc_part = clean_line.split(":", 1)[1].strip()
                    if svc_part:
                        services = svc_part.split()
                elif lower_line.startswith("ports:"):
                    # Example: "ports: 80/tcp 443/tcp"
                    ports_part = clean_line.split(":", 1)[1].strip()
                    if ports_part:
                        ports_list = ports_part.split()

            rule_index = 1

            # Build rules for services
            for svc in services:
                if rule_index > 10:
                    break
                rules.append({
                    "Rule": "service {}".format(svc),
                    "Rule_Status": "allow",
                    "name": "Rule{}".format(rule_index)
                })
                rule_index += 1

            # Build rules for ports
            for port_entry in ports_list:
                if rule_index > 10:
                    break
                rules.append({
                    "Rule": "port {}".format(port_entry),
                    "Rule_Status": "allow",
                    "name": "Rule{}".format(rule_index)
                })
                rule_index += 1

            # Total rules = all non-empty lines plus any services/ports we parsed
            total_rules = len([l for l in lines if l.strip()])
            default_zone = self.run_command("firewall-cmd --get-default-zone")
            active_zones = self.run_command("firewall-cmd --get-active-zones")
            default_policies.append({
                "Chain": "default_zone",
                "Policy": default_zone or zone_name or "-",
                "name": "Chain1"
            })
            maindata["firewall_active_zones"] = active_zones or "-"

        elif fw_cmd == "nft":
            output = self.run_command("nft list ruleset")
            lines = output.splitlines()
            total_rules = len([l for l in lines if l.strip()])
            for i, line in enumerate(lines[:10]):
                clean_line = line.strip()
                if not clean_line:
                    continue
                rules.append({
                    "Rule": "rule_{}".format(i + 1),
                    "Rule_Status": "unknown",
                    "name": "Rule{}".format(i + 1)
                })

        if not rules:
            rules = [{"Rule": "-", "Rule_Status": "-", "name": "Rule1"}]

        if not default_policies:
            default_policies = [{
                "Chain": "-",
                "Policy": "-",
                "Packets": "-",
                "Bytes": "-",
                "name": "Chain1"
            }]

        maindata["Firewall_Rules"] = rules
        maindata["Firewall_Default_Policies"] = default_policies
        maindata["firewall_total_rules"] = total_rules

    def get_listening_ports(self):
        """Collect only non-ephemeral TCP listening ports"""
        cmd = "ss -lntup" if shutil.which("ss") else "netstat -tulpn"
        output = self.run_command(cmd)
        ports = []

        EPHEMERAL_PORT_START = 49152
        EPHEMERAL_PORT_END = 65535

        lines = output.splitlines()
        if len(lines) <= 1:
            maindata["Listening_Ports"] = [{
                "Protocol": "tcp",
                "Port_No": "-",
                "Process_Name": "-",
                "name": "Port1"
            }]
            return

        for line in lines[1:]:
            port_no = "-"
            process_name = "-"

            parts = line.split()
            if not parts:
                continue

            protocol = parts[0].lower()
            if not protocol.startswith("tcp"):
                continue

            local_addr = ""
            if "ss" in cmd and len(parts) > 4:
                local_addr = parts[4]
            elif "netstat" in cmd and len(parts) > 3:
                local_addr = parts[3]

            match = re.search(r":(\d+)$", local_addr)
            if match:
                port_no = match.group(1)
            else:
                continue

            if not port_no.isdigit():
                continue
            port_int = int(port_no)
            if EPHEMERAL_PORT_START <= port_int <= EPHEMERAL_PORT_END:
                continue

            if "ss" in cmd:
                proc_match = re.search(r'users:\(\("([^"]+)"', line)
                if proc_match:
                    process_name = proc_match.group(1)
            else:
                if "/" in parts[-1]:
                    process_name = parts[-1].split("/")[-1]

            ports.append({
                "Protocol": "tcp",
                "Port_No": port_no,
                "Process_Name": process_name,
                "name": "Port{}".format(len(ports) + 1)
            })

            if len(ports) >= 10:
                break

        if not ports:
            ports = [{
                "Protocol": "tcp",
                "Port_No": "-",
                "Process_Name": "-",
                "name": "Port1"
            }]

        maindata["Listening_Ports"] = ports

    def get_user_status_table(self):
        output = self.run_command("w -h")
        users = []
        lines = output.splitlines()
        active_users = 0

        for i, line in enumerate(lines[:10]):
            parts = line.split()
            if len(parts) >= 5:
                user = {
                    "User name": parts[0],
                    "TTY": parts[1],
                    "From": parts[2],
                    "Login_Time": parts[3],
                    "Idle": parts[4],
                    "name": "User{}".format(i + 1)
                }
                users.append(user)
                active_users += 1

        if not users:
            users = [{
                "User name": "-",
                "TTY": "-",
                "From": "-",
                "Login_Time": "-",
                "Idle": "-",
                "name": "User1"
            }]

        maindata["User_Status"] = users
        maindata["total_users"] = len(lines)
        maindata["active_users"] = active_users

    def get_rdp_connections(self):
        """Detect RDP/xRDP/VNC connections if any"""
        cmd = "ss -tupn | grep -E '3389|5900|xrdp|vnc'"
        output = self.run_command(cmd)
        rdp_conns = []

        lines = output.splitlines()
        for i, line in enumerate(lines[:10]):
            parts = line.split()
            if len(parts) >= 5:
                match = re.search(r":(\d+)", parts[4])
                port = match.group(1) if match else "-"
                proc_match = re.search(r'users:\(\("([^"]+)"', line)
                proc_name = proc_match.group(1) if proc_match else "-"
                rdp_conns.append({
                    "Protocol_rdp": "tcp",
                    "Port_rdp": port,
                    "Process_rdp": proc_name,
                    "Remote_Address": parts[4],
                    "name": "RDP{}".format(i + 1)
                })

        if not rdp_conns:
            rdp_conns = [{
                "Protocol_rdp": "tcp",
                "Port_rdp": "-",
                "Process_rdp": "-",
                "Remote_Address": "-",
                "name": "RDP1"
            }]

        maindata["RDP_Connections"] = rdp_conns

    def get_remote_connections(self):
        """Detect active remote SSH or telnet sessions"""
        cmd = "ss -tupn | grep -E 'ssh|telnet'"
        output = self.run_command(cmd)
        remote_conns = []

        lines = output.splitlines()
        for i, line in enumerate(lines[:10]):
            parts = line.split()
            if len(parts) >= 5:
                match = re.search(r":(\d+)", parts[4])
                port = match.group(1) if match else "-"
                proc_match = re.search(r'users:\(\("([^"]+)"', line)
                proc_name = proc_match.group(1) if proc_match else "-"
                remote_conns.append({
                    "Protocol_remote": "tcp",
                    "Port_remote": port,
                    "Process_remote": proc_name,
                    "IPAddress": parts[4],
                    "name": "Remote{}".format(i + 1)
                })

        if not remote_conns:
            remote_conns = [{
                "Protocol_remote": "tcp",
                "Port_remote": "-",
                "Process_remote": "-",
                "IPAddress": "-",
                "name": "Remote1"
            }]

        maindata["Remote_Connections"] = remote_conns

    def get_auth_events(self):
        """Summarize recent failed SSH authentication attempts."""
        failed_output = ""
        if shutil.which("journalctl"):
            failed_output = self.run_command(
                "journalctl -n 500 -u sshd --no-pager 2>/dev/null | grep -i 'Failed password'"
            )
        if not failed_output:
            failed_output = self.run_command(
                "grep -i 'Failed password' /var/log/auth.log /var/log/secure 2>/dev/null | tail -n 200"
            )

        failed_lines = [l for l in failed_output.splitlines() if l.strip()]
        now = datetime.now()
        window_start = now - timedelta(hours=24)

        def parse_syslog_timestamp(line):
            # Expect formats like: "Jan 10 12:34:56 hostname sshd[123]: Failed password ..."
            ts_match = re.match(r"^(?P<month>\w{3})\s+(?P<day>\d{1,2})\s+(?P<time>\d{2}:\d{2}:\d{2})", line)
            if not ts_match:
                return None
            ts_str = f"{ts_match.group('month')} {int(ts_match.group('day')):02d} {now.year} {ts_match.group('time')}"
            try:
                ts = datetime.strptime(ts_str, "%b %d %Y %H:%M:%S")
                # Handle year boundary (e.g., logs from Dec 31 when now is Jan 1)
                if ts > now + timedelta(hours=1):
                    ts = ts.replace(year=ts.year - 1)
                return ts
            except Exception:
                return None

        failed_lines = [
            line for line in failed_lines
            if (ts := parse_syslog_timestamp(line)) is None or ts >= window_start
        ]
        total_failed = len(failed_lines)

        ip_counts = {}
        for line in failed_lines:
            ip_match = re.search(r"from (\S+)", line)
            ip = ip_match.group(1) if ip_match else "unknown"
            ip_counts[ip] = ip_counts.get(ip, 0) + 1

        auth_table = []
        for i, (ip, count) in enumerate(sorted(ip_counts.items(), key=lambda x: x[1], reverse=True)[:10]):
            auth_table.append({
                "Source_IP": ip,
                "Failed_Attempts": count,
                "name": "Auth{}".format(i + 1)
            })

        if not auth_table:
            auth_table = [{
                "Source_IP": "-",
                "Failed_Attempts": 0,
                "name": "Auth1"
            }]

        maindata["Auth_Failed_Attempts"] = auth_table
        maindata["auth_failed_total"] = total_failed

    def get_privileged_accounts(self):
        """List users with elevated privileges (sudo/wheel/adm members or uid 0)."""
        privileged_groups = ["sudo", "wheel", "adm"]
        users = {}
        try:
            all_groups = grp.getgrall()
            all_users = {u.pw_name: u for u in pwd.getpwall()}
        except Exception:
            maindata["Privileged_Accounts"] = [{
                "User": "-",
                "Groups": "-",
                "name": "Priv1"
            }]
            maindata["privileged_user_count"] = 0
            return

        for g in all_groups:
            if g.gr_name in privileged_groups:
                for member in g.gr_mem:
                    users.setdefault(member, set()).add(g.gr_name)

        for name, user in all_users.items():
            if user.pw_uid == 0:
                users.setdefault(name, set()).add("uid0")

        table = []
        for i, (user, groups_set) in enumerate(sorted(users.items())[:20]):
            table.append({
                "User": user,
                "Groups": ",".join(sorted(groups_set)),
                "name": "Priv{}".format(i + 1)
            })

        if not table:
            table = [{
                "User": "-",
                "Groups": "-",
                "name": "Priv1"
            }]

        maindata["Privileged_Accounts"] = table
        maindata["privileged_user_count"] = len(users)

    def get_resource_anomalies(self):
        """Identify processes consuming unusually high CPU or memory."""
        cmd = "ps -eo comm,%cpu,%mem --sort=-%cpu | head -n 20"
        output = self.run_command(cmd)
        lines = output.splitlines()

        if len(lines) <= 1:
            maindata["High_Resource_Processes"] = [{
                "Process": "-",
                "CPU_Percent": 0.0,
                "MEM_Percent": 0.0,
                "name": "Res1"
            }]
            return

        anomalies = []
        cpu_cores = max(1, os.cpu_count() or 1)
        for line in lines[1:]:
            parts = line.split()
            if len(parts) < 3:
                continue
            proc = parts[0]
            try:
                cpu_raw = float(parts[1])
                mem = float(parts[2])
            except ValueError:
                continue
            cpu = cpu_raw
            if cpu_raw > 100.0:
                # ps reports %CPU per-core; normalize by cores and cap at 100
                cpu = round(min(cpu_raw / cpu_cores, 100.0), 2)

            if cpu >= 50.0 or mem >= 30.0:
                anomalies.append({
                    "Process": proc,
                    "CPU_Percent": cpu,
                    "MEM_Percent": mem,
                    "name": "Res{}".format(len(anomalies) + 1)
                })

            if len(anomalies) >= 10:
                break

        if not anomalies:
            anomalies = [{
                "Process": "-",
                "CPU_Percent": 0.0,
                "MEM_Percent": 0.0,
                "name": "Res1"
            }]

        maindata["High_Resource_Processes"] = anomalies


def run(param=None):
    insight = LinuxInsightMonitor()
    insight.get_firewall_status()
    insight.get_firewall_info()
    insight.get_listening_ports()
    insight.get_user_status_table()
    insight.get_rdp_connections()
    insight.get_remote_connections()
    insight.get_auth_events()
    insight.get_privileged_accounts()
    insight.get_resource_anomalies()
    maindata["tabs"] = {
                "RDP Connections": {
                    "order": 1,
                    "tablist": ["RDP_Connections"]
                },
                "Remote Connections": {
                    "order": 2,
                    "tablist": ["Remote_Connections"]
                }}
    return maindata


if __name__ == "__main__":
    print(json.dumps(run(), indent=4))
