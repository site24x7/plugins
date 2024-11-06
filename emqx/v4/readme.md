# EMQX Monitoring

### Prerequisites
- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.
- Python 3.6 or higher version should be installed.

### Installation  

- Create a directory named "emqx".
  	```
	mkdir emqx
	```
- Install the **requests** python module.
	```
	pip3 install requests
	```

	
- Download the below files in the "emqx" folder and place it under the "emqx" directory.

		wget https://raw.githubusercontent.com/site24x7/plugins/master/emqx/v4/emqx.py && sed -i "1s|^.*|#! $(which python3)|" emqx.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/emqx/v4/emqx.cfg

- Execute the below command with appropriate arguments to check for the valid json output:
	```bash
       python3 emqx.py --host "hostname" --port "port no" --username "user name" --password "password"
	 ```
- After the above command with parameters gives the expected output, please configure the relevant parameters in the emqx.cfg file.
	```
    [emqx]
    host="localhost"
    port="18083"
    username="user"
    password="user"
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

# Supported Metrics

## Delivery Metrics

| Metric                        | Description                                                                                   |
|-------------------------------|-----------------------------------------------------------------------------------------------|
| Delivery Dropped              | Total number of messages that were dropped due to various reasons.                           |
| Delivery Dropped Expired      | Count of messages dropped because they expired before delivery.                              |
| Delivery Dropped No_Local     | Messages dropped because the `no_local` flag was set, avoiding delivery to the sender itself.|
| Delivery Dropped Qos0_Msg     | Messages with QoS 0 dropped due to lack of subscriber acknowledgment.                        |
| Delivery Dropped Queue_Full   | Messages dropped because the delivery queue was full.                                        |
| Delivery Dropped Too_Large    | Messages dropped because their size exceeded the allowed limit.                              |

## Client Metrics

| Metric                           | Description                                                                                           |
|----------------------------------|-------------------------------------------------------------------------------------------------------|
| Client Acl Allow                 | Count of client access requests that were allowed by ACL rules.                                       |
| Client Acl Cache_Hit             | Count of ACL checks that were resolved through cached results, enhancing efficiency.                  |
| Client Acl Deny                  | Count of client access requests that were denied by ACL rules.                                       |
| Client Auth Failure              | Number of client authentication attempts that failed.                                                 |
| Client Auth Success              | Number of successful client authentication attempts.                                                  |
| Client Auth Success Anonymous    | Successful anonymous client authentications without specific credentials.                            |
| Client Authenticate              | Total attempts to authenticate clients.                                                               |
| Client Check_Acl                 | Total ACL checks performed for clients to verify resource access.                                    |
| Client Connack                   | Total number of CONNACK (connection acknowledgment) packets sent to clients.                         |
| Client Connect                   | Number of CONNECT packets received from clients, initiating a connection request.                    |
| Client Connected                 | Total active clients that are currently connected to the broker.                                     |
| Client Disconnected              | Number of clients that disconnected from the broker.                                                 |
| Client Subscribe                 | Total number of SUBSCRIBE packets received from clients.                                             |
| Client Unsubscribe               | Total number of UNSUBSCRIBE packets received from clients.                                           |

## Messages Metrics

| Metric                            | Description                                                                                       |
|-----------------------------------|---------------------------------------------------------------------------------------------------|
| Messages Acked                    | Total number of acknowledged messages.                                                            |
| Messages Delayed                  | Messages delayed due to specific routing or delivery rules.                                      |
| Messages Delivered                | Total count of successfully delivered messages.                                                  |
| Messages Dropped                  | Total messages dropped before reaching their destination.                                        |
| Messages Dropped Await_Pubrel_Timeout | Messages dropped due to timeout while waiting for PUBREL packets.                         |
| Messages Dropped No_Subscribers   | Messages dropped because no subscribers were available for them.                                |
| Messages Forward                  | Messages forwarded from one client to another.                                                   |
| Messages Publish                  | Total count of PUBLISH packets sent by clients.                                                  |
| Messages Qos0 Received            | Total QoS 0 (at most once) messages received.                                                    |
| Messages Qos0 Sent                | Total QoS 0 (at most once) messages sent.                                                        |
| Messages Qos1 Received            | Total QoS 1 (at least once) messages received.                                                   |
| Messages Qos1 Sent                | Total QoS 1 (at least once) messages sent.                                                       |
| Messages Qos2 Received            | Total QoS 2 (exactly once) messages received.                                                    |
| Messages Qos2 Sent                | Total QoS 2 (exactly once) messages sent.                                                        |
| Messages Received                 | Total number of messages received from clients.                                                  |
| Messages Retained                 | Total retained messages, which are stored to send to new subscribers of a topic.                 |
| Messages Sent                     | Total number of messages sent to clients.                                                        |

## Packets Metrics

| Metric                             | Description                                                                                         |
|------------------------------------|-----------------------------------------------------------------------------------------------------|
| Packets Auth Received              | Total AUTH packets received, generally part of enhanced authentication mechanisms.                 |
| Packets Auth Sent                  | Total AUTH packets sent, part of the client authentication process.                                |
| Packets Connack Auth_Error         | Number of CONNACK packets indicating an authentication error.                                      |
| Packets Connack Error              | Total CONNACK packets sent due to various errors.                                                  |
| Packets Connack Sent               | Total CONNACK packets successfully sent in response to CONNECT packets.                            |
| Packets Connect Received           | Total number of CONNECT packets received, marking connection attempts by clients.                  |
| Packets Disconnect Received        | Total DISCONNECT packets received from clients.                                                    |
| Packets Disconnect Sent            | Total DISCONNECT packets sent to clients.                                                          |
| Packets Pingreq Received           | Total PINGREQ packets received from clients, often for connection keep-alive.                      |
| Packets Pingresp Sent              | Total PINGRESP packets sent in response to client PINGREQs.                                        |
| Packets Puback Inuse               | Count of PUBACK packets actively in use, acknowledging QoS 1 messages.                             |
| Packets Puback Missed              | Total PUBACK packets missed, indicating potential transmission issues.                             |
| Packets Puback Received            | Total PUBACK packets received, acknowledging QoS 1 messages from clients.                          |
| Packets Puback Sent                | Total PUBACK packets sent to clients, confirming receipt of QoS 1 messages.                        |
| Packets Pubcomp Inuse              | Count of PUBCOMP packets actively in use, completing QoS 2 message exchanges.                      |
| Packets Pubcomp Missed             | Total PUBCOMP packets missed, indicating potential network or processing issues.                   |
| Packets Pubcomp Received           | Total PUBCOMP packets received, finalizing QoS 2 message delivery.                                |
| Packets Pubcomp Sent               | Total PUBCOMP packets sent, completing QoS 2 acknowledgments.                                      |
| Packets Publish Auth_Error         | PUBLISH packets dropped due to authentication errors.                                              |
| Packets Publish Dropped            | Total PUBLISH packets dropped before delivery to subscribers.                                      |
| Packets Publish Error              | Count of errors encountered during PUBLISH operations.                                             |
| Packets Publish Inuse              | Number of PUBLISH packets actively in use.                                                         |
| Packets Publish Received           | Total PUBLISH packets received from clients.                                                       |
| Packets Publish Sent               | Total PUBLISH packets sent to clients.                                                             |
| Packets Pubrec Inuse               | Count of PUBREC packets actively in use, part of QoS 2 delivery.                                   |
| Packets Pubrec Missed              | Total PUBREC packets missed, indicating possible transmission or processing delays.                |
| Packets Pubrec Received            | Total PUBREC packets received, part of QoS 2 acknowledgments.                                      |
| Packets Pubrec Sent                | Total PUBREC packets sent to clients.                                                              |
| Packets Pubrel Missed              | Total PUBREL packets missed, impacting QoS 2 message completion.                                   |
| Packets Pubrel Received            | Total PUBREL packets received, advancing QoS 2 message processing.                                 |
| Packets Pubrel Sent                | Total PUBREL packets sent, progressing QoS 2 message flow.                                         |
| Packets Received                   | Total packets received from clients.                                                               |
| Packets Sent                       | Total packets sent to clients.                                                                     |
| Packets Suback Sent                | Total SUBACK packets sent in response to SUBSCRIBE requests.                                       |
| Packets Subscribe Auth_Error       | SUBSCRIBE packets dropped due to authentication errors.                                            |
| Packets Subscribe Error            | Total SUBSCRIBE packets that encountered errors.                                                   |
| Packets Subscribe Received         | Total SUBSCRIBE packets received, marking client subscription requests.                            |
| Packets Unsuback Sent              | Total UNSUBACK packets sent to confirm unsubscribe requests.                                       |
| Packets Unsubscribe Error          | Count of UNSUBSCRIBE packets that encountered errors.                                              |
| Packets Unsubscribe Received       | Total UNSUBSCRIBE packets received from clients.                                                   |

