#!/usr/bin/python

# import the necessary packages

import requests
import json
import sys
import argparse
import base64

execfile("/home/krft.net/kht8234/utility.py")

ap = argparse.ArgumentParser(description='Delete tag')
ap.add_argument("-g", "--tag", required=True, help="insert tag name")
ap.add_argument("-n", "--env", required=True, help="insert environment (DEV - TST - PRD)")
ap.add_argument("-f", "--force", required=False, help="force deletion")

args = ap.parse_args()
 
TAG_ENV= args.env
if (TAG_ENV!="DEV" and TAG_ENV!="TST" and TAG_ENV!="PRD"):
        print ("ENVIRONMENT DOES NOT MATCH to DEV / TST / PRD")
        quit()

USER, PASSWORD, ATLAS_DOMAIN, ATLAS_PORT = load_user(TAG_ENV)

TAG_NAME = args.tag 
FORCE_DEL = args.force

tag_exists=False
tag_delete=False
no_relationships=False
first_line=True

if FORCE_DEL=="yes":
	tag_delete=True


tagAttributeResults = atlasGET("/api/atlas/v2/types/typedefs?type=classification", USER, PASSWORD)

tagDetails = tagAttributeResults['classificationDefs']
for tag in tagDetails:
	if tag['name'] == TAG_NAME:
		tag_exists = True


if tag_exists == True:

	payload = {
	        "excludeDeletedEntities":True,
        	"attributes":[
	        ],
        	"classification":TAG_NAME
	}

	results = atlasPOST("/api/atlas/v2/search/basic", payload, USER, PASSWORD)

	if len(results) > 2:
		entityDetail = results['entities']
		entityList = []

		for entity in entityDetail:
			entity_name= entity['attributes']['name']
	      		typename = entity['typeName']
		        owner = entity['attributes']['owner']
		        guid = entity['guid']
		        classificationList = entity['classificationNames']
	        	if len(classificationList)>0:
        	        	for classifications in classificationList:
					if classifications == TAG_NAME:
						if tag_delete== True:
							delete_relationship (guid, TAG_NAME)
							print ("TAG {0} RELATIONSHIPS ".format (TAG_NAME))
							print (' ')
							print ("%-55s %-15s %-15s %-36s %-15s" %("ENTITY NAME", "OWNER", "TYPE", "GUID", "TAG"))
							print ("_____________________________________________________________________________________________________________________________________________")
						else:
							if first_line==True:
								print (' ')
				                                print ("FORCE DELETE FLAG REQUIRED TO DELETE TAGS WITH RELATIONSHIPS")
								print (' ')
								print ("TAG {0} RELATIONSHIPS ".format (TAG_NAME))
								print (' ')
								print ("%-55s %-15s %-15s %-36s %-15s" %("ENTITY NAME", "OWNER", "TYPE", "GUID", "TAG"))
								print ("_____________________________________________________________________________________________________________________________________________")
								first_line=False
	                	        	print ("%-55s %-15s %-15s %-35s %-15s" %(entity_name, owner,  typename, guid, classifications))
		
	else: 
		no_relationships=True

			
	for tag in tagDetails:
	        if tag['name'] == TAG_NAME:
		      	if no_relationships== True or (no_relationships== False and tag_delete== True):
		 		delete_tag(tag['guid'], TAG_NAME)
				print (' ')
	                	print ("TAG {0} DELETED".format (TAG_NAME))
else: 
	print ("TAG {0} NOT PRESENT ".format (TAG_NAME))				


