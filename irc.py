
import socket
import re

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('irc.oamk.fi', 6667))

s.send('NICK %s\r\n' % 'raeq_')
s.send('USER %s %s bla :%s\r\n' % ('raeq_', 'irc.oamk.fi', 'teemu'))


buffer = ''
split = buffer.split
while(1):
	buffer += s.recv(512)
	li = buffer.split('\r\n')
	buffer = li.pop()

	for i in li:
		print i

