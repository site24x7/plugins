# Plugin for Monitoring etcd performance

Monitor your etcd Store Statistics.

### etcd_store Plugin installation
---
##### Linux 

- Create a directory "etcd_store" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/etcd_store
- Download the file [etcd_store.py] and place it under the "etcd_store" directory

##### Windows
 
- Create a directory "etcd_store" under Site24x7 Linux Agent plugin directory - C:\Program Files\Site24x7\WinAgent\monitoring\Plugins\etcd_store
- Download the file [etcd_store.py] and place it under the "etcd_store" directory
- Download [etcd_store.ps1] and place it under "etcd_store" directory
- Replace `$python="C:\Python27\python.exe"` in "etcd_store.ps1" file with your python path `$python=<python exe path>`

### etcd_store Plugin configuration
---

- `url = "http://localhost:2379" `  The etcd server url to monitor.

### etcd_store Metrics
---

Name		            	| Description
---         		   	 	|   ---
gets_success 				| Rate of successful get requests
gets_fail    				| Rate of failed get requests
sets_success				| Rate of successful set requests
sets_fail					| Rate of failed set requests
delete_success				| Rate of successful delete requests
delete_fail					| Rate of failed delete requests
update_success				| Rate of successful update requests
update_fail					| Rate of failed update requests
create_success				| Rate of successful create requests
create_fail					| Rate of failed create requests
compare_and_swap_success	| Rate of successful compare and swap requests
compare_and_swap_fail		| Rate of failed compare and swap requests
compare_and_delete_success	| Rate of successful compare and delete requests
compare_and_delete_fail		| Rate of failed compare and delete requests
expire_count				| Count of expired keys
watchers					| Watchers count

### Related Plugins
---
- [etcd_self plugin] - monitor the Self Statistics of etcd node.

[etcd_store.py]: <https://raw.githubusercontent.com/site24x7/plugins/master/etcd_store/etcd_store.py>
[etcd_store.ps1]: <https://raw.githubusercontent.com/site24x7/plugins/master/etcd_store/etcd_store.ps1>
[etcd_self plugin]: <https://github.com/site24x7/plugins/tree/master/etcd_self/>