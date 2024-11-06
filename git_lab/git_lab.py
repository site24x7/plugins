#!/usr/bin/python
import requests
import json
import argparse

# Default values for plugin version and heartbeat
PLUGIN_VERSION = "1"
HEARTBEAT = "true"

class GitLab:
    def __init__(self, args):
        self.gitlab_url = args.gitlab_url
        self.project_id = args.project_id
        self.personal_access_token = args.personal_access_token
        self.api_url = f"{self.gitlab_url}/api/v4"
        self.result_json = {
            "plugin_version": PLUGIN_VERSION,
            "heartbeat_required": HEARTBEAT
        }
        self.private_token = {"PRIVATE-TOKEN": self.personal_access_token}
        self.count_request_map = {}

    def construct_urls(self):
        self.count_request_map = {
            'merge_requests': f"{self.api_url}/projects/{self.project_id}/merge_requests",
            'issues_statistics': f"{self.api_url}/projects/{self.project_id}/issues_statistics",
            'milestones': f"{self.api_url}/projects/{self.project_id}/milestones",
            'branches': f"{self.api_url}/projects/{self.project_id}/repository/branches",
            'commits': f"{self.api_url}/projects/{self.project_id}/repository/commits",
            'dependencies': f"{self.api_url}/projects/{self.project_id}/dependencies",
            'deployments': f"{self.api_url}/projects/{self.project_id}/deployments",
            'environments': f"{self.api_url}/projects/{self.project_id}/environments",
            'events': f"{self.api_url}/projects/{self.project_id}/events",
            'managed_licenses': f"{self.api_url}/projects/{self.project_id}/managed_licenses",
            'contributors': f"{self.api_url}/projects/{self.project_id}/repository/contributors",
            'total_fetches': f"{self.api_url}/projects/{self.project_id}/statistics",
            'members': f"{self.api_url}/projects/{self.project_id}/members",
            'pipeline_schedules': f"{self.api_url}/projects/{self.project_id}/pipeline_schedules",
            'pipeline_triggers': f"{self.api_url}/projects/{self.project_id}/triggers",
            'protected_branches': f"{self.api_url}/projects/{self.project_id}/protected_branches",
            'pipelines': f"{self.api_url}/projects/{self.project_id}/pipelines",
            'releases': f"{self.api_url}/projects/{self.project_id}/releases"
        }

    def get_metrics_counts(self):
        try:
            for key, url in self.count_request_map.items():
                response = requests.get(url, headers=self.private_token, timeout=3.0)
                if response.status_code == 200:
                    if key == 'total_fetches':
                        fetches_data = response.json().get('fetches', {})
                        self.result_json[key] = int(fetches_data.get('total', 0))
                    elif key == 'issues_statistics':
                        counts = response.json().get('statistics', {}).get('counts', {})
                        self.result_json.update({
                            'opened_issues': counts.get('opened', 0),
                            'closed_issues': counts.get('closed', 0),
                            'all_issues': counts.get('all', 0)
                        })
                    else:
                        self.result_json[key] = len(response.json())
                else:
                    self.result_json[key] = 0
        except Exception as e:
            self.result_json.update({
                'status': 0,
                'msg': f"Exception occurred while collecting data: {e}"
            })

    def trigger_action(self):
        if not self.project_id:
            self.result_json.update({
                'status': 0,
                'msg': 'Project ID is empty'
            })
            return

        try:
            project_response = requests.get(f"{self.api_url}/projects/{self.project_id}",
                                            headers=self.private_token, timeout=3.0)
            if project_response.status_code == 200:
                project_data = project_response.json()
                if str(self.project_id) == str(project_data['id']):
                    self.construct_urls()
                    self.get_metrics_counts()
                    self.result_json.update({
                        'project_name': project_data['name'],
                        'visibility': project_data['visibility'],
                        'default_branch': project_data['default_branch']
                    })
                else:
                    self.result_json.update({
                        'status': 0,
                        'msg': 'Given Project ID and fetched Project ID are different'
                    })
            else:
                self.result_json.update({
                    'status': 0,
                    'msg': project_response.json().get('message', 'Error fetching project data')
                })
        except Exception as e:
            self.result_json.update({
                'status': 0,
                'msg': f"Exception occurred while collecting data: {e}"
            })

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--gitlab_url', help='GitLab URL', default="https://gitlaburl.com")
    parser.add_argument('--project_id', required=True, help='GitLab project ID')
    parser.add_argument('--personal_access_token', required=True, help='GitLab personal access token')
    args = parser.parse_args()

    git_lab = GitLab(args)
    git_lab.trigger_action()
    print(json.dumps(git_lab.result_json, indent=4 sort_keys=True))
