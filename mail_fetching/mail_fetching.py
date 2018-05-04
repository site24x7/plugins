'''
Created on 04-May-2018

@author: giri
'''
import json
import traceback
import poplib
from email.mime.text import MIMEText

#POP SERVER CONFIGURATIONS
POP_SERVER = "<POP_SERVER_NAME>"
POP_PORT = "<POP_SERVER_PORT>"
POP_ENABLED = 1

#IMAP SERVER CONFIGURATIONS
IMAP_SERVER = "<IMAP_SERVER_NAME>"
IMAP_PORT = "<IMAP_SERVER_PORT>"
IMAP_ENABLED = 1

if IMAP_ENABLED == 1:
	import imaplib

#credentials
USERNAME = "demo+enterprise@site24x7.com"
PASSWORD = "s247demo"


PLUGIN_VERSION = "1"

# Setting this to true will alert you when there is a communication problem while posting plugin data to server
HEARTBEAT = "true"


result_json = {}
result_json["plugin_version"] = PLUGIN_VERSION
result_json["heartbeat_required"] = HEARTBEAT
result_json["status"] = 1

sender = USERNAME
destination = [USERNAME]


def log_helper(func):
	def wrapper(*args, **kwargs):
		try:
			func()
		except Exception as e:
			if func.__name__ == "handle_pop":
				result_json["POP_STATUS"] = 0
			elif func.__name__ == "handle_imap":
				result_json["IMAP_STATUS"] = 0
			else:
				if POP_ENABLED == 1:
					result_json["POP_STATUS"] = 0
				if IMAP_ENABLED == 1:
					result_json["IMAP_STATUS"] = 0
			result_json["status"] = 0
			result_json["msg"] = repr(e)
	return wrapper

@log_helper
def handle_pop():
	Mailbox = poplib.POP3_SSL(POP_SERVER, int(POP_PORT))
	Mailbox.user(USERNAME) 
	Mailbox.pass_(PASSWORD)
	stats = Mailbox.stat()
	content = Mailbox.retr(stats[0])
	result_json["POP_STATUS"] = 1

@log_helper
def handle_imap():
	mail = imaplib.IMAP4_SSL(IMAP_SERVER, int(IMAP_PORT))
	mail.login(USERNAME, PASSWORD)
	mail.list()
	result_json["IMAP_STATUS"] = 1

@log_helper
def mail_fetching():
	if POP_ENABLED == 1:
		handle_pop()
	if IMAP_ENABLED == 1:
		handle_imap()


if __name__ == '__main__':
	mail_fetching()
	print(json.dumps(result_json))


