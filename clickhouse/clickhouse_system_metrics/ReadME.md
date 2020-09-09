Clickhouse monitoring
---  
ClickHouse is a fast open-source OLAP database management system. For more details, refer their website: https://clickhouse.tech

### Prerequisites
Clickhouse Python Driver
https://clickhouse-driver.readthedocs.io/en/latest/installation.html

To install the driver, execute the command :
    pip install clickhouse-driver

### Configurations
hostname
port
database
user
password
timeout

### Metrics Captured
    BackgroundBufferFlushSchedulePoolTask
    BackgroundDistributedSchedulePoolTask
    BackgroundMovePoolTask
    BackgroundPoolTask
    BackgroundSchedulePoolTask
    CacheDictionaryUpdateQueueBatches
    CacheDictionaryUpdateQueueKeys
    ContextLockWait
    DelayedInserts
    DictCacheRequests
    DiskSpaceReservedForMerge
    DistributedFilesToInsert
    DistributedSend
    EphemeralNode
    GlobalThread
    GlobalThreadActive
    HTTPConnection
    InterserverConnection
    LocalThread
    LocalThreadActive
    MemoryTracking
    MemoryTrackingForMerges
    MemoryTrackingInBackgroundBufferFlushSchedulePool
    MemoryTrackingInBackgroundDistributedSchedulePool
    MemoryTrackingInBackgroundMoveProcessingPool
    MemoryTrackingInBackgroundProcessingPool
    MemoryTrackingInBackgroundSchedulePool
    Merge
    MySQLConnection
    OpenFileForRead
    OpenFileForWrite
    PartMutation
    PostgreSQLConnection
    Query
    QueryPreempted
    QueryThread
    RWLockActiveReaders
    RWLockActiveWriters
    RWLockWaitingReaders
    RWLockWaitingWriters
    Read
    ReadonlyReplica
    ReplicatedChecks
    ReplicatedFetch
    ReplicatedSend
    Revision
    SendExternalTables
    SendScalars
    StorageBufferBytes
    StorageBufferRows
    TCPConnection
    VersionInteger
    Write
    ZooKeeperRequest
    ZooKeeperSession
    ZooKeeperWatch
