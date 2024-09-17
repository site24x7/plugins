
import sys
import re
import subprocess


### Monitoring iDRAC Servers - SNMPUtil

### It uses net-snmp packages to execut the snmp commands to get the data from the network devices
### snmpget, snmpwalk commands are supported
### 
### Author: Anita, Zoho Corp
### Language : Python
### Tested in Ubuntu
### Tested for snmp version 2c

# Utility class to execute snmp commands
class SNMPPARSER: 
    def __init__(self,command,HOST,VERSION,COMMUNITY,oids,MIB,elements = None):
        self.command = command
        self.host = HOST
        self.snmp_version = VERSION
        self.snmp_community = COMMUNITY
        self.oids = oids
        self.mibs = MIB
        
        if elements != None:
            data = ''
            for _ in elements:
                data = data + _ + ',' 
            self.elements = data.split(',')
            
        self.data = {}
    
    
    def get_snmp_output(self, snmp_command):
        
        try:
            p = subprocess.Popen(snmp_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            p_status = p.wait()
            output = output.rstrip()
            if type(output) != str : output = output.decode("utf-8") 
            return p_status, output, err
        
        except Exception as e:
            print("snmp ", e) 
            raise ValueError(e)
    
    def executeSNMPCommand(self):
        
        snmp_command = self.command+ ' -O q -v '+ self.snmp_version + ' -c ' + self.snmp_community +' '+ self.host +' '+ self.oids 
        #print(snmp_command)
        status, output, err = self.get_snmp_output(snmp_command)
        
        if status != 0:
            if 'Unknown Object Identifier' in output: raise ValueError('Unable to connect.Please check configurations.')
            elif 'Timeout:' in output: raise ValueError('SNMP timeout!')
            else: raise ValueError(err.decode("utf-8"))
        else:
            if self.command == 'snmpget' : return output
            else : return output.split('\n') 
        
    # Parsing snmpget data
    def parseGetData(self):
        value = ''.join(self.output.split()[1:])
        data = {}
        data[self.oids] = value
        return data
    
    # Parsing snmpget/snmpwalk data and return the raw data as output
    def getRawData(self):
        if self.command == 'snmpget':#retrieving data from a host
            self.output = self.executeSNMPCommand()
        elif self.command == 'snmpwalk':#retrieving lots of data at once
            self.output = self.executeSNMPCommand()
        else:
            raise Exception(self.command+" Not Supported") 
        return self.output
        
    # Parsing snmpget,snmpwalk data
    def getData(self):
        if self.command == 'snmpget':#retrieving data from a host
            self.data = self.getRawData()
            self.output = self.parseGetData()
        elif self.command == 'snmpwalk':#retrieving lots of data at once
            self.output = self.getRawData()
            self.data = self.parseWalkData()
        else:
            print(self.command+" Not Supported")   
        return self.data
    
    # Parsing snmpwalk data
    def parseWalkData(self):
        data = {}
        
        pattern = ''
        for _ in self.elements:
            pattern += _ + "\."
             
            if _ != self.elements[-1]:
                pattern += "|"
        
        item = re.compile(pattern)
        for _ in self.output:
            if item.search(_):
                key = _.split()[0].split('::')[1].replace('"','')
                value = ' '.join(_.split()[1:]).replace('"','')
                #print(_.split()[1:])
                data[key] = value
        return data
