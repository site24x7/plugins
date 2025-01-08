#!/usr/bin/python
'''
Created on 25-Sep-2020
Site24x7 Plugin for monitoring hping3 commands
'''

import subprocess
import re
import json
import argparse

### Pass command line params as dict keys and values. Case sensitive
config = {}
## -c --count packet count
config['c'] = 2
## -i interval count
config['i'] = 2
## -S SYN flag is set to true
config['S'] = None
## -p destination port
config['p'] = 8040


class Hping3Monitoring():
    
    def __init__(self) :
        parser = argparse.ArgumentParser()
        parser.add_argument('--host', help='kvm host to connect', nargs='?', default='localhost')
        parser.add_argument('--plugin_version', help='plugin template version', type=int,  nargs='?', default=1)
        parser.add_argument('--heartbeat', help='alert if monitor does not send data', type=bool, nargs='?', default=True)

        args = parser.parse_args()
        
        self.host = args.host
        self.heartbeat = args.heartbeat
        self.plugin_version = args.plugin_version

        self.cmd = ''
        

    def _initialize_cmd_line_params(self, config):
        self.config = config;
        self.data = {}
        self.data['host'] = self.host
        self.data['heartbeat_required'] = self.heartbeat
        self.data['plugin_version'] = self.plugin_version

        
    def _frame_command_(self):
        self.hping = 'hping3 '
        self.cmd = ''

        for _ in self.config :
            self.cmd = self.cmd + '-' + str(_) + ' '
            if self.config[_] is not None : self.cmd = self.cmd + str(self.config[_]) + ' ' 
        
        self.cmd = self.cmd + ' ' + self.host
        
        self.cmd = self.hping  + self.cmd
        output = self._execute_command_()
        self._parse_output_data_(output)
        

        
        return  self.data
    
    def _execute_command_(self):
   
        # using the Popen function to execute the, command and store the result in temp. 
        # it returns a tuple that contains the data and the error if any. 
        temp = subprocess.Popen(self.cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, close_fds=False ) 
        
        # we use the communicate function, to fetch the output 
        output = str(temp.communicate()) 
        
        output = output.strip()
        
        #splitting the output so that, we can parse them line by line 
        output = output.split("\\n")     
    
        return output 

    
    def _parse_output_data_(self, output):
        
        ignore_start_line = "--- "+str(self.host)+" hping statistic ---"
        _read_ = False
        
        # iterate through the output, line by line
        for lineno in range(0, len(output)): 
            if  not _read_ : 
                if output[lineno] == ignore_start_line :
                    _read_ = True 
                    
                    _packet_details_ = output[lineno+1]
                    _rt_details = output[lineno+2]
                                        
                    _pkt_ = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", _packet_details_)
                    _rt_ = re.findall("[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?", _rt_details)
                    
                    self.data['packets transmitted'] = _pkt_[0]
                    self.data['packets received'] = _pkt_[1]
                    self.data['packets loss'] = _pkt_[2]
                    
                    self.data['rt min'] = _rt_[0]
                    self.data['rt avg'] = _rt_[1]
                    self.data['rt max'] = _rt_[2] 
            else : pass
                
        return self.data
    
if __name__ == "__main__":

    hping3 = Hping3Monitoring()
    hping3._initialize_cmd_line_params(config)
    result = hping3._frame_command_()
    
    print(json.dumps(result))
    
