#!/usr/bin/python3
import json
import subprocess
import shutil
import re

PLUGIN_VERSION = "1"
HEARTBEAT = "true"

maindata = {
    "plugin_version": PLUGIN_VERSION,
    "heartbeat_required": HEARTBEAT
}


class LinuxInsightMonitor:

    def run_command(self, cmd):
        try:
            output = subprocess.check_output(cmd, shell=True, stderr=subprocess.DEVNULL, universal_newlines=True)
            return output.strip()
        except subprocess.CalledProcessError:
            return ""
        except Exception:
            return ""

    def detect_firewall_cmd(self):
        """Auto-detects firewall command for any distro"""
        if shutil.which("firewall-cmd"):
            return "firewall-cmd"
        elif shutil.which("ufw"):
            return "ufw"
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

    def get_firewall_rules(self):
        """Get simplified rule list with rule name and status"""
        fw_cmd = self.detect_firewall_cmd()
        rules = []
        output = ""

        if fw_cmd == "firewall-cmd":
            output = self.run_command("firewall-cmd --list-all")
        elif fw_cmd == 'ufw' or fw_cmd == "iptables":
            output = self.run_command("iptables -L -n")
        elif fw_cmd == "nft":
            output = self.run_command("nft list ruleset")
        else:
            output = "No firewall command found."

        lines = output.splitlines()
        for i, line in enumerate(lines[:10]):  # limit to 10
            clean_line = line.strip()
            if not clean_line:
                continue

            rule_name = "-"
            rule_status = "unknown"
            lower_line = clean_line.lower()

            if fw_cmd == "ufw":
                match = re.search(r"^(\S+)", clean_line)
                if match:
                    rule_name = match.group(1)
            elif fw_cmd == "iptables":
                if clean_line.startswith("Chain"):
                    match = re.search(r"Chain\s+(\S+)", clean_line)
                    if match:
                        rule_name = match.group(1)
                else:
                    port_match = re.search(r"(\d{2,5})", clean_line)
                    rule_name = port_match.group(1) if port_match else "rule_{}".format(i + 1)
            elif fw_cmd == "firewall-cmd":
                rule_name = clean_line.split()[0] if clean_line else "rule_{}".format(i + 1)
            elif fw_cmd == "nft":
                rule_name = "rule_{}".format(i + 1)

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
                "name": "Rule{}".format(i + 1)
            })

        if not rules:
            rules = [{"Rule": "-", "Rule_Status": "-", "name": "Rule1"}]

        maindata["Firewall_Rules"] = rules

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
            protocol = "-"

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
                    "User": parts[0],
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
                "User": "-",
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


def run(param=None):
    insight = LinuxInsightMonitor()
    insight.get_firewall_status()
    insight.get_firewall_rules()
    insight.get_listening_ports()
    insight.get_user_status_table()
    insight.get_rdp_connections()
    insight.get_remote_connections()
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
