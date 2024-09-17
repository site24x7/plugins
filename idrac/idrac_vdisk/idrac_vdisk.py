#!/usr/bin/python3

import json
import SNMPUtil
import argparse

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
        self.hardware = 'vdisk'
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
        disks = []
        online_count = 0
        offline_count = 0
        disk_map = {}

        for snmp_item in self.snmp_data:
            if not snmp_item.startswith(OIDREPLACE):
                if snmp_item.startswith(SMISTR):
                    snmp_item = snmp_item.replace(SMISTR, OIDREPLACE)
                elif snmp_item.startswith(ISOSTR):
                    snmp_item = snmp_item.replace(ISOSTR, OIDREPLACE)

            snmp_item = snmp_item.replace('\n', '').replace('\r', '').replace('"', '')

            for index, oid in enumerate(hardware[self.hardware]):
                if oid in snmp_item:
                    name = snmp_item.split(' ')[0]
                    elementname = name.split('.')[-1] 
                    value = ' '.join(snmp_item.split(' ')[1:]).strip()

                    if ':' in value:
                        value = value.split(':')[-1].strip()

                    elem = names[self.hardware][index]
                    attribute = elem if isinstance(elem, str) else list(elem.keys())[0]

                    if elementname not in disk_map:
                        disk_map[elementname] = {}

                    disk_map[elementname][attribute] = value

        unitdata = {
        'disk': {
            'Size': 'MB',
            'DiskBlockSizeInBytes': 'Bytes'
        }
    }
        for elementname, disk_data in disk_map.items():
            disk = {
                'name': f'v_disk_{disk_data.get("name", "")}',
                'State': disk_data.get('State', ''),
                'ComponentStatus': disk_data.get('ComponentStatus', ''),
                'Size': disk_data.get('Size', ''),
                'DiskBlockSizeInBytes': disk_data.get('DiskBlockSizeInBytes', ''),
                'DiskSecured': disk_data.get('DiskSecured', ''),
                'DiskOperationalState': disk_data.get('DiskOperationalState', '')
            }

            if disk['ComponentStatus'] == '3':
                online_count += 1
            else:
                offline_count += 1

            disks.append(disk)

        output_data['data']['disk'] = disks
        output_data['units'] = unitdata
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
