from django.utils import simplejson
from utils.client import oauth_req, dsa_urlopen, build_consumer_oauth_request
from urllib2 import Request
from urllib import urlencode
from utils.aggregated_data import complete_google_info, complete_profile


G_API_KEY = "AIzaSyDwzw-NWn7vmJOwXa5QVhX-aGlc-9hLapM"

def google_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "google-oauth2":
        ##print kwargs
        data = kwargs.get('response')
        access_token = data["access_token"]
        g_id = data["id"]
        #print get_contacts(backend, access_token)
        profile =  get_profile(access_token)
        gplus_profile = get_gplus_profile(g_id, access_token)
        gplus_contacts = get_gplus_contacts(g_id, access_token)
        gplus_contacts_count = int(gplus_contacts["totalItems"])
        
        complete_google_info(social_user.user, gplus_contacts_count)
        if "gender" in data:
            gender = data["gender"]
            if gender == "male":
                gender = "m"
            else:
                gender ="f"
                
        email = ""
        if "email" in data :
            email = data["email"]
        complete_profile(social_user, email, None, gender)
        result.update(data)
        result.update(profile)
        result.update(gplus_profile)
        result.update(gplus_contacts)
        social_user.extra_data.update(result)
        social_user.save()
          
        return result


def get_profile(access_token):
    url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    data = {'access_token': access_token, 'alt': 'json'}
    request = Request(url + '?' + urlencode(data))
    try:
        return simplejson.loads(dsa_urlopen(request).read())
    except Exception,e:
        return e
    

def get_gplus_profile(g_id, access_token):
    #url = "https://www.googleapis.com/plus/v1/people/%s/people/visible"%g_id
    url = " https://www.googleapis.com/plus/v1/people/%s"%g_id
    data = {'access_token': access_token, 'alt': 'json' ,"api-key": G_API_KEY}
    request = Request(url + '?' + urlencode(data))
    try:
        return simplejson.loads(dsa_urlopen(request).read())
    except Exception,e:
        return e

def get_gplus_contacts(g_id, access_token):
    url = "https://www.googleapis.com/plus/v1/people/%s/people/visible"%g_id
    data = {'access_token': access_token, 'alt': 'json' ,"api-key": G_API_KEY}
    request = Request(url + '?' + urlencode(data))
    try:
        return simplejson.loads(dsa_urlopen(request).read())
    except Exception,e:
        return e
    