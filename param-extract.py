import glob
import sys
import re

def getParams(regex, content):
	params = re.findall(regex, content)
	return params


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
	with open(filename, 'r') as f:
		for line in f.readlines():
			content += line

	regexphp = re.compile(r"(.*?)\$_GET\['(.*?)'\]")
	regexaspx = re.compile(r"(.*?)QueryString\[\"(.*?)\"\]")
	regexaspx2 = re.compile(r"(.*?)QueryString\(\"(.*?)\"\)")

	phpparams = getParams(regexphp, content)
	aspxparams = getParams(regexaspx, content)
	aspxparams2 = getParams(regexaspx2, content)
	
	
	for p in phpparams:
		print(p[1])

	for p in aspxparams:
		print(p[1])

	for p in aspxparams2:
		print(p[1])



