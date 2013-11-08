"""
DailyMile
"""
import json
import requests


from django.utils import simplejson
from utils.client import oauth_req, dsa_urlopen, build_consumer_oauth_request
from utils.date_util import get_days_list

def dailymile_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "dailymile":
        data = kwargs.get('response')
        dm = DailymileClient(data['access_token'], data['username'])
        dm.get_user_friends()
        print data
        

class DailymileClient():
    PAGE_SIZE = 25

    def __init__(self, access_token, username):
        self.api_host = 'https://api.dailymile.com/people'
        self.headers = {"Content-type": "application/json", "Authorization": "Bearer %s" % access_token}
        self.username = username

    
    def make_api_call(self, url):
        res = requests.get(url)
        if res.status_code == 200:
            data = json.loads(res.text)
        else:
            data = None        
        return data


    def date_formatter(self, date_obj):
        """format date to jawbone type int YYYYMMDD"""
        return date_obj.strftime('%Y%m%d')
    
    
    def get_params_url(self, params_dic):
        return "/?" + "&".join(["%s=%s" % (k, v) for k, v in params_dic.items()])


    def get_user_profile(self):
        url = self.api_host
        return self.make_api_call(url)


    def get_user_friends(self):
        url = self.api_host + "/%s/friends.json" % self.username       
        return self.make_api_call(url)
    
    
        