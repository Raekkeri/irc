
import socket
import re

host = 'irc.fi.quakenet.org'

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, 6667))

s.send('NICK %s\r\n' % 'raeq_')
#s.send('USER %s %s bla :%s\r\n' % ('raeq', 'whatnot', 'teemu husso'))

rexps = (
)

ping = re.compile(r'ping :(?P<data>\w+)', re.IGNORECASE)
#notice_auth = re.compile(r'notice auth', re.IGNORECASE)

buffer = ''
while(1):
	buffer += s.recv(512)
	li = buffer.split('\r\n')
	buffer = li.pop()
	print 'BUFFER: %s<' % buffer

	for line in li:
		match = ping.match(line)
		if match:
			sendbuf = 'PONG :%s' % match.group('data')
			s.send(sendbuf)
			print 'SENT: %s' % sendbuf
			continue

		print 'NOT HANDLED: %s' % line