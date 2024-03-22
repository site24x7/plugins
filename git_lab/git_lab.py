#!/usr/bin/python
import requests
import json
import argparse


# provide the gitlab host URL and Personal Access Token  of your account.
GIT_URL = "https://gitlab.com"

PERSONAL_ACCESS_TOKEN = ''

PROJECT_ID=""

API_URL = GIT_URL+"/api/v4"

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

result_json = {}
class gitLab:
    count_request_map={}
    keys_list=[]
    private_token = {}
    
    def read_args(self):
        global PROJECT_ID
        parser = argparse.ArgumentParser()
        parser.add_argument('--project_id')
        parser.add_argument('--personal_access_token')
        args = parser.parse_args()
        if args.project_id:
            PROJECT_ID = str(args.project_id)
        if args.personal_access_token:
            PERSONAL_ACCESS_TOKEN=args.personal_access_token
        self.private_token={
        "PRIVATE-TOKEN" : PERSONAL_ACCESS_TOKEN
        }
        
    def construct_urls(self):
        self.count_request_map['merge_requests']=API_URL+"/projects/"+PROJECT_ID+"/merge_requests"
        self.count_request_map['issues_statistics']=API_URL+"/projects/"+PROJECT_ID+"/issues_statistics"
        self.count_request_map['milestones']=API_URL+"/projects/"+PROJECT_ID+"/milestones"
        self.count_request_map['branches']=API_URL+"/projects/"+PROJECT_ID+"/repository/branches"
        self.count_request_map['commits']=API_URL+"/projects/"+PROJECT_ID+"/repository/commits"
        self.count_request_map['dependencies']=API_URL+"/projects/"+PROJECT_ID+"/dependencies"
        self.count_request_map['deployments']=API_URL+"/projects/"+PROJECT_ID+"/deployments"
        self.count_request_map['environments']=API_URL+"/projects/"+PROJECT_ID+"/environments"
        self.count_request_map['events']=API_URL+"/projects/"+PROJECT_ID+"/events"
        self.count_request_map['managed_licenses']=API_URL+"/projects/"+PROJECT_ID+"/managed_licenses"
        self.count_request_map['contributors']=API_URL+"/projects/"+PROJECT_ID+"/repository/contributors"
        self.count_request_map['total_fetches']=API_URL+"/projects/"+PROJECT_ID+"/statistics"
        self.count_request_map['members']=API_URL+"/projects/"+PROJECT_ID+"/members"
        self.count_request_map['pipeline_schedules']=API_URL+"/projects/"+PROJECT_ID+"/pipeline_schedules"
        self.count_request_map['pipeline_triggers']=API_URL+"/projects/"+PROJECT_ID+"/triggers"
        self.count_request_map['protected_branches']=API_URL+"/projects/"+PROJECT_ID+"/protected_branches"
        self.count_request_map['pipelines']=API_URL+"/projects/"+PROJECT_ID+"/pipelines"
        self.count_request_map['releases']=API_URL+"/projects/"+PROJECT_ID+"/releases"
    
    def get_metrics_counts(self):
        global result_json
        try:
            for key in self.count_request_map.keys():
                if key not in self.keys_list:
                    count_response = requests.get(self.count_request_map.get(key), headers=self.private_token,timeout=3.0)
                    self.keys_list.append(key)
                    if count_response.status_code == 200:
                        if key == 'total_fetches':
                            json_value = count_response.json()
                            fetches_data = json_value['fetches']
                            result_json[key]=int(fetches_data['total'])
                        elif key == 'issues_statistics':
                            json_value = count_response.json()
                            statistics_json = json_value['statistics']
                            counts_json=statistics_json['counts']
                            result_json['opened_issues'] = int(counts_json['opened'])
                            result_json['closed_issues'] = int(counts_json['closed'])
                            result_json['all_issues'] = int(counts_json['all'])
                        else:
                            result_json[key]=len(count_response.json())
                    else:
                        result_json[key]=int(0)
       
        except Exception as e:
            result_json['status'] = 0
            result_json['msg'] = 'Exception occured while collecting data : ' + str(e)

                   
    def trigger_action(self):
        if(not(PROJECT_ID and PROJECT_ID.strip())): 
            result_json['status'] = 0
            result_json['msg'] = 'Project Id is empty'
            return
        try:
            project_response = requests.get(API_URL+"/projects/"+PROJECT_ID,headers=self.private_token,timeout=3.0)
            if project_response.status_code == 200:
                response_json=project_response.json()
                if PROJECT_ID==str(response_json['id']):
                    self.construct_urls()
                    self.get_metrics_counts()
                    result_json['project_name']=str(response_json['name'])
                    result_json['visibility']=str(response_json['visibility'])
                    result_json['default_branch']=str(response_json['default_branch'])  
                else:
                    result_json['status'] = 0
                    result_json['msg'] = 'Given Project Id and fetched Project Id are different' + PROJECT_ID
                    return
            
            else:          
                result_json['status'] = 0
                result_json['msg'] = str(project_response.json()['message'])
                return  
        except Exception as e:
            result_json['status'] = 0
            result_json['msg'] = 'Exception occured while collecting data : ' + str(e)       
if __name__ == '__main__':        
    git_lab=gitLab()
    git_lab.read_args()
    git_lab.trigger_action()
    
    result_json["plugin_version"] = PLUGIN_VERSION
    result_json["heartbeat_required"] = HEARTBEAT
    
    print(json.dumps(result_json, indent=4, sort_keys=True))

