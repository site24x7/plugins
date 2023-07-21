# Plugin for monitoring GitHub

## Plugin installation
___
### Prerequisites
* To monitor your github account we need an username , repository name and a Personal Access Token.
	
	Please refer this link to create "Personal Access Token" with read access- https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line

### Plugin configuration
---

* Create a directory "git_hub".

* Download the files "git_hub.py" , "git_hub.cfg" and place it under the "git_hub" directory

		wget https://raw.githubusercontent.com/site24x7/plugins/master/git_hub/git_hub.py

		wget https://raw.githubusercontent.com/site24x7/plugins/master/git_hub/git_hub.cfg

- Follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers) to update the Python path in the git_hub.py script.

* Open the "git_hub.cfg" file and add the configuration details to it.
	Sample configuration file looks like:
	#git_hub.cfg
		
		[display_name]
		user_name="user@github"
		personal_access_token="123ascejsfnkl"
		repo_name="Sample_repo1"

	display_name denotes - plugin monitor name to be displayed in site24x7 client
	
	user_name denotes - user name of the github account
	
	personal_access_token denotes - personal access token created for the github account 
	
	repo_name denotes - actual repository name to be monitored

* If you have more than one repositories needs to be monitored create one more section and configure it as above.

* Move the directory "git_hub" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/git_hub


The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


### Metrics captured
---
* notifications
* deployments
* milestones
* releases
* pullrequests
* downloads
* issues
* merges
* issues_comments
* comments
* commits
* subscription
* contributors
* subscribers
* assignees
* events
* issue_events
* teams
* collaborators
* is_private_repository
* default_branch
* created_at
* repository_name
