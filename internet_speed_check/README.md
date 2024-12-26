Plugin for Monitoring the Internet speed 
========================================

### PreRequisites

- Download and install the latest version of the [Site24x7 Linux agent] (https://www.site24x7.com/help/admin/adding-a-monitor/linux-server-monitoring.html#add-linux-server-monitor) in the server where you plan to run the plugin. 

- Plugin Uses "speedtest" python module.
	
- How to install speedtest :
  
      python2:    python -m pip install --upgrade pip speedtest-cli
      python3:    python3 -m pip install --upgrade pip speedtest-cli
      if pip command not present kindly install using the below section

- How to install pip :
      curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
      python get-pip.py

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
    wget https://raw.githubusercontent.com/site24x7/plugins/master/internet_speed_check/speedtest-cli.zip
    ```

3. **Extract speedtest-cli.zip**:
    ```
    mkdir -p speedtest-cli
    unzip speedtest-cli.zip -d speedtest-cli
    ```

4. **Ensure the directory structure**:
    ```
    internet_speed_check
    ├── internet_speed_check.py
    ├── speedtest-cli
    ```

5. **Update Python Path**: Follow the steps in this article to update the Python path in the `internet_speed_check.py` script:
    https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers

6. **Verify the script**:
    ```
    python internet_speed_check.py
    ```

7. **Move the directory** under the Site24x7 Linux Agent plugin directory:
    ```
    mv internet_speed_check /opt/site24x7/monagent/plugins/
    ```

    The Site24x7 agent will automatically execute the plugin within five minutes, and you can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

### For Windows

1. **Download the required files**:
    - `internet_speed_check.py`
    - `speedtest-cli.zip`

2. **Create a directory**:
    ```
    mkdir internet_speed_check
    ```

3. **Place the downloaded files** inside the `internet_speed_check` directory.

4. **Extract speedtest-cli.zip**.

5. **Ensure the directory structure**:
    ```
    internet_speed_check
    ├── internet_speed_check.py
    ├── speedtest-cli
    ```

6. **Verify the script**:
    ```
    python internet_speed_check.py
    ```

7. **Move the directory** under the Site24x7 Windows Agent plugin directory:
    ```
    C:\Program Files (x86)\Site24x7\monagent\plugins\internet_speed_check
    ```

The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.


### Metrics Captured
---

upload - Upload speed of your internet connection

download - Download speed of your internet connection

ping - Reaction time of your internet connection
