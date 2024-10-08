# Kafka Topics Monitoring
                                                                                              
## Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent/Site24x7 Windows agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

## Quick installation

If you're using Linux servers, use the Kafka_topics plugin installer that checks the prerequisites and installs the plugin with a bash script. You don't need to manually set up the plugin if you're using the installer.

Execute the command below in the terminal to run the installer and follow the instructions displayed on-screen:

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/refs/heads/master/kafka/kafka_topics/installer/Site24x7KafkaTopicsPluginInstaller.sh && sudo bash Site24x7KafkaTopicsPluginInstaller.sh
```
## Standard Installation
If you're not using Linux servers or want to install the plugin manually, follow the steps below.

### Plugin Installation  

- Create a directory named `kafka_topics`.
  
```bash
mkdir kafka_topics
cd kafka_topics/
```
      
- Download below files and place it under the "kafka_topics" directory.

```bash
wget https://raw.githubusercontent.com/site24x7/plugins/refs/heads/master/kafka/kafka_topics/kafka_topics.py && sed -i "1s|^.*|#! $(which python3)|" kafka.py
wget https://raw.githubusercontent.com/site24x7/plugins/refs/heads/master/kafka/kafka_topics/kafka_topics.cfg
```

- Execute the below command with appropriate arguments to check for the valid json output:

```bash
python kafka_topics.py --kafka_host "localhost" --kafka_jmx_port "9999" --kafka_server_port "9092" --kafka_topic_name "quickstart-events" --kafka_home "/home/users/kafka"
```

- Provide your Kafka topics configurations in kafka_topics.cfg file.

```bash
[kafka_instance]
kafka_host="localhost"
kafka_jmx_port=9999
kafka_server_port=9092
kafka_topic_name="quickstart-events"
kafka_home="/home/users/kafka"
```

- Since it's a Python plugin, to run the plugin in a Windows server please follow the steps in [this link](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers). The remaining configuration steps are the same.

### Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "kafka_topics" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv kafka_topics /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "kafka_topics" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.
