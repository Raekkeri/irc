
import socket
import re
import threading
import datetime
import ircconnection
import ircregexp
import helpers


host = 'irc.fi.quakenet.org'
port = 6667
nickname = 'raeq_'
realname = 'th'

running = True

class IrcMessage(object):
	def __init__(self, raw_message, timestamp=None):
		if timestamp == None:
			timestamp = datetime.datetime.now()
		self.raw_message = raw_message
		self.timestamp = timestamp


regexps = [ircregexp.RegExpFormat(r[0], r[1]) for r in \
	helpers.parse_regexps_file('regexps.txt', '!<>!')]

regexps.append(ircregexp.RegExpPing(
	re.compile(r'^ping (?P<data>[:aA-zZ0-9]+)', re.IGNORECASE),
	'PONG %(data)s\r\n'))


conn = ircconnection.IrcConnection(host, port, nickname, realname, regexps)
conn.start()

buffer = ''
while(running):
	buf = raw_input('')
	if buf == 'quit':
		conn.close()
		running = False

conn.join()