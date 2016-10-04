#!/usr/bin/env python

import commands
import json
import SNMPUtil

### Monitoring iDRAC Servers - Performance
### 
### This plugin can be used to get the overall status of the hardwares of iDRAC Servers
### It uses snmpwalk command to get the hadrware data from the iDRAC Servers.
### SNMPUtil.py is used to get the snmp raw data and parsed to get the output json
### Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server
### 
### Author: Anita, Zoho Corp
### Language : Python
### Tested in Ubuntu
### Tested for snmp version 1 and 2c

### iDRAC Server Configuration Details
HOST = 'localhost'
VERSION = '2c' 
COMMUNITY = 'public'
MIB = 'MIB LOCATION'

OIDS = {
        'battery'   : ['systemBattery'], 
        'cpu'       : ['processorDeviceTable'],  
        'fan'       : ['coolingDeviceTable'], 
        'memory'    : ['memoryDeviceTable'],
        'pdisk'     : ['physicalDiskTable'], 
        'PS'        : ['powerSupplyTable'],
        'PU'        : ['powerUnitTable'],
        'sensor'    : ['temperatureProbeTable'],  
        'vdisk'     : ['virtualDiskTable']
}

hardware = {
        'battery'   : ['systemBatteryStatus'],
        'cpu'       : ['processorDeviceCoreCount',],
        'fan'       : ['coolingDeviceReading'],
        'memory'    : ['memoryDeviceSize'],
        'pdisk'     : ['physicalDiskCapacityInMB'],
        'PS'        : ['powerSupplyStatus'],
        'PU'        : ['powerUnitStatus'],
        'sensor'    : ['temperatureProbeReading'],
        'vdisk'     : ['virtualDiskBadBlocksDetected',]
}


names = {
        'battery'   : ['status'],
        'cpu'       : ['cores'],
        'fan'       : [{'rotations':'rpm'}],
        'memory'    : [{'size': 'KB'}],
        'pdisk'     : [{'size': 'MB'}],
        'PS'        :  ['status'], 
        'PU'        : ['status'],
        'sensor'    : ['reading'],
        'vdisk'     : ['badblocks']
        }



class HardwareParser:
    def __init__(self):
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
                snmpdata = SNMPUtil.SNMPPARSER('snmpwalk',HOST,VERSION,COMMUNITY,_,MIB,hardware[self.hardware])
                self.snmp_data = snmpdata.getRawData()
                output_data = self.parseSNMPData(output_data)
            
                #output_data = self.parseSNMPData(output_data)
            
        return output_data
    
    def parseSNMPData(self,output_data):
        jsondata = output_data['data'] 
        unitdata = output_data['units']
        
        for _ in self.snmp_data:
            for index, __ in enumerate(hardware[self.hardware]) :
                if __ in _:        
                    
                    name = ''.join(_.split("::")[1:]).replace('"','').split(' ')[0].split('.')
                    elementname = name[len(name)-1]
                    value = ''.join( _.split()[1:]).replace('"','')
                    
                    if ':' in value:
                        val = value.split(':')[1:] 
                        value = val[len(val)-1]
                        
                    elem = names[self.hardware][index]
                    attribute = ''
                    unit = ''
                    
                    if type(elem) is str:
                        attribute = elem
                    elif type(elem) is dict:
                        attribute = (elem.keys())[0]
                        unit = elem[(elem.keys())[0]]
                        
                    key = (self.hardware +'_'+  attribute +'_'+elementname).replace(' ','')
                    jsondata[key] = value
                     
                    if unit!='':
                        unitdata[key] = unit 
                 
        output_data['data'] = jsondata
        output_data['units'] = unitdata

        return output_data



if __name__ == '__main__':
    
    parser = HardwareParser()
    result = parser.getData()
    print(json.dumps(result, indent=2, sort_keys=True))
    
