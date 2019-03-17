import glob
import sys
import re
from termcolor import colored
import urllib.request


def getParams(regexstr, content):
	regexcomp = re.compile(r"" + regexstr +"")
	params = re.findall(regexcomp, content)
	return params

regexlist = []
urlList = []

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
	with open(filename, 'r') as f:
		for line in f.read():
			content += line
		
		paramstr = ""
		paramstrprint = ""

	for x in range(0, len(regexlist)):
		phpparams = getParams(str(regexlist[x]), content)
		phpparams = set(phpparams)

		for param in phpparams:
			paramstr += str(param[1]) + "=" + payload + "&"
			paramstrprint += colored(str(param[1]), 'green') + "=" + payload + "&"
	if paramstr:
		url = siteurl + (filename.replace(sys.argv[1], "")) + "?" + paramstr[:-1]
		print (siteurl + (filename.replace(sys.argv[1], "")) + "?" + paramstrprint[:-1])
		urlList.append(url.rstrip())

yesorno = input('Check for reflections? y/n')

if yesorno == 'y':
	for url in urlList:
		try:
			with urllib.request.urlopen(url) as response:
			   	resp = response.read()
			   	if payload in str(resp):
			   		print(colored('Reflected input! ', 'green'), url)
		except urllib.error.HTTPError as err:
#   			if err.code == 404:
   				print(colored(err.code, 'red'), url)
