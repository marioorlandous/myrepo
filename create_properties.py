#!/usr/bin/python

# import the necessary packages

import requests
import json
import sys
import argparse
import base64
import getpass
import os
import sys, tty, termios

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

execfile("/home/krft.net/kht8234/utility.py")


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Create property File')
ap.add_argument("-u", "--user", required=False, help="user")
ap.add_argument("-p", "--passw", required=False, help="password")
ap.add_argument("-n", "--env", required=True, help="insert environent (DEV - TST - PRD)")
	
args = ap.parse_args()
 
TAG_ENV= args.env
if (TAG_ENV!="DEV" and TAG_ENV!="TST" and TAG_ENV!="PRD"):
        print ("ENVIRONMENT DOES NOT MATCH to DEV / TST / PRD")
        quit()

ATLAS_DOMAIN, ATLAS_PORT = load_env(TAG_ENV)

USER = args.user if args.user is not None else getpass.getuser()

if args.passw is None:
	key = ""
	print 
	print('Enter User Password:')
	while True:
	    ch = getch()
	    if ch == '\r':
		break
	    key += ch
	    sys.stdout.write('*')
	print
	PASS = key
else:
	PASS = args.passw

tagAttributeResults = atlasGET("/api/atlas/v2/types/typedefs?type=classification", USER, PASS)
if tagAttributeResults=='Error':
	quit()
else:
	text= "#PROPERTY FILE FOR ATLAS API SCRIPTS\n# add_tags.py\n# search_entity.py\n# add_relationship.py\n# delete_relationship.py\n# add_bulk_relationship.py\n# delete_bulk_relationship.py\nUSER="+USER+"\nPASSWORD="+PASS

	encrypted_text=set_user(text)

	filename = "/home/krft.net/"+USER+"/atlasuser.properties"

	print (' ')
	print ("ENCRIPTED FILE {0} CREATED".format(filename))
	print (' ')
	file = open (filename, "w")

	file.write(encrypted_text)

	file.close
