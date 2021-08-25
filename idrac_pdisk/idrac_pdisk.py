#!/usr/bin/env python

import json
import SNMPUtil
import argparse

### Monitoring iDRAC Servers - Physical disk Performance

### It uses snmpwalk command to get the hadrware data from the iDRAC Servers.
### SNMPUtil.py is used to get the snmp raw data and parsed to get the output json
### Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server
### 
### Author: Anita, Zoho Corp
### Language : Python
### Tested in Ubuntu
### Tested for snmp version 2c



### OIDS for Getting Physical Disk Details
OIDS = {'pdisk' : ['physicalDiskTable']}
### OID Attributes
hardware = {'pdisk' : ['physicalDiskName','physicalDiskState','physicalDiskCapacityInMB','physicalDiskMediaType']}
### Output Keys and their units
names = {'pdisk' : ['name','state',{'size': 'MB'},'type']}


class HardwareParser:
    def __init__(self, hostname, snmp_version, snmp_community_str, mib_location):
        self.hostname = hostname
        self.snmp_version = snmp_version
        self.snmp_community_str = snmp_community_str
        self.mib_location = mib_location
        
        self.hardware = ''
        self.oids = ''
        self.pattern = ''
        
    def getData(self):
        output_data = {}
        output_data['data'] = {}
        output_data['units'] = {}
        for _ in OIDS:
            self.hardware = _
            self.oids = OIDS[self.hardware]
            
            for _ in self.oids:
                try:
                    ### SNMPUtil module is used to get the snmp output for the input OIDS
                    snmpdata = SNMPUtil.SNMPPARSER('snmpwalk',self.hostname, self.snmp_version, self.snmp_community_str,_, self.mib_location, hardware[self.hardware])
                    ### get Raw SNMP Output as a dict
                    self.snmp_data = snmpdata.getRawData()
                    ### Method to parse the SNMP command output data
                    output_data = self.parseSNMPData(output_data)
                except Exception as e:
                    raise Exception(e)
                
        return output_data
    
    
    ### Method to parse the SNMP command output data
    def parseSNMPData(self,output_data):
        jsondata = output_data['data'] 
        unitdata = output_data['units'] 
        
        for _ in self.snmp_data:
            for index, __ in enumerate(hardware[self.hardware]) :
                if __ in _:        
                    
                    name = ''.join(_.split("::")[1:]).replace('"','').split(' ')[0].split('.')
                    
                    elementname = name[len(name)-1] # Name
                    value = ''.join(_.split()[1:]).replace('"','')  # Name
                    
                    if ':' in value:
                        val = value.split(':')[1:] 
                        value = val[len(val)-1]
                   
                    elem = names[self.hardware][index]
                    
                    attribute = '' # Attribute Name
                    unit = ''      # Attribute Value
                    
                    if type(elem) is str: # Attributes with no units specified
                        attribute = elem
                    elif type(elem) is dict: # Attributes with units
                        attribute = (elem.keys())[0]
                        unit = elem[(elem.keys())[0]]
                    
                    key = (attribute +'_'+elementname).replace(' ','')
                    jsondata[key] = value
                    
                    if unit!='':
                        unitdata[key] = unit 
                 
        output_data['data'] = jsondata
        output_data['units'] = unitdata
        
        return output_data



if __name__ == '__main__':
    
    result = {}
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', help='hostname', nargs='?', default='localhost')
    parser.add_argument('--snmp_version', help='snmp version', type=str, nargs='?', default="2c")
    parser.add_argument('--snmp_community_str', help='snmp community version',  nargs='?', default='public')
    parser.add_argument('--idrac_mib_file_locn', help='idrac mib file location',  nargs='?', default='')
    parser.add_argument('--plugin_version', help='plugin template version',  nargs='?', default='1')
    parser.add_argument('--heartbeat_required', help='Enable heartbeat for monitoring',  nargs='?', default="true")
    args = parser.parse_args()
    
    try:
        parser = HardwareParser(args.hostname, args.snmp_version, args.snmp_community_str, args.idrac_mib_file_locn)
        output = parser.getData()
        result = output['data']
        result['units'] = output['units']
    except Exception as e:
        result['msg'] = str(e)
    
    result['plugin_version'] = args.plugin_version
    result['heartbeat_required'] = args.heartbeat_required
    print(json.dumps(result, indent=2, sort_keys=True))
    