# coding=utf-8

from oauth2 import Consumer as OAuthConsumer, Token, Request as OAuthRequest, \
                   SignatureMethod_HMAC_SHA1, HTTP_METHOD, Client, SignatureMethod_PLAINTEXT
                   
from social_auth.backends import OAuthBackend, NutritionBackend, BaseOAuth,\
    ConsumerBasedOAuth
from nutrition.clients.base_device_client import BaseDeviceClient
import requests
from social_auth.utils import dsa_urlopen, setting
from utils.date_util import DateUtils
#from wikilife_utils.formatters.date_formatter import DateFormatter
from utils.date_util import get_days_list_int_tuple

"""
Client_id The ID for the client request
client_secret The key for the request
access_token The token for access
sc The serial number for the user
sv This is type of one on one value based on sv
"""

class IhealthClient(BaseDeviceClient):

    _api_host = None
    _access_token = None
    _user_info = None
    
    def __init__(self, api_host, access_token):
        self._api_host = api_host
        self._access_token = access_token


    def get_user_activity(self):
        url = self._api_host + "application/activity.json"
        #days = get_days_list_int_tuple(7)
        #result = []
        result = self._get_activities(url)
        #for d in days:
        #    day = self._get_user_food(d[1])
        #    if day["food_entries"]:
        #        day["food_entries"]["date"] = d[0]
            #    for food in day["food_entries"]["food_entry"]:
            #        food["food_info"] = self._get_food_info(food["food_id"])
        #        result.append(day)
        
        return result

    def get_user_sleep(self):
        url = self._api_host + "application/sleep.json"
        result = self._get_sleep(url)
        return result
    
    def _get_activities(self, url):
        
        """
            [{
            "Calories": 109,
            "DataID": "e34032089471451b926a6a4*****",
            "DistanceTraveled": 0.36088,
            "Lat": 19.579758571265153,
            "Lon": 86.49735491466585,
            "MDate": 1362483513,
            "Note": "",
            "Steps": 694
            },]
        """
        key = setting("IHEALTH_ACTIVITY_SV")
        return self._get(url, key)

    def _get_sleep(self, url):
        
        """
            [{
            "Awaken": 5,
            "DataID": "6ca9e6f4c8c34e4d9a9eccc*****",
            "EndTime": 1372103460,
            "FellSleep": 25,
            "HoursSlept": 260,
            "Lat": 28.584006583590064,
            "Lon": 69.43493275457757,
            "Note": "",
            "SleepEfficiency": 92,
            "StartTime": 1372085160
            },]
        """
        key = setting("IHEALTH_SLEEP_SV")
        return self._get(url, key)
    
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

    
    def _get(self, url, info_key):
        
        key = setting("IHEALTH_CONSUMER_KEY")
        secret = setting("IHEALTH_CONSUMER_SECRET")
        sc = setting('IHEALTH_USER_SN')
        params = {"Client_id": key, "client_secret": secret, "access_token":self._access_token, "sc": sc, "sv":info_key}
        response = requests.get(url, params=params)
        return response.json()
    
    