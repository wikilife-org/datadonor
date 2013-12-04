# coding=utf-8

from datetime import date
import requests
from social.clients.base_device_client import BaseDeviceClient

class FoursquareClient(BaseDeviceClient):

    _api_host = None
    _access_token = None
    _user_info = None
    
    def __init__(self, api_host, access_token):
        self._api_host = api_host
        self._access_token = access_token
        self._user_info = self.get_user_info()
    
    def get_user_info(self, params=None, headers=None):
        PROFILE_URL = "users/self"
        response = self.make_request('GET', PROFILE_URL, params=params, headers=headers)
        response = response.json()
        return response
    
    def get_location(self):
        location = None
        try:
            if not self._user_info:
                self._user_info = self.get_user_info()
            location = self._user_info["response"]["user"]["homeCity"]
            return location
        except:
            return location
    
    def get_email(self):
        email = None
        try:
            if not self._user_info:
                self._user_info = self.get_user_info()
            email = self._user_info["response"]["user"]["contact"]["email"]
            return email
        except:
            return email
    
    def get_first_name(self):
        first_name = None
        try:
            if not self._user_info:
                self._user_info = self.get_user_info()
            first_name = self._user_info["response"]["user"]["firstName"]
            return first_name
        except:
            return first_name
    
    def get_last_name(self):
        last_name = None
        try:
            if not self._user_info:
                self._user_info = self.get_user_info()
            last_name = self._user_info["response"]["user"]["lastName"]
            return last_name
        except:
            return last_name
    
    def get_gender(self):
        gender = None
        try:
            if not self._user_info:
                self._user_info = self.get_user_info()
            gender = self._user_info["response"]["user"]["gender"]
            if gender:
                if gender == "male":
                    gender = "m"
                else:
                    gender = "f"
            return gender
        except:
            return gender
    
    def get_friends_count(self):
        if not self._user_info:
            self._user_info = self.get_user_info()
        return int(self._user_info["response"]["user"]["friends"]["count"])

    def make_request(self, method, url, data=None, params=None, headers=None, timeout=60):
        if headers is None:
            headers = {'x-li-format': 'json', 'Content-Type': 'application/json'}
        else:
            headers.update({'x-li-format': 'json', 'Content-Type': 'application/json'})
        
        v = date.today().strftime("%Y%m%d")
        if params is None:
            params = {'oauth_token': self._access_token, 'v':v}
        else:
            params['oauth_token'] = self._access_token
            params['v'] = v
        
        kw = dict(data=data, params=params, headers=headers, timeout=timeout)
        request_url = self._api_host + url
        
        return requests.request(method.upper(), request_url, **kw)