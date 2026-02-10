#!/usr/bin/python3
import json
import traceback
import asyncio

PURESNMP_AVAILABLE = False
PURESNMP_VERSION = None
IMPORT_ERROR = None

try:
    from puresnmp import Client, V2C, PyWrapper
    PURESNMP_AVAILABLE = True
    PURESNMP_VERSION = "2.x"
except Exception as e:
    try:
        from puresnmp import walk
        PURESNMP_AVAILABLE = True
        PURESNMP_VERSION = "1.x"
    except Exception as e2:
        IMPORT_ERROR = f"puresnmp 2.x: {str(e)}, puresnmp 1.x: {str(e2)}"

class SNMPPARSER: 
    def __init__(self, HOST, VERSION, COMMUNITY, oids):
        self.host = HOST
        self.snmp_version = VERSION
        self.snmp_community = COMMUNITY
        self.oids = oids
        
        if not PURESNMP_AVAILABLE:
            error_msg = "puresnmp module is not available. "
            if IMPORT_ERROR:
                error_msg += f"Import error: {IMPORT_ERROR}"
            else:
                error_msg += "Install it using: pip install puresnmp"
            raise ImportError(error_msg)
        
        if PURESNMP_VERSION == "2.x":
            self.credentials = V2C(self.snmp_community)
            self.client = PyWrapper(Client(self.host, self.credentials))
    
    def snmpwalk(self):
        try:
            results = []
            
            if PURESNMP_VERSION == "2.x":
                async def do_walk():
                    walk_results = []
                    async for pyvarbind in self.client.walk(self.oids):
                        oid_str = pyvarbind.oid
                        value = pyvarbind.value
                        
                        if isinstance(value, bytes):
                            try:
                                value_str = value.decode('utf-8')
                            except:
                                value_str = str(value)
                        else:
                            value_str = str(value)
                        
                        walk_results.append(f"{oid_str} {value_str}")
                    return walk_results
                
                results = asyncio.run(do_walk())
            
            else:  
                for varbind in walk(self.host, self.snmp_community, self.oids):
                    oid_str = str(varbind.oid)
                    value = varbind.value
                    
                    if isinstance(value, bytes):
                        try:
                            value_str = value.decode('utf-8')
                        except:
                            value_str = str(value)
                    else:
                        value_str = str(value)
                    
                    results.append(f"{oid_str} {value_str}")
            
            return results
            
        except Exception as e:
            raise ValueError(str(e))

OIDREPLACE = "1.3.6.1.4.1"
SMISTR="SNMPv2-SMI::enterprises"
ISOSTR="iso.3.6.1.4.1" 


