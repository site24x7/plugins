#!/usr/bin/python3

import json
import os
import hashlib

PLUGIN_VERSION="1"

HEARTBEAT="true"

FILE_PATH=""

HASH_TYPE=""
hash_storage_path=""
metric_units={"file_size":"bytes","hash_value_changed":"bool"}
def get_data(FILE_PATH,HASH_TYPE):
    data={}
    data['plugin_version']=PLUGIN_VERSION
    data['heartbeat_required']=HEARTBEAT
    data['units']=metric_units
    try:
        fname=FILE_PATH.split('/')
        hash_value_changed=0
        previous_hash_value=""
        if HASH_TYPE=="blake2b":
            data["hashing"]=hashlib.blake2b(open(FILE_PATH,'rb').read()).hexdigest()
        elif HASH_TYPE=="blake2s":
            data["hashing"]=hashlib.blake2s(open(FILE_PATH,'rb').read()).hexdigest()
        elif HASH_TYPE=="md5":
            data["hashing"]=hashlib.md5(open(FILE_PATH,'rb').read()).hexdigest()
        elif HASH_TYPE=="sha1":
            data["hashing"]=hashlib.sha1(open(FILE_PATH,'rb').read()).hexdigest()
        elif HASH_TYPE=="sha224":
            data["hashing"]=hashlib.sha224(open(FILE_PATH,'rb').read()).hexdigest()
        elif HASH_TYPE=="sha256":
            data["hashing"]=hashlib.sha256(open(FILE_PATH,'rb').read()).hexdigest()
        elif HASH_TYPE=="sha384":
            data["hashing"]=hashlib.sha384(open(FILE_PATH,'rb').read()).hexdigest()
        elif HASH_TYPE=="sha3_224":
            data["hashing"]=hashlib.sha3_224(open(FILE_PATH,'rb').read()).hexdigest()
        elif HASH_TYPE=="sha3_256":
            data["hashing"]=hashlib.sha3_256(open(FILE_PATH,'rb').read()).hexdigest()
        elif HASH_TYPE=="sha3_384":
            data["hashing"]=hashlib.sha3_384(open(FILE_PATH,'rb').read()).hexdigest()
        elif HASH_TYPE=="sha3_512":
            data["hashing"]=hashlib.sha3_512(open(FILE_PATH,'rb').read()).hexdigest()
        elif HASH_TYPE=="sha512":
            data["hashing"]=hashlib.sha3_512(open(FILE_PATH,'rb').read()).hexdigest()

        name,extension=os.path.splitext(FILE_PATH)
        if(os.path.exists(hash_storage_path)):
        	file=open(hash_storage_path)
        	previous_hash_value=file.readlines()
        	if len(previous_hash_value)==0:
        		previous_hash_value=""
        	else:
        		previous_hash_value=previous_hash_value[0].strip()
        	file.close()
        if ((previous_hash_value != "") and (previous_hash_value!=data["hashing"])):
        	hash_value_changed=1
        if previous_hash_value=="" or previous_hash_value!=data["hashing"]:
        	file=open(hash_storage_path,'w+')
        	file.write(data["hashing"])
        	file.close()
        data["file_type"]=extension
        data["file_size"]=os.stat(FILE_PATH).st_size
        data["hash_value_changed"]=hash_value_changed
    except Exception as e:
        data["status"]=0
        data["msg"]=str(e)
    return data

if __name__=="__main__":
    import argparse
    parser=argparse.ArgumentParser()
    parser.add_argument('--filepath',help="file to monitor",type=str)
    parser.add_argument('--hashtype',help="type of the hash",type=str)
    parser.add_argument('--hash_storage_path',help="Storage Path for storing hash values ",type=str)
    args=parser.parse_args()

    if args.filepath:
        FILE_PATH=args.filepath
    if args.hashtype:
        HASH_TYPE=args.hashtype
    if args.hash_storage_path:
    	hash_storage_path=args.hash_storage_path
    HASH_TYPE=HASH_TYPE.lower()
    data=get_data(FILE_PATH,HASH_TYPE)
    print(json.dumps(data,indent=4))    
