Clickhouse monitoring
---  
ClickHouse is a fast open-source OLAP database management system. For more details, refer their website: https://clickhouse.tech

### Prerequisites
Clickhouse Python Driver
https://clickhouse-driver.readthedocs.io/en/latest/installation.html

To install the driver, execute the command :
	* pip install clickhouse-driver

### Configurations
hostname
port
database
user
password
timeout

### Metrics Captured
    CompiledExpressionCacheCount
    MarkCacheBytes
    MarkCacheFiles
    MaxPartCountForPartition
    MemoryCode
    MemoryDataAndStack
    MemoryResident
    MemoryShared
    MemoryVirtual
    NumberOfDatabases
    NumberOfTables
    ReplicasMaxAbsoluteDelay
    ReplicasMaxInsertsInQueue
    ReplicasMaxMergesInQueue
    ReplicasMaxQueueSize
    ReplicasMaxRelativeDelay
    ReplicasSumInsertsInQueue
    ReplicasSumMergesInQueue
    ReplicasSumQueueSize
    UncompressedCacheBytes
    UncompressedCacheCells
    Uptime
    jemalloc.active
    jemalloc.allocated
    jemalloc.arenas.all.dirty_purged
    jemalloc.arenas.all.muzzy_purged
    jemalloc.arenas.all.pactive
    jemalloc.arenas.all.pdirty
    jemalloc.arenas.all.pmuzzy
    jemalloc.background_thread.num_runs
    jemalloc.background_thread.num_threads
    jemalloc.background_thread.run_intervals
    jemalloc.epoch
    jemalloc.mapped
    jemalloc.metadata
    jemalloc.metadata_thp
    jemalloc.resident
    jemalloc.retained
