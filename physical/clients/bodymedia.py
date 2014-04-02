# coding=utf-8


from physical.clients.base_device_client import BaseDeviceClient
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
from social_auth.utils import setting
from oauth2 import Consumer as OAuthConsumer, Token, Request as OAuthRequest, \
                 Client, SignatureMethod_PLAINTEXT
                   
from social_auth.backends import OAuthBackend, NutritionBackend, BaseOAuth,\
    ConsumerBasedOAuth
from utils.date_util import get_days_list_int_tuple
import simplejson
import oauth2 as oauth

SIGNATURE_METHOD = 'HMAC-SHA1'
OAUTH_VERSION = '1.0'

class BodymediaClient(BaseDeviceClient):
    PAGE_SIZE = 25

    _api_host = None
    _access_token = None
    _user_info = None
    _key = None
    _secret = None
    _default_params = None
    _headers = None

    def __init__(self, api_host, access_token):
        self._api_host = api_host
        self._access_token = access_token
        self._key = setting("BODYMEDIA_CONSUMER_KEY")
        self._secret = setting("BODYMEDIA_CONSUMER_SECRET")
        self._headers = {"Content-type": "application/json"}
        self._default_params = {"api_key": self._key,}
        self._user_info = self._get_user_info()

    
    def get_user_profile(self):
        return self._user_info

    def get_user_steps(self):
        return self._get_user_activity_last_7_days("/step/day/")

    def get_user_sleep(self):
        return self._get_user_activity_last_7_days("/sleep/day/")

    def get_user_nutrition(self):
        return self._get_user_activity_last_6_days("/consumption/day/micro/")


    def _get_user_activity_last_6_days(self, activity_code):
        date_to = DateUtils.get_date_utc()
        date_from = DateUtils.add_days(date_to, -6)
        return self._get_user_activity(activity_code, date_from, date_to)

    def _get_user_activity_last_7_days(self, activity_code):
        date_to = DateUtils.get_date_utc()
        date_from = DateUtils.add_days(date_to, -7)
        return self._get_user_activity(activity_code, date_from, date_to)

    def _get_user_activity(self, activity_code, date_from, date_to):
        result = {}
        result["items"] = None
        result["activity"] = activity_code
        result["date_from"] = date_from
        result["date_to"] = date_to
        
        uri = activity_code
        if date_from:
            uri = uri + date_from.strftime("%Y%m%d") + "/"
        if date_to:
            uri = uri + date_to.strftime("%Y%m%d") + "/"
    
        response = self._get(uri)
        result["items"] = response["days"]

 
        return result

    def _get_user_info(self):
        return self._get("/user/info")
        
    def _get(self, service_uri, params={} ):
        token = Token.from_string(self._access_token)
        consumer = OAuthConsumer(self._key, self._secret)
        client = oauth.Client(consumer, token)
        client.set_signature_method(oauth.SignatureMethod_PLAINTEXT())
        url =  self._api_host + service_uri + "?api_key=%s" % (self._key)



        # and launch the request
        resp, content = client.request(url, "GET", headers=self._headers)
        if resp['status'] != '200':
            print content
            raise Exception("Invalid response from BodyMedia.")

        # return the interpreted data
        return simplejson.loads(content)