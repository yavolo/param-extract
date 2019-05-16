import glob
import sys
import re
from termcolor import colored
import urllib.request
import requests

print("----------------------------------------------------")
print(r"""
    ____   ____ _ _____ ____ _ ____ ___        
   / __ \ / __ `// ___// __ `// __ `__ \ ______
  / /_/ // /_/ // /   / /_/ // / / / / //_____/
 / .___/ \__,_////    \__,_//_/ /_/ /_/__      
/_/__   _  __ / /_ _____ ____ _ _____ / /_     
 / _ \ | |/_// __// ___// __ `// ___// __/     
/  __/_>  < / /_ / /   / /_/ // /__ / /_       
\___//_/|_| \__//_/    \__,_/ \___/ \__/       
                                              
""")
print("----------------------------------------------------")
print("Server side web parameter extractor v 1.0")
print("----------------------------------------------------")


def getParams(regexstr, content):
	regexcomp = re.compile(r"" + regexstr +"")
	params = re.findall(regexcomp, content)
	return params


def getByFileTypes(filetypes, wwwroot):
	print(wwwroot)
	filelist = []
	for ft in filetypes:
		globobj = glob.iglob((wwwroot +"/**/"+ ft), recursive=True)

		for line in globobj:
			filelist.append(line)
	return filelist


regexlist = []
urlList = []

with open("./regex", 'r') as f:
	for line in f.readlines():
		regexlist.append(line.rstrip())

if len(sys.argv) >= 3:
	wwwrootpath2 = sys.argv[1]

	filetypes = ['*.jsp', '*.aspx', '*.php', '*.cs']
	siteurl = sys.argv[2]
	payload = sys.argv[3]

else:
	print('Missing argument variables. wwwroot siteurl payload')
	exit()

filepaths = getByFileTypes(filetypes, wwwrootpath2)

for filename in filepaths:
	content = ""
	with open(filename, 'r', encoding="utf8", errors='ignore') as f:
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
		   		else:
		   			print(colored('2XX ', 'yellow') + url)

		except urllib.error.HTTPError as err:
#   			if err.code == 404:
			print(colored(err.code, 'red'), url)
			continue


yesorno = input('Send to proxy? y/n')

if yesorno == 'y':
	for url in urlList:
		proxies = {
			  "http": "http://127.0.0.1:8080",
			  "https": "http://127.0.0.1:8080",
			}

		requests.get(url, proxies=proxies)
