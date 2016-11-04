# Plugin for iNode Monitoring

Monitor iNode usage on servers.

### Prerequisites
---
- Site24X7 iNodeMon plugin uses python's "psutil" package to collect metrics.
    - Installation
    
            pip install psutil

- For more detail on installation refer  [How to install psutil?]

### iNodeMon Plugin installation
---
##### Linux

- Create a directory "iNodeMon" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/iNodeMon
- Download the file [iNodeMon.py] and place it under the "iNodeMon" directory

### iNodeMon Metrics
---

Name            	| Description
---             	|   ---
inode_total     	| Total inodes available
inode_used			| Number of inodes in use
inode_free       	| Number of inodes free
inode_use_percent	| Percentage of inodes used

[How to install psutil?]: <https://github.com/giampaolo/psutil/blob/master/INSTALL.rst>
[iNodemon.py]: <https://raw.githubusercontent.com/site24x7/plugins/master/iNodeMon/iNodeMon.py>
