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
    ArenaAllocBytes
    ArenaAllocChunks
    CompressedReadBufferBlocks
    CompressedReadBufferBytes
    ContextLock
    CreatedReadBufferOrdinary
    CreatedWriteBufferOrdinary
    DiskReadElapsedMicroseconds
    DiskWriteElapsedMicroseconds
    FailedQuery
    FailedSelectQuery
    FileOpen
    FunctionExecute
    IOBufferAllocBytes
    IOBufferAllocs
    InsertedBytes
    InsertedRows
    Merge
    MergeTreeDataWriterBlocks
    MergeTreeDataWriterBlocksAlreadySorted
    MergeTreeDataWriterCompressedBytes
    MergeTreeDataWriterRows
    MergeTreeDataWriterUncompressedBytes
    MergedRows
    MergedUncompressedBytes
    MergesTimeMilliseconds
    NetworkReceiveElapsedMicroseconds
    NetworkSendElapsedMicroseconds
    OSCPUVirtualTimeMicroseconds
    OSCPUWaitMicroseconds
    OSWriteBytes
    OSWriteChars
    Query
    RWLockAcquiredReadLocks
    RWLockReadersWaitMilliseconds
    ReadBufferFromFileDescriptorRead
    ReadBufferFromFileDescriptorReadBytes
    ReadCompressedBytes
    RealTimeMicroseconds
    RegexpCreated
    SelectQuery
    SoftPageFaults
    SystemTimeMicroseconds
    UserTimeMicroseconds
    WriteBufferFromFileDescriptorWrite
    WriteBufferFromFileDescriptorWriteBytes
