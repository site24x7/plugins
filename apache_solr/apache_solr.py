#!/usr/bin/python

'''
Created on 24-August-2018

@author: giri
'''


import six.moves.urllib.request as urlconnection
import traceback
import json
import os
import sys

SOLR_HOST = "127.0.0.1" #solr host
SOLR_PORT = "8983" #solr port
SOLR_METRICS_URL = "solr/admin/cores?action=status"

PLUGIN_VERSION = "1"

CORES = [] #mention the core names as needed

HEARTBEAT_REQUIRED = "true"

final_dict = {}



def final_parser(func):
    def wrapper():
        try:
            result = func()
            if not result is None:
                result_json = json.loads(result)
                final_dict["status"] = 1
                final_dict["num_of_cores"] = len(result_json["status"])
                for core in result_json["status"]:
                    if CORES and not core in CORES:
                        continue
                    elif CALC_CORES and len(CALC_CORES) > 5 and not core in CALC_CORES:
                        continue
                    if not core in CALC_CORES:
                        CALC_CORES.append(core)
                    final_dict["{}_size_in_bytes".format(core)] = result_json["status"][core]["index"]["sizeInBytes"]
                    final_dict["{}_num_docs".format(core)] = result_json["status"][core]["index"]["numDocs"]
                    final_dict["{}_del_docs".format(core)] = result_json["status"][core]["index"]["deletedDocs"]
                    final_dict["{}_index_heap_bytes".format(core)] = result_json["status"][core]["index"]["indexHeapUsageBytes"]
                if CALC_CORES:
                    with open(CALC_CORES_FILE_NAME, "w") as fp:
                        fp.write(json.dumps(CALC_CORES))
        except Exception as e:
            final_dict["status"] = 0
            final_dict["msg"] = repr(e)
    return wrapper



def log_decorator(func):
    def wrapper():
        result = None
        try:
            result = func()
            if not result is str:
                result = result.decode()
        except Exception as e:
            final_dict["status"] = 0
            final_dict["msg"] = repr(e)
        return result
    return wrapper


@final_parser
@log_decorator
def start_data_collection():
    request_obj = urlconnection.Request("http://{}:{}/{}".format(SOLR_HOST, SOLR_PORT, SOLR_METRICS_URL))
    response = urlconnection.urlopen(request_obj)
    resp_data = response.read()
    return resp_data


def pre_work():
    global CALC_CORES
    global CALC_BOOL_FLAG
    global CALC_CORES_FILE_NAME
    CALC_CORES_FILE_NAME = os.path.join(os.path.dirname(os.path.realpath(sys.argv[0])), "calc_cores.json")
    content = None
    if os.path.isfile(CALC_CORES_FILE_NAME):
        with open(CALC_CORES_FILE_NAME, "r") as fp:
            content = fp.read()
    CALC_CORES = json.loads(content) if not content in [None, ""] else []
    CALC_BOOL_FLAG = True if CALC_CORES else False


if not CORES:
    pre_work()
start_data_collection()
final_dict["plugin_version"] = PLUGIN_VERSION
final_dict["heartbeat_required"] = HEARTBEAT_REQUIRED
print(json.dumps(final_dict))