OIDS = {
    'battery' : ['1.3.6.1.4.1.674.10892.5.4.600.50.1'],
    'cpu' : ['1.3.6.1.4.1.674.10892.5.4.1100.30.1'],
    'fan' : ['1.3.6.1.4.1.674.10892.5.4.700.12.1'],
    'memory' : ['1.3.6.1.4.1.674.10892.5.4.1100.50.1'],
    'pdisk' : ['1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1'],
    'power' : ['1.3.6.1.4.1.674.10892.5.4.600.30.1.6','1.3.6.1.4.1.674.10892.5.4.600.20.1.6'],
    'sensor' : ['1.3.6.1.4.1.674.10892.5.4.700.20.1'],
    'vdisk' : ['1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1']
}
hardware = {
    'battery' : ['1.3.6.1.4.1.674.10892.5.4.600.50.1.2','1.3.6.1.4.1.674.10892.5.4.600.50.1.4','1.3.6.1.4.1.674.10892.5.4.600.50.1.5','1.3.6.1.4.1.674.10892.5.4.600.50.1.6','1.3.6.1.4.1.674.10892.5.4.600.50.1.7'],
    'cpu' : ['1.3.6.1.4.1.674.10892.5.4.1100.30.1.2','1.3.6.1.4.1.674.10892.5.4.1100.30.1.4','1.3.6.1.4.1.674.10892.5.4.1100.30.1.5','1.3.6.1.4.1.674.10892.5.4.1100.30.1.17','1.3.6.1.4.1.674.10892.5.4.1100.30.1.19','1.3.6.1.4.1.674.10892.5.4.1100.30.1.18','1.3.6.1.4.1.674.10892.5.4.1100.30.1.23','1.3.6.1.4.1.674.10892.5.4.1100.30.1.26','1.3.6.1.4.1.674.10892.5.4.1100.30.1.11','1.3.6.1.4.1.674.10892.5.4.1100.30.1.12'],
    'fan' : ['1.3.6.1.4.1.674.10892.5.4.700.12.1.5','1.3.6.1.4.1.674.10892.5.4.700.12.1.6','1.3.6.1.4.1.674.10892.5.4.700.12.1.8'],
    'memory' : ['1.3.6.1.4.1.674.10892.5.4.1100.50.1.8','1.3.6.1.4.1.674.10892.5.4.1100.50.1.4','1.3.6.1.4.1.674.10892.5.4.1100.50.1.5','1.3.6.1.4.1.674.10892.5.4.1100.50.1.7','1.3.6.1.4.1.674.10892.5.4.1100.50.1.14','1.3.6.1.4.1.674.10892.5.4.1100.50.1.15'],
    'pdisk' : ['1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.2','1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.4','1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.24','1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.11','1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.35','1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.17','1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.19','1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.52','1.3.6.1.4.1.674.10892.5.5.1.20.130.4.1.58'],
    'power' : ['1.3.6.1.4.1.674.10892.5.4.600.30.1.6','1.3.6.1.4.1.674.10892.5.4.600.20.1.6'],
    'sensor' : ['1.3.6.1.4.1.674.10892.5.4.700.20.1.4','1.3.6.1.4.1.674.10892.5.4.700.20.1.5','1.3.6.1.4.1.674.10892.5.4.700.20.1.6','1.3.6.1.4.1.674.10892.5.4.700.20.1.8'],
    'vdisk' : ['1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.2','1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.4','1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.20','1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.6','1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.33','1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.38','1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.24','1.3.6.1.4.1.674.10892.5.5.1.20.140.1.1.30']
}
names = {
    'battery' : ['index','state','status','reading','location'],
    'cpu' : ['index','state','status','cores','threads','cores_enabled','brand_name','socket_location','max_speed','current_speed'],
    'fan' : ['status','current_rpm','location'],
    'memory' : ['location','state','status','type','size','speed'],
    'pdisk' : ['name','state','status','size','type','used_space','free_space','security_status','block_size'],
    'sensor' : ['state','status','reading','location'],
    'vdisk' : ['name','state','status','size','type','block_size','secured','operational_state']
}

UNITS = {
    'CPU': {
        'CPU_Maximum_CPU_Speed': 'MHz',
        'CPU_Current_CPU_Speed': 'MHz'
    },
    'Fan': {
        'Current_RPM': 'rpm'
    },
    'Memory': {
        'Memory_Size': 'KB',
        'Memory_Speed': 'MHz'
    },
    'Physical_Disk': {
        'PDisk_Size': 'MB',
        'PDisk_Used_Space': 'MB',
        'PDisk_Free_Space': 'MB',
        'PDisk_Block_Size': 'Bytes'
    },
    'Current': {
        'Current': 'Ampere'
    },
    'Voltage': {
        'Voltage': 'Volts'
    },
    'Thermal_Sensor': {
        'Temperature_Reading': 'C'
    },
    'Virtual_Disk': {
        'VDisk_Size': 'MB',
        'VDisk_Block_Size': 'Bytes'
    }
}

