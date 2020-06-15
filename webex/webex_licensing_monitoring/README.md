# Plugin for monitoring WebEx Account 
## Plugin installation  
### Prerequisites  
* WebEx account with Admin and Compliance manager privileges. 
* Kindly follow the steps given below to get access_token,refresh_token,client_id and client_secret.
	1. To create your integration through the Webex for Developers Portal, simply log into your Webex account at https://developer.webex.com, click on your avatar at the top right, then click "My Webex Teams Apps". This will take you to the "My Apps" page. Click the blue plus at the top right and then choose "Create an Integration". You should now be on the "New Integration" page. Choose a unique name, a contact email (for Cisco internal support use only, it won't be referenced anywhere publicly), an icon, and the general description or purpose of the integration.

	2. Once these are completed, provide a Redirect URI.

	3. Next, choose which scopes the integration needs. Kindly provide all spark,spark-admin,spark-compliance GET roles to fetch all metrics that the plugin supports.

	4. Submit the app by clicking on the "Create Integration" button at the bottom.

	5. The OAuth Authorization URL shown at the bottom of the integration details page provide the following, in this order:
    	(A)client_id
    	(B)response-type
    	(C)redirect_uri
    	(D)scopes
    	(E)state

	6. Hit the authorization URL from the browser you will need to sign in again to and accept all the privileges being requested by the integration on completion of which will be 	redirected to the page which you have mentioned earlier in redirect_uri. In the url you will be able to find the authorization code[code] along with the URI.

	7. To retrieve the Access Token kindly do a HTTP POST to https://webexapis.com/v1/access_token with
		(A) grant_type — This should be set to "authorization_code"
		(B) client_id — Issued when creating your integration
		(C) client_secret — Remember this guy? You kept it safe somewhere when creating your integration.
		(D) code — The Authorization Code from the previous step
		(E) redirect_uri — Must match the one used in the previous step

	8. You will retrive the access token, refresh token.

	9. Kindly provide the access token, refresh token, client id and client secret in the plugin configuration file.

### Plugin Installation 

      	1) Create a directory "webex_licensing_monitoring" under Site24x7 Linux Agent plugin directory - /opt/site24x7/monagent/plugins/webex_licensing_monitoring
            
            mkdir /opt/site24x7/monagent/plugins/webex_licensing_monitoring

		2) Download the files "webex_licensing_monitoring.py" and place it under the "webex_licensing_monitoring" directory

		    wget https://raw.githubusercontent.com/site24x7/plugins/master/webex_licensing_monitoring/webex_licensing_monitoring.py

        3) Download the file "webex_licensing_monitoring.cfg" and place it under the "webex_licensing_monitoring" directory

            wget https://raw.githubusercontent.com/site24x7/plugins/master/webex_licensing_monitoring/webex_licensing_monitoring.cfg

### Plugin configuration  
	1) In /opt/site24x7/monagent/conf/monagent.cfg set plugin_time_out = 80.
 
	2) In the webex_licensing_monitoring.cfg file enter the value for the mandatory fields access_token, use_custom_fields, client_id, client_secret, refresh_token, logging.
		1. access_token --> Used to authenticate the WebEx Apis used for metrics collection.
		2. client_id --> Used to retrieve the new Access Token from refresh token if the provided access token is invalid/expired.
		3. client_secret --> Used to retrieve the new Access Token from refresh token if the provided access token is invalid/expired.
		4. refresh_token --> Used to retrieve the new Access Token from refresh token if the provided access token is invalid/expired.
		5. use_custom_fields --> True/False. If set to true will use the custom Ord Ids and Team Ids mentioned in 6 and 7
		6. orgids --> List of Organization Ids to check for while collecting metrics.
		7. teams --> List of Team Ids to check for while collecting metrics
		8. logging --> To log performace and exception trace(If any) of Apis used in the plugin.
	
	3) Restart the server monitoring agent to get the plugin added for monitoring.

* NOTE :- If field 5 is set to true fields 6 and 7 must be both configured.
* All Api's performance and error logs will be available in the plugin_perf.log in the plugin directory.
  
  
Metrics captured  
---  
1. Admin - Org Count  -----> Count of Organizations being monitored
2. Admin - Teams Count  -----> Count of Teams being monitored 
3. Admin - Devices Count  -----> Count of devices configured within the org/'s
4. People Count  -----> Count of people within the org/'s
5. Hybrid - Clusters Count  -----> Count of Hybrid Clusters configured within the org/'s
6. Hybrid - Connectors Count  -----> Count of Hybrid Connectors configured within the org
7. Room - Memberships Count  -----> Count of Rooms Configured within the org/'s
8. Places Count  -----> Count of places Configured within the org/'s
9. Admin - Roles Count  -----> Count of Admin roles the current authenticated is privileged with.
10. Total Messages Exchanged  -----> Count of total messages exchanged within org.
11. Room - Memberships Count  -----> Count of all memberships associated with each team.