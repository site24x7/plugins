# Plugin for monitoring GitHub

## Plugin installation
___
### Prerequisites
* To monitor your github account we need an username and a Personal Access Token.
	
	Please refer this link to create "Personal Access Token" with read access- https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line

### Supported OS ( Linux & OSX )

### Plugin configuration
---

* Create a directory "git_hub" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/git_hub

* Download the files "git_hub.py" , "git_hub.cfg" and place it under the "git_hub" directory

	wget https://raw.githubusercontent.com/site24x7/plugins/master/git_hub/git_hub.py

	wget https://raw.githubusercontent.com/site24x7/plugins/master/git_hub/git_hub.cfg


* Open git_hub.py file. Set the values for **USER_NAME**, **PERSONAL_ACCESS_TOKEN**.

* Open the "git_hub.cfg" file and add repository name(s) to be monitored under keyword "repo_name" as given below.
	Sample configuration file looks like:
	
	#git_hub.cfg
	
		[repo_1]
		repo_name="Sample_repo1"

	where repo_1 denotes - plugin monitor name to be displayed in site24x7 client

	repo_name denotes - actual repository name to be monitored

* After completing above steps please run "python git_hub.py --repo_name='Sample_repo1'" to make sure data is obtained.

* If you have more than one repositories needs to be monitored create one more section and configure it as above.


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
