#!/usr/bin/python

# import the necessary packages

import requests
import json
import sys
import argparse
import base64
import getpass

execfile("/home/krft.net/kht8234/utility.py")

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Display Tags')
ap.add_argument("-n", "--env", required=True, help="insert environent (DEV - TST - PRD)")

args = ap.parse_args()

TAG_ENV= args.env
if (TAG_ENV!="DEV" and TAG_ENV!="TST" and TAG_ENV!="PRD"):
	print ("ENVIRONMENT DOES NOT MATCH to DEV / TST / PRD")
	quit()

USER, PASSWORD, ATLAS_DOMAIN, ATLAS_PORT = load_user(TAG_ENV)

tagAttributeResults = atlasGET("/api/atlas/v2/types/typedefs?type=classification", USER, PASSWORD)

tagDetails = tagAttributeResults['classificationDefs']

print ("%-20s %-45s %-15s %-15s" %("TAG", "DESCRIPTION", "ATTRIBUTE", "TYPE"))
print ("_____________________________________________________________________________________________________________________________________________")

old_tag=""

for tag in tagDetails:
        attributeList = tag['attributeDefs']
        if len(attributeList)>0:
                for attribute in attributeList:
                        if old_tag!=tag['name']:
                                print ("%-20s %-45s %-15s %-15s" %(tag['name'], tag['description'], attribute['name'], attribute['typeName']))
                                old_tag=tag['name']
                        else:
                                print ("%-20s %-45s %-15s %-15s" %("", "", attribute['name'], attribute['typeName']))
        else:
                print ("%-20s %-45s" %(tag['name'], tag['description']))


