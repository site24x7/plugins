Windows DFS monitoring:

What is  Distributed File System:

The Distributed File System (DFS) functions provide the ability to logically group shares on multiple servers and to transparently link shares into a single hierarchical namespace. DFS organizes shared resources on a network in a treelike structure.It is a file system that is distributed on multiple file servers or multiple locations. It allows programs to access or store isolated files as they do with the local ones, allowing programmers to access files from any network or computer. 

For Installation:
Create a directory "WindowsDFSMonitoring" under Site24x7 Windows Agent plugin directory :

          Windows           ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\WindowsDFSMonitoring

Download all the files and edit the cfg file run using this command on the command prompt: 

          notepad.exe path_to_the_file

Once it opens the following contents will be shown 

          [DFS_Namespace]
          path=\\windowsserver20\public-1\*


[DFS_Namespace] is the name of the monitor , you can change the name of the monitor by entering the name inside the [].

When you replace the path '\*' must be added to the end of the path like in the example or else it will not work. Then run the following command on Power shell:

          Install-WindowsFeature FS-DFS-Namespace, RSAT-DFS-Mgmt-Con

After the above steps are done place the WindowsDFSMonitoring.cfg and WindowsDFSMonitoring.ps1 files under the "WindowsDFSMonitoring" under Site24x7 Windows Agent plugin directory

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

The plugin contains the following metrics.


          1) Server Name - The Name of the Server which is monitored.

          2) Namespace - The DFS Namespace which is being monitored.

          3) Total - Total no.of Folders in the DFS Namespace.

          4) Total Online - No.of Folders online.

          5) Total Offline - No.of Folders which are offline.

          6) Folder1,2,3,etc,. -The List of the folders present in DFS Namespace.

          7) FolderName_Status - Displays 1 if the particular folder is online if else 0.
