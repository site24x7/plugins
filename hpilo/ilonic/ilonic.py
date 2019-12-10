#!/usr/bin/env python

import commands
import json
import sys
import re
import SNMPUtil

### Monitoring HP Integrated Lights Out (iLo)  Servers - Battery Performance

### It uses snmpwalk command to get the hadrware data from the HP Integrated Lights Out (iLo)  Servers.
### SNMPUtil.py is used to get the snmp raw data and parsed to get the output json
### Download and install the latest version of Site24x7 Linux Agent. The agent will execute the plugin and push the data to the Site24x7 server
### 
### Author: Anita, Zoho Corp
### Language : Python
### Tested in Ubuntu
### Tested for snmp version 2c


### HP Integrated Lights Out (iLo)  Server Configuration Details
HOST = 'HOSTNAME'
VERSION = '2c' 
COMMUNITY = 'public'
MIB = 'MIB LOCATION'

PLUGIN_VERSION="1"
HEARTBEAT="false"


### OIDS for Getting Battery Details
OIDS = {'nic' : ['cpqSm2NicStatsTable']}
### OID Attributes
hardware = {'nic' : ['cpqSm2NicStatsLocation','cpqSm2NicXmitBytes', 'cpqSm2NicXmitTotalPackets', 'cpqSm2NicXmitUnicastPackets', 'cpqSm2NicXmitNonUniPackets', 'cpqSm2NicXmitDiscardPackets', 'cpqSm2NicXmitErrorPackets', 'cpqSm2NicXmitQueueLength', 'cpqSm2NicRecvBytes', 'cpqSm2NicRecvTotalPackets', 'cpqSm2NicRecvUnicastPackets', 'cpqSm2NicRecvNonUniPackets', 'cpqSm2NicRecvDiscardPackets', 'cpqSm2NicRecvErrorPackets', 'cpqSm2NicRecvUnknownPackets']}
### Output Keys and their units
names = {'nic' : ['Location',{'Bytes Transmitted' : 'bytes'} , 'Total Transmit Packets', 'Unicast Transmit Packets', 'Non-Unicast Transmit Packets', 'Transmit Discarded Packets', 'Error Transmit Packets', ' Outstanding Packets in Transmit Queue', {'Bytes Received' : 'bytes'} , 'Total Receive Packets', 'Unicast Receive Packets', 'Non-Unicast Receive Packets', 'Total Receive Discarded Packets', 'Total Receive Error Packets', 'Unknown Protocol Packets']}

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
                ### SNMPUtil module is used to get the snmp output for the input OIDS
                snmpdata = SNMPUtil.SNMPPARSER('snmpwalk',HOST,VERSION,COMMUNITY,_,MIB,hardware[self.hardware])
                ### get Raw SNMP Output as a dict
                self.snmp_data = snmpdata.getRawData()
                ### Method to parse the SNMP command output data
                output_data = self.parseSNMPData(output_data)
                
        return output_data
    
    
    ### Method to parse the SNMP command output data
    def parseSNMPData(self,output_data):
        jsondata = output_data['data'] 
        unitdata = output_data['units'] 
        
        for _ in self.snmp_data:
            for index, __ in enumerate(hardware[self.hardware]) :
                if __ in _:        
                    
                    name = ''.join(_.split("::")[1:]).replace('"','').split(' ')[0].split('.')
                    
                    elementname = name[len(name)-1]     # Name
                    value = ''.join(_.split()[1:]).replace('"','') # Value
                    
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
    
    parser = HardwareParser()
    result = {}
    try:
        output = parser.getData()
        result = output['data']
	result['plugin_version'] = PLUGIN_VERSION
        result['heartbeat_required']=HEARTBEAT
        result['units'] = output['units']
    except ValueError as e:
        result['msg'] = str(e)
    print(json.dumps(result, indent=2, sort_keys=True))
    
