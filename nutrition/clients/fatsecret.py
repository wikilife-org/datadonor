# coding=utf-8

"""
Fatsecret
http://platform.fatsecret.com/api/Default.aspx?screen=rapih
"""
from oauth2 import Consumer as OAuthConsumer, Token, Request as OAuthRequest, \
                   SignatureMethod_HMAC_SHA1, HTTP_METHOD, Client, SignatureMethod_PLAINTEXT
                   
from social_auth.backends import OAuthBackend, NutritionBackend, BaseOAuth,\
    ConsumerBasedOAuth
from nutrition.clients.base_device_client import BaseDeviceClient
import requests
from social_auth.utils import dsa_urlopen, setting
from utils.date_util import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
from utils.date_util import get_days_list_int_tuple

class FatsecretClient(BaseDeviceClient):

    _api_host = None
    _access_token = None
    _user_info = None
    
    def __init__(self, api_host, access_token):
        self._api_host = api_host
        self._access_token = access_token


    def get_user_food_last_7_days(self):
        days = get_days_list_int_tuple(7)
        result = []
        for d in days:
            day = self._get_user_food(d[1])
            if day["food_entries"]:
                day["food_entries"]["date"] = d[0]
            #    for food in day["food_entries"]["food_entry"]:
            #        food["food_info"] = self._get_food_info(food["food_id"])
                result.append(day)
        
        return result

    
    def _get_food_info(self, food_id):
        
        params = {"method": "food.get", "format":"json", "food_id":food_id}
        return self._get(params)
    
    def _get_user_food(self, f_date):
        
        params = {"method": "food_entries.get", "format":"json", "date":f_date}
        return self._get(params)
    

    def get_user_nutrients_last_7_days(self):
        date_to = DateUtils.get_date_utc()
        date_from = DateUtils.add_days(date_to, -7)
        return self._get_user_nutrients(date_from, date_to)
    
    def _get_user_nutrients(self, from_date, to_date):
        
        params = {"method": "food_entries.get_month", "format":"json"}
        return self._get(params)

    
    def _get(self, params={}):
        
        """     
        oauth_verifier = self.data.get('oauth_verifier')
        if oauth_verifier:
            params['oauth_verifier'] = oauth_verifier
        """
        key = setting("FATSECRET_REST_API_ACCESS_KEY")
        secret = setting("FATSECRET_REST_API_SHARED_SECRET")
        consumer = OAuthConsumer(key, secret)
        token = Token.from_string(self._access_token)
        request = OAuthRequest.from_consumer_and_token(consumer,
                                                       token=token,
                                                       http_method="GET",
                                                       http_url=self._api_host,
                                                       parameters=params,
                                                       is_form_encoded=True)
        request.sign_request(SignatureMethod_HMAC_SHA1(), consumer, token)
        response = requests.get(request.to_url())
        return response.json()
    
    def _get_last_7_days_tuple(self):
        pass
        #response = dsa_urlopen(request.to_url())
        #return '\n'.join(response.readlines())
    