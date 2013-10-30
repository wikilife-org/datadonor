# coding=utf-8

"""
Mood Panda
http://www.moodpanda.com/api/

"""

from health.clients.base_device_client import BaseDeviceClient
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
import requests


class MoodPandaClient(BaseDeviceClient):
    PAGE_SIZE = 25

    _api_host = None
    _api_key = None
    _user_email = None
    _user_info = None
    _user_id = None

    def __init__(self, api_host, api_key, user_email):
        self._api_host = api_host
        self._api_key = api_key
        self._user_email = user_email
        self._user_id = self._get_user_id()

    def _get_user_activity(self, activity_code, date_from, date_to):
        result = {}
        result["items"] = None
        result["activity"] = activity_code
        result["date_from"] = date_from
        result["date_to"] = date_to

        uri =  self._user_info[activity_code] 

        params = {}
        params["page"] = 0 
        params["pageSize"] = self.PAGE_SIZE 
        params["noEarlierThan"] = DateFormatter.to_date(date_from)
        params["noLaterThan"] = DateFormatter.to_date(date_to)

        response = self._get(uri, params=params)
        result["items"] = response["items"]

        while (params["page"]+1)*self.PAGE_SIZE < response["size"]:
            params["page"] += 1
            response = self._get(uri, params=params)
            result["items"].extend(response["items"])

        return result

    def get_user_profile(self):

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
 
        return self._get("/user/getid/data.ashx", params)
    
    def _get(self, service_uri, params={}):
        """
        service_uri: String
        params: Dict<String, String>
        """
        url =  self._api_host + service_uri
        params["key"] = self._api_key
        params["format"] = "xml"
        response = requests.request("GET", url, params=params)
        return response.json()