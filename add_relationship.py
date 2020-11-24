#!/usr/bin/python

# import the necessary packages

import requests
import json
import sys
import argparse
import base64
import getpass
import os

execfile("/home/krft.net/kht8234/utility.py")
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Add Relationship')
ap.add_argument("-e", "--entity", required=True, help="enter entity GUID")
ap.add_argument("-g", "--tag", required=True, help="add tag name")
ap.add_argument("-a", "--attr", required=False, help="insert attribute name")
ap.add_argument("-v", "--value", required=False, help="insert attribute value")
ap.add_argument("-n", "--env", required=True, help="insert environment (DEV - TST - PRD)")

args = ap.parse_args()
 
TAG_ENV= args.env
if (TAG_ENV!="DEV" and TAG_ENV!="TST" and TAG_ENV!="PRD"):
        print ("ENVIRONMENT DOES NOT MATCH to DEV / TST / PRD")
        quit()

USER, PASSWORD, ATLAS_DOMAIN, ATLAS_PORT = load_user(TAG_ENV)

SEARCH_ENTITY = args.entity if args.entity is not None else "" 
TAG_NAME = args.tag if args.tag is not None else ""
SEARCH_ATTR = args.attr if args.attr is not None else ""
SEARCH_ATYPE = args.value if args.value is not None else ""

tag_exists=False

tagAttributeResults = atlasGET("/api/atlas/v2/types/typedefs?type=classification", USER, PASSWORD)

tagDetails = tagAttributeResults['classificationDefs']

for tag in tagDetails:
	if tag['name'] == TAG_NAME:
		tag_exists=True


if tag_exists==True:

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
                        if guid == SEARCH_ENTITY:
                        	if len(classificationList)>0:
                               		for classifications in classificationList:
                                        	if classifications == TAG_NAME:
							print ("CAN'T ADD RELATIONSHIP BETWEEN TAG {0} AND ENTITY. TAG ALREADY EXISTS FOR THIS ENTITY ".format (TAG_NAME))
 							quit()


else:
	print ("TAG {0} DOES NOT EXIST. FIRST CREATE THE TAG BEFORE ADDING IT TO THIS ENTITY ".format (TAG_NAME))
	quit()



payload = {
	"classification":{
		"typeName":TAG_NAME,
		"attributes":{
			SEARCH_ATTR:SEARCH_ATYPE
		}
	},
	"entityGuids":[
		SEARCH_ENTITY
	]
}

results = atlasPOST("/api/atlas/v2/entity/bulk/classification", payload, USER, PASSWORD)
results = atlasGET("/api/atlas/v2/entity/guid/"+SEARCH_ENTITY, USER, PASSWORD)

entity = results['entity']

print ("%-55s %-15s %-15s %-36s %-15s" %("ENTITY NAME", "OWNER", "TYPE", "GUID", "TAG"))
entity_name= entity['attributes']['name']
typename = entity['typeName']
owner = entity['attributes']['owner']
guid = entity['guid']
classificationList = entity['classifications']
if len(classificationList)>0:
	for classifications in classificationList:
		classificationname = classifications['typeName']
		print ("%-55s %-15s %-15s %-35s %-15s" %(entity_name, owner,  typename, guid, classificationname))
else:
 	print ("%-55s %-15s %-15s %-15s" %(entity_name, owner,  typename, guid));

