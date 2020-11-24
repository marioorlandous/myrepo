#!/usr/bin/python

# import the necessary packages

import requests
import json
import sys
import argparse
import base64

execfile("/home/krft.net/kht8234/utility.py")

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Search Relationship')
ap.add_argument("-t", "--type", required=False, help="search type name")
ap.add_argument("-g", "--tag", required=False, help="search tag name")
ap.add_argument("-x", "--text", required=False, help="search text name")
ap.add_argument("-n", "--env", required=True, help="insert environment (DEV - TST - PRD)")

args = ap.parse_args()

TAG_ENV= args.env
if (TAG_ENV!="DEV" and TAG_ENV!="TST" and TAG_ENV!="PRD"):
        print ("ENVIRONMENT DOES NOT MATCH to DEV / TST / PRD")
        quit()

USER, PASSWORD, ATLAS_DOMAIN, ATLAS_PORT = load_user(TAG_ENV)

SEARCH_TYPE = args.type  
SEARCH_TAG = args.tag  
SEARCH_TEXT = args.text 
tag_exists=False

tagAttributeResults = atlasGET("/api/atlas/v2/types/typedefs?type=classification", USER, PASSWORD)

tagDetails = tagAttributeResults['classificationDefs']
for tag in tagDetails:
	if tag['name'] == SEARCH_TAG:
		tag_exists=True

if tag_exists==False and SEARCH_TAG!= None:
	print ("TAG {0} DOES NOT EXISTS".format (SEARCH_TAG))
	quit()

if SEARCH_TAG==None:
	payload = {
	        "excludeDeletedEntities":True,
        	"attributes":[
	        ],
       		"query":SEARCH_TEXT,
       	 	"offset":0,
        	"limit":300,
        	"typeName":SEARCH_TYPE
	}

else:
	payload = {
		"excludeDeletedEntities":True,
		"attributes":[
		],
		"query":SEARCH_TEXT,
		"classification":SEARCH_TAG,
		"offset":0,
		"limit":300,
		"typeName":SEARCH_TYPE
	}


results = atlasPOST("/api/atlas/v2/search/basic", payload, USER, PASSWORD)

try:
	entityDetail = results['entities']
except KeyError:
	print (' ')
	print ("SEARCH DID NOT PRODUCE RESULTS")
	print (' ')
else:
	entityDetail = results['entities']
	entityList = []
	print ("%-55s %-15s %-15s %-36s %-15s" %("ENTITY NAME", "OWNER", "TYPE", "GUID", "TAG"))
	print ("_____________________________________________________________________________________________________________________________________________")

	for entity in entityDetail:
		entity_name= entity['attributes']['name']
		typename = entity['typeName']
		owner = entity['attributes']['owner']
		guid = entity['guid']
		classificationList = entity['classificationNames']
		if len(classificationList)>0:
			for classifications in classificationList:
				if SEARCH_TAG!=None:
					if classifications==SEARCH_TAG:	
						print ("%-55s %-15s %-15s %-35s %-15s" %(entity_name, owner,  typename, guid, classifications))
				else:	
					print ("%-55s %-15s %-15s %-35s %-15s" %(entity_name, owner,  typename, guid, classifications))
		else:
	 		print ("%-55s %-15s %-15s %-15s" %(entity_name, owner,  typename, guid));


