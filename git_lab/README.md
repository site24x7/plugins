# Plugin for monitoring GitLab

### Prerequisites
* To monitor your gitlab account we need Private token of the gitlab account.
	
	Please refer this link to create Personal Access Token (PRIVATE_TOKEN) - https://docs.gitlab.com/ee/user/profile/personal_access_tokens.html

### Plugin configuration
---

* Create a directory "git_lab".

* Download the files "git_lab.py" , "git_lab.cfg" and place it under the "git_lab" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/git_lab/git_lab.py

		wget https://raw.githubusercontent.com/site24x7/plugins/master/git_lab/git_lab.cfg
  
- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the git_lab.py script.

* Open the "git_lab.cfg" file and add the configuration details to it. Sample configuration file looks like: #git_lab.cfg
	
	Sample configuration file looks like:
	#git_lab.cfg
	
		[display_name]
		personal_access_token='9LdYrk1ju3avs-Xth&jkQyu'
		project_id='1689076'

	display name denotes - plugin monitor name to be displayed in site24x7 client
	
	personal_access_token denotes - personal access token created for the github account
	
	project_id denotes - actual project id to be monitored

* If you have more than one projects needs to be monitored create one more section and configure it as above.

* Move the directory "git_lab" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/git_lab

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


### Metrics captured
---
* merge_requests
* milestones
* branches
* commits
* dependencies
* deployments
* environments
* events
* managed_licenses
* contributors
* total_fetches
* members
* pipeline_schedules
* pipeline_triggers
* protected_branches
* pipelines
* releases
* opened_issues
* closed_issues
* all_issues
* project_name
* visibility
* default_branch
