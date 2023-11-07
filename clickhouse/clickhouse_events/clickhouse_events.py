#!/usr/bin/python
'''
Site24x7 Plugin to monitor Clickhouse Asynchronous metrics
'''

from clickhouse_driver import Client
import json
import argparse

### Query: SELECT event, value FROM system.events
### Ignored metrics
### "ArenaAllocBytes", "ArenaAllocChunks", "CreatedReadBufferOrdinary", "CreatedWriteBufferOrdinary", "FunctionExecute", "IOBufferAllocBytes", "IOBufferAllocs", 
### "MergeTreeDataWriterBlocks", "MergeTreeDataWriterBlocksAlreadySorted", "MergeTreeDataWriterCompressedBytes", "MergeTreeDataWriterRows", 
### "MergeTreeDataWriterUncompressedBytes", "MergedRows", "MergedUncompressedBytes","OSCPUVirtualTimeMicroseconds", "OSCPUWaitMicroseconds", "OSWriteBytes", 
### "OSWriteChars", "ReadBufferFromFileDescriptorRead", "ReadBufferFromFileDescriptorReadBytes","RealTimeMicroseconds", "RegexpCreated",  
###  "SystemTimeMicroseconds", "UserTimeMicroseconds",  "WriteBufferFromFileDescriptorWrite", "WriteBufferFromFileDescriptorWriteBytes"

METRICS = [ "CompressedReadBufferBlocks", "CompressedReadBufferBytes", "ContextLock","DiskReadElapsedMicroseconds", "DiskWriteElapsedMicroseconds", 
           "FailedQuery", "FailedSelectQuery", "FileOpen", "InsertedBytes", "InsertedRows", 
           "Merge",  "MergesTimeMilliseconds", "NetworkReceiveElapsedMicroseconds", 
           "NetworkSendElapsedMicroseconds",  "Query", "RWLockAcquiredReadLocks", "RWLockReadersWaitMilliseconds", 
            "ReadCompressedBytes", "SelectQuery", "SoftPageFaults",]


class ClickHouse:
    def __init__(self) :
        pass
    
    def _connect_(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--hostname', help='hostname', nargs='?', default='localhost')
        parser.add_argument('--port', help='port number', type=int, nargs='?', default=9000)
        parser.add_argument('--database', help='database',  nargs='?', default='default')
        parser.add_argument('--user', help='user',  nargs='?', default='default')
        parser.add_argument('--password', help='password',  nargs='?', default='')
        parser.add_argument('--timeout', help='connection timeout', type=int,  nargs='?', default=10)
        args = parser.parse_args()
        return Client(host=args.hostname, port=args.port, database=args.database,user=args.user,password=args.password,connect_timeout=args.timeout)
        
    def _get_data_(self):
        QUERY = 'SELECT event, value FROM system.events'
        connection = self._connect_()
        self.metrics = dict(connection.execute(QUERY))
        connection.disconnect()
        
        data = {}
        for key in self.metrics:
            if key in METRICS : data[key] = self.metrics[key]
        data['plugin_version']=1
        data['heartbeat_required']="true"
    
        return dict(data)        
    
if __name__ == '__main__':
    clickhouse = ClickHouse()
    result = clickhouse._get_data_()
    print(json.dumps(result, indent=4, sort_keys=True))    
