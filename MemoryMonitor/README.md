# Server Memory Monitor #

Plugin to monitor memory related metric like CommittedBytes,PercentCommittedBytesInUse,SystemCacheResidentBytes etc

#### OS Supported : Windows ####

#### Attributes ####

* CommitLimit - The amount of virtual memory that can be committed without having to extend the paging file(s)
* AvailableKBytes - The amount of physical memory, in Kilobytes, immediately available for allocation to a process or for system use
* CacheBytes - The size, in bytes, of the portion of the system file cache which is currently resident and active in physical memory
* CommittedBytes - The amount of committed virtual memory, in bytes
* PercentCommittedBytesInUse - The ratio of Committed Bytes to the Commit Limit. 
* FreeAndZeroPageListBytes - The amount of physical memory, in bytes, that is assigned to the free and zero page lists.
* FreeSystemPageTableEntries - The number of page table entries not currently in used by the system.
* ModifiedPageListBytes - The amount of physical memory, in bytes, that is assigned to the modified page list.
* PoolNonpagedBytes - The size, in bytes, of the nonpaged pool, an area of the system virtual memory that is used for objects that cannot be written to disk, but must remain in physical memory as long as they are allocated.
* PoolPagedBytes - The size, in bytes, of the paged pool, an area of the system virtual memory that is used for objects that can be written to disk when they are not being used.
* SystemDriverTotalBytes - The size, in bytes, of the pageable virtual memory currently being used by device drivers.
* PoolPagedResidentBytes - The size, in bytes, of the portion of the paged pool that is currently resident and active in physical memory.
* StandbyCacheCoreBytes - The amount of physical memory, in bytes, that is assigned to the core standby cache page lists.
* StandbyCacheNormalPriorityBytes - The amount of physical memory, in bytes, that is assigned to the normal priority standby cache page lists.
* StandbyCacheReserveBytes - The amount of physical memory, in bytes, that is assigned to the reserve standby cache page lists.
* SystemCacheResidentBytes - The size, in bytes, of the portion of the system file cache which is currently resident and active in physical memory.
* SystemCodeResidentBytes - The size, in bytes, of the pageable operating system code that is currently resident and active in physical memory.
* SystemCodeTotalBytes - The size, in bytes, of the pageable operating system code currently mapped into the system virtual address space.
* SystemDriverResidentBytes - The size, in bytes, of the pageable physical memory being used by device drivers.

## Plugin installation ##

* Create a directory "MemoryMonitor" under Site24x7 Windows Agent plugin directory - <Agent Installation Directory>\monitoring\Plugins\FileCountMonitor

* Download the file "MemoryMonitor.ps1"  

* place MemoryMonitor.ps1 script under the "MemoryMonitor" directory


###### The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center. ######
