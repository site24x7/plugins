#! /usr/bin/env python3

'''
Created on 02-Dec-2020

@author: anita-1372
'''
import argparse
import libvirt
import json

if __name__ == '__main__':
    
    conn = None
    data = {}
        
    try:
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--host', help='kvm host to connect', nargs='?', default='qemu:///system')
        parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=1)
        parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=True)

        args = parser.parse_args()
        conn = libvirt.openReadOnly(args.host)
    except Exception as e:
        data['status'] = 0
        data['msg'] = str(e)
    
    data['heartbeat_required'] = args.heartbeat
    data['plugin_version'] = args.plugin_version

    
    if conn is not None : 
        data['host'] = conn.getHostname() 
        
        
        '''
            System host details
        '''
        cpu_model, mem_in_mb, active_cpus, cpu_freq_in_hz, numa_node_count, sockets_per_node, cores_per_socket, threads_per_core = conn.getInfo()     
        data['cpu_model'] = cpu_model
        data['mem_in_mb'] = mem_in_mb
        data['active_cpus'] = active_cpus
        data['cpu_freq_in_hz'] = cpu_freq_in_hz
        data['numa_node_count'] = numa_node_count
        data['sockets_per_node'] = sockets_per_node
        data['cores_per_socket'] = cores_per_socket
        data['threads_per_core'] = threads_per_core
        
        '''
            System virtualization details
        '''
        data['virtualization_type'] = conn.getType()
        data['version'] = conn.getVersion()
        data['libvirt_version'] = conn.getLibVersion()
        data['uri'] = conn.getURI()
        data['conn_encrypted'] = True if conn.isEncrypted() else False 
        data['conn_secure'] = True if conn.isSecure() else False
        
        
        '''
            System memory details
        '''
        memory_params = conn.getMemoryParameters()
        for param in memory_params:
            data[param] = memory_params[param] 
            
        mem_stats = conn.getMemoryStats(libvirt.VIR_NODE_MEMORY_STATS_ALL_CELLS)
        for param in mem_stats:
            data[param+'_memory'] = mem_stats[param] 
            
        memlist = conn.getCellsFreeMemory(0, numa_node_count)
        cell = 0
        for cellfreemem in memlist:
            data['node_'+str(cell)+'_free_mem_in_kb'] = cellfreemem
            cell += 1
        
        
        '''
            System cpu utilization details
        '''
        stats = conn.getCPUStats(0)
        
        data['kernel'] = stats['kernel']
        data['iowait_time'] = stats['iowait']
        data['user_time'] = stats['user']
        data['idle_time'] = stats['idle']
        
        #print(conn.getSysinfo())
        
        '''
            count details
        '''
        data['vms_count'] = len(conn.listAllDomains())
        data['networks_count'] = len(conn.listAllNetworks())
        data['storage_pool_count'] = len(conn.listAllStoragePools())
        
        conn.close()
        
    print(json.dumps(data, indent=4, sort_keys=True))
