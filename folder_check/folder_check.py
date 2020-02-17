#!/usr/bin/env python

import json,os,time

PLUGIN_VERSION="1"

HEARTBEAT="true"

#set this value to 1 if the file count needs to be recursive
INCLUDE_RECURSIVE_FILES=None

FOLDER_NAME="/"

def get_data():
    folder_checks_data = {}
    folder_checks_data['plugin_version'] = PLUGIN_VERSION
    folder_checks_data['heartbeat_required'] = HEARTBEAT
    try:
        if INCLUDE_RECURSIVE_FILES:
            file_count = sum([len(files) for r, d, files in os.walk(FOLDER_NAME)])
            directory_count = sum([len(d) for r, d, files in os.walk(FOLDER_NAME)])
        else:
            path, dirs, files = next(os.walk(FOLDER_NAME))
            file_count = len(files)
            directory_count = len(dirs)
        folder_checks_data['file_count'] = file_count
        folder_checks_data['directory_count'] = directory_count
        
    except Exception as e:
        folder_checks_data['status']=0
        folder_checks_data['msg']=str(e)
    return folder_checks_data

if __name__ == "__main__":
    data = get_data()
    print(json.dumps(data,indent=4))