class HardwareParser:
    def __init__(self, hostname, snmp_version, snmp_community_str):
        self.hostname = hostname
        self.snmp_version = snmp_version
        self.snmp_community_str = snmp_community_str
    
        self.hardware = ''
        self.oids = ''
        self.current_map = {}
        self.voltage_map = {}
        self.sensor_map = {}
        self.vdisk_map = {}
        
    def getData(self):
        output_data = {}
        output_data['data'] = {}
        output_data['units'] = UNITS
        output_data['data']['tabs']={
                "Compute Resources": {
                    "order": 1,
                    "tablist": ["CPU", "Memory"]
                },
                "Storage": {
                    "order": 2,
                    "tablist": ["Physical_Disk", "Virtual_Disk"]
                },
                "Thermal Management": {
                    "order": 3,
                    "tablist": ["Thermal_Sensor", "Fan"]
                },
                "Power Management": {
                    "order": 4,
                    "tablist": ["Battery", "Current", "Voltage"]
                }
            }
        for _ in OIDS:
            self.hardware = _
            self.oids = OIDS[self.hardware]
            
            for _ in self.oids:
                try:
                    snmpdata = SNMPPARSER(self.hostname, self.snmp_version, self.snmp_community_str, _)
                    self.snmp_data = snmpdata.snmpwalk()
                    output_data = self.parseSNMPData(output_data)
                except Exception as e:
                    raise Exception(e)
        return output_data
    
    
    def parseSNMPData(self, output_data):
        if 'Battery' not in output_data['data']:
            output_data['data']['Battery'] = []
            output_data['data']['Total Batteries'] = 0
        if 'CPU' not in output_data['data']:
            output_data['data']['CPU'] = []
            output_data['data']['Total CPU'] = 0
            output_data['data']['Total Active Cores'] = 0
            output_data['data']['Total Cores'] = 0
            output_data['data']['Total Threads'] = 0
        if 'Fan' not in output_data['data']:
            output_data['data']['Fan'] = []
            output_data['data']['Total Fans'] = 0
        if 'Memory' not in output_data['data']:
            output_data['data']['Memory'] = []
            output_data['data']['Total Memory'] = 0
            output_data['data']['Total Memory Size'] = 0
        if 'Physical_Disk' not in output_data['data']:
            output_data['data']['Physical_Disk'] = []
            output_data['data']['Total Physical Disks'] = 0
        if 'Current' not in output_data['data']:
            output_data['data']['Current'] = []
            output_data['data']['Total Current Probes'] = 0
        if 'Voltage' not in output_data['data']:
            output_data['data']['Voltage'] = []
            output_data['data']['Total Voltage Probes'] = 0
        if 'Thermal_Sensor' not in output_data['data']:
            output_data['data']['Thermal_Sensor'] = []
            output_data['data']['Total Thermal Sensors'] = 0
        if 'Virtual_Disk' not in output_data['data']:
            output_data['data']['Virtual_Disk'] = []
            output_data['data']['Total Virtual Disks'] = 0
        
        if self.hardware == 'battery':
            battery_map = {}
            
            for line in self.snmp_data:
                if not line.startswith(OIDREPLACE):
                    if line.startswith(SMISTR):
                        line = line.replace(SMISTR, OIDREPLACE)
                    elif line.startswith(ISOSTR):
                        line = line.replace(ISOSTR, OIDREPLACE)
                
                line = line.replace('\n', '').replace('\r', '').replace('"', '')
                
                for index, oid in enumerate(hardware[self.hardware]):
                    if oid in line:
                        name = line.split(' ')[0]
                        elementname = name.split('.')[-1]
                        
                        parts = line.split(' ')
                        parts.pop(0)
                        value = ' '.join(parts)
                        
                        if ':' in value:
                            value = value.split(':')[-1].strip()
                        
                        elem = names[self.hardware][index]
                        attribute = elem if type(elem) is str else list(elem.keys())[0]
                        
                        if elementname not in battery_map:
                            battery_map[elementname] = {}
                        
                        if attribute == 'index':
                            battery_map[elementname]['Battery_Index'] = value
                        elif attribute == 'state':
                            battery_map[elementname]['Battery_State'] = value
                        elif attribute == 'status':
                            battery_map[elementname]['Battery_Status'] = value
                        elif attribute == 'reading':
                            battery_map[elementname]['Battery_Charge_Level'] = value
                        elif attribute == 'location':
                            battery_map[elementname]['Battery_Location'] = value
            
            battery_list = []
            for bat_id, bat_data in sorted(battery_map.items()):
                battery_entry = {"name": f"Battery_{bat_id}"}
                battery_entry.update(bat_data)
                battery_list.append(battery_entry)
            
            if len(battery_list) == 0:
                battery_list.append({
                    'name': '-',
                    'Battery_Index': '-1',
                    'Battery_State': '-1',
                    'Battery_Status': '-1',
                    'Battery_Charge_Level': '-1',
                    'Battery_Location': '-'
                })
                output_data['data']['Battery'] = battery_list
                output_data['data']['Total Batteries'] = 0
            else:
                output_data['data']['Battery'] = battery_list
                output_data['data']['Total Batteries'] = len(battery_list)
        
        elif self.hardware == 'cpu':
            cpu_map = {}
            
            for line in self.snmp_data:
                if not line.startswith(OIDREPLACE):
                    if line.startswith(SMISTR):
                        line = line.replace(SMISTR, OIDREPLACE)
                    elif line.startswith(ISOSTR):
                        line = line.replace(ISOSTR, OIDREPLACE)
                
                line = line.replace('\n', '').replace('\r', '').replace('"', '')
                
                for index, oid in enumerate(hardware[self.hardware]):
                    if oid in line:
                        name = line.split(' ')[0]
                        elementname = name.split('.')[-1]
                        
                        parts = line.split(' ')
                        parts.pop(0)
                        value = ' '.join(parts)
                        
                        if ':' in value:
                            value = value.split(':')[-1].strip()
                        
                        elem = names[self.hardware][index]
                        attribute = elem
                        
                        if elementname not in cpu_map:
                            cpu_map[elementname] = {}
                        
                        if attribute == 'index':
                            cpu_map[elementname]['CPU_Index'] = value
                        elif attribute == 'state':
                            cpu_map[elementname]['CPU_State'] = value
                        elif attribute == 'status':
                            cpu_map[elementname]['CPU_Status'] = value
                        elif attribute == 'cores':
                            cpu_map[elementname]['CPU_Total_Cores'] = value
                        elif attribute == 'threads':
                            cpu_map[elementname]['CPU_Threads'] = value
                        elif attribute == 'cores_enabled':
                            cpu_map[elementname]['CPU_Cores_Enabled_Count'] = value
                        elif attribute == 'brand_name':
                            cpu_map[elementname]['CPU_Brand_Name'] = value
                        elif attribute == 'socket_location':
                            cpu_map[elementname]['CPU_Physical_Socket_Location'] = value
                        elif attribute == 'max_speed':
                            cpu_map[elementname]['CPU_Maximum_CPU_Speed'] = value
                        elif attribute == 'current_speed':
                            cpu_map[elementname]['CPU_Current_CPU_Speed'] = value
            
            cpu_list = []
            total_cores = 0
            total_active_cores = 0
            total_threads = 0
            
            for cpu_id, cpu_data in sorted(cpu_map.items()):
                cpu_entry = {"name": f"CPU_{cpu_id}"}
                cpu_entry.update(cpu_data)
                cpu_list.append(cpu_entry)
                
                if 'CPU_Total_Cores' in cpu_data:
                    total_cores += int(cpu_data['CPU_Total_Cores'])
                if 'CPU_Cores_Enabled_Count' in cpu_data:
                    total_active_cores += int(cpu_data['CPU_Cores_Enabled_Count'])
                if 'CPU_Threads' in cpu_data:
                    total_threads += int(cpu_data['CPU_Threads'])
            
            if len(cpu_list) == 0:
                cpu_list.append({
                    'name': '-',
                    'CPU_Index': '-',
                    'CPU_State': '-1',
                    'CPU_Status': '-1',
                    'CPU_Maximum_CPU_Speed': '-1',
                    'CPU_Current_CPU_Speed': '-1',
                    'CPU_Total_Cores': '-1',
                    'CPU_Cores_Enabled_Count': '-1',
                    'CPU_Threads': '-1',
                    'CPU_Brand_Name': '-',
                    'CPU_Physical_Socket_Location': '-'
                })
                output_data['data']['CPU'] = cpu_list
                output_data['data']['Total CPU'] = 0
                output_data['data']['Total Active Cores'] = 0
                output_data['data']['Total Cores'] = 0
                output_data['data']['Total Threads'] = 0
            else:
                output_data['data']['CPU'] = cpu_list
                output_data['data']['Total CPU'] = len(cpu_list)
                output_data['data']['Total Active Cores'] = total_active_cores
                output_data['data']['Total Cores'] = total_cores
                output_data['data']['Total Threads'] = total_threads
        
        elif self.hardware == 'fan':
            fan_map = {}
            
            for line in self.snmp_data:
                if not line.startswith(OIDREPLACE):
                    if line.startswith(SMISTR):
                        line = line.replace(SMISTR, OIDREPLACE)
                    elif line.startswith(ISOSTR):
                        line = line.replace(ISOSTR, OIDREPLACE)
                
                line = line.replace('\n', '').replace('\r', '').replace('"', '')
                
                for index, oid in enumerate(hardware[self.hardware]):
                    if oid in line:
                        name = line.split(' ')[0]
                        elementname = name.split('.')[-1]
                        
                        parts = line.split(' ')
                        parts.pop(0)
                        value = ' '.join(parts)
                        
                        if ':' in value:
                            value = value.split(':')[-1].strip()
                        
                        elem = names[self.hardware][index]
                        attribute = elem
                        
                        if elementname not in fan_map:
                            fan_map[elementname] = {}
                        
                        if attribute == 'status':
                            fan_map[elementname]['Fan_Status'] = value
                        elif attribute == 'current_rpm':
                            fan_map[elementname]['Current_RPM'] = value
                        elif attribute == 'location':
                            fan_map[elementname]['name'] = value
            
            fan_list = []
            for fan_id, fan_data in sorted(fan_map.items()):
                fan_entry = {}
                if 'name' in fan_data:
                    fan_entry['name'] = fan_data['name']
                if 'Fan_Status' in fan_data:
                    fan_entry['Fan_Status'] = fan_data['Fan_Status']
                if 'Current_RPM' in fan_data:
                    fan_entry['Current_RPM'] = fan_data['Current_RPM']
                fan_list.append(fan_entry)
            
            if len(fan_list) == 0:
                fan_list.append({
                    'name': '-',
                    'Fan_Status': '-1',
                    'Current_RPM': '-1'
                })
                output_data['data']['Fan'] = fan_list
                output_data['data']['Total Fans'] = 0
            else:
                output_data['data']['Fan'] = fan_list
                output_data['data']['Total Fans'] = len(fan_list)
        
        elif self.hardware == 'memory':
            memory_map = {}
            
            for line in self.snmp_data:
                if not line.startswith(OIDREPLACE):
                    if line.startswith(SMISTR):
                        line = line.replace(SMISTR, OIDREPLACE)
                    elif line.startswith(ISOSTR):
                        line = line.replace(ISOSTR, OIDREPLACE)
                
                line = line.replace('\n', '').replace('\r', '').replace('"', '')
                
                for index, oid in enumerate(hardware[self.hardware]):
                    if oid in line:
                        name = line.split(' ')[0]
                        elementname = name.split('.')[-1]
                        
                        parts = line.split(' ')
                        parts.pop(0)
                        value = ' '.join(parts)
                        
                        if ':' in value:
                            value = value.split(':')[-1].strip()
                        
                        elem = names[self.hardware][index]
                        attribute = elem
                        
                        if elementname not in memory_map:
                            memory_map[elementname] = {}
                        
                        if attribute == 'location':
                            memory_map[elementname]['name'] = value
                        elif attribute == 'state':
                            memory_map[elementname]['Memory_State'] = value
                        elif attribute == 'status':
                            memory_map[elementname]['Memory_Status'] = value
                        elif attribute == 'type':
                            memory_map[elementname]['Memory_Type'] = value
                        elif attribute == 'size':
                            memory_map[elementname]['Memory_Size'] = value
                        elif attribute == 'speed':
                            memory_map[elementname]['Memory_Speed'] = value
            
            memory_list = []
            total_memory_size = 0
            
            for mem_id, mem_data in sorted(memory_map.items()):
                memory_entry = {}
                if 'name' in mem_data:
                    memory_entry['name'] = mem_data['name']
                if 'Memory_State' in mem_data:
                    memory_entry['Memory_State'] = mem_data['Memory_State']
                if 'Memory_Status' in mem_data:
                    memory_entry['Memory_Status'] = mem_data['Memory_Status']
                if 'Memory_Type' in mem_data:
                    memory_entry['Memory_Type'] = mem_data['Memory_Type']
                if 'Memory_Size' in mem_data:
                    memory_entry['Memory_Size'] = mem_data['Memory_Size']
                    total_memory_size += int(mem_data['Memory_Size'])
                if 'Memory_Speed' in mem_data:
                    memory_entry['Memory_Speed'] = mem_data['Memory_Speed']
                memory_list.append(memory_entry)
            
            if len(memory_list) == 0:
                memory_list.append({
                    'name': '-',
                    'Memory_State': '-1',
                    'Memory_Status': '-1',
                    'Memory_Type': '-1',
                    'Memory_Size': '-1',
                    'Memory_Speed': '-1'
                })
                output_data['data']['Memory'] = memory_list
                output_data['data']['Total Memory'] = 0
                output_data['data']['Total Memory Size'] = 0
            else:
                output_data['data']['Memory'] = memory_list
                output_data['data']['Total Memory'] = len(memory_list)
                output_data['data']['Total Memory Size'] = total_memory_size
        
        elif self.hardware == 'pdisk':
            pdisk_map = {}
            
            for line in self.snmp_data:
                if not line.startswith(OIDREPLACE):
                    if line.startswith(SMISTR):
                        line = line.replace(SMISTR, OIDREPLACE)
                    elif line.startswith(ISOSTR):
                        line = line.replace(ISOSTR, OIDREPLACE)
                
                line = line.replace('\n', '').replace('\r', '').replace('"', '')
                
                for index, oid in enumerate(hardware[self.hardware]):
                    if oid in line:
                        name = line.split(' ')[0]
                        elementname = name.split('.')[-1]
                        
                        parts = line.split(' ')
                        parts.pop(0)
                        value = ' '.join(parts)
                        
                        if ':' in value:
                            value = value.split(':')[-1].strip()
                        
                        elem = names[self.hardware][index]
                        attribute = elem
                        
                        if elementname not in pdisk_map:
                            pdisk_map[elementname] = {}
                        
                        if attribute == 'name':
                            pdisk_map[elementname]['name'] = value
                        elif attribute == 'state':
                            pdisk_map[elementname]['PDisk_State'] = value
                        elif attribute == 'status':
                            pdisk_map[elementname]['PDisk_Status'] = value
                        elif attribute == 'size':
                            pdisk_map[elementname]['PDisk_Size'] = value
                        elif attribute == 'type':
                            pdisk_map[elementname]['PDisk_Type'] = value
                        elif attribute == 'used_space':
                            pdisk_map[elementname]['PDisk_Used_Space'] = value
                        elif attribute == 'free_space':
                            pdisk_map[elementname]['PDisk_Free_Space'] = value
                        elif attribute == 'security_status':
                            pdisk_map[elementname]['PDisk_Security_Status'] = value
                        elif attribute == 'block_size':
                            pdisk_map[elementname]['PDisk_Block_Size'] = value
            
            pdisk_list = []
            
            for pdisk_id, pdisk_data in sorted(pdisk_map.items()):
                pdisk_entry = {}
                if 'name' in pdisk_data:
                    pdisk_entry['name'] = pdisk_data['name']
                if 'PDisk_State' in pdisk_data:
                    pdisk_entry['PDisk_State'] = pdisk_data['PDisk_State']
                if 'PDisk_Status' in pdisk_data:
                    pdisk_entry['PDisk_Status'] = pdisk_data['PDisk_Status']
                if 'PDisk_Size' in pdisk_data:
                    pdisk_entry['PDisk_Size'] = pdisk_data['PDisk_Size']
                if 'PDisk_Type' in pdisk_data:
                    pdisk_entry['PDisk_Type'] = pdisk_data['PDisk_Type']
                if 'PDisk_Used_Space' in pdisk_data:
                    pdisk_entry['PDisk_Used_Space'] = pdisk_data['PDisk_Used_Space']
                if 'PDisk_Free_Space' in pdisk_data:
                    pdisk_entry['PDisk_Free_Space'] = pdisk_data['PDisk_Free_Space']
                if 'PDisk_Security_Status' in pdisk_data:
                    pdisk_entry['PDisk_Security_Status'] = pdisk_data['PDisk_Security_Status']
                if 'PDisk_Block_Size' in pdisk_data:
                    pdisk_entry['PDisk_Block_Size'] = pdisk_data['PDisk_Block_Size']
                pdisk_list.append(pdisk_entry)
            
            if len(pdisk_list) == 0:
                pdisk_list.append({
                    'name': '-',
                    'PDisk_State': '-1',
                    'PDisk_Status': '-1',
                    'PDisk_Size': '-1',
                    'PDisk_Type': '-1',
                    'PDisk_Used_Space': '-1',
                    'PDisk_Free_Space': '-1',
                    'PDisk_Security_Status': '-1',
                    'PDisk_Block_Size': '-1'
                })
                output_data['data']['Physical_Disk'] = pdisk_list
                output_data['data']['Total Physical Disks'] = 0
            else:
                output_data['data']['Physical_Disk'] = pdisk_list
                output_data['data']['Total Physical Disks'] = len(pdisk_list)
        
        elif self.hardware == 'power':
            for line in self.snmp_data:
                if not line.startswith(OIDREPLACE):
                    if line.startswith(SMISTR):
                        line = line.replace(SMISTR, OIDREPLACE)
                    elif line.startswith(ISOSTR):
                        line = line.replace(ISOSTR, OIDREPLACE)
                
                line = line.replace('\n', '').replace('\r', '').replace('"', '')
                
                for index, oid in enumerate(hardware[self.hardware]):
                    if oid in line:
                        name = line.split(' ')[0]
                        elementname = name.split('.')[-1]
                        
                        parts = line.split(' ')
                        parts.pop(0)
                        value = ' '.join(parts)
                        
                        if ':' in value:
                            value = value.split(':')[-1].strip()
                        
                        if oid == '1.3.6.1.4.1.674.10892.5.4.600.30.1.6':
                            try:
                                value = float(value) / 10.0
                                if elementname not in self.current_map:
                                    self.current_map[elementname] = {}
                                self.current_map[elementname]['Current'] = str(value)
                                self.current_map[elementname]['name'] = f"Current_Probe_{elementname}"
                            except:
                                pass
                        
                        elif oid == '1.3.6.1.4.1.674.10892.5.4.600.20.1.6': 
                            try:
                                value = float(value) / 1000.0
                                if elementname not in self.voltage_map:
                                    self.voltage_map[elementname] = {}
                                self.voltage_map[elementname]['Voltage'] = str(value)
                                self.voltage_map[elementname]['name'] = f"Voltage_Probe_{elementname}"
                            except:
                                pass
            
            current_list = []
            for probe_id, probe_data in sorted(self.current_map.items(), key=lambda x: int(x[0])):
                current_entry = {
                    'name': probe_data['name'],
                    'Current': probe_data['Current']
                }
                current_list.append(current_entry)
            
            voltage_list = []
            for probe_id, probe_data in sorted(self.voltage_map.items(), key=lambda x: int(x[0])):
                voltage_entry = {
                    'name': probe_data['name'],
                    'Voltage': probe_data['Voltage']
                }
                voltage_list.append(voltage_entry)
            
            if len(current_list) == 0:
                current_list.append({'name': '-', 'Current': '-1'})
                output_data['data']['Current'] = current_list
                output_data['data']['Total Current Probes'] = 0
            else:
                output_data['data']['Current'] = current_list
                output_data['data']['Total Current Probes'] = len(current_list)
                
            if len(voltage_list) == 0:
                voltage_list.append({'name': '-', 'Voltage': '-1'})
                output_data['data']['Voltage'] = voltage_list
                output_data['data']['Total Voltage Probes'] = 0
            else:
                output_data['data']['Voltage'] = voltage_list
                output_data['data']['Total Voltage Probes'] = len(voltage_list)
        
        elif self.hardware == 'sensor':
            for line in self.snmp_data:
                if not line.startswith(OIDREPLACE):
                    if line.startswith(SMISTR):
                        line = line.replace(SMISTR, OIDREPLACE)
                    elif line.startswith(ISOSTR):
                        line = line.replace(ISOSTR, OIDREPLACE)
                
                line = line.replace('\n', '').replace('\r', '').replace('"', '')
                
                for index, oid in enumerate(hardware[self.hardware]):
                    if oid in line:
                        name = line.split(' ')[0]
                        elementname = name.split('.')[-1] 
                        
                        parts = line.split(' ')
                        parts.pop(0)
                        value = ' '.join(parts)
                        
                        if ':' in value:
                            value = value.split(':')[-1].strip()
                        
                        elem = names[self.hardware][index]
                        attribute = elem
                        
                        if elementname not in self.sensor_map:
                            self.sensor_map[elementname] = {}
                        
                        if attribute == 'state':
                            self.sensor_map[elementname]['Thermal_Sensor_State'] = value
                        elif attribute == 'status':
                            self.sensor_map[elementname]['Thermal_Sensor_Status'] = value
                        elif attribute == 'reading':
                            try:
                                temp_value = float(value) / 10.0
                                self.sensor_map[elementname]['Temperature_Reading'] = str(temp_value)
                            except:
                                self.sensor_map[elementname]['Temperature_Reading'] = value
                        elif attribute == 'location':
                            self.sensor_map[elementname]['name'] = value
            
            sensor_list = []
            for sensor_id, sensor_data in sorted(self.sensor_map.items(), key=lambda x: int(x[0])):
                sensor_entry = {}
                if 'name' in sensor_data:
                    sensor_entry['name'] = sensor_data['name']
                if 'Thermal_Sensor_State' in sensor_data:
                    sensor_entry['Thermal_Sensor_State'] = sensor_data['Thermal_Sensor_State']
                if 'Thermal_Sensor_Status' in sensor_data:
                    sensor_entry['Thermal_Sensor_Status'] = sensor_data['Thermal_Sensor_Status']
                if 'Temperature_Reading' in sensor_data:
                    sensor_entry['Temperature_Reading'] = sensor_data['Temperature_Reading']
                sensor_list.append(sensor_entry)
            
            if len(sensor_list) == 0:
                sensor_list.append({
                    'name': '-',
                    'Thermal_Sensor_State': '-1',
                    'Thermal_Sensor_Status': '-1',
                    'Temperature_Reading': '-1'
                })
                output_data['data']['Thermal_Sensor'] = sensor_list
                output_data['data']['Total Thermal Sensors'] = 0
            else:
                output_data['data']['Thermal_Sensor'] = sensor_list
                output_data['data']['Total Thermal Sensors'] = len(sensor_list)
        
        elif self.hardware == 'vdisk':
            for line in self.snmp_data:
                if not line.startswith(OIDREPLACE):
                    if line.startswith(SMISTR):
                        line = line.replace(SMISTR, OIDREPLACE)
                    elif line.startswith(ISOSTR):
                        line = line.replace(ISOSTR, OIDREPLACE)
                
                line = line.replace('\n', '').replace('\r', '').replace('"', '')
                
                for index, oid in enumerate(hardware[self.hardware]):
                    if oid in line:
                        name = line.split(' ')[0]
                        elementname = name.split('.')[-1]  
                        
                        parts = line.split(' ')
                        parts.pop(0)
                        value = ' '.join(parts)
                        
                        if ':' in value:
                            value = value.split(':')[-1].strip()
                        
                        elem = names[self.hardware][index]
                        attribute = elem
                        
                        if elementname not in self.vdisk_map:
                            self.vdisk_map[elementname] = {}
                        
                        if attribute == 'name':
                            self.vdisk_map[elementname]['name'] = value
                        elif attribute == 'state':
                            self.vdisk_map[elementname]['VDisk_State'] = value
                        elif attribute == 'status':
                            self.vdisk_map[elementname]['VDisk_Status'] = value
                        elif attribute == 'size':
                            self.vdisk_map[elementname]['VDisk_Size'] = value
                        elif attribute == 'type':
                            self.vdisk_map[elementname]['VDisk_Type'] = value
                        elif attribute == 'block_size':
                            self.vdisk_map[elementname]['VDisk_Block_Size'] = value
                        elif attribute == 'secured':
                            self.vdisk_map[elementname]['VDisk_Secured'] = value
                        elif attribute == 'operational_state':
                            self.vdisk_map[elementname]['VDisk_Operational_State'] = value
            
            vdisk_list = []
            for vdisk_id, vdisk_data in sorted(self.vdisk_map.items(), key=lambda x: int(x[0])):
                vdisk_entry = {}
                if 'name' in vdisk_data:
                    vdisk_entry['name'] = vdisk_data['name']
                if 'VDisk_State' in vdisk_data:
                    vdisk_entry['VDisk_State'] = vdisk_data['VDisk_State']
                if 'VDisk_Status' in vdisk_data:
                    vdisk_entry['VDisk_Status'] = vdisk_data['VDisk_Status']
                if 'VDisk_Size' in vdisk_data:
                    vdisk_entry['VDisk_Size'] = vdisk_data['VDisk_Size']
                if 'VDisk_Type' in vdisk_data:
                    vdisk_entry['VDisk_Type'] = vdisk_data['VDisk_Type']
                if 'VDisk_Block_Size' in vdisk_data:
                    vdisk_entry['VDisk_Block_Size'] = vdisk_data['VDisk_Block_Size']
                if 'VDisk_Secured' in vdisk_data:
                    vdisk_entry['VDisk_Secured'] = vdisk_data['VDisk_Secured']
                if 'VDisk_Operational_State' in vdisk_data:
                    vdisk_entry['VDisk_Operational_State'] = vdisk_data['VDisk_Operational_State']
                vdisk_list.append(vdisk_entry)
            
            if len(vdisk_list) == 0:
                vdisk_list.append({
                    'name': '-',
                    'VDisk_State': '-1',
                    'VDisk_Status': '-1',
                    'VDisk_Size': '-1',
                    'VDisk_Type': '-1',
                    'VDisk_Block_Size': '-1',
                    'VDisk_Secured': '-1',
                    'VDisk_Operational_State': '-1'
                })
                output_data['data']['Virtual_Disk'] = vdisk_list
                output_data['data']['Total Virtual Disks'] = 0
            else:
                output_data['data']['Virtual_Disk'] = vdisk_list
                output_data['data']['Total Virtual Disks'] = len(vdisk_list)
        
        return output_data

if __name__ == '__main__':
    import argparse
    
    result = {}
    parser = argparse.ArgumentParser()
    parser.add_argument('--hostname', help='hostname', nargs='?', default='localhost')
    parser.add_argument('--snmp_version', help='snmp version', type=str, nargs='?', default="2c")
    parser.add_argument('--snmp_community_str', help='snmp community version',  nargs='?', default='public')
    parser.add_argument('--plugin_version', help='plugin template version',  nargs='?', default='1')
    parser.add_argument('--heartbeat_required', help='Enable heartbeat for monitoring',  nargs='?', default="true")
    args = parser.parse_args()
    
    try:
        parser = HardwareParser(args.hostname, args.snmp_version, args.snmp_community_str)
        output = parser.getData()
        result = output['data']
        result['units'] = output['units']
    except Exception as e:
        result['status'] = 0
        result['msg'] = traceback.format_exc()
    
    result['plugin_version'] = args.plugin_version
    result['heartbeat_required'] = args.heartbeat_required
    print(json.dumps(result))