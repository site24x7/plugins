# Disk Folder monitoring #

A plugin to monitor the specfic folder in a disk. For IT operation team, there are critical application folders that they have to 
monitor with the below metrics during operations. This will ensure technicans that whether the critical application folders are in 
idle state or growing beyond the limit or folder runs in usual state. 

    * Size : Size of the Folder.
    * File count : Number of files present in the given folder. 
    * Directory : Number of directories present in the given folder.
    * File created : Number of files created since last poll of the plugin.
    * Directory created : Number of directories created since last poll of the plugin.
    * File Modified : Number of files modified since last poll of the plugin.
    * Directory Modified : Number of files modified since last poll of the plugin.
    
## **Prerequisites**

Download and install the latest version of the [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
    
## Plugin installation ##

* Create a directory "DiskFolderMonitoring" 
* 
* Download the file "DiskFolderMonitoring.ps1" and place under DiskFolderMonitoring.

* Edit  DiskFolderMonitoring.ps1 script and update $path with the path of the folder you want to monitor.

* Move the directory "DiskFolderMonitoring" to Site24x7 Windows Agent plugin directory - \monitoring\Plugins\

###### The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center. ######



