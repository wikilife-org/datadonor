"""
DailyMile
"""
import json
import requests


from django.utils import simplejson
from utils.client import oauth_req, dsa_urlopen, build_consumer_oauth_request
from utils.date_util import get_days_list
from datetime import date


class DailymileClient():
    PAGE_SIZE = 25

    def __init__(self, api_host, access_token):
        self.api_host = api_host
        self.access_token = access_token
        self.headers = {"Content-type": "application/json", "Authorization": "Bearer %s" % access_token}
        self.user_profile = self.get_user_profile()
        self.username = self.user_profile["username"]

    
    def make_api_call(self, url, params={}):
        params["oauth_token"] = self.access_token
        p = self.get_params_url(params)
        url = url +p
        res = requests.request("GET", url, headers=self.headers)
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
        url = self.api_host + "/me.json"
        return self.make_api_call(url)

    def get_user_activities(self):
        from_date = date(1970,01,01)
        today = date.today()
        params = {}
        params["since"] = (today- from_date).days
        url = self.api_host + "/%s/entries.json"%self.username
        return self.make_api_call(url)
    
    def get_user_friends(self):
        url = self.api_host + "/%s/friends.json" % self.username       
        return self.make_api_call(url)
    