#!/usr/bin/python

# import the necessary packages

import requests
import json
import sys
import argparse
import base64

execfile("/home/krft.net/kht8234/utility.py")
 
def delete_relationship (guid, first_line):
        SEARCH_ENTITY= guid
        payload = {
                "classification":{
                        "typeName":SEARCH_TAG,
                        "attributes":{
                        }
                },
                "entityGuids":[
                        SEARCH_ENTITY
                ]
        }

	results = atlasDELETE("/api/atlas/v2/entity/guid/"+SEARCH_ENTITY+"/classification/"+SEARCH_TAG, USER, PASSWORD)

        results = atlasGET("/api/atlas/v2/entity/guid/"+SEARCH_ENTITY, USER, PASSWORD)

        entity = results['entity']

        if first_line==True:
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


# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser(description='Delete Relationship')
ap.add_argument("-g", "--tag", required=True, help="add tag name")
ap.add_argument("-n", "--env", required=True, help="insert environment (DEV - TST - PRD)")
ap.add_argument("-f", "--filename", required=False, help="file to import entities")

args = ap.parse_args()

TAG_ENV= args.env
if (TAG_ENV!="DEV" and TAG_ENV!="TST" and TAG_ENV!="PRD"):
        print ("ENVIRONMENT DOES NOT MATCH to DEV / TST / PRD")
        quit()

USER, PASSWORD, ATLAS_DOMAIN, ATLAS_PORT = load_user(TAG_ENV)


SEARCH_TAG = args.tag if args.tag is not None else ""
SEARCH_FILE = args.filename if args.filename is not None else ""

previous=""
first_line=True

if not sys.stdin.isatty():
    input_stream = sys.stdin
    linenum=0
    for line in input_stream:
        inner_list = line[88:124]
        linenum+=1
        if linenum>2:
		if inner_list!=previous:
	                delete_relationship(inner_list, first_line)
			previous=inner_list
			first_line=False

# otherwise, read the given filename                                            
else:
    try:
        input_filename = sys.argv[1]
    except IndexError:
        message = 'need filename as first argument if stdin is not full'
        raise IndexError(message)
    else:
	list_of_lists = []
 	linenum=0
	with open(SEARCH_FILE) as f:
	   for line in f:
        	inner_list = line[88:124]
	        linenum+=1
	        if linenum>2:
			if inner_list!=previous:
                        	delete_relationship(inner_list, first_line)
                        	previous=inner_list
				first_line=False

