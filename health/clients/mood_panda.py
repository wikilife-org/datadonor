# coding=utf-8

"""
Mood Panda
http://www.moodpanda.com/api/

"""

from health.clients.base_device_client import BaseDeviceClient
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
from xml.etree import ElementTree
import requests


class MoodPandaClient(BaseDeviceClient):

    _api_host = None
    _api_key = None
    _user_email = None
    _user_info = None
    _user_id = None

    def __init__(self, api_host, api_key, user_email=None, user_id=None):
        
        self._api_host = api_host
        self._api_key = api_key
        
        if user_id != None:
            self._user_id = user_id
        elif user_email != None:
            self._user_email = user_email
            self._user_id = self._get_user_id()
        else:
            raise Exception("Missing user_email or user_id")

    def _get_user_mood(self, date_from, date_to):
        
        """
        http://moodpanda.com/api/user/feed/data.ashx?userid=1&from=2013-09-30&to=2013-10-30&format=xml&DateOrder=ASC&key=abc
        """
        
        uri = "/user/feed/data.ashx"
        params = {}
        params["from"] = date_from
        params["to"] = date_to
        params["userid"] = self._user_id
        result = self._get(uri, params=params)
        return result

    def _get_user_mood_last_30_days(self):
        date_to = DateUtils.get_date_utc()
        date_from = DateUtils.add_days(date_to, -30)
        return self._get_user_mood(date_from, date_to)
    
    def _get_avg_mood_last_30_days(self):
        result = self._get_user_mood_last_30_days()
        sum_mood = 0
        count_mood = 0
        avg = 0
        for mood in result:
            
            sum_mood += int(mood[1].text)
            count_mood = count_mood + 1
        
        if count_mood:
            avg = int(sum_mood/count_mood)
            
        return avg
            
    def _get_user_profile(self):

        """
        http://moodpanda.com/api/user/data.ashx?userid=4&format=xml&key=abc
        """
        
        params = {}
        params["userid"] = self._user_id
        return self._get("/user/data.ashx", params)

    def _get_user_id(self):
        """
        http://moodpanda.com/api/user/getid/data.ashx?email=email@email.com&format=xml&key=abc
        """
        params = {}
        params["email"] = self._user_email
 
        data = self._get("/user/getid/data.ashx", params)
        try:
            return data[0][0].text
        except:
            return ""
    
    def _get(self, service_uri, params={}):
        """
        service_uri: String
        params: Dict<String, String>
        """
        url =  self._api_host + service_uri
        params["key"] = self._api_key
        params["format"] = "xml"
        response = requests.request("GET", url, params=params)
        return ElementTree.fromstring(response.content)
    