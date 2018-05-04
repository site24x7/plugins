'''
Created on 04-May-2018

@author: giri
'''
import json
import traceback
import smtplib
from email.mime.text import MIMEText
import poplib

#SMTP SERVER CONFIGURATIONS
SMTP_SERVER = "<SMTP_SERVER_NAME>"
SMTP_PORT = "<SMTP_SERVER_PORT>"


USERNAME = "<SMTP_USERNAME>"
PASSWORD = "<SMTP_PASSWORD>"


PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"


result_json = {}
result_json["plugin_version"] = PLUGIN_VERSION
result_json["heartbeat_required"] = HEARTBEAT
result_json["status"] = 1

sender = USERNAME
destination = [USERNAME]

text_subtype = 'plain'


content="""\
Mail server check
"""

subject="Sent from site24x7 agent"


def log_helper(func):
	def wrapper(*args, **kwargs):
		try:
			func()
		except Exception as e:
			result_json["status"] = 0
			result_json["msg"] = e
	return wrapper

@log_helper
def send_mail():
	try:
		msg = MIMEText(content, text_subtype)
		msg['Subject']= subject
		conn = smtplib.SMTP(SMTP_SERVER, int(SMTP_PORT))
		conn.ehlo()
		conn.starttls()
		conn.login(USERNAME, PASSWORD, None)
		conn.sendmail(sender, destination, msg.as_string())
		result_json["SMTP_STATUS"] = 1
	except Exception as e:
		result_json["SMTP_STATUS"] = 0
		result_json["status"] = 0
		result_json["msg"] = repr(e)

@log_helper
def smtp_monitoring():
	send_mail()
	print(json.dumps(result_json))


if __name__ == '__main__':
	smtp_monitoring()

