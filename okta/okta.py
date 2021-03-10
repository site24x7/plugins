"""

Site24x7 Okta Logs Plugin

"""

from datetime import datetime, timedelta
import json
import os
import sys
import time
import traceback
import glob
import socket

PYTHON_MAJOR_VERSION = sys.version_info[0]
if PYTHON_MAJOR_VERSION == 3:
    import urllib
    import urllib.request as urlconnection
    from urllib.error import URLError, HTTPError
elif PYTHON_MAJOR_VERSION == 2:
    import urllib2 as urlconnection
    from urllib2 import HTTPError, URLError


OKTA_DOMAIN= 'yourOktaDomain'

OKTA_API_TOKEN= 'apiToken'

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

AGENT_HOME = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0]))))

LOG_FILE_DIR = os.path.join(AGENT_HOME, 'temp', 'scriptout')

LOG_ROTATION_INTERVAL='HOUR'

LOG_API_END_POINT='https://'+OKTA_DOMAIN+'/api/v1/logs'


class LogCollector:
    
    def __init__(self):
        pass
    
    def collect_logs(self):
        data = {}
        data['plugin_version'] = PLUGIN_VERSION
        data['heartbeat_required']=HEARTBEAT
        try:
            headers = { 'Authorization': 'SSWS ' + OKTA_API_TOKEN }
            startTime = datetime.utcnow() - timedelta(0, 300)
            request_url = LOG_API_END_POINT+'?since='+ startTime.isoformat()[:-3] + 'Z'
            
            handle, error = self.readUrl(request_url, headers);
            if error is not None:
                data['msg'] = error
                data['status'] = 0
            else:
                okta_events = json.loads(handle.read().decode('utf-8'))
                if not os.path.exists(LOG_FILE_DIR):
                    os.makedirs(LOG_FILE_DIR)
                file_suffix = datetime.now().strftime("%Y-%m-%d-%H" if LOG_ROTATION_INTERVAL == 'HOUR' else "%Y-%m-%d")
                file_path = os.path.join(LOG_FILE_DIR, 'events-'+file_suffix+'.log')
                with open(file_path, 'a') as _file:
                    for okta_event in okta_events:
                        _file.write(json.dumps(okta_event))
                        _file.write("\n")
                        
                try:
                    link_headers = handle.getheader('link').split(',');
                    for link  in link_headers:
                        if 'next' in link:
                            handle, error = self.readUrl(link[2:link.index('>')], headers=headers)
                            if error is None:
                                okta_events = json.loads(handle.read().decode('utf-8'))
                                with open(file_path, 'a') as _file:
                                    for okta_event in okta_events:
                                        _file.write(json.dumps(okta_event))
                                        _file.write("\n")
                except Exception as e:
                    pass
                
                data['msg']= 'Success'
                data['status']=1
        except Exception as e:
            data['msg']= 'Failure : '+str(e)
            data['status']=0
            traceback.print_exc()
        return data
    
    def readUrl(self, url_end_point, headers):
        error=None
        try:
            req = urlconnection.Request(url_end_point, headers=headers)
            handle = urlconnection.urlopen(req, None)
            return handle, error
        except HTTPError as e:
            if(e.code==401):
                error="ERROR: Unauthorized user. Does not have permissions. %s" %(e)
            elif(e.code==403):
                error="ERROR: Forbidden, yours credentials are not correct. %s" %(e)
            else:
                error="ERROR: The server couldn\'t fulfill the request. %s" %(e)
        except URLError as e:
            error = 'ERROR: We failed to reach a server. Reason: %s' %(e.reason)    
        except socket.timeout as e:
            error = 'ERROR: Timeout error'
        except socket.error as e:
            error = "ERROR: Unable to connect with host "+self.host+":"+self.port
        except:
            traceback.print_exc(e)
            error = "ERROR: Unexpected error: %s"%(sys.exc_info()[0])
        return None,error
    
    def cleanup_logs(self):
        try:
            inode_size_map = {}
            stat_file_name = os.path.join(AGENT_HOME, 'statefiles', 'local.properties')
            with open(stat_file_name) as _file:
                lines = _file.readlines()
                for line in lines:
                    if '=' in line:
                        line = line.strip()
                        inode_size_map[line.split('=')[0].strip()] = line.split('=')[1].strip() 
            
            log_files = glob.glob(os.path.join(LOG_FILE_DIR, 'events-*.log'))
            sorted_files = sorted( log_files, key = lambda file: os.path.getmtime(file), reverse=True)
            for log_file in sorted_files[1:]:
                statusObj = os.stat(log_file)
                inode = str(statusObj.st_ino)
                lmtime = datetime.fromtimestamp(statusObj.st_mtime)
                time_delta = datetime.now() - lmtime 
                if (24 * time_delta.days + time_delta.seconds/3600) < 24:
                    file_size = statusObj.st_size
                    if inode in inode_size_map and file_size == int(inode_size_map[inode]):
                        os.remove(log_file)
                else:
                    os.remove(log_file)
        except Exception as e:
            traceback.print_exc(e)
            

if __name__ == "__main__":
    log_collector = LogCollector()
    result = log_collector.collect_logs()
    log_collector.cleanup_logs()
    print(json.dumps(result, indent=4, sort_keys=True))
