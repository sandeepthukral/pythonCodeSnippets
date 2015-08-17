from sys import argv
import re
inport pprint

filename = "C:\\dev\\workspaces\\11S05\\oscar-service\\src\\test\\groovy\\nl\\tele2\\oscar\\script\\whitelist-data.csv"

# read the file and split into lines
content = open(filename,'r').read()
lines = content.rsplit()

# regexp for finding houseNumber
regexpPostCodeStart = re.compile(r'(.*,.*,.*,.*,)(\d\d)(\d\d.*)')

# iterate over the list, identify unique postcodeprefix
postcodePrefixes = []

for i in range(len(lines)):
	mo = regexpPostCodeStart.search(lines[i])
	matchedPrefix = mo.group(2)
	if matchedPrefix not in postcodePrefixes:
		postcodePrefixes.append(matchedPrefix)

postcodePrefixes.sort()

pprint.pprint(postcodePrefixes)