#!/usr/bin/python

# import the necessary packages

import requests
import json
import sys
import argparse
import base64

execfile("/home/krft.net/kht8234/utility.py")

ap = argparse.ArgumentParser(description='Adding tags')
ap.add_argument("-g", "--tag", required=True, help="insert tag name")
ap.add_argument("-d", "--desc", required=False, help="insert description")
ap.add_argument("-a", "--attr", required=False, help="insert attribute")
ap.add_argument("-t", "--atype", required=False, help="insert attribute type")
ap.add_argument("-n", "--env", required=True, help="insert environment (DEV - TST - PRD)")


args = ap.parse_args()
 
TAG_ENV= args.env
if (TAG_ENV!="DEV" and TAG_ENV!="TST" and TAG_ENV!="PRD"):
        print ("ENVIRONMENT DOES NOT MATCH to DEV / TST / PRD")
        quit()

USER, PASSWORD, ATLAS_DOMAIN, ATLAS_PORT = load_user(TAG_ENV)

TAG_NAME = args.tag 
TAG_DESC = args.desc 
TAG_ATTR = args.attr 
TAG_ATYPE = args.atype 
tag_exists=False


#results = atlasGET("/api/atlas/discovery/search/dsl?query={0}".format(TAG_NAME), USER, PASSWORD)

#count = len(results)
#print count

#print results


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

	tagAttributeResults = atlasGET("/api/atlas/v2/types/typedefs?type=classification", USER, PASSWORD)

	tagDetails = tagAttributeResults['classificationDefs']
	print ("CAN'T CREATE TAG {0}. TAG ALREADY EXISTS WITH FOLLOWING DETAILS ".format (TAG_NAME))
	print (' ')
	for tag in tagDetails:
		if tag['name'] == TAG_NAME:
               		attributeList = tag['attributeDefs']
			print ("%-20s %-45s %-15s %-15s" %("TAG", "DESCRIPTION", "ATTRIBUTE", "TYPE"))
			print ("_____________________________________________________________________________________________________________________________________________")
			if len(attributeList)>0:
				for attribute in attributeList:
					print ("%-20s %-45s %-15s %-15s" %(TAG_NAME, tag['description'], attribute['name'], attribute['typeName']))
			else:
				print ("%-20s %-45s " %(TAG_NAME, tag['description']))
				print (' ')

	if len(results) > 2:
		entityDetail = results['entities']
		entityList = []
		print (' ')
		print ("TAG {0} HAS THE FOLLOWING RELATIONSHIPS ".format (TAG_NAME))
		print (' ')
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
					if classifications == TAG_NAME:
	                	        	print ("%-55s %-15s %-15s %-35s %-15s" %(entity_name, owner,  typename, guid, classifications))
	        	else:
        	        	print ("%-55s %-15s %-15s %-15s" %(entity_name, owner,  typename, guid))
	else:
		print ("TAG {0} HAS NO RELATIONSHIPS ".format (TAG_NAME))
		print (' ')

				
else:	
	if (TAG_ATTR!='' and TAG_ATYPE!= ''):
		payload = { 
			"classificationDefs":[{
				"name":TAG_NAME,
				"description":TAG_DESC,
				"superTypes":[],
				"attributeDefs":[{
					"name":TAG_ATTR,
					"typeName":TAG_ATYPE,
					"isOptional":"true",
					"cardinality":"SINGLE",
					"valuesMinCount":0,
					"valuesMaxCount":1,
					"isUnique":"false",
					"isIndexable":"false"
				}]}],
			"entityDefs":[],
			"enumDefs":[],
			"structDefs":[]
		}
	else: 
		payload = {
                        "classificationDefs":[{
                                "name":TAG_NAME,
                                "description":TAG_DESC,
                                "superTypes":[],
                                "attributeDefs":[{
                                }]}],
                        "entityDefs":[],
                        "enumDefs":[],
                        "structDefs":[]
                }
	
	results = atlasPOST("/api/atlas/v2/types/typedefs", payload, USER, PASSWORD)
	
	print ("TAG {0} CREATED".format (TAG_NAME));
