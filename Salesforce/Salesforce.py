"""

Site24x7 Salesforce Logs Plugin

"""
import argparse
from datetime import datetime, timedelta
import json
import csv
import os
import sys
import io
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


# if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"

AGENT_HOME = os.path.dirname(os.path.dirname(os.path.realpath(sys.argv[0])))

LOG_FILE_DIR = os.path.join(AGENT_HOME, 'temp', 'scriptout')

LOG_FILE_NAME_PREFIX = 'sf-events-'

LOG_ROTATION_INTERVAL = 'HOUR'

SF_TIME_LAG_MINUTE = 180

class LogCollector:

    def __init__(self, config):
        self.sf_domain = config.get('domain')
        self.sf_username = config.get('username')
        self.sf_password = config.get('password')
        self.sf_security_token = config.get('security_token')
        self.sf_consumer_key = config.get('consumer_key')
        self.sf_consumer_secret = config.get('consumer_secret')
        self.auth_token_endpoint = 'https://' + self.sf_domain + '/services/oauth2/token'
        self.query_api_endpoint = 'https://' + self.sf_domain + '/services/data/v54.0/query'
        self.data = {}
        self.sf_access_token = self.authenticate()

    def authenticate(self):
        payload = urllib.parse.urlencode({'grant_type':'password','client_id':self.sf_consumer_key,'client_secret':self.sf_consumer_secret,'username':self.sf_username,'password':self.sf_password+self.sf_security_token}).encode('utf-8')
        req = urlconnection.Request(self.auth_token_endpoint)
        try:
            rawResponse = urlconnection.urlopen(req, data=payload)
            if rawResponse.code == 200:
                response = json.loads(rawResponse.read().decode('utf-8'))
                return response['access_token']
        except urllib.error.HTTPError as e:
            self.data['msg'] = str(e.code)+':'+e.reason
            self.data['status'] = 0
            return None

    def execute_query(self, query):
        headers = {'Authorization': 'Bearer ' + self.sf_access_token}
        request_url = self.query_api_endpoint + '?q='+query
        print('Making Reqeust :',request_url)
        handle, error = self.readUrl(request_url, headers)
        if error is not None:
            self.data['msg'] = error
            self.data['status'] = 0
        else:
            response_json = json.loads(handle.read().decode('utf-8'))
            return response_json['records'], None

    def get_report_names(self):
        query = 'SELECT+Id,+Name+From+Report'
        records, error = self.execute_query(query)
        report_dict = {}
        for record in records:
            report_dict[record['Id']] = record['Name']
        return report_dict

    def get_document_names(self):
        query = 'SELECT+Id,+Name+From+Document'
        records, error = self.execute_query(query)
        report_dict = {}
        for record in records:
            report_dict[record['Id']] = record['Name']
        return report_dict

    def get_event_log_files(self):
        start_time = datetime.utcnow() - timedelta(minutes=SF_TIME_LAG_MINUTE + 120)
        end_time = start_time + timedelta(minutes=60)
        whereClause = 'WHERE+LogDate>=' + start_time.strftime('%Y-%m-%dT%H:00:00.000Z') + 'AND+LogDate<' + end_time.strftime('%Y-%m-%dT%H:00:00.000Z') + '+AND+Interval=\'Hourly\''
        query = "SELECT+Id+,+EventType+,+LogFile+,+LogDate+,+LogFileLength+FROM+EventLogFile+" + whereClause
        records, error = self.execute_query(query)
        if error is None:
            return records
        else:
            return None

    def read_event_log(self, event_log_files):
        if not os.path.exists(LOG_FILE_DIR):
            os.makedirs(LOG_FILE_DIR)
        file_suffix = datetime.now().strftime("%Y-%m-%d-%H" if LOG_ROTATION_INTERVAL == 'HOUR' else "%Y-%m-%d")
        file_path = os.path.join(LOG_FILE_DIR, LOG_FILE_NAME_PREFIX + file_suffix + '.log')
        meta = {'report' : self.get_report_names(), 'document': self.get_document_names()}
        headers = {'Authorization': 'Bearer ' + self.sf_access_token}
        for record in event_log_files:
            try:
                handle, error = self.readUrl('https://' + self.sf_domain + record['LogFile'], headers=headers)
                if error is None:
                    sf_event_log = handle.read().decode('utf-8')
                    with open(file_path, 'a') as _file:
                        for sf_event in csv.DictReader(io.StringIO(sf_event_log)):
                            processed_event = self.process_event_log(sf_event, meta)
                            _file.write(json.dumps(processed_event))
                            _file.write("\n")
            except Exception as e:
                pass

    def process_event_log(self, event, meta):
        try:
            event_type = event['EVENT_TYPE']
            if event_type == 'Report' and event['REPORT_ID_DERIVED']:
                event['REPORT_ID_DERIVED_NAME'] = meta['report'][event['REPORT_ID_DERIVED']]
            elif event_type == 'DocumentAttachmentDownloads' and event['ENTITY_ID']:
                    event['FILE_NAME'] = meta['document'][event['ENTITY_ID']]
        except Exception as e:
            pass
        return  event


    def collect_logs(self):
        try:
            if self.sf_access_token:
                event_log_files = self.get_event_log_files()
                if event_log_files:
                    print('Event Log Files Count', len((event_log_files)))
                    self.read_event_log(event_log_files)
                    open('ct_info', 'w').write(str(round(time.time() * 1000)))
                self.data['msg'] = 'Success'
                self.data['status'] = 1
        except Exception as e:
            self.data['msg'] = 'Failure : ' + str(e)
            self.data['status'] = 0
            traceback.print_exc()
        return self.data

    def readUrl(self, url_end_point, headers):
        error = None
        try:
            req = urlconnection.Request(url_end_point, headers=headers)
            handle = urlconnection.urlopen(req, None)
            return handle, error
        except HTTPError as e:
            if (e.code == 401):
                error = "ERROR: Unauthorized user. Does not have permissions. %s" % (e)
            elif (e.code == 403):
                error = "ERROR: Forbidden, yours credentials are not correct. %s" % (e)
            else:
                error = "ERROR: The server couldn\'t fulfill the request. %s" % (e)
        except URLError as e:
            error = 'ERROR: We failed to reach a server. Reason: %s' % (e.reason)
        except socket.timeout as e:
            error = 'ERROR: Timeout error'
        except socket.error as e:
            error = "ERROR: Unable to connect with host " + self.host + ":" + self.port
        except:
            traceback.print_exc()
            error = "ERROR: Unexpected error: %s" % (sys.exc_info()[0])
        return None, error

    def cleanup_logs(self):
        try:
            inode_size_map = {}
            stat_file_name = os.path.join(AGENT_HOME, 'statefiles', 'local.properties')
            if os.path.exists(stat_file_name):
                with open(stat_file_name) as _file:
                    lines = _file.readlines()
                    for line in lines:
                        if '=' in line:
                            line = line.strip()
                            inode_size_map[line.split('=')[0].strip()] = line.split('=')[1].strip()

                log_files = glob.glob(os.path.join(LOG_FILE_DIR, 'events-*.log'))
                sorted_files = sorted(log_files, key=lambda file: os.path.getmtime(file), reverse=True)
                for log_file in sorted_files[1:]:
                    statusObj = os.stat(log_file)
                    inode = str(statusObj.st_ino)
                    lmtime = datetime.fromtimestamp(statusObj.st_mtime)
                    time_delta = datetime.now() - lmtime
                    if (24 * time_delta.days + time_delta.seconds / 3600) < 24:
                        file_size = statusObj.st_size
                        if inode in inode_size_map and file_size == int(inode_size_map[inode]):
                            os.remove(log_file)
                    else:
                        os.remove(log_file)
        except Exception as e:
            traceback.print_exc(e)

