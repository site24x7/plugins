# WordPress Site Health Monitor

## About WordPress

WordPress is a free and open-source content management system (CMS) written in PHP and paired with a MySQL or MariaDB database, with support for HTTPS. Features include a plugin architecture and a template system referred to as "Themes."

WordPress is a powerful CMS that enables you to manage your website’s content efficiently. It is used by over 74 million websites of all types and sizes to publish fresh content every second.

---

## Prerequisites

1. Download and install the latest version of the [Site24x7 Linux Agent](https://www.site24x7.com/app/client#/admin/inventory/add-monitor) on the server where you plan to run the plugin.
2. Ensure your WordPress site uses HTTPS and generate an application password.
   - To generate an application password, follow this [documentation](https://wordpress.com/support/security/two-step-authentication/application-specific-passwords/).

---

## Plugin Installation

1. Create a directory named `wordpress_site_health_monitoring`:

    ```bash
    mkdir wordpress_site_health_monitoring
    ```

2. Download the required files into the newly created directory:

    ```bash
    wget https://raw.githubusercontent.com/site24x7/plugins/master/wordpress_site_health_monitoring/wordpress_site_health_monitoring.cfg
    wget https://raw.githubusercontent.com/site24x7/plugins/master/wordpress_site_health_monitoring/wordpress_site_health_monitoring.py
    ```

3. Update the Python path in the `wordpress_site_health_monitoring.py` script by following [this guide](https://support.site24x7.com/portal/en/kb/articles/updating-python-path-in-a-plugin-script-for-linux-servers).

4. Run the following command to validate the setup and ensure the plugin outputs valid JSON:

    ```bash
    python3 wordpress_site_health_monitoring.py --url="https://Domain or Website/" --username="WordPress Username" --application_password="Application Password"
    ```

---

## Configuration

1. Open the `wordpress_site_health_monitoring.cfg` file and provide your WordPress site configuration:

    ```ini
    [wordpress]
    url="https://localhost/wordpress/"
    username="wordpress_username"
    application_password="application_password"
    ```
2. For multiple server tracking, use the following configuration:

    ```ini
    [wordpress_site1]
    url="https://localhost/wordpress/"
    username="wordpress_username"
    application_password="application_password"

    [wordpress_site2]
    url="https://localhost/wordpress/"
    username="wordpress_username"
    application_password="application_password"
    ```

   **Notes:**
   - Ensure the WordPress username has administrator privileges or API access.
   - Use the application password generated in **Admin Login > Users > All Users > Application Passwords**. **Do not use the user's account password.**

3. Move the plugin under the Site24x7 agent directory

#### Linux

- Move the "wordpress_site_health_monitoring" directory under the Site24x7 Linux Agent plugin directory: 

```bash
mv wordpress_site_health_monitoring /opt/site24x7/monagent/plugins/
```
		
#### Windows

- Move the "wordpress_site_health_monitoring" directory under the Site24x7 Windows Agent plugin directory:

```
C:\Program Files (x86)\Site24x7\WinAgent\monitoring\Plugins\
```
The agent will automatically execute the plugin within five minutes and user can see the plugin monitor under Site24x7 > Plugins > Plugin Integrations.

---

## Supported Metrics

| Metric               | Description                                  |
|----------------------|----------------------------------------------|
| `authorization-header` | Monitors the availability of the Authorization header. |
| `background-updates`   | Verifies if WordPress background updates are functioning. |
| `dotorg-communication` | Checks WordPress communication with WordPress.org. |
| `https-status`         | Confirms if the site is using HTTPS correctly. |
| `loopback-requests`    | Validates loopback requests for WordPress functionality. |

---
