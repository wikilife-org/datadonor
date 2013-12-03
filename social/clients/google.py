# coding=utf-8

from django.utils import simplejson
from utils.client import dsa_urlopen
from urllib2 import Request
from urllib import urlencode
from social.clients.base_device_client import BaseDeviceClient

G_API_KEY = "AIzaSyC0iHcxDeCDMUc6Yv2CxhmKGFTu5ZDqxZw"

class GoogleClient(BaseDeviceClient):

    _api_host = None
    _access_token = None
    _g_id = None

    def __init__(self, api_host, access_token, g_id):
        self._api_host = api_host
        self._access_token = access_token
        self._g_id = g_id

    def get_profile(self):
        url = "people/%s"%self._g_id
        return self._get_resource(url)
    
    def get_contacts(self):
        url = "people/%s/people/visible"%self._g_id
        return self._get_resource(url)
 
    def get_contacts_count(self):
        return int(self.get_contacts()["totalItems"])
 
    def _get_resource(self, url):
        request_url = self._api_host + url
        data = {'access_token': self._access_token, 'alt': 'json' ,"api-key": G_API_KEY}
        request = Request(request_url + '?' + urlencode(data))
        try:
            return simplejson.loads(dsa_urlopen(request).read())
        except Exception,e:
            return e
