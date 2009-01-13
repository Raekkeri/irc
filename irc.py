
import socket
import re



s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('irc.quakenet.org', 6667))

s.send('NICK %s\r\n' % 'raeq_')
s.send('USER %s %s bla :%s\r\n' % ('raeq_', 'irc.quakenet.org', 'teemu'))

rexps = (
)

ping = re.compile(r'ping :(?P<data>\w+)', re.IGNORECASE)

buffer = ''
while(1):
	buffer += s.recv(512)
	li = buffer.split('\r\n')
	buffer = li.pop()

	for line in li:
		match = ping.match(line)
		if match:
			sendbuf = 'PONG :%s' % match.group('data')
			s.send(sendbuf)
			print 'SENT: %s' % sendbuf
		else:
			print 'NOT HANDLED: %s' % line
