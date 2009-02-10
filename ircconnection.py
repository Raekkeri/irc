import threading
import socket
import re
import ircregexp
import datetime


class IrcMessage(object):
	def __init__(self, raw_message, timestamp=None):
		if timestamp == None:
			timestamp = datetime.datetime.now()
		self.raw_message = raw_message
		self.timestamp = timestamp

	def __str__(self):
		return '<%s> %s' % (self.timestamp.strftime('%H:%M:%S'),
			self.raw_message)


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
		self.buffers = dict()

		self.message_handlers = {
			ircregexp.MESSAGE: self.handle_message,
			ircregexp.RESPONSE: self.send_response
		}

		self.connected = False

	def close(self):
		self.sock.shutdown(socket.SHUT_RDWR)
		self.connected = False

	def run(self):
		self.sock.connect((self.host, self.port))
		self.sock.send('NICK %s\r\n' % self.nickname)
		self.sock.send('USER %s 0 bla :%s\r\n' % (self.nickname,
			self.realname))

		self.connected = True
		buffer = ''
		while self.connected:
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
			msg = IrcMessage(line)
			self.unrecognized_messages.append(msg)

	def send_response(self, match, regexp):
		sendbuf = regexp.get_format() % match.groupdict()
		self.sock.send(sendbuf)
		return 0

	def handle_message(self, match, regexp):
		groupdict = match.groupdict()
		s = regexp.get_format() % groupdict
		msg = IrcMessage(s)
		if 'target' in groupdict:
			target = groupdict['target']
			if target in self.buffers:
				self.buffers[target].append(msg)
			else:
				self.buffers[target] = [msg]

		self.recognized_messages.append(msg)
		print s
		return 1
