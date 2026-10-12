# Pinecone Monitoring

[Pinecone](https://www.pinecone.io/) is a fully managed, cloud-native vector database used for similarity search, retrieval-augmented generation (RAG), and other embedding-based workloads. This plugin auto-discovers every index in a Pinecone project and reports index health, capacity, and configuration metrics to Site24x7 - no index names or endpoints need to be entered manually.

## Prerequisites

- Download and install the latest version of the [Site24x7 Server Monitoring agent](https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) on the server where you plan to run the plugin.

- A Pinecone API key with read access to the project you want to monitor.

## API Key Creation

1. Log in to the [Pinecone console](https://app.pinecone.io/).
2. Open your project, then navigate to **API Keys**.
3. Create a new key (or use an existing one) with at least read access.
4. Copy the key - it is shown only once.

## Plugin Installation

### Linux

- Create a directory named `pinecone_monitoring`.

		mkdir pinecone_monitoring
		cd pinecone_monitoring/

- Download the plugin files into the `pinecone_monitoring` directory:

		wget https://raw.githubusercontent.com/site24x7/plugins/master/pinecone_monitoring/pinecone_monitoring.py
		wget https://raw.githubusercontent.com/site24x7/plugins/master/pinecone_monitoring/pinecone_monitoring.cfg

- Execute the below command with the appropriate arguments to confirm valid JSON output:

		python3 pinecone_monitoring.py --api_key 'your-pinecone-api-key' --api_version '2025-10'

- Update your Pinecone configuration in the `pinecone_monitoring.cfg` file. On Linux, set `use_agent_python=1` so the Site24x7 agent runs the plugin with its own bundled Python interpreter (which already includes `requests`):

		[global_configurations]
		use_agent_python=1

		[pinecone_monitoring]
		api_key = "your-pinecone-api-key"
		api_version = "2025-10"

- Move the `pinecone_monitoring` directory under the Site24x7 Linux Agent plugin directory:

		mv pinecone_monitoring /opt/site24x7/monagent/plugins/

### Windows

To run a Python-based plugin on a Windows server, follow the steps in [this article](https://support.site24x7.com/portal/en/kb/articles/run-python-plugin-scripts-in-windows-servers) to set up the required wrapper before continuing below.

- Create a directory named `pinecone_monitoring`.

- Place `pinecone_monitoring.py` and `pinecone_monitoring.cfg` under the `pinecone_monitoring` directory.

- Install the required Python package:

		pip install requests

- Execute the below command with the appropriate arguments in `cmd` or PowerShell to confirm valid JSON output:

		python pinecone_monitoring.py --api_key "your-pinecone-api-key" --api_version "2025-10"

- Update your Pinecone configuration in the `pinecone_monitoring.cfg` file. The `use_agent_python` option does **not** apply on Windows - the Windows agent has no bundled Python, so the system Python is used:

		[pinecone_monitoring]
		api_key = "your-pinecone-api-key"
		api_version = "2025-10"

- Move the `pinecone_monitoring` folder under the Site24x7 Windows Agent plugin directory:

		C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins

The agent will automatically execute the plugin within five minutes, and you can view the plugin monitor under **Site24x7 > Plugins > Plugin Integrations**.

## Configuration Parameters

| Parameter | Description | Default |
| --- | --- | --- |
| `api_key` | Your Pinecone API key with read access to the project. | - |
| `api_version` | Pinecone API version header sent with every request. | `2025-10` |

## Supported Metrics

### Cluster Overview

Name					|	Unit		|	Description
---					|	---		|	---
Index Count				|	indexes		|	Total number of indexes found in the Pinecone project
Ready Indexes				|	indexes		|	Number of indexes currently in a ready state
Not Ready Indexes			|	indexes		|	Number of indexes that are not yet ready to serve requests
Total Vectors				|	vectors		|	Sum of vector counts across all indexes in the project
Total Namespaces			|	namespaces	|	Sum of namespace counts across all indexes

### Capacity

Name					|	Unit		|	Description
---					|	---		|	---
Average Vectors Per Index		|	vectors		|	Average number of vectors per index across the project
Indexes With Zero Vectors		|	indexes		|	Number of indexes currently holding no vectors
Average Index Fullness			|	percent		|	Average index fullness across all indexes (serverless indexes report `0`)
Maximum Index Fullness			|	percent		|	Highest fullness percentage among all indexes

### Configuration

Name					|	Unit		|	Description
---					|	---		|	---
Serverless Indexes			|	indexes		|	Number of serverless-type indexes
Pod Based Indexes			|	indexes		|	Number of pod-based indexes
Average Dimension			|	dimensions	|	Average vector dimension across all indexes
Unique Regions				|	regions		|	Number of distinct cloud regions in use
Unique Cloud Providers			|	providers	|	Number of distinct cloud providers in use
Indexes Failed To Respond		|	indexes		|	Number of indexes whose `describe_index_stats` call failed

### Imports

Name					|	Unit		|	Description
---					|	---		|	---
Active Imports				|	imports		|	Number of bulk import jobs currently pending or in progress (serverless indexes only)
Completed Imports			|	imports		|	Number of bulk import jobs that completed successfully
Failed Imports				|	imports		|	Number of bulk import jobs that failed
Cancelled Imports			|	imports		|	Number of bulk import jobs that were cancelled

### Index Details

Name					|	Description
---					|	---
name					|	Name of the index
Vector_Count				|	Number of vectors stored in this index
Dimension				|	Vector dimension configured for this index
Index_Fullness				|	Fullness percentage for this index (serverless indexes report `0`)
Metric					|	Distance metric used by the index (`cosine`, `dotproduct`, or `euclidean`)
Vector_Type				|	Vector type used by the index (`dense` or `sparse`)
Cloud					|	Cloud provider hosting the index (`aws`, `gcp`, `azure`)
Region					|	Cloud region where the index is hosted
Ready_Status				|	Whether this index is ready to serve requests (`Ready` or `Not Ready`)

### Namespace Details

Name					|	Description
---					|	---
name					|	Combined `<index>_<namespace>` identifier for this row
Index					|	Name of the index the namespace belongs to
Namespace				|	Namespace name (`(default)` for the unnamed default namespace)
Vector_Count				|	Number of vectors stored in this namespace

## Sample Image

<img width="3282" height="1689" alt="image" src="https://github.com/user-attachments/assets/f9ba5c86-cb3b-46cc-8c3d-d6a66c29086e" />

<img width="3282" height="1689" alt="image" src="https://github.com/user-attachments/assets/72c2e48b-6400-499a-8edf-b86d9bd9b26d" />

