Plugin for Disk partition  Monitoring
===========

Update the disk partition name in the script before adding the plugin 

The following metrics are provided for the disk partition I/O plugin:

    * CurrentDiskQueueLength: Number of outstanding requests on the disk at the time the performance data is collected.
    * AvgDisksecPerTransfer: Time, in seconds, of the average disk transfer.
    * DiskTransfersPersec: Rate of read and write operations on the disk.
    * DiskWritesPersec: Rate of write operations on the disk.
    * DiskReadsPersec: Rate of read operations on the disk.
    * PercentDiskReadTime: Percentage of elapsed time when the selected disk drive is busy servicing read requests.
    * DiskWriteBytesPersec: Rate at which bytes are transferred to the disk during write operations.
    * AvgDiskQueueLength: Average number of both read and write requests that were queued for the selected disk during the sample interval.
    * DiskReadBytesPersec: Rate at which bytes are transferred from the disk during read operations.
    * PercentDiskWriteTime: Percentage of elapsed time when the selected disk drive is busy servicing write requests.
    * DiskBytesPersec: Rate at which bytes are transferred to or from the disk during write or read operations.
    * PercentDiskTime: Percentage of elapsed time that the selected disk drive is busy servicing read or write requests.
    * PercentIdleTime: Percentage of time during the sample interval that the disk was idle.
    
## **Prerequisites**

Download and install the latest version of the [Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
    
## Plugin installation ##

* Create a directory "DiskPartitionIO" 

* Download the file "DiskPartitionIO.ps1" and place under DiskPartitionIO.

* Move the directory "DiskFolderMonitoring" to Site24x7 Windows Agent plugin directory 

```
    Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\DiskFolderMonitoring
```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


