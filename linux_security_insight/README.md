# Site24x7 Plugin: Server Security Insight

This Site24x7 plugin monitors the security insight of your server's firewall, active firewall rules, listening ports, user sessions, and remote connections. It provides a comprehensive overview of your server's security and connectivity status, making it easier to detect unauthorized access or configuration issues.

## Plugin Installation
---
##### Linux 

- Execute below command to download the `linux_security_insight` plugin.
  
	```bash
 	mkdir linux_security_insight
  cd linux_security_insight
  wget https://raw.githubusercontent.com/site24x7/plugins/master/linux_security_insight/linux_security_insight.py
  wget https://raw.githubusercontent.com/site24x7/plugins/master/linux_security_insight/linux_security_insight.cfg
	```

- Move the directory `linux_security_insight` into the Site24x7 Linux Agent plugin directory.

	```
	mv linux_security_insight /opt/site24x7/monagent/plugins/
	```

  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Metrics Collected

### 1. Firewall Status
- **Firewall_Status**: Indicates if the firewall is `active` or `inactive`.
- **firewall_status_numeric**: Numeric representation of firewall status (`1` for active, `0` for inactive`).

### 2. Firewall Rules
A list of firewall rules with their status:
- **Rule**: The name/type of the rule.
- **Rule_Status**: Status of the rule (`allow`, `deny`, or `unknown`).
- **name**: Identifier for the rule.

### 3. Listening Ports
A list of all currently open/listening TCP ports:
- **Protocol**: Protocol used (e.g., `tcp`).
- **Port_No**: Port number.
- **Process_Name**: Name of the process using the port.
- **name**: Identifier for the port entry.

### 4. User Status
Information about users currently logged into the system:
- **User**: Username.
- **TTY**: Terminal type.
- **From**: Source of login.
- **Login_Time**: Time of login.
- **Idle**: Idle time.
- **name**: Identifier for the user session.
- **total_users**: Total number of users logged in.
- **active_users**: Number of active users.

### 5. RDP Connections
Details of Remote Desktop Protocol connections:
- **Protocol_rdp**: Protocol used.
- **Port_rdp**: Port number.
- **Process_rdp**: Process name.
- **Remote_Address**: Remote address.
- **name**: Identifier for the RDP connection.

### 6. Remote Connections
Details of other remote connections:
- **Protocol_remote**: Protocol used.
- **Port_remote**: Port number.
- **Process_remote**: Process name.
- **IPAddress**: Remote IP address.
- **name**: Identifier for the remote connection.

---

## How It Works

- The plugin collects and reports the above metrics in JSON format.
- Data is visualized in Site24x7 dashboards for easy monitoring and alerting.
- Use this plugin to proactively monitor server security and connectivity.

---

## Example Output

```json
{
  "Firewall_Status": "inactive",
  "firewall_status_numeric": 0,
  "Firewall_Rules": [
    {"Rule": "Chain", "Rule_Status": "allow", "name": "Rule1"}
  ],
  "Listening_Ports": [
    {"Protocol": "tcp", "Port_No": "3306", "Process_Name": "mysqld", "name": "Port1"}
  ],
  "User_Status": [
    {"User": "muralik-", "TTY": "tty2", "From": "-", "Login_Time": "10:06", "Idle": "6:01m", "name": "User1"}
  ],
  "total_users": 1,
  "active_users": 1,
  "RDP_Connections": [
    {"Protocol_rdp": "tcp", "Port_rdp": "-", "Process_rdp": "-", "Remote_Address": "-", "name": "RDP1"}
  ],
  "Remote_Connections": [
    {"Protocol_remote": "tcp", "Port_remote": "-", "Process_remote": "-", "IPAddress": "-", "name": "Remote1"}
  ]
}

## Sample Image

