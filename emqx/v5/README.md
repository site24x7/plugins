


# EMQX Monitoring


## Standard Installation
If you're not using Linux servers or want to install the plugin manually, follow the steps below.

### Prerequisites
- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python 3.6 or higher version should be installed.

### Installation  

- Create a directory named "emqx".
- Install the **requests** python module.
	```
	pip3 install requests
	```

	
- Download the below files in the "emqx" folder and place it under the "emqx" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/emqx/v5/emqx.py && sed -i "1s|^.*|#! $(which python3)|" emqx.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/emqx/v5/emqx.cfg

- Execute the below command with appropriate arguments to check for the valid json output:
	```bash
       python3 emqx.py --host "hostname" --port "port no" --api_key "api key" --secret_key "api secret key"
	 ```
- After the above command with parameters gives the expected output, please configure the relevant parameters in the emqx.cfg file.
	```
    [emqx]
    host="localhost"
    port="18083"
    api_key="api_key"
    secret_key="secret api key"
	```	
#### Linux
- Move the "emqx" directory under the Site24x7 Linux Agent plugin directory: 

	```bash
	mv emqx /opt/site24x7/monagent/plugins/
	```

#### Windows
- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in the below link. The remaining configuration steps are the same.
https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers
-  Further, move the folder "emqx" into the  Site24x7 Windows Agent plugin directory:

        Windows          ->   C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\emqx


The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

## Supported Metrics:


**Connections and Sessions:**

- `Client Connect`: Number of times clients have attempted to connect to the broker.
- `Client Connected`: Number of successful client connections.
- `Client Disconnected`: Number of client disconnections.
- `Session Created`: Number of new client sessions created.
- `Session Resumed`: Number of existing client sessions resumed.
- `Session Discarded`: Number of client sessions that were discarded (e.g., due to inactivity).
- `Session Takenover`: Number of client sessions that were taken over (potentially by another client).

**Subscriptions and Unsubscriptions:**

- `Client Subscribe`: Number of times clients have requested subscriptions to topics.
- `Client Unsubscribe`: Number of times clients have requested to unsubscribe from topics.
- `Packets Subscribe Received`: Number of `SUBSCRIBE` packets received from clients.
- `Packets Unsubscribe Received`: Number of `UNSUBSCRIBE` packets received from clients.
- `Packets Suback Sent`: Number of `SUBACK` packets sent to clients in response to successful subscriptions.
- `Packets Unsuback Sent`: Number of `UNSUBACK` packets sent to clients in response to successful unsubscriptions.

**Messages and Delivery:**

- `Messages Publish`: Number of publish messages received from clients.
- `Messages Sent`: Total number of messages sent by the broker (includes all QoS levels).
- `Messages Acked`: Number of messages for which the broker received acknowledgments (QoS 1 or 2).
- `Messages Delivered`: Number of messages successfully delivered to subscribers.
- `Messages Qos0 Sent`: Number of QoS 0 messages sent by the broker (fire-and-forget).
- `Messages Qos1 Sent`: Number of QoS 1 messages sent by the broker (requires acknowledgment).
- `Messages Qos2 Sent`: Number of QoS 2 messages sent by the broker (requires multiple acknowledgments).
- `Messages Qos0 Received`: Number of QoS 0 messages received from clients.
- `Messages Qos1 Received`: Number of QoS 1 messages received from clients.
- `Messages Qos2 Received`: Number of QoS 2 messages received from clients.
- `Messages Forward`: Number of messages forwarded by the broker to subscribers.
- `Messages Persisted`: Number of messages persisted by the broker (if persistence is enabled).
- `Messages Delayed`: Number of messages currently delayed due to various factors.

**Authorization and Authentication:**

- `Authentication Success`: Number of successful client authentications.
- `Authentication Failure`: Number of failed client authentication attempts.
- `Authentication Success Anonymous`: Number of successful anonymous client authentications (if allowed).
- `Client Auth Anonymous`: Number of client attempts to authenticate anonymously (if allowed).
- `Client Authorize`: Number of client attempts to authorize (potentially using tokens).
- `Client Authenticate`: Number of client attempts to authenticate (potentially using username/password).
- `Authorization Matched Allow`: Number of times authorization rules allowed access.
- `Authorization Matched Deny`: Number of times authorization rules denied access.
- `Authorization Allow`: Number of times authorization explicitly allowed access (regardless of rules).
- `Authorization Deny`: Number of times authorization explicitly denied access (regardless of rules).
- `Authorization Nomatch`: Number of authorization checks that didn't match any rule.
- `Authorization Cache_Hit`: Number of times authorization information was retrieved from the cache.
- `Authorization Cache_Miss`: Number of times authorization information was not found in the cache.
- `Authorization Superuser`: Number of times a superuser accessed the broker (if superuser access is enabled).

**Packets:**

- `Packets Received`: Total number of packets received by the broker.
- `Packets Sent`: Total number of packets sent by the broker.
- `Packets Connect Received`: Number of `CONNECT` packets received from clients.
- `Packets Connack Sent`: Number of `CONNACK` packets sent to clients in response to connection attempts.
- `Packets Puback Sent`: Number of `PUBACK` packets sent to clients acknowledging QoS 1 messages.
- `Packets Pubrel Sent`: Number of `PUBREL` packets sent to clients (part of QoS 2 flow).
- `Packets Pubrec Sent`: Number of `PUBREC` packets sent to clients (part of QoS 2 flow).
- `Packets Disconnect Received`: Number of `DISCONNECT` packets received from clients.
- `Packets Disconnect Sent`: Number of `DISCONNECT` packets sent to clients (e.g., due to errors).
- `Packets Pingreq Received`: Number of `PINGREQ` packets received from clients for checking connection status.


