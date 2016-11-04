# Plugin for Monitoring etcd performance

Monitor your etcd server metrics.

### etcd_self Plugin installation
---
##### Linux 

- Create a directory "etcd_self" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/etcd_self
- Download the file [etcd_self.py] and place it under the "etcd_self" directory

##### Windows
 
- Create a directory "etcd_self" under Site24x7 Linux Agent plugin directory - C:\Program Files\Site24x7\WinAgent\monitoring\Plugins\etcd_self
- Download the file [etcd_self.py] and place it under the "etcd_self" directory
- Download [etcd_self.ps1] and place it under "etcd_self" directory
- Replace `$python="C:\Python27\python.exe"` in "etcd_self.ps1" file with your python path `$python=<python exe path>`

### etcd_self Plugin configuration
---

- `url = "http://localhost:2379" `  The etcd server url to monitor.

### etcd_self Metrics
---

Name		            	| Description
---         		   	 	|   ---
self_recv_appendreq_cnt 	| number of append requests this node has processed
self_recv_pkg_rate    		| number of requests per second this node is receiving (follower only). This value is 0 for a leader member.
self_recv_bandwidth_rate	| number of bytes per second this node is receiving (follower only). This value is 0 for a leader member.
self_appendreq_cnt			| number of requests that this node has sent
self_send_pkg_rate			| number of requests per second this node is sending (leader only). This value is 0 on single member clusters/ follower.
sendBandwidthRate			| number of bytes per second this node is sending (leader only). This value is 0 on single member clusters/ follower.

### Related Plugins
---
- [etcd_store plugin] - monitor the Store Statistics of etcd node.

[etcd_self.py]: <https://raw.githubusercontent.com/site24x7/plugins/master/etcd_self/etcd_self.py>
[etcd_self.ps1]: <https://raw.githubusercontent.com/site24x7/plugins/master/etcd_self/etcd_self.ps1>
[etcd_store plugin]: <https://github.com/site24x7/plugins/tree/master/etcd_store/>