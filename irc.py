
import socket
import re
import threading
import helpers

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

class RegExpFormat(object):
	def __init__(self, regexp, format=None):
		if format == None:
			format = 'NO FORMAT'
		self.regexp = regexp
		self.format = format

	def match(self, line):
		match = self.regexp.match(line)
		return match

	def get_format(self):
		return self.format


class RegExpPing(RegExpFormat):
	def __init__(self, regexp, format):
		RegExpFormat.__init__(self, regexp, format)

	def match(self, line):
		#match = RegExpFormat.match(line)
		#return match
		# What to do here!!!!!
		pass


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, 6667))

s.send('NICK %s\r\n' % 'raeq_')
s.send('USER %s %s bla :%s\r\n' % ('raeq', '0', 'teemu husso'))

regexps = [RegExpFormat(r[0], r[1]) for r in \
	helpers.parse_regexps_file('regexps.txt', '!<>!')]

ping = re.compile(r'^ping (?P<data>[:aA-zZ0-9]+)', re.IGNORECASE)
#numeric_response = re.compile(':[aA-zZ\.:]+ (?P<code>[0-9]+)')
#notice_auth = re.compile(r'notice auth', re.IGNORECASE)

buffer = ''
while(running):
	buffer += s.recv(512)
	li = buffer.split('\r\n')
	buffer = li.pop()

	for line in li:
		match_found = False
		for r in regexps:
			match = r.match(line)
			if match:
				if match_found:
					print "DOUBLE MATCH: %s" \
						% r.regexp.pattern
				print r.get_format() % match.groupdict()
				match_found = True
		if not match_found:
			match = ping.match(line)
			if match:
				print line
				sendbuf = 'PONG %s\r\n' % match.group('data')
				s.send(sendbuf)
				print 'SENT: %s' % sendbuf
				continue

			print 'NO MATCH: %s' % line
