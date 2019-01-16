#!/usr/bin/python

"""
Author :  Vijay, Zoho Corp
Language:  Python
Tested in Ubuntu
"""

import os
import json
import psutil

# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"


class iNodeMon():

    metrics = None
    units = {}

    def __init__(self):
        self.metrics = {}

    def _get_metrics(self):
        inode_files = 0
        inode_free = 0
        total_inode_files = 0
        total_inode_free = 0

        self.metrics['plugin_version'] = PLUGIN_VERSION
        self.metrics['heartbeat_required'] = HEARTBEAT

        for part in psutil.disk_partitions(True):
            if part.fstype == 'tmpfs':
               inode_stats = self.__get_inode_stats(part.mountpoint)
               inode_files += inode_stats.f_files
               inode_free += inode_stats.f_ffree

               inode_use_pct = 0
               inode_used = inode_files - inode_free
               self.metrics[part.mountpoint+'_inode_total'] = inode_files
               self.metrics[part.mountpoint+'_inode_used'] = inode_used
               self.metrics[part.mountpoint+'_inode_free'] = inode_free
               if inode_files > 0:
                  inode_use_pct =  "{:.2f}".format((inode_used * 100.0) / inode_files )
               self.metrics[part.mountpoint + '_inode_use_percent'] = inode_use_pct
               self.units[part.mountpoint+'_inode_use_percent'] = "%"
               self.metrics["units"] = self.units
               total_inode_files += inode_files
               total_inode_free += inode_free
        total_inode_used = total_inode_files - total_inode_free
        self.metrics['total_inode_files'] = total_inode_files;
        self.metrics['total_inode_free'] = total_inode_free;
        self.metrics['total_inode_used'] = total_inode_used;
        if(total_inode_files):
          total_inode_use_pct =  "{:.2f}".format((total_inode_used * 100.0) / inode_files )
        self.metrics['total_inode_use_pct'] = total_inode_use_pct
        self.units['total_inode_use_pct'] = '%'
        self.metrics['units'] = self.units
        return self.metrics

    def __get_inode_stats(self, path):
        return os.statvfs(path)

if __name__ == '__main__':

    mon = iNodeMon()
    metrics = mon._get_metrics()
    print json.dumps(metrics)

