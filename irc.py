
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


class Keyboard(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		while (1):
			buf = raw_input('')
			if (buf == 'q'):
				running = False
			if (buf == 'n'):
				s.send('NICK %s\r\n' % 'raeq_')
			if (buf == 'u'):
				s.send('USER %s %s bla :%s\r\n' % \
					('raeq', '0', 'teemu husso'))

Keyboard().start()


regexps = [ircregexp.RegExpFormat(r[0], r[1]) for r in \
	helpers.parse_regexps_file('regexps.txt', '!<>!')]


conn = ircconnection.IrcConnection(host, port, nickname, realname, regexps)
conn.start()

buffer = ''
while(running):
	pass
