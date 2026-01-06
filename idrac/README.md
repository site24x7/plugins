# IDRAC Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- The plugin requires the `puresnmp` Python library. Install it using:

```bash
pip install puresnmp
```

### Plugin Installation  

- Create a directory named `idrac`.
  
```bash
mkdir idrac
cd idrac/
```
      
- Download below files and place it under the "idrac" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/master/idrac/idrac.py && sed -i "1s|^.*|#! $(which python3)|" idrac.py
wget https://raw.githubusercontent.com/site24x7/plugins/master/idrac/idrac.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python3 idrac_test.py --hostname "ip-address" --snmp_version "2c" --snmp_community_str "public"
```

- Provide your idrac configurations in idrac.cfg file.

```bash
[idrac]
hostname = "ip-address"
snmp_version = "2c" 
snmp_community_str = "public"
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "idrac" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv idrac /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "idrac" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

## iDRAC Monitoring Plugin Metrics

### Summary

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| Total Batteries             | Total number of battery units detected                                 |
| Total CPU                   | Total number of CPU sockets populated                                  |
| Total Active Cores          | Total number of active/enabled CPU cores across all processors         |
| Total Cores                 | Total number of physical CPU cores across all processors               |
| Total Threads               | Total number of threads supported across all processors                |
| Total Fans                  | Total number of fan units detected                                     |
| Total Memory                | Total number of memory modules installed                               |
| Total Memory Size           | Total memory capacity installed in the system (KB)                     |
| Total Physical Disks        | Total number of physical disk drives detected                          |
| Total Current Probes        | Total number of current monitoring probes                              |
| Total Voltage Probes        | Total number of voltage monitoring probes                              |
| Total Thermal Sensors       | Total number of temperature sensors detected                           |
| Total Virtual Disks         | Total number of virtual disks/RAID volumes configured                  |

### CPU

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| CPU_Index                   | Unique identifier for the CPU socket                                   |
| CPU_State                   | Current state of the CPU                                               |
| CPU_Status                  | Health status of the CPU                                               |
| CPU_Total_Cores             | Total number of physical cores available in the CPU                    |
| CPU_Cores_Enabled_Count     | Number of cores currently enabled and active                           |
| CPU_Threads                 | Total number of threads supported by the CPU                           |
| CPU_Brand_Name              | Manufacturer and model name of the CPU                                 |
| CPU_Physical_Socket_Location| Physical socket location on the motherboard                            |
| CPU_Maximum_CPU_Speed       | Maximum clock speed of the CPU (MHz)                                   |
| CPU_Current_CPU_Speed       | Current operating clock speed of the CPU (MHz)                         |

### Memory

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| Memory_State                | Current state of the memory module                                     |
| Memory_Status               | Health status of the memory module                                     |
| Memory_Type                 | Type of memory module |
| Memory_Size                 | Size of the memory module (KB)                                         |
| Memory_Speed                | Operating speed of the memory module (MHz)                             |

### Physical_Disk

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| PDisk_State                 | Current state of the physical disk                                     |
| PDisk_Status                | Health status of the physical disk                                     |
| PDisk_Size                  | Total capacity of the physical disk (MB)                               |
| PDisk_Type                  | Type of physical disk |
| PDisk_Used_Space            | Amount of used space on the disk (MB)                                  |
| PDisk_Free_Space            | Amount of free space available on the disk (MB)                        |
| PDisk_Security_Status       | Security and encryption status of the disk                             |
| PDisk_Block_Size            | Block size used by the disk (Bytes)                                    |

### Virtual_Disk

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| VDisk_State                 | Current state of the virtual disk                                      |
| VDisk_Status                | Health status of the virtual disk                                      |
| VDisk_Size                  | Total capacity of the virtual disk (MB)                                |
| VDisk_Type                  | RAID type or configuration of the virtual disk |
| VDisk_Block_Size            | Block size used by the virtual disk (Bytes)                            |
| VDisk_Secured               | Indicates if the virtual disk is encrypted/secured                     |
| VDisk_Operational_State     | Current operational state of the virtual disk                          |

### Thermal_Sensor

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| Thermal_Sensor_State        | Current state of the temperature sensor                                |
| Thermal_Sensor_Status       | Health status of the temperature sensor                                |
| Temperature_Reading         | Current temperature reading from the sensor (°C)                       |

### Fan

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| Fan_Status                  | Health status of the fan unit                                          |
| Current_RPM                 | Current rotational speed of the fan (rpm)                              |

### Battery

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| Battery_Index               | Unique identifier for the battery unit                                 |
| Battery_State               | Current state of the battery                                           |
| Battery_Status              | Health status of the battery                                           |
| Battery_Charge_Level        | Current charge level of the battery                                    |
| Battery_Location            | Physical location of the battery on the system                         |

### Current

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| Current                     | Current draw measured by the probe (Ampere)                            |

### Voltage

| **Metric Name**             | **Description**                                                        |
|-----------------------------|------------------------------------------------------------------------|
| Voltage                     | Voltage level measured by the probe (Volts)                            |


## Sample Image

<img width="1641" height="960" alt="image" src="https://github.com/user-attachments/assets/dcd66979-d022-42f7-bb04-a12dbf9317f9" />
