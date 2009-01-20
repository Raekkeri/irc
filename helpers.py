import re

def parse_regexps_file(filename, separator):
	regexps = []
	try:
		handle = open(filename, 'r')
	except Exception, e:
		raise e
	try:
		for line in handle:
			items = line.split(separator)
			if len(items) == 2:
				try:
					regexp = re.compile(items[0])
				except Exception:
					continue
				regexps.append((regexp, items[1]))
	finally:
		handle.close()
	return regexps



sep = '!<>!'
file = 'regexps.txt'
