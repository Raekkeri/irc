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
		self.unrecognized_messages = list()
		self.recognized_messages = list()

		self.message_handlers = {
			ircregexp.MESSAGE: self.handle_message,
			ircregexp.RESPONSE: self.send_response
		}

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
		total_matches = 0
		for r in self.regexps:
			match, msg_type = r.match(line)
			if match:
				total_matches += self.message_handlers[msg_type](match, r)

		if total_matches == 0:
			print 'NO MATCH: %s' % line
			self.unrecognized_messages.append(line)

	def send_response(self, match, regexp):
		sendbuf = regexp.get_format() % match.groupdict()
		self.sock.send(sendbuf)
		return 0

	def handle_message(self, match, regexp):
		s = regexp.get_format() % match.groupdict()
		recognized_messages.append(s)
		print s
		return 1
