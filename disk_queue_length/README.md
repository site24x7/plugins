# Plugin for Monitoring Disk Queue Length

### PreRequisites

Plugin Uses iostat command to get the disk queue length metric

command used : iostat -xmt 1 3

### Plugin installation
---
##### Linux 

- Create a directory "disk_queue_length" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/disk_queue_length
- Download the file "disk_queue_length.py" and place it under the "disk_queue_length" directory
  
  wget https://raw.githubusercontent.com/site24x7/plugins/master/disk_queue_length/disk_queue_length.py
	
  The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.



### Plugin configurations
---

- By default plugin captures all the disks queue length. 
- If any specific disk queue length needs to be captured provide the disk name in the DISKS field of disk_queue_length.py
- for eg if 'nvme0n1' needs to be monitored configure as DISKS=['nvme0n1']