def log_collection_allowed():
    if os.path.exists('ct_info'):
        last_ct = int(open('ct_info').read())
        delta =   (round(time.time() * 1000)) - last_ct
        return True if delta > (1000*60*60) else False
    else:
        return True

def run(config):
    result = {}
    if log_collection_allowed():
        log_collector = LogCollector(config)
        result = log_collector.collect_logs()
        log_collector.cleanup_logs()
    else:
        result['msg'] = 'Success'
        result['status'] = 1

    result['plugin_version'] = config.get('plugin_version')
    result['heartbeat_required'] = config.get('heartbeat_required')

    applog = {"logs_enabled":  True if config.get('logs_enabled') in ['True', 'true', '1'] else False}
    if (applog["logs_enabled"]):
        applog["log_type_name"] = config.get('log_type_name')
        applog["log_file_path"] = config.get('log_file_path')
    result['applog'] = applog

    return result

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain', help='Salesforce domain name', nargs='?')
    parser.add_argument('--username', help='user name', nargs='?')
    parser.add_argument('--password', help='password', nargs='?')
    parser.add_argument('--security_token', help='security token', nargs='?')
    parser.add_argument('--consumer_key', help='consumer key', nargs='?')
    parser.add_argument('--consumer_secret', help='consumer secret', nargs='?')

    parser.add_argument('--logs_enabled', help='enable log collection for this plugin application', type=bool,nargs='?', default=True)
    parser.add_argument('--log_type_name', help='Display name of the log type', nargs='?', default=None)
    parser.add_argument('--log_file_path', help='list of comma separated log file paths', nargs='?', default=os.path.join(LOG_FILE_DIR, LOG_FILE_NAME_PREFIX+"*"))

    parser.add_argument('--plugin_version', help='plugin template version', type=int, nargs='?', default=PLUGIN_VERSION)
    parser.add_argument('--heartbeat_required', help='alert if monitor does not send data', type=bool, nargs='?', default=HEARTBEAT)
    args = parser.parse_args()

    result = run(vars(args))
    print(json.dumps(result, indent=4, sort_keys=True))
