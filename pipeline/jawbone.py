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
        jc = JawboneClient(data['access_token'])
        extra_data = jc.get_user_profile()
        print jc.get_user_friends()
        print jc.get_user_workouts()
        print data
        
    
class JawboneClient():
    PAGE_SIZE = 25

    def __init__(self, access_token):
        self.api_host = 'https://jawbone.com/nudge/api/users/@me'
        self.headers = {"Content-type": "application/json", "Authorization": "Bearer %s" % access_token}

    
    def make_api_call(self, url):
        res = requests.get(url , headers=self.headers)
        if res.status_code == 200:
            data = json.loads(res.text)
        else:
            data = None        
        return data


    def get_user_profile(self):
        url = self.api_host
        return self.make_api_call(url)


    def get_user_friends(self):
        url =  self.api_host + "/friends"       
        return self.make_api_call(url)


    def get_user_mood(self):
        url =  self.api_host + "/mood"
        return self.make_api_call(url)


    def get_user_trends(self):
        url =  self.api_host + "/trends"
        return self.make_api_call(url)
    

    def get_user_workouts(self):
        url =  self.api_host + "/workout"
        return self.make_api_call(url)
    
    
    def get_user_body_events(self):
        url =  self.api_host + "/body_events"
        return self.make_api_call(url)
    
    
    def get_user_cardiac_events(self):
        url =  self.api_host + "/cardiac_events"
        return self.make_api_call(url)
    
    
    def get_user_meals(self):
        url =  self.api_host + "/meals"
        return self.make_api_call(url)