Plugin for Monitoring the Internet speed 
========================================

### PreRequisites

- Download and install the latest version of the [Site24x7 Linux agent](https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "speedtest-cli" python module.
	
Plugin Installation
-------------------

### For Linux

1. **Create a directory**:
    ```
    mkdir internet_speed_check
    ```

2. **Download the required files**:
    ```
    wget https://raw.githubusercontent.com/site24x7/plugins/master/internet_speed_check/internet_speed_check.py
    wget https://raw.githubusercontent.com/site24x7/plugins/master/internet_speed_check/speedtest-cli.pyz
    ```

3. **Ensure the directory structure**:
    ```
    internet_speed_check
    ├── internet_speed_check.py
    ├── speedtest-cli.pyz
    ```

4. **Update Python Path**: Follow the steps in this article to update the Python path in the `internet_speed_check.py` script:
    https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers

5. **Verify the script**:
    ```
    python internet_speed_check.py
    ```

6. **Move the directory** under the Site24x7 Linux Agent plugin directory:
    ```
    mv internet_speed_check /opt/site24x7/monagent/plugins/
    ```

    The Site24x7 agent will automatically execute the plugin within five minutes, and you can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### For Windows

1. **Download the required files**:
    - [`internet_speed_check.py`](https://raw.githubusercontent.com/site24x7/plugins/master/internet_speed_check/internet_speed_check.py)
    - [`speedtest-cli.pyz`](https://raw.githubusercontent.com/site24x7/plugins/master/internet_speed_check/speedtest-cli.pyz)

2. **Create a directory**:
    ```
    mkdir internet_speed_check
    ```

3. **Place the downloaded files** inside the `internet_speed_check` directory.

4. **Ensure the directory structure**:
    ```
    internet_speed_check
    ├── internet_speed_check.py
    ├── speedtest-cli.pyz
    ```

5. **Verify the script**:
    ```
    python internet_speed_check.py
    ```

6. **Move the directory** under the Site24x7 Windows Agent plugin directory:
    ```
    C:\Program Files (x86)\Site24x7\monagent\plugins\
    ```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


### Metrics Captured
---

| Metric   | Description                                |
|----------|--------------------------------------------|
| upload   | Upload speed of your internet connection   |
| download | Download speed of your internet connection |
| ping     | Reaction time of your internet connection  |
