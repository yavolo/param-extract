import glob
import sys
import re

def getParams(regexstr, content):
	regexcomp = re.compile(r"" + regexstr +"")
	params = re.findall(regexcomp, content)
	return params

regexlist = []

with open("./regex", 'r') as f:
	for line in f.readlines():
		regexlist.append(line.rstrip())

if len(sys.argv) >= 3:
	wwwrootpath = sys.argv[1] +  '/**/*.*'	
	siteurl = sys.argv[2]
	payload = sys.argv[3]

else:
	print('Missing argument variables. wwwroot siteurl payload')
	exit()

filepaths = glob.iglob((wwwrootpath), recursive=True)

for filename in filepaths:
	content = ""
	print(filename)
	with open(filename, 'r') as f:
		for line in f.read():
			content += line

	for x in range(0, len(regexlist)):
		phpparams = getParams(str(regexlist[x]), content)

		for param in phpparams:
			test = siteurl + filename + "?" + param[1] + "=" + payload
			print(test)
