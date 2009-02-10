
import re
import ircconnection
import ircregexp
import helpers


host = 'irc.fi.quakenet.org'
port = 6667
nickname = 'raeq_'
realname = 'th'

running = True

regexps = [ircregexp.RegExpFormat(r[0], r[1]) for r in \
	helpers.parse_regexps_file('regexps.txt', '!<>!')]

regexps.append(ircregexp.RegExpPing(
	re.compile(r'^ping (?P<data>[:aA-zZ0-9]+)', re.IGNORECASE),
	'PONG %(data)s\r\n'))


conn = ircconnection.IrcConnection(host, port, nickname, realname, regexps)
conn.start()

buffer = ''
while(running):
	buf = raw_input('quit/lsu/lsr/raw>')
	if buf == 'quit':
		conn.close()
		running = False
	elif buf == 'lsu':
		for i in conn.unrecognized_messages:
			print i
	elif buf == 'lsr':
		for i in conn.recognized_messages:
			print i
	elif buf == 'raw':
		raw = raw_input('raw>')
		conn.sock.send('%s\r\n' % raw)

conn.join()