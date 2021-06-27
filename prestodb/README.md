# Plugin for monitoring PrestoDB

This plugin monitors the collection of detailed performance-oriented metrics throughout the life cycle of Presto service and its various components.

### Prerequisites

- Download and install the latest version of the [Site24x7 Linux agent] / [Site24x7 Windows agent] (https://www.site24x7.com/app/client#/admin/inventory/add-monitor) in the server where you plan to run the plugin.

- Plugin Uses "JPype" python library. This module is used to execute the jmx query and get data. Execute the below command to install python JPype modeule in your server.

      pip install JPype1

- Configure the JMX Port in the etc/config.properties file in the PresodDB installation folder

      jmx.rmiregistry.port=36799

### Plugin installation

---

##### Linux

- Create a directory "prestodb" under Site24x7 Linux Agent plugin directory :

      Linux             ->   /opt/site24x7/monagent/plugins/prestodb

- Download all the files in "prestodb" folder and place it under the "prestodb" directory

      wget https://raw.githubusercontent.com/site24x7/plugins/master/prestodb/prestodb.py
      wget https://raw.githubusercontent.com/site24x7/plugins/master/prestodb/prestodb.cfg
  
- Configure the host and port of the prestodb to be montiored in prestodb.cfg, as mentioned in the configuration section below..

- Execute the below command with appropriate arguments to check for the valid json output.

      python prestodb.py --host=localhost --port=36799

The agent will automatically execute the plugin within five minutes and send performance data to the Site24x7 data center.

### Configurations

---

    [display_name]
    host = “<your_host_name>”
    port = “<port number you mentioned in etc/config.properties>”

### Metrics Captured

---

      execution_abandoned_queries_total_count       ->      Total number of abandoned queries
      execution_canceled_queries_total_count        ->      Total number of canceled queries
      execution_completed_queries_total_count       ->      Total number of completed queries
      execution_consumed_cpu_time_secs_total_count  ->      Total time(seconds) of CPU(processing) time consumed
      execution_started_queries_total_count         ->      Total number of started queries
      executor_active_count                         ->      Number of active executor
      executor_completed_task_count                 ->      Number of completed tasks in executor
      executor_core_pool_size                       ->      Core pool size of executor
      executor_largest_pool_size                    ->      Largest pool size of executor
      executor_maximum_pool_size                    ->      Maximum pool size of executor
      executor_queued_task_count                    ->      Queued task count of executor
      executor_task_count                           ->      Task count of executor
      failure_detector_active_count                 ->      Number of active nodes
      cluster_memory_bytes                          ->      Cluster memory size shown in bytes
      memory_assigned_queries                       ->      Memory of assigned queries shown as byte
      memory_blocked_nodes                          ->      Memory of blocked nodes shown as byte
      memory_free_distributed_bytes                 ->      Memory of free distributed bytes shown as byte
      memory_nodes                                  ->      Memory of nodes shown as byte
      memory_reserved_distributed_bytes             ->      Memory of reserved distributed bytes shown as byte
      memory_reserved_revocable_distributed_bytes   ->      Memory of reserved revocable distributed bytes shown as byte
      memory_total_distributed_bytes                ->      Memory of total distributed bytes shown as byte
      memory_free_bytes                             ->      Memory of free bytes shown as byte
      memory_max_bytes                              ->      Memory of max bytes shown as byte
      memory_reserved_bytes                         ->      Memory of reserved bytes shown as byte
      memory_reserved_revocable_bytes               ->      Memory of reserved revocable bytes shown as byte
