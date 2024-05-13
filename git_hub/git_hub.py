#!/usr/bin/python
import requests
import json
import argparse

#Enter the User Name of your gitHub Account
USER_NAME = '' 

#Enter the PERSONAL_ACCESS_TOKEN of your gitHub Account
PERSONAL_ACCESS_TOKEN = ''

REPO_NAME=""
GITHUB_URL ="https://api.github.com"

#if any impacting changes to this plugin kindly increment the plugin version here.
PLUGIN_VERSION = "1"

#Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT="true"

result_json={}   

class gitHub:
    count_request_map={}
    keys_list=[]

    def read_args(self):
        global REPO_NAME
        parser = argparse.ArgumentParser()
        parser.add_argument('--user_name')
        parser.add_argument('--repo_name')
        parser.add_argument('--personal_access_token')
        args = parser.parse_args()
        if args.repo_name:
            REPO_NAME = args.repo_name
        if args.personal_access_token:
            PERSONAL_ACCESS_TOKEN = args.personal_access_token
        if args.user_name:
            USER_NAME = args.user_name
    
    def construct_urls(self):
        self.count_request_map['notifications']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/notifications"
        self.count_request_map['deployments']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/deployments"
        self.count_request_map['releases']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/releases"
        self.count_request_map['milestones']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/milestones"
        self.count_request_map['pull_requests']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/pulls"
        self.count_request_map['downloads']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/downloads"
        self.count_request_map['issues']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/issues"
        self.count_request_map['merges']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/merges"
        self.count_request_map['issues_comments']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/issues/comments"
        self.count_request_map['comments']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/comments"
        self.count_request_map['commits']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/commits"
        self.count_request_map['subscription']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/subscription"
        self.count_request_map['contributors']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/contributors"
        self.count_request_map['subscribers']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/subscribers"
        self.count_request_map['assignees']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/assignees"
        self.count_request_map['events']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/events"
        self.count_request_map['issue_events']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/issues/events"
        self.count_request_map['teams']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+USER_NAME+"/teams"
        self.count_request_map['collaborators']=GITHUB_URL+"/repos"+"/"+USER_NAME+"/"+REPO_NAME+"/collaborators"

    def get_metrics_counts(self):
        global result_json
        result_json['msg']=''
        no_metric=True
        try:
            for key in self.count_request_map.keys():
                if key not in self.keys_list:
                    self.keys_list.append(key)
                    count_response = requests.get(self.count_request_map.get(key), auth=(USER_NAME,PERSONAL_ACCESS_TOKEN),timeout=3.0)
                    if count_response.status_code==200:
                        result_json[key]=len(count_response.json())
                        no_metric=False
                    else:
                        result_json[key]=int(0)
                        if result_json['msg']=='':
                            result_json['msg']=self.count_request_map.get(key)+": "+str(count_response.status_code)
                        else:
                             result_json['msg']= result_json['msg']+", "+self.count_request_map.get(key)+": "+str(count_response.status_code)
            if no_metric:
                result_json['status'] = 0
   
        except Exception as e:
            result_json['status'] = 0
            result_json['msg'] = 'Exception occured in collecting data : ' + str(e)
      
            
    def get_repo_details(self):
        global result_json
        global REPO_NAME
        self.repo_check=False
        try:
            repo_response = requests.get(GITHUB_URL + '/user/repos', auth=(USER_NAME, PERSONAL_ACCESS_TOKEN),timeout=3.0)       
            if repo_response.status_code==200:
                repos_json = repo_response.json()
                for data in repos_json:  
                    if data['name'].__eq__(REPO_NAME):
                        self.construct_urls()
                        self.get_metrics_counts()
                        self.repo_check=True
                        result_json['is_private_repository'] =str(data['private'])
                        result_json['created_at'] =str(data['created_at'])
                        result_json['default_branch'] =str(data['default_branch'])
                        result_json["repository_name"] =REPO_NAME
                        break;
            else:
                result_json['status'] = 0
                result_json['msg'] = str(repo_response.json()['message'])
            if self.repo_check is False and repo_response.status_code==200:
                result_json['status'] = 0
                result_json['msg'] = "Given Repository name is not matched - "+REPO_NAME
        except Exception as e:
            result_json['status'] = 0
            result_json['msg'] = 'Exception occured in collecting data : ' + str(e)

    def trigger_action(self):
        self.read_args()
        if(not(REPO_NAME and REPO_NAME.strip())): 
            result_json['status'] = 0
            result_json['msg'] = 'Repository name is empty'
            return
        self.get_repo_details()
 
if __name__ == '__main__':
    
    git_hub = gitHub()
    git_hub.trigger_action()
    
    result_json["plugin_version"] = PLUGIN_VERSION
    result_json["heartbeat_required"] = HEARTBEAT

    print(json.dumps(result_json, indent=4, sort_keys=True))
