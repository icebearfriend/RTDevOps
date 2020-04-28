# RTDevOps
Work smarter not harder

Update: 4-28-20

Updated newop.py to take a json argument

Update: 4-27-20

## newop.py, targets.json

This script will generate a set of opnotes for you using a json file configured with target data, saving you time as you begin your op. 

The script assumes the following:

 * Unix
 * Python3
 * sublime is installed
   * this can be configured differently in the script. Look for the comment
 * a /redteam folder is already created. This can be configured in the script. Look for it, it's only called once
 * targets.json is in the same path as newop.py. If you move one, move both together
 
 ### How to Use
 
 To use newop.py, first you need to open the targets.json file in edit mode. Go through the json file and place in data where appropriate. 
 
 MyHost will contain the IP address and Hostname values for your host. The Targets key will contain up to five targets for you to fill in IP and Hostname information. 
 
 The Credentials key can contain any creds or other useful info (like pastables) that you might need during your op. Leave blank if you desire

Save the json when you are complete, and run newop.py <opname> <jsonfile>. Example: newop.py testop targets.json

The script will parse the json and generate a form for based on date + opname in a folder based on the date. 

Example: newop.py testop target.json

This produces ./04-27-20/04-27-20_testop_opnotes.txt

![creating opnotes the easy way](https://raw.githubusercontent.com/icebearfriend/stash/master/opnotes.jpg)


## Tarball.sh

This script is used to push files to an S3 bucket on the fly. It will create folders by date, so you can secure your opnotes/loot/files in the cloud without taking your eyes off the terminal. Alias the script and you can use it anywhere!

Requires AWS CLI installed and configured with access keys. 

![Uploading to S3](https://raw.githubusercontent.com/icebearfriend/stash/master/tarball_upload.png)

![Folder on S3](https://raw.githubusercontent.com/icebearfriend/stash/master/S3_Tarball.png)


