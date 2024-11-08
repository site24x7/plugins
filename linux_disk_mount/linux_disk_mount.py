#!/usr/bin/python3
import json
import subprocess
import os

PLUGIN_VERSION = 1
HEARTBEAT = True
INFO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "info.txt")
METRICS_UNITS = {
    "Total_No_Of_Disk_Partitions": "count",
    "Total_Disk_Capacity": "GB",
    "Total_Used_Disk": "GB",
    "Total_Free_Disk": "GB",
    "File_System": {
        "Free_Size": "GB",
        "Used_Size": "GB",
        "Total_Size": "GB",
        "Used_Utilization": "%",
        "Free_Utilization": "%"
    }
}

class DiskPartitionTracking:
    def __init__(self):
        self.result = {
            "plugin_version": PLUGIN_VERSION,
            "heartbeat_required": HEARTBEAT,
            "File_System": []
        }
        self.total_disk_capacity = 0.0
        self.total_used_disk = 0.0
        self.total_free_disk = 0.0
        self.saved_filesystems = self.load_info_file()

    def load_info_file(self):
        """Load saved file system names from info.txt. Create the file if it does not exist."""
        if not os.path.exists(INFO_FILE):
            open(INFO_FILE, 'w').close()
            return []
        else:
            with open(INFO_FILE, 'r') as f:
                return [line.strip() for line in f.readlines()]

    def save_info_file(self, current_filesystems):
        """Append new file system names to info.txt if they don't already exist."""
        with open(INFO_FILE, 'a') as f:
            for fs in current_filesystems:
                if fs not in self.saved_filesystems:
                    f.write(f"{fs}\n")
                    self.saved_filesystems.append(fs)

    def metriccollector(self):
        try:
            df_output = subprocess.check_output(['df', '-h']).decode('utf-8').splitlines()
            current_filesystems = []

            for line in df_output[1:]:
                columns = line.split()
                
                filesystem = f"{columns[0]}-{' '.join(columns[5:])}"
                current_filesystems.append(filesystem)
                size = columns[1]
                used = columns[2]
                available = columns[3]
                used_percent = columns[4]

                size_gb = self.convert_to_gb(size)
                used_gb = self.convert_to_gb(used)
                available_gb = self.convert_to_gb(available)

                self.total_disk_capacity += size_gb
                self.total_used_disk += used_gb
                self.total_free_disk += available_gb

                used_utilization = float(used_percent.strip('%'))
                free_utilization = 100 - used_utilization

                status = 1 if size_gb > 0 else 0

                self.result["File_System"].append({
                    "name": filesystem,
                    "Free_Size": f"{available_gb:.5f}",
                    "Used_Size": f"{used_gb:.5f}",
                    "Total_Size": f"{size_gb:.5f}",
                    "Used_Utilization": f"{used_utilization:.2f}",
                    "Free_Utilization": f"{free_utilization:.2f}",
                    "status": status
                })

            for fs in self.saved_filesystems:
                if fs not in current_filesystems:
                    self.result["File_System"].append({
                        "name": fs,
                        "Free_Size": "0",
                        "Used_Size": "0",
                        "Total_Size": "0",
                        "Used_Utilization": "0",
                        "Free_Utilization": "0",
                        "status": 0
                    })

            self.save_info_file(current_filesystems)

            self.result["Total_No_Of_Disk_Partitions"] = len(current_filesystems)  
            self.result["Total_Disk_Capacity"] = f"{self.total_disk_capacity:.2f}"
            self.result["Total_Used_Disk"] = f"{self.total_used_disk:.2f}"
            self.result["Total_Free_Disk"] = f"{self.total_free_disk:.2f}"

        except Exception as e:
            self.result["msg"] = f"Error in collecting disk metrics: {e}"
            self.result["status"] = 0

    def convert_to_gb(self, size_str):
        """Convert size to GB if it is in K, M, or G."""
        if size_str[-1].isdigit(): 
            return float(size_str) / (1024 * 1024 * 1024)
        
        size = float(size_str[:-1])
        unit = size_str[-1].upper()

        if unit == 'T':
            return size * 1024 
        elif unit == 'G':
            return size  
        elif unit == 'M':
            return size / 1024
        elif unit == 'K':
            return size / (1024 * 1024) 
        else:
            return 0  

if __name__ == "__main__":
    tracker = DiskPartitionTracking()
    tracker.metriccollector()
    print(json.dumps(tracker.result, indent=4))
