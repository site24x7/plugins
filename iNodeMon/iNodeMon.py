#!/usr/bin/python

"""

__author__ = Vijay, Zoho Corp
Language = Python

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

        self.metrics['plugin_version'] = PLUGIN_VERSION
        self.metrics['heartbeat_required'] = HEARTBEAT

        for part in psutil.disk_partitions(all=False):
            inode_stats = self.__get_inode_stats(part.mountpoint)
            inode_files += inode_stats.f_files
            inode_free += inode_stats.f_ffree

        inode_use_pct = 0
        inode_used = inode_files - inode_free
        self.metrics['inode_total'] = inode_files
        self.metrics['inode_used'] = inode_used
        self.metrics['inode_free'] = inode_free
        if inode_files > 0:
            inode_use_pct =  "{:.2f}".format((inode_used * 100.0) / inode_files )
        self.metrics['inode_use_percent'] = inode_use_pct
        self.units['inode_use_percent'] = "%"

        self.metrics["units"] = self.units
        return self.metrics

    def __get_inode_stats(self, path):
        return os.statvfs(path)

if __name__ == '__main__':

    mon = iNodeMon()
    metrics = mon._get_metrics()
    print json.dumps(metrics)
