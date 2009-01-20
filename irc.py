
import socket
import re
import threading

host = 'irc.fi.quakenet.org'

running = True

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


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, 6667))

s.send('NICK %s\r\n' % 'raeq_')
s.send('USER %s %s bla :%s\r\n' % ('raeq', '0', 'teemu husso'))

rexps = (
)

ping = re.compile(r'^ping (?P<data>[:aA-zZ0-9]+)', re.IGNORECASE)
numeric_response = re.compile(':[aA-zZ\.:]+ (?P<code>[0-9]+)')
#notice_auth = re.compile(r'notice auth', re.IGNORECASE)

registered = False

buffer = ''
while(running):
	buffer += s.recv(512)
	li = buffer.split('\r\n')
	buffer = li.pop()

	for line in li:
		match = ping.match(line)
		if match:
			print line
			sendbuf = 'PONG %s\r\n' % match.group('data')
			s.send(sendbuf)
			print 'SENT: %s' % sendbuf
			continue

		print 'NO MATCH: %s' % line
