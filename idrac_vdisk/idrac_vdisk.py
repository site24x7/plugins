#!/usr/bin/python3

import json
import SNMPUtil
import argparse

### Monitoring iDRAC Servers - virtual disk Performance

### It uses snmpwalk command to get the hadrware data from the iDRAC Servers.
### SNMPUtil.py is used to get the snmp raw data and parsed to get the output json
### Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server
### 
### Author: Anita, Zoho Corp
### Language : Python
### Tested in Ubuntu
### Tested for snmp version 2c

OIDREPLACE = "1.3.6.1.4.1"
SMISTR = "SNMPv2-SMI::enterprises"
ISOSTR = "iso.3.6.1.4.1"

### OIDS for Getting virtual Disk Details
OIDS = {'vdisk': ['1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1']}
### OID Attributes
hardware = {'vdisk': ['1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.2', '1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.4', '1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.20', '1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.6', '1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.33', '1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.38', '1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.24', '1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.30']}
### Output Keys and their units
names = {'vdisk': ['name', 'State', 'ComponentStatus', {'Size': 'MB'}, 'Type', {'DiskBlockSizeInBytes': 'Bytes'}, 'DiskSecured', 'DiskOperationalState']}

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
        output_data = {'data': {}, 'units': {}}
        for _ in OIDS:
            self.hardware = _
            self.oids = OIDS[self.hardware]
            
            for _ in self.oids:
                try:
                    ### SNMPUtil module is used to get the SNMP output for the input OIDS
                    snmpdata = SNMPUtil.SNMPPARSER('snmpwalk', self.hostname, self.snmp_version, self.snmp_community_str, _, self.mib_location, hardware[self.hardware])
                    ### Get Raw SNMP Output as a dict
                    self.snmp_data = snmpdata.getRawData()
                    ### Method to parse the SNMP command output data
                    output_data = self.parseSNMPData(output_data)
                except Exception as e:
                    raise Exception(e)
                
        return output_data
    
    ### Method to parse the SNMP command output data
    def parseSNMPData(self, output_data):
        jsondata = output_data['data']
        unitdata = output_data['units']
        
        disks = []
        online_count = 0
        offline_count = 0
        
        # Process the SNMP data
        for _ in self.snmp_data:
            if not _.startswith(OIDREPLACE) and _.startswith(SMISTR):
                _ = _.replace(SMISTR, OIDREPLACE)
            elif not _.startswith(OIDREPLACE) and _.startswith(ISOSTR):
                _ = _.replace(ISOSTR, OIDREPLACE)
            
            for index, __ in enumerate(hardware[self.hardware]):
                if __ in _:
                    _ = _.replace('\n', '').replace('\r', '').replace('"', '')
                    name = _.split(' ')[0]
                    elementname = name[len(name) - 1]

                    l = _.split(' ')
                    l.pop(0)
                    value = ' '.join(l)
                    
                    if ':' in value:
                        val = value.split(':')[1:] 
                        value = val[len(val) - 1]
                
                    elem = names[self.hardware][index]
                    
                    attribute = ''
                    unit = ''
                    
                    if type(elem) is str:
                        attribute = elem
                    elif type(elem) is dict:
                        attribute = list(elem.keys())[0]
                        unit = elem[list(elem.keys())[0]]
                    
                    key = (attribute + '_' + elementname).replace(' ', '')
                    jsondata[key] = value
                    
                    if unit != '':
                        unitdata[key] = unit 

        # Aggregating data into disk list and counting states
        disk_attributes = {item if isinstance(item, str) else list(item.keys())[0] for item in names[self.hardware]}
        
        disk_map = {}
        
        for key, value in jsondata.items():
            attribute = key.split('_')[0]
            index = key.split('_')[1]
            
            if index not in disk_map:
                disk_map[index] = {attr: "" for attr in disk_attributes}
            
            disk_map[index][attribute] = value
        
        for index, attributes in disk_map.items():
            disk = {
                'name': f'v_disk_{attributes.get("name", "")}',
                'State': attributes.get('State', ''),
                'ComponentStatus': attributes.get('ComponentStatus', ''),
                'Size': attributes.get('Size', ''),
                'Type': attributes.get('Type', ''),
                'DiskBlockSizeInBytes': attributes.get('DiskBlockSizeInBytes', ''),
                'DiskSecured': attributes.get('DiskSecured', ''),
                'DiskOperationalState': attributes.get('DiskOperationalState', '')
            }
            if disk['name']:
                disks.append(disk)
                if disk['ComponentStatus'] == '3':
                    online_count += 1
                else:
                    offline_count += 1
        
        units = {attr: unit for item in names[self.hardware] if isinstance(item, dict) for attr, unit in item.items()}

        output_data['data'] = {'disk': disks}
        output_data['units'] = {'disk': units}
        
        output_data['Disks Online'] = online_count
        output_data['Disks Offline'] = offline_count
        
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
        
        total_v_disks = len(result.get('disk', []))
        result['Total virtual Disks'] = total_v_disks
        
        result['Vdisk Plugin Status'] = "ok"
        result['Disks Online'] = output.get('Disks Online', 0)
        result['Disks Offline'] = output.get('Disks Offline', 0)
    except Exception as e:
        result['msg'] = str(e)
    
    result['plugin_version'] = args.plugin_version
    result['heartbeat_required'] = args.heartbeat_required
    print(json.dumps(result))
