"""
Jawbone
"""

from django.utils import simplejson
from utils.client import oauth_req, dsa_urlopen, build_consumer_oauth_request
from utils.date_util import get_days_list

import requests
import json

def jawbone_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "jawbone":
        data = kwargs.get('response')
        jc = JawboneClient(backend, data['access_token'])
        extra_data = jc.get_user_profile()
        jc.get_user_trends()
        jc.get_move()
        print data
        
    
class JawboneClient():
    PAGE_SIZE = 25

    def __init__(self, backend, access_token):
        self.backend = backend
        self.access_token = access_token
        self.api_host = 'https://jawbone.com/nudge/api/v.1.0/users/@me'


    def get_user_profile(self):
        url =  self.api_host
        headers = {"Content-type": "application/json", "Authorization": "Bearer %s" % self.access_token}
        res = requests.get(url , headers=headers)
        if res.status_code == 200:
            data = json.loads(res.text)
        else:
            data = None        
        return data
    
    def get_user_friends(self):
        url =  self.api_host + "/friends"
        headers = {"Content-type": "application/json", "Authorization": "Bearer %s" % self.access_token}
        res = requests.get(url , headers=headers)
        if res.status_code == 200:
            data = json.loads(res.text)
        else:
            data = None        
        return data
    
    def get_user_mood(self):
        url =  self.api_host + "/mood"
        headers = {"Content-type": "application/json", "Authorization": "Bearer %s" % self.access_token}
        res = requests.get(url , headers=headers)
        if res.status_code == 200:
            data = json.loads(res.text)
        else:
            data = None        
        return data
    
    def get_user_trends(self):
        url =  self.api_host + "/trends"
        headers = {"Content-type": "application/json", "Authorization": "Bearer %s" % self.access_token}
        res = requests.get(url , headers=headers)
        print res.text
        if res.status_code == 200:
            data = json.loads(res.text)
        else:
            print res.status_code
            data = None        
        return data
    

    def get_move(self, move_xid='BwiqMyh8M'):
        url =  "https://jawbone.com/nudge/api/v.1.0/moves/%s" % move_xid
        print url
        headers = {"Content-type": "application/json", "Authorization": "Bearer %s" % self.access_token}
        res = requests.get(url, headers=headers) # , headers=headers)
        if res.status_code == 200:
            data = json.loads(res.text)
        else:
            data = None
            print res.status_code        
        return data