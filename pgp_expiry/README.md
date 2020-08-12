# Monitoring Expiry days for PGP public keys

To monitor the number of days to expire for the public keys in PGP. For more details regarding pgp key configurations, please refer https://packaging.ubuntu.com/html/getting-set-up.html

### Prerequisites
python-gnupg driver

to install the driver to the python path, use the following command

/usr/bin/python -m pip install python-gnupg

For more details on the python-gnupg driver , refer https://pypi.org/project/python-gnupg/#description

### Configurations

keys_to_check - the absolute path of file name containing the gpg public keys to check
key_server - key server name - default : "keyserver.ubuntu.com"
gpg_location - gpg location - default "/home/local/.gnupg"
plugin_version = 1
heartbeat = True

### Metrics Captured
    keyname - No of days for expiry from today
