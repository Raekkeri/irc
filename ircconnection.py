import threading
import socket
import re
import ircregexp

class IrcConnection(threading.Thread):
	def __init__(self, host, port, nickname, realname, regexps):
		threading.Thread.__init__(self)
		self.host = host
		self.port = port
		self.nickname = nickname
		self.realname = realname
		self.regexps = regexps
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.unrecognized_messages = []
		
		
		ping = re.compile(r'^ping (?P<data>[:aA-zZ0-9]+)', \
			re.IGNORECASE)
		self.regexps.append(ircregexp.RegExpPing(
			ping, 'PONG %(data)s\r\n'))

	def run(self):
		self.sock.connect((self.host, self.port))
		self.sock.send('NICK %s\r\n' % self.nickname)
		self.sock.send('USER %s 0 bla :%s\r\n' % (self.nickname,
			self.realname))

		connected = True
		buffer = ''
		while connected:
			buffer += self.sock.recv(512)
			li = buffer.split('\r\n')
			buffer = li.pop()

			for line in li:
				self.handle_line(line)

	def handle_line(self, line):
		match_found = False
		for r in self.regexps:
			(match, type) = r.match(line)
			if match:
				if type == ircregexp.MESSAGE:
					if match_found:
						print "DOUBLE MATCH: %s" \
							% r.regexp.pattern
					print r.get_format() \
						% match.groupdict()
					match_found = True
				elif type == ircregexp.RESPONSE:
					sendbuf = r.get_format() % \
						match.groupdict()
					self.sock.send(sendbuf)
					print 'SENT: %s' % sendbuf
		if not match_found:
			print 'NO MATCH: %s' % line
			self.unrecognized_messages.append(line)
