
import json
import subprocess
import re
import traceback
import os
import argparse

PLUGIN_VERSION = 1
HEARTBEAT = True
METRICS_UNITS = {"Mounted Shares": "shares", "Unmounted Shares": "shares"}

TABS = {"tabs": {"Size Stats": {"order": "1", "tablist": ["Size"]}}}
# Get the current file path
current_file_path = os.path.dirname(os.path.abspath(__file__))


class cifs:

    def __init__(self, plugin_version=PLUGIN_VERSION):
        self.maindata = {}
        self.maindata["plugin_version"] = plugin_version
        self.maindata["heartbeat_required"] = HEARTBEAT
        self.maindata["units"] = METRICS_UNITS
        self.mounts = {}
        self.mount_points = []

    def execute_cmd(self, command):

        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result

    def convert_to_gb(self, value, unit):

        if unit == "G":
            return value
        elif unit == "M":
            return round(value / 1024, 2)
        elif unit == "T":
            return round(value * 1024, 2)
        elif unit == "K":
            return round(value / (1024 * 1024), 2)
        elif unit == "B":
            return round(value / (1024 * 1024 * 1024), 2)
        else:
            return round(value / (1024 * 1024 * 1024), 2)

    def rem(self, mount_data):
        while "" in mount_data:
            mount_data.remove("")
        return mount_data

    def mount_status(self):

        global file_exists, file_written, mounted, unmounted
        mounted, unmounted = "", ""
        file_written = False
        file_exists = False
        mount_status_file = os.path.join(current_file_path, "mount_points.txt")

        if os.path.isfile(mount_status_file):
            try:
                f = open(mount_status_file, "r")
                mount_check = f.read().split("\n")
                if "" in mount_check:
                    mount_check = self.rem(mount_check)
                file_exists = True
            except:
                pass

            set1 = set(mount_check)
            set2 = set(self.mount_points)

            mounted = set1.intersection(set2)
            unmounted = list(set1 - set2)

            for i in mounted:
                self.maindata[i + " State"] = "Mounted"

            for i in unmounted:
                self.maindata[i + " State"] = "Unmounted"

            self.maindata["Mounted Shares"] = len(mounted)
            self.maindata["Unmounted Shares"] = len(unmounted)
            self.maindata["Shares Monitored"] = str(len(mount_check)) + " Shares"

            try:
                if len(list(set2 - set1)) != 0:
                    updated_mounts = set1.union(set2)
                    f = open(mount_status_file, "w")
                    f.write("\n".join(updated_mounts))
                    f.close()
                    self.maindata["Shares Monitored"] = len(updated_mounts)

            except:
                pass

        else:
            try:
                f = open(mount_status_file, "a")
                f.write("\n".join(self.mount_points))
                f.close()
                file_written = True
                for i in self.mount_points:
                    self.maindata[i + " State"] = "Mounted"
            except:
                pass

            self.maindata["Mounted Shares"] = len(self.mount_points)
            self.maindata["Unmounted Shares"] = 0
            self.maindata["Shares Monitored"] = str(len(self.mount_points)) + " Shares"

    def get_mounts(self):

        try:
            mount_cmd = ["mount", "-l", "-t", "cifs"]
            result = subprocess.run(
                mount_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )
            cifs_mount_data = result.stdout.decode().split("\n")

            for cifs_mount in cifs_mount_data:
                mount_data = cifs_mount.split(" ")
                mount_data = self.rem(mount_data)
                if len(mount_data) != 0:
                    for i in mount_data:
                        if "vers" in i:
                            info = i[1:-1].split(",")
                            break
                    if "rw" in info[0]:
                        self.maindata[mount_data[2] + " Permission"] = "read/write"
                    elif "ro" in info[0]:
                        self.maindata[mount_data[2] + " Permission"] = "read only"
                    if "vers" in info[2]:
                        self.maindata["Cifs Version"] = info[2].split("=")[-1]

                    self.mounts[mount_data[2]] = mount_data[0]
                    self.mount_points.append(mount_data[2])
            self.mount_status()

            return self.mounts

        except Exception as e:
            self.maindata["status"] = 0
            self.maindata["msg"] = str(e)

    def basic_metrics(self, output, path):

        subdata = {}
        data = output.split("\n")[0].split()

        Total_Size, Used_Size, Avail_Size = data[1:4]
        percent_used = data[4].strip("%")

        if Total_Size == "0":
            Total_Size = 0.0
        else:
            Total_Size = self.convert_to_gb(float(Total_Size[:-1]), Total_Size[-1])
        if Used_Size == "0":
            Used_Size = 0.0
        else:
            Used_Size = self.convert_to_gb(float(Used_Size[:-1]), Used_Size[-1])
        if Avail_Size == "0":
            Avail_Size = 0.0
        else:
            Avail_Size = self.convert_to_gb(float(Avail_Size[:-1]), Avail_Size[-1])

        subdata["name"] = path
        subdata["disk_usage_percentage"] = percent_used
        subdata["total_size_gb"] = Total_Size
        subdata["used_size_gb"] = Used_Size
        subdata["avail_size_gb"] = Avail_Size

        return subdata

    def metriccollector(
        self,
    ):

        try:

            cifs_cmd_1 = ["df", "-hP"]
            result = self.execute_cmd(cifs_cmd_1)

            if result.returncode == 0:
                result = result.stdout.decode().split("\n")
            else:
                self.maindata["msg"] = result.stderr.decode()
                self.maindata["status"] = 0

            cifs_mounts = self.get_mounts()
            if cifs_mounts == {}:
                self.maindata["status"] = 0
                self.maindata["msg"] = "No cifs shares found."

            cifs_mount_data = []

            for i in unmounted:
                basic_data = {}
                basic_data["name"] = i
                basic_data["status"] = 0
                cifs_mount_data.append(basic_data)

            for key, values in cifs_mounts.items():
                for i in result:
                    if key in i:
                        output_data = i
                basic_data = self.basic_metrics(output_data, key)

                if file_exists:
                    if key in mounted:
                        basic_data["status"] = 1
                    if key in unmounted:
                        basic_data["status"] = 0
                elif file_written:
                    basic_data["status"] = 1
                cifs_mount_data.append(basic_data)

            self.maindata["Size"] = cifs_mount_data
            mount_from = {}

            for i, j in cifs_mounts.items():
                mount_from[i + " Mounted From"] = j

            self.maindata.update(mount_from)
            self.maindata.update(TABS)

            if "status" in self.maindata:
                if self.maindata["status"] == 0:
                    return self.maindata

        except Exception as e:
            self.maindata["status"] = 0
            self.maindata["msg"] = str(e)

        return self.maindata

def run(param):
    plugin_version = str(param.get("plugin_version")).strip('"') if param else PLUGIN_VERSION
    cifs_instance = cifs(plugin_version)
    result = cifs_instance.metriccollector()
    return result


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--plugin_version", help="plugin version", default=PLUGIN_VERSION
    )
    args = parser.parse_args()
    cifs = cifs(args.plugin_version)
    result = cifs.metriccollector()
    print(json.dumps(result, indent=True))
