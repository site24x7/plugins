#!/usr/bin/python3

import json
import SNMPUtil
import argparse

### Monitoring iDRAC Servers - Memory Performance

### It uses snmpwalk command to get the hadrware data from the iDRAC Servers.
### SNMPUtil.py is used to get the snmp raw data and parsed to get the output json
### Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server
### 
### Author: Anita, Zoho Corp
### Language : Python
### Tested in Ubuntu
### Tested for snmp version 2c

### iDRAC Server Configuration Details

OIDREPLACE = "1.3.6.1.4.1"
SMISTR = "SNMPv2-SMI::enterprises"
ISOSTR = "iso.3.6.1.4.1"

### OIDS for Getting Memory Details
OIDS = {'memory': ['1.3.6.1.4.1.674.10892.5.4.1100.50.1']}
### OID Attributes
hardware = {'memory': ['1.3.6.1.4.1.674.10892.5.4.1100.50.1.23', '1.3.6.1.4.1.674.10892.5.4.1100.50.1.4', '1.3.6.1.4.1.674.10892.5.4.1100.50.1.5', '1.3.6.1.4.1.674.10892.5.4.1100.50.1.7', '1.3.6.1.4.1.674.10892.5.4.1100.50.1.14', '1.3.6.1.4.1.674.10892.5.4.1100.50.1.15']}
### Output Keys and their units
names = {'memory': ['name','state', 'status', 'type', {'size': 'KB'}, {'speed': 'nanosec'}]}

class HardwareParser:
    def __init__(self, hostname, snmp_version, snmp_community_str, mib_location):
        self.hostname = hostname
        self.snmp_version = snmp_version
        self.snmp_community_str = snmp_community_str
        self.mib_location = mib_location
        self.hardware = 'memory'
        self.oids = OIDS[self.hardware]
        
    def getData(self):
        output_data = {'data': {}, 'units': {}}
        oid = self.oids[0]
        
        try:
            snmpdata = SNMPUtil.SNMPPARSER('snmpwalk', self.hostname, self.snmp_version, self.snmp_community_str, oid, self.mib_location, hardware[self.hardware])
            self.snmp_data = snmpdata.getRawData()
            output_data = self.parseSNMPData(output_data)
        except Exception as e:
            raise Exception(e)
            
        return output_data

    def parseSNMPData(self, output_data):
        unitdata = {}
        online_count = 0
        offline_count = 0

        memory_map = {}
        memory_attributes = set() 

        for line in self.snmp_data:
            if not line.startswith(OIDREPLACE):
                line = line.replace(SMISTR, OIDREPLACE).replace(ISOSTR, OIDREPLACE)

            line = line.replace('\n', '').replace('\r', '').replace('"', '')
            parts = line.split(' ')
            if len(parts) < 2:
                continue
            
            name = parts[0]
            value = parts[1].split(':')[-1].strip() if ':' in parts[1] else parts[1]

            for index, oid in enumerate(hardware[self.hardware]):
                if oid in name:
                    attribute = names[self.hardware][index]
                    if isinstance(attribute, dict):
                        attribute, unit = list(attribute.items())[0]
                        unitdata[attribute] = unit
                    
                    if isinstance(attribute, dict):
                        attribute = list(attribute.keys())[0]

                    key = name.split('.')[-1]
                    if key not in memory_map:
                        memory_map[key] = {attr: "" for attr in memory_attributes}
                    
                    memory_map[key][attribute] = value

                    memory_attributes.add(attribute)
                    break 

        memory_list = []
        for attributes in memory_map.values():
            memory = {
                'name': attributes.get('name', ''),
                'State': attributes.get('state', ''),
                'Size': attributes.get('size', ''),
                'Type': attributes.get('type', ''),
                'Status': attributes.get('status', ''),
                'Speed': attributes.get('speed', ''),
            }
            memory_list.append(memory)
            if memory['name']:
                if memory['Status'] == '3':
                    online_count += 1
                else:
                    offline_count += 1

        output_data['data'] = {'memory': memory_list}
        output_data['units'] = {'memory': unitdata}
        output_data['Memory Online'] = online_count
        output_data['Memory Offline'] = offline_count

        return output_data

if __name__ == '__main__':
    
    result = {}
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', help='hostname', nargs='?', default='localhost')
    parser.add_argument('--snmp_version', help='snmp version', type=str, nargs='?', default="2c")
    parser.add_argument('--snmp_community_str', help='snmp community version',  nargs='?', default='public')
    parser.add_argument('--idrac_mib_file_locn', help='idrac mib file location',  nargs='?', default='')
    parser.add_argument('--plugin_version', help='plugin template version',  nargs='?', default='2')
    parser.add_argument('--heartbeat_required', help='Enable heartbeat for monitoring',  nargs='?', default="true")
    args = parser.parse_args()
    
    try:
        parser = HardwareParser(args.hostname, args.snmp_version, args.snmp_community_str, args.idrac_mib_file_locn)
        output = parser.getData()
        result = output['data']
        result['units'] = output['units']
        
        total_memories = len(result.get('memory', []))
        result['Total Memories'] = total_memories
        result['Memory Plugin Status'] = "ok"

        result['Memory Online'] = output.get('Memory Online', 0)
        result['Memory Offline'] = output.get('Memory Offline', 0)

    except Exception as e:
        result['msg'] = str(e)
    
    result['plugin_version'] = args.plugin_version
    result['heartbeat_required'] = args.heartbeat_required
    print(json.dumps(result))
