#!/usr/bin/env python

import json,os,time

METRIC_UNITS={
    "directory_size":"MB"
}


PLUGIN_VERSION="1"

HEARTBEAT="true"

#set this value to 1 if the file count needs to be recursive
INCLUDE_RECURSIVE_FILES=None

FOLDER_NAME="/"

FILE_THRESHOLD_COUNT=10

DIR_THRESHOLD_COUNT=10
    
def get_data(FOLDER_NAME):
    folder_checks_data = {}
    size = 0
    folder_checks_data['plugin_version'] = PLUGIN_VERSION
    folder_checks_data['heartbeat_required'] = HEARTBEAT
    folder_checks_data['units'] = METRIC_UNITS
    try:
        if os.path.exists(FOLDER_NAME):
            
            if INCLUDE_RECURSIVE_FILES:
                file_count = sum([len(files) for r, d, files in os.walk(FOLDER_NAME)])
                directory_count = sum([len(d) for r, d, files in os.walk(FOLDER_NAME)])
            else:
                path, dirs, files = next(os.walk(FOLDER_NAME))
                file_count = len(files)
                directory_count = len(dirs)
            folder_checks_data['file_count'] = file_count
            folder_checks_data['directory_count'] = directory_count
        
            for path, dirs, files in os.walk(FOLDER_NAME):
                for f in files:
                    fp = os.path.join(path, f)
                    # skip if it is symbolic link
                    if os.path.exists(f) and not os.path.islink(fp):
                        size += os.path.getsize(fp)
            folder_checks_data['directory_size']=round(size/float(1000*1000),2)
        
            #logical conditions
            if file_count > FILE_THRESHOLD_COUNT:
               folder_checks_data['status']=0
               folder_checks_data['msg']='File Count Exceeds the threshold'
               return folder_checks_data

            if directory_count > DIR_THRESHOLD_COUNT:
                folder_checks_data['status']=0
                folder_checks_data['msg']='Directory Count Exceeds the threshold'    
                return folder_checks_data

            if file_count > FILE_THRESHOLD_COUNT and directory_count > DIR_THRESHOLD_COUNT:
                folder_checks_data['status']=0
                folder_checks_data['msg']='File / Directory Counts Exceeded the threshold'
        else:
            folder_checks_data['msg']="Folder name does not exist" 
    except Exception as e:
        folder_checks_data['status']=0
        folder_checks_data['msg']=str(e)
    return folder_checks_data

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--folder_name', help="folder to monitor",type=str)
    parser.add_argument('--include_recursive_files',help="include recursive file(s) / directory(s)",type=str)
    parser.add_argument('--file_count_threshold',help="threshold value for file count",type=int)
    parser.add_argument('--directory_count_threshold',help="threshold value for directory count",type=int)
    
    args = parser.parse_args()

    if args.folder_name:
        FOLDER_NAME = args.folder_name
    if args.include_recursive_files:
        INCLUDE_RECURSIVE_FILES = args.include_recursive_files
    if args.file_count_threshold:
        FILE_THRESHOLD_COUNT = args.file_count_threshold
    if args.directory_count_threshold:
        DIR_THRESHOLD_COUNT = args.directory_count_threshold

    data = get_data(FOLDER_NAME)
    print(json.dumps(data,indent=4))
