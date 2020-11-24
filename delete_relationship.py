#!/usr/bin/python

# import the necessary packages

import requests
import json
import sys
import argparse
import base64

execfile("/home/krft.net/kht8234/utility.py")
 
# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Delete Relationship')
ap.add_argument("-e", "--entity", required=True, help="enter entity GUID")
ap.add_argument("-g", "--tag", required=True, help="delete tag name")
ap.add_argument("-n", "--env", required=True, help="insert environment (DEV - TST - PRD)")


args = ap.parse_args()
 
TAG_ENV= args.env
if (TAG_ENV!="DEV" and TAG_ENV!="TST" and TAG_ENV!="PRD"):
        print ("ENVIRONMENT DOES NOT MATCH to DEV / TST / PRD")
        quit()

USER, PASSWORD, ATLAS_DOMAIN, ATLAS_PORT = load_user(TAG_ENV)

SEARCH_ENTITY = args.entity if args.entity is not None else "" 
SEARCH_TAG = args.tag if args.tag is not None else ""

results = atlasDELETE("/api/atlas/v2/entity/guid/"+SEARCH_ENTITY+"/classification/"+SEARCH_TAG, USER, PASSWORD)

results = atlasGET("/api/atlas/v2/entity/guid/"+SEARCH_ENTITY, USER, PASSWORD)

entity = results['entity']
print ("TAG DELETED FOR THIS ENTITY. OTHER TAG RELATONSHIPS FOR THIS ENTITY")
print (' ')
print ("%-55s %-15s %-15s %-36s %-15s" %("ENTITY NAME", "OWNER", "TYPE", "GUID", "TAG"))
print ("_____________________________________________________________________________________________________________________________________________")
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
