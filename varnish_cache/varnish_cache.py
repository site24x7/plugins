#!/usr/bin/python

"""
Site24x7 Varnish Plugin

author: selvakumar.cs
Edited to support all types of data from varnish cache

"""
import importlib
import json
import os
import subprocess
import re

# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

# Config Section:
VARNISH_INSTANCE = ""

# Mention the units of your metrics . If any new metrics are added, make an entry here for its unit if needed.
METRICS_UNITS_V3 = {'cache_hit': 'units', 'cache_miss': 'units', 'n_wrk_create': 'units', 'n_wrk_lqueue': 'units',
                 'sess_pipe_overflow': 'units'}

METRICS_UNITS_V4 = {'cache_hit': 'count', 'cache_miss': 'count','cache_hitpass': 'count','cache_hitmiss': 'count', 'threads_created': 'count', 'threads_limited': 'count', 'threads': 'count', 'threads_destroyed': 'count', 'threads_failed': 'count', 'thread_queue_len': 'count', 'backend_busy': 'count', 'backend_fail': 'count', 'backend_reuse': 'count', 'backend_recycle': 'count', 'backend_retry': 'count', 'ws_session_overflow': 'count', 'ws_backend_overflow': 'count', 'ws_client_overflow': 'count', 'ws_session_overflow': 'count', 'mempool_creat': 'count', 'mempool_destroy': 'count', 'mempool_locks': 'count', 'mempool_dbg_busy': 'count', 'mempool_dbg_try_fail': 'count', 'management_uptime': 'count', 'management_child_start': 'count', 'management_child_exit': 'count', 'management_child_stop': 'count', 'management_child_died': 'count', 'management_child_dump': 'count', 'management_child_panic': 'count', 'sess_conn': 'count', 'sess_fail': 'count'}

METRICS_UNITS_V4_METRIC= {'MAIN.cache_hit': 'cache_hit', 'MAIN.cache_miss': 'cache_miss','MAIN.cache_hitpass': 'cache_hitpass','MAIN.cache_hitmiss': 'cache_hitmiss', 'MAIN.threads_created': 'threads_created', 'MAIN.threads_limited': 'threads_limited', 'MAIN.threads': 'threads', 'MAIN.threads_destroyed': 'threads_destroyed', 'MAIN.threads_failed': 'threads_failed', 'MAIN.thread_queue_len': 'thread_queue_len', 'MAIN.backend_busy': 'backend_busy', 'MAIN.backend_fail': 'backend_fail', 'MAIN.backend_reuse': 'backend_reuse', 'MAIN.backend_recycle': 'backend_recycle', 'MAIN.backend_retry': 'backend_retry', 'MAIN.ws_session_overflow': 'ws_session_overflow', 'MAIN.ws_backend_overflow': 'ws_backend_overflow', 'MAIN.ws_client_overflow': 'ws_client_overflow', 'MAIN.ws_session_overflow': 'ws_session_overflow', 'LCK.mempool.creat': 'mempool_creat', 'LCK.mempool.destroy': 'mempool_destroy', 'LCK.mempool.locks': 'mempool_locks', 'LCK.mempool.dbg_busy': 'mempool_dbg_busy', 'LCK.mempool.dbg_try_fail': 'mempool_dbg_try_fail', 'MGT.uptime': 'management_uptime', 'MGT.child_start': 'management_child_start', 'MGT.child_exit': 'management_child_exit', 'MGT.child_stop': 'management_child_stop', 'MGT.child_died': 'management_child_died', 'MGT.child_dump': 'management_child_dump', 'MGT.child_panic': 'management_child_panic','MAIN.sess_conn': 'sess_conn','MAIN.sess_fail': 'sess_fail'}

class VarnishCache(object):
    def __init__(self, config):
        self.configurations = config
        self.connection = None

    def metric_collector(self):
        try:
            data = {
                'plugin_version': PLUGIN_VERSION, 'heartbeat_required': HEARTBEAT
            }
        
            varnish_command = ['varnishstat', '-1', '-j']

            if VARNISH_INSTANCE != "":
                varnish_command.append('-n')
                varnish_command.append(VARNISH_INSTANCE)    

            output = subprocess.check_output(varnish_command)
            j = json.loads(output.decode())
            varnish_version = self.get_major_version()
            metric_value=j["counters"]
            if int(varnish_version) < 4:
                data['cache_hit'] = j['cache_hit']['value']
                data['cache_miss'] = j['cache_miss']['value']
                data['n_wrk_create'] = j['n_wrk_create']['value']
                data['n_wrk_lqueue'] = j['n_wrk_lqueue']['value']
                data['sess_pipe_overflow'] = j['sess_pipe_overflow']['value']
                data['units'] = METRICS_UNITS_V3
            else:
                for key,value in metric_value.items():
                    if key in METRICS_UNITS_V4_METRIC:
                        data[METRICS_UNITS_V4_METRIC[key]]=value['value']
                data['units'] = METRICS_UNITS_V4
        except Exception as e:
            data["msg"]=str(e)
            data["status"]=0    
        return data
    def get_major_version(self):
        output = subprocess.check_output(['varnishd', '-V'], stderr=subprocess.STDOUT).decode('utf-8')
        version = re.search('varnish-(.*) ', output)
        return version.group(1)[0]

if __name__ == "__main__":
    configurations = {}
    varnish_plugins = VarnishCache(configurations)
    result = varnish_plugins.metric_collector()
    print(json.dumps(result, indent=4, sort_keys=True))

