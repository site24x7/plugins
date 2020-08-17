#!/usr/bin/python

import gnupg
import datetime
import json
import argparse

class pgp_expiry_monitoring:
    def __init__(self):
        self.data = {}
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--keys_to_check', help="public keys to check for expiry", nargs="?")
        parser.add_argument('--key_server', help ="keyserver name", nargs="?", default='keyserver.ubuntu.com')
        parser.add_argument('--gpg_location', help ="gpg location", nargs="?", default='/home/local/.gnupg')
        parser.add_argument('--plugin_version', help='plugin_version', type=int,  nargs='?', default=1)
        parser.add_argument('--heartbeat', help='is heartbeat enabled', type=bool, nargs='?', default=True)
        
        args = parser.parse_args()
        
        self.keys_to_check = args.keys_to_check
        self.key_server = args.key_server
        self.gpg_location = args.gpg_location
        self.data['plugin_version'] = args.plugin_version
        self.data['heartbeat_required'] = args.heartbeat
    
    def _check_expiry_(self):
        cur_date = datetime.datetime.utcnow()
        gpg = gnupg.GPG(gnupghome=self.gpg_location)
        public_keys = gpg.list_keys()        
        keyset = self.keys_to_check.split(',')
        for key in public_keys:
            keyid = key["keyid"] ## Public Key
            if keyid in keyset :
                expires = key["expires"] 
                if expires:
                    fl_expires = datetime.datetime.fromtimestamp( float(expires) )
                    days_to_expire = int((fl_expires - cur_date).days)
                    self.data[keyid] = days_to_expire
                else:
                    self.data[keyid] = -1
            
        return self.data
    
    
if __name__ == '__main__':
    mon = pgp_expiry_monitoring()
    result = mon._check_expiry_()
    print(json.dumps(result, indent=4, sort_keys=True))
