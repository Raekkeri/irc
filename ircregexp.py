MESSAGE = 10
RESPONSE = 99

class RegExpFormat(object):
	def __init__(self, regexp, format=None):
		if format == None:
			format = 'NO FORMAT'
		self.regexp = regexp
		self.format = format

	def get_match(self, line):
		return self.regexp.match(line)

	def match(self, line):
		match = self.get_match(line)
		return match, MESSAGE

	def get_format(self):
		return self.format


class RegExpPing(RegExpFormat):
	def match(self, line):
		match = RegExpFormat.get_match(self, line)
		return match, RESPONSE
