from Crypto.Cipher import DES
import getpass
import os

key_passw = "qwertyui"

def atlasGET( restAPI, USER, PASSWORD ) :
    url = "http://"+ATLAS_DOMAIN+":"+ATLAS_PORT+restAPI
    r= requests.get(url, auth=( USER, PASSWORD))
    try:
	return(json.loads(r.text))
    except ValueError:
        print (' ')
        print ("USER PASS COMBINATION NOT ALLOWED TO CONNECT TO ATLAS")
        print (' ')
	return('Error')
    else:
	return(json.loads(r.text))



def atlasPOST(restAPI , Payload, USER, PASSWORD) :
        url = "http://"+ATLAS_DOMAIN+":"+ATLAS_PORT+restAPI
        r= requests.post(url, data=json.dumps(Payload), auth=( USER, PASSWORD), headers={"Content-Type": "application/json", "X-Requested-By": "ambari", "X-XSRF-HEADER": "valid", "cache-control": "no-cache"})
        r.raise_for_status()
        if r.text <> "":
                return(json.loads(r.text));
        else:
                return(r.json);

def load_properties(filepath, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """
    props = {}
    with open(filepath, "rt") as f:
        for line in f:
            l = line.strip()
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"')
                props[key] = value
    return props

def load_properties_enc(filepath, sep='=', comment_char='#'):
    """
    Read the file passed as parameter as a properties file.
    """

    des = DES.new(key_passw, DES.MODE_ECB)	
    props = {}
    f_enc=open(filepath, "r")
    f=des.decrypt(f_enc.read())
    my_str=f.split("\n")    
    for l in my_str:
            if l and not l.startswith(comment_char):
                key_value = l.split(sep)
                key = key_value[0].strip()
                value = sep.join(key_value[1:]).strip().strip('"')
                props[key] = value
    return props

def atlasDELETE( restAPI , USER, PASSWORD) :
        url = "http://"+ATLAS_DOMAIN+":"+ATLAS_PORT+restAPI
        r= requests.delete(url, auth=( USER, PASSWORD))
        if r.text <> "":
                return(json.loads(r.text));
        else:
                return(r.json);

def atlasDELETE2(restAPI , Payload, USER, PASSWORD) :
    url = "http://"+ATLAS_DOMAIN+":"+ATLAS_PORT+restAPI
    r= requests.delete(url, data=json.dumps(Payload), auth=(USER, PASSWORD), headers={"Content-Type": "application/json", "X-Requested-By": "ambari", "X-XSRF-HEADER": "valid", "cache-control": "no-cache"})
    r.raise_for_status()
    if r.text <> "":
           return(json.loads(r.text));
    else:
           return(r.json);


def delete_relationship (guid, TAG_NAME):
        SEARCH_ENTITY= guid
        SEARCH_TAG= TAG_NAME

        results = atlasDELETE("/api/atlas/v2/entity/guid/"+SEARCH_ENTITY+"/classification/"+SEARCH_TAG, USER, PASSWORD)


def delete_tag (guid, TAG_NAME):

        payload = {
                "classificationDefs":[{
                "category":"CLASSIFICATION",
                "guid":guid,
                "name":TAG_NAME,
                "attributeDefs":[],
                "superTypes":[]}],
                "entityDefs":[],
                "enumDefs":[],
                "structDefs":[]
                }

        results = atlasDELETE2("/api/atlas/v2/types/typedefs?type=classification",payload, USER, PASSWORD)


def load_user(TAG_ENV):
	homedir="/home/krft.net/"
	propfile="properties/atlas.properties"
	username = getpass.getuser()
	propuserfile=homedir+username+"/atlasuser.properties"

	if os.path.exists(propuserfile):
		properties=load_properties (homedir + "kht8234/"+ propfile)
		userproperties=load_properties_enc (propuserfile)

		ATLAS_DOMAIN=properties.get (TAG_ENV+'_ATLAS_DOMAIN')
		ATLAS_PORT=properties.get (TAG_ENV+'_ATLAS_PORT')
		USER=userproperties.get('USER')
		PASSWORD=userproperties.get('PASSWORD')

		return USER, PASSWORD, ATLAS_DOMAIN, ATLAS_PORT
	else:
		print
		print ("USER PROPERTY FILE DOES NOT EXISTS. PLS MAKE SURE THE ATLASUSER.PROPERTIES FILE IS CREATED")
		print
		quit()


def load_env(TAG_ENV):
        homedir="/home/krft.net/"
        propfile="properties/atlas.properties"
        properties=load_properties (homedir + "kht8234/"+ propfile)

        ATLAS_DOMAIN=properties.get (TAG_ENV+'_ATLAS_DOMAIN')
        ATLAS_PORT=properties.get (TAG_ENV+'_ATLAS_PORT')

        return ATLAS_DOMAIN, ATLAS_PORT


def pad(text):
	while len(text) % 8 != 0:
	    text += ' '
	return text

def set_user(text):
	des = DES.new(key_passw, DES.MODE_ECB)
	padded_text = pad(text)
	encrypted_text = des.encrypt(padded_text)
	return encrypted_text



