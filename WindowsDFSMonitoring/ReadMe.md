# Windows DFS monitoring

#### What is Distributed File System:

The Distributed File System (DFS) functions provide the ability to logically group shares on multiple servers and to transparently link shares into a single hierarchical namespace. DFS organizes shared resources on a network in a treelike structure.It is a file system that is distributed on multiple file servers or multiple locations. It allows programs to access or store isolated files as they do with the local ones, allowing programmers to access files from any network or computer. 

## Prerequisites: 
   
- FS-DFS-Namespace and RSAT-DFS-Mgmt-Con powershell cmdlets are required for monitoring Windows DFS. 

- Goto the server where would monitor the Windows DFS and execute the below command in the powershell
          ```
          Install-WindowsFeature FS-DFS-Namespace, RSAT-DFS-Mgmt-Con
          ```

## Installation Steps:

- Create a directory "WindowsDFSMonitoring"

- Download the below files and place under above created directory
          ```
           https://raw.githubusercontent.com/site24x7/plugins/master/WindowsDFSMonitoring/WindowsDFSMonitoring.cfg
           https://github.com/site24x7/plugins/raw/master/WindowsDFSMonitoring/WindowsDFSMonitoring.ps1
          ```
        
- Open and edit the downloaded file WindowsDFSMonitoring.cfg

          notepad.exe <dir>\WindowsDFSMonitoring.cfg

- The WindowsDFSMonitoring.cfg file will contains the below content

          [DFS_Namespace]
          path=<Path to the DFS Namespace>\*

          - [DFS_Namespace] is the name of the monitor, you can change the name based on your need.
          - Replace "<Path to the DFS Namespace>" with your the path of DFS Namespace. Don't delete the '\*' as it require to collect metrics. 

After finish the configuration, move the folder "WindowsDFSMonitoring" into the Site24x7 Windows Agent plugin directory:
    Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\WindowsDFSMonitoring

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


### Metrics collected :

          1) Server Name - The Name of the Server which is monitored.

          2) Namespace - The DFS Namespace which is being monitored.

          3) Total - Total no.of Folders in the DFS Namespace.

          4) Total Online - No.of Folders online.

          5) Total Offline - No.of Folders which are offline.

          6) Folder1,2,3,etc,. -The List of the folders present in DFS Namespace.

          7) FolderName_Status - Displays 1 if the particular folder is online if else 0.
