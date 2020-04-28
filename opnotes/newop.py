#!/usr/bin/env python3

import glob, os, json, sys, subprocess
from datetime import date

# gathering date for file string later on
d = date.today()
# this is the json file we will parse
jsonfile = "targets.json"

# opening the jsonfile variable, located in the /redteam folder. Change value if you are hosting somewhere else
with open('/redteam/'+jsonfile) as data_file:
	data = json.load(data_file)

# init variable
opnotes = ''

# operator name, goes at the top of the opnotes
# myIP is the host that you want to reflect as your attacking host. example: VPN ip
# myHost is your hostname
operatorname = data["handle"]
myIP = data['MyHost'][0]['ip']
myHost = data['MyHost'][0]['hostname']

# this function formats all targets that come after your host, found in the "targets" dictionary in the json file
def targetFormat(targetIP, targetHost):
	output = "\n>>{0:<25}\t{1}".format(targetIP, targetHost)
	return output

# this function parses the "targets" section of jsonfile and sends it to targetFormat
def jsonTargetLoop(json):
	collector = ''
	for i in range(len(json)):
		target = "target" + str(i + 1)
		targetloop = json[target][0]
		if targetloop["ip"]:
			targetIP = targetloop["ip"]
			targetHost = targetloop["hostname"]
			collector += targetFormat(targetIP, targetHost)

	return collector
			
# this function iterates through all "credentials" in the jsonfile
def credloop(json):
	collector = ''
	for i in range(len(json["credentials"][0])):
		creds = "cred" + str(i + 1)
		credloop = json["credentials"][0][creds]
		if credloop:
			collector += credloop + "\n"

	return collector

# this function builds the "body" of the opnotes
def targetBody(json):
	collector = ''

	# the full jsonfile is passed from buildit() during this iteration and hits on "MyHost" and then returns data
	if "MyHost" in json:
		collector += "=" * 30 + "\n"
		collector += "\t" + ("=" * 5) + " "
		collector += "{0} // {1}\n".format(json["MyHost"][0]["ip"], json["MyHost"][0]["hostname"])
		collector += "=" * 30
		collector += "\n" * 5
		return collector

	# target specific version of the jsonfile is passed from buildit() that points directly to "targets"
	else:
		for i in range(len(json)):
			target = "target" + str(i + 1)
			if json[target][0]["ip"]:
				collector += "=" * 30 + "\n"
				collector += "\t" + ("=" * 5) + " "
				collector += "{0} // {1}\n".format(json[target][0]["ip"], json[target][0]["hostname"])
				collector += "=" * 30
				collector += "\n" * 5

		# this builds in the extra section when the "targets" section above is complete
		collector += "=" * 30 + "\n"
		collector += "\t" + ("=" * 5) + " "
		collector += "Extra\n"
		collector += "=" * 30 + "\n"
		return collector

# this builds the opnotes
def buildit(data):
	opnotes = ''
	opnotes += "Operator: {} \n".format(operatorname)
	opnotes += "\n" * 2
	opnotes += ">{0:<25}\t{1}".format(myIP, myHost)
	opnotes += jsonTargetLoop(data["targets"][0])
	opnotes += "\n" * 3
	opnotes += "Useful items:\n"
	opnotes += credloop(data)
	opnotes += "\n" * 3
	opnotes += targetBody(data)
	targetcollect = targetBody(data["targets"][0])
	opnotes += targetcollect
	return opnotes

# this function creates the directory, writes the opnote file to disk, and opens it up w/ sublime
# !!!if you do not have sublime, change the command or comment it out
def buildFile (opname):
	dtg = d.strftime("%m-%d-%y")
	directory = "./{0}".format(dtg)
	access_rights = 0o755 # default chmod is 777, we are changing it to 755
	if os.path.exists(directory): # checking to see if you've made this directory before
		os.chdir(directory) # goes to it
	else:
		os.mkdir(directory, access_rights) # if you haven't built, build it
		os.chdir(directory) # change into it
	opnote_file = "{0}_{1}_opnotes.txt".format(dtg, opname)
	try:
		f = open(opnote_file, 'x') # try to create a brand new file. The x will ensure that you do not overwrite
	except:
		print("\n(-) File {0} exists already. Give it another name and try again".format(opnote_file))

	output = buildit(data)
	f.write(output)
	f.close()

	subprocess.run(['subl', opnote_file])
	exit



if __name__== "__main__":
	if len(sys.argv) != 2:
		print("(+) Usage: {0} <opname>").format(sys.argv[0])
		print("Please enter your OP name")

	opname = sys.argv[1]
	buildFile(opname)

