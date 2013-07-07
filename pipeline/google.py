from django.utils import simplejson
from utils.client import oauth_req, dsa_urlopen, build_consumer_oauth_request
from urllib2 import Request
from urllib import urlencode

def google_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "google-oauth2":
        ##print kwargs
        data = kwargs.get('response')
        access_token = data["access_token"]
        #print get_contacts(backend, access_token)
        profile =  get_profile(access_token)
        contacts = get_contacts(access_token)
        print contacts
        result.update(profile)
        social_user.extra_data.update(result)
        social_user.save()
          
        return result

def get_contacts(backend, access_token):
    url = "https://www.google.com/m8/feeds/contacts/default/full"
    request = build_consumer_oauth_request(backend,access_token, url)
    response = '\n'.join(dsa_urlopen(request.to_url()).readlines())
    response = simplejson.loads(response)
    return response

def get_profile(access_token):
    url = 'https://www.googleapis.com/oauth2/v1/userinfo'
    data = {'access_token': access_token, 'alt': 'json'}
    request = Request(url + '?' + urlencode(data))
    try:
        return simplejson.loads(dsa_urlopen(request).read())
    except Exception,e:
        return e
    

def get_contacts(access_token):
    url = 'https://www.googleapis.com/plus/v1/people/me'
    data = {'access_token': access_token, 'alt': 'json'}
    request = Request(url + '?' + urlencode(data))
    try:
        return simplejson.loads(dsa_urlopen(request).read())
    except Exception,e:
        return e