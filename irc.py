import sys
import re
import ircconnection


host = 'irc.fi.quakenet.org'
port = 6667
nickname = 'raeq_'
realname = 'th'


if len(sys.argv) >= 2:
	host = sys.argv[1]
if len(sys.argv) >= 3:
	port = sys.argv[2]
if len(sys.argv) >= 4:
	nick = sys.argv[3]

running = True


conn = ircconnection.IrcConnection(host, port, nickname, realname,
	ircconnection.IrcConnection.regexps)
conn.start()

buffer = ''
while(running):
	buf = raw_input('')
	if buf == 'quit':
		conn.close()
		running = False
	elif buf == 'lsu':
		for i in conn.unrecognized_messages:
			print i
	elif buf == 'lsr':
		for i in conn.recognized_messages:
			print i
	elif buf == 'lsb':
		for k, v in conn.buffers.iteritems():
			print '************** %s' % k
			for i in v:
				print i
	elif buf == 'raw':
		raw = raw_input('raw>')
		conn.sock.send('%s\r\n' % raw)
	elif buf == 'help':
		print 'quit/lsu/lsr/lsb/raw'

conn.join()