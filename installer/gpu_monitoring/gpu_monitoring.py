#!/usr/bin/python3
import re
import json
import argparse
import gpustat
import subprocess

PLUGIN_VERSION = 1  ###Mandatory -If any changes in the plugin metrics, increment the version number.

HEARTBEAT = "true"  ###Mandatory -Set this to true to receive alerts when there is no data from the plugin within the poll interval
# METRIC_UNITS = { "GPU":"%","Memory":"MB","Utilization":"%"} ###OPTIONAL - The unit defined here will be displayed in the Dashboard.


class Plugin:
    def __init__(self):
        self.data = {}
        self.data["plugin_version"] = PLUGIN_VERSION
        self.data["heartbeat_required"] = HEARTBEAT
        self.data["units"] = {}  # METRIC_UNITS   ###Comment this line, if you haven't defined METRIC_UNITS

    def rem(self, smi):
        while "" in smi:
            smi.remove("")
        return smi

    def getDriverInfo(self):
        try:
            pattern = "Driver Version"
            smi = subprocess.check_output("nvidia-smi", shell=True).decode().split("\n")
            for line in smi:
                if re.search(pattern, line):
                    info = self.rem(line.replace("|", "").split("    "))
            for driver in info:
                if "Driver Version:" in driver:
                    self.data["Driver Version"] = "v" + driver.split(":")[-1]
                elif "CUDA Version:" in driver:
                    self.data["CUDA Version"] = "v" + driver.split(":")[-1]
                    
        except Exception as e:
            self.data["status"] = 0  ###OPTIONAL-In case of any errors,Set 'status'=0 to mark the plugin as down.
            self.data["msg"] = str(e)  ###OPTIONAL- Set the custom message to be displayed in the "Errors" field of Log Report


    def getData( self ):  ### The getData method contains Sample data. User can enhance the code to fetch Original data
        try:  ##set the data object based on the requirement
            output = gpustat.GPUStatCollection.new_query()
            memory_usage = []
            memory_total = []

            for row in output:

                self.data[f"GPU{row.index}"] = str(f"{row.name}")
                self.data[f"GPU{row.index} Total Memory"] = str(f"{str(row.memory_total)} MB")
                self.data[f"GPU{row.index} - Memory"] = float(row.memory_used)
                self.data[f"GPU{row.index} - Temperature"] = row.temperature
                self.data[f"GPU{row.index} - Power Draw"] = row.power_draw
                self.data[f"GPU{row.index} - Power Limit"] = str(row.power_limit) + " W"
                self.data["units"][f"GPU{row.index} - Memory"] = "MB"
                self.data[f"GPU{row.index} - Utilization"] = float(row.utilization)
                self.data["units"][f"GPU{row.index} - Utilization"] = "%"
                self.data["units"][f"GPU{row.index} - Temperature"] = "C"
                self.data["units"][f"GPU{row.index} - Power Draw"] = "W"
                # print(row)
                memory_usage.append(float(row.memory_used))
                memory_total.append(float(row.memory_total))
                
            self.data["Average Memory - Percentage"] = round(sum(memory_usage) * 100 / sum(memory_total), 2)
            self.data["units"]["Average Memory - Percentage"] = "%"

            self.getDriverInfo()

            pass
        except Exception as e:
            self.data["status"] = 0  ###OPTIONAL-In case of any errors,Set 'status'=0 to mark the plugin as down.
            self.data["msg"] = str(e)  ###OPTIONAL- Set the custom message to be displayed in the "Errors" field of Log Report
            
        return self.data


if __name__ == "__main__":
    plugin = Plugin()
    data = plugin.getData()
    print(json.dumps(data, indent=4, sort_keys=True))  ###Print the output in JSON format
