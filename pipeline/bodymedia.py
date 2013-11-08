"""
Bodymedia
"""
import random
from time import time
import json

from django.utils import simplejson
from utils.client import oauth_req, dsa_urlopen, build_consumer_oauth_request
from utils.date_util import get_days_list
import requests


BASE_API = 'http://api.bodymedia.com/v2'
SIGNATURE_METHOD = 'HMAC-SHA1'
OAUTH_VERSION = '1.0'
API_KEY = '3dh55bqrxns3pwwqdz59puynvyjvd376'


def bodymedia_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "bodymedia":
        data = kwargs.get('response')
        #token = data['access_token'][0]['oauth_token']
        #token_secret = data['access_token']
        bm = BodymediaClient('fdf','fdfd','sfdf')
        extra_data = bm.get_user_info()
        import pdb;pdb.set_trace()
        
    
class BodymediaClient():
    PAGE_SIZE = 25
#https://developer.bodymedia.com/forum/read/160754 --> api request
#http://api.bodymedia.com/v2/user/info?api_key=t6bjhaa7jqrnwgxxxxxxxxxx&oauth_consumer_key=t6bjhaa7jqrnwgxxxxxxxxxx&oauth_version=1.0&oauth_signature_method=HMAC-SHA1&oauth_nonce=6L278xHiJvMoY5f&oauth_timestamp=1356036823&oauth_token=fc83b2e7-b0d8-xxxxxx&oauth_signature=9RGA7nlUTwZzODfYY1cGpRmZBbQ%3D
    def __init__(self, oauth_consumer_key, oauth_token, oauth_token_secret):
        self.api_host = BASE_API
        self.api_key = API_KEY
        self.oauth_consumer_key = oauth_consumer_key
        self.oauth_token = oauth_token
        #Toncatenated Consumer Secret and Token Secret separated by an "&" character
        self.oauth_signature = ""
        self.headers = {"Content-type": "application/json"} #, "Authorization": "Bearer %s" % access_token}

    
    def get_req_values(self):
        nonce_string = ['a','b','c','d','e','f','g','h','i']
        nonce = "".join(random.shuffle(nonce_string))
        timestamp = time()
        return nonce, timestamp
    
    
    def make_api_call(self, url):
        res = requests.get(url , headers=self.headers)
        if res.status_code == 200:
            data = json.loads(res.text)
        else:
            data = None        
        return data

    
    def get_user_info(self):
        nonce, timestamp = self.get_req_values()
        url = '%s/user/info/?api_key=%s&oauth_consumer_key=%s&oauth_version=%s&oauth_signature_method=%s&oauth_nonce=%s&oauth_timestamp=%s&oauth_token=%s&oauth_signature=%s' % (self.api_host, self.api_key, self.oauth_consumer_key, \
                      OAUTH_VERSION, SIGNATURE_METHOD, nonce, timestamp, self.oauth_token, self.oauth_signature) 
        data = self.make_api_call(url=url)

   