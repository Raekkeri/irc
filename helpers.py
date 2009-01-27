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
					regexp = re.compile(items[0],
						re.IGNORECASE)
				except Exception:
					continue
				format = items[1].strip('\n\r')
				regexps.append((regexp, format))
	finally:
		handle.close()
	return regexps



sep = '!<>!'
file = 'regexps.txt'
