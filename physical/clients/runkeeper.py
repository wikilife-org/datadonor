# coding=utf-8

"""
Runkeeper
http://developer.runkeeper.com/healthgraph/overview
"""

from physical.clients.base_device_client import BaseDeviceClient
from utils.date_util import DateUtils
#from wikilife_utils.formatters.date_formatter import DateFormatter
import requests


class RunkeeperClient(BaseDeviceClient):
    PAGE_SIZE = 25

    _api_host = None
    _access_token = None
    _user_info = None

    def __init__(self, api_host, access_token):
        self._api_host = api_host
        self._access_token = access_token
        self._user_info = self._get_user_info()

    def get_user_profile(self):
        return self._get(self._user_info["profile"])

    def get_user_fitness_activities(self):
        return self._get_user_activity_last_7_days("fitness_activities")

    def get_user_strength_training_activities(self):
        return self._get_user_activity_last_7_days("strength_training_activities")

    def get_user_background_activities(self):
        return self._get_user_activity_last_7_days("background_activities")

    def get_user_sleep(self):
        return self._get_user_activity_last_7_days("sleep")

    def get_user_nutrition(self):
        return self._get_user_activity_last_7_days("nutrition")

    def get_user_weight(self):
        return self._get_user_activity_last_7_days("weight")

    def get_user_general_measurements(self):
        return self._get_user_activity_last_7_days("general_measurements")

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

        uri =  self._user_info[activity_code] 

        params = {}
        params["page"] = 0 
        params["pageSize"] = self.PAGE_SIZE 
        params["noEarlierThan"] = date_from.strftime("%Y-%m-%d")
        params["noLaterThan"] = date_to.strftime("%Y-%m-%d")

        response = self._get(uri, params=params)
        result["items"] = response["items"]

        while (params["page"]+1)*self.PAGE_SIZE < response["size"]:
            params["page"] += 1
            response = self._get(uri, params=params)
            result["items"].extend(response["items"])

        return result

    def _get_user_info(self):
        """
        {
        "userID": 1234567890,
        "profile": "/profile",
        "settings": "/settings",
        "fitness_activities": "/fitnessActivities",
        "strength_training_activities": "/strengthTrainingActivities",
        "background_activities": "/backgroundActivities",
        "sleep": "/sleep",
        "nutrition": "/nutrition",
        "weight": "/weight",
        "general_measurements": "/generalMeasurements",
        "diabetes": "/diabetes",
        "records": "/records",
        "team": "/team"
        }
        """
        return self._get("/user")

    def _get(self, service_uri, params={}):
        """
        service_uri: String
        params: Dict<String, String>
        """
        url =  self._api_host + service_uri
        params["access_token"] = self._access_token
        response = requests.request("GET", url, params=params)
        return response.json()
