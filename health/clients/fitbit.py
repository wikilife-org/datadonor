# coding=utf-8

"""
Fitbit
https://wiki.fitbit.com/display/API/Fitbit+Resource+Access+API
"""

from health.clients.base_device_client import BaseDeviceClient
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
import requests

FITBIT_END_POINTS = {"sleep":"/user/-/sleep/date/",
                     "nutrition": "/1/user/-/foods/log/date/",
                     "activity": "/1/user/-/activities/date/",
                     "heart_rate":"/1/user/-/heart/date/",
                     "blood_pressure": "/1/user/-/bp/date/",
                     "glucose": "/1/user/-/glucose/date/",
                     }

class FitbitClient(BaseDeviceClient):
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
        return self._get_user_activity_last_7_days("activity")

    def get_user_sleep(self):
        return self._get_user_activity_last_7_days("sleep")

    def get_user_heart_rate(self):
        return self._get_user_activity_last_7_days("heart_rate")

    def get_user_blood_pressure(self):
        return self._get_user_activity_last_7_days("blood_pressure")

    def get_user_nutrition(self):
        return self._get_user_activity_last_7_days("nutrition")

    def get_user_weight(self):
        return (self._user_info["weight"], self._user_info["weightUnit"])

    def get_user_height(self):
        return (self._user_info["height"], self._user_info["heightUnit"])

    def get_user_glucose(self):
        return self._get_user_activity_last_7_days("glucose")

    def _get_user_activity_last_7_days(self, activity_code):
        date_to = DateUtils.get_date_utc()
        date_from = DateUtils.add_days(date_to, -7) #2010-02-25.json
        return self._get_user_activity(activity_code, date_from, date_to)

    def _get_user_activity(self, activity_code, date_from, date_to):
        result = {}
        result["items"] = None
        result["activity"] = activity_code
        result["date_from"] = date_from
        result["date_to"] = date_to

        uri =  FITBIT_END_POINTS[activity_code] 

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

    def _get_user_info(self):
        """
        {
        "user":{
        "aboutMe":<value>,
        "avatar":<value>,
        "avatar150":<value>,
        "city":<value>,
        "country":<value>,
        "dateOfBirth":"<value>,
        "displayName":<value>,
        "distanceUnit":<value>,
        "encodedId":<value>,
        "foodsLocale":<value>
        "fullName":<value>,
        "gender":<FEMALE|MALE|NA>,
        "glucoseUnit":<value>,
        "height":<value>,
        "heightUnit":<value>,
        "locale":<value>,
        "memberSince":<value>,
        "nickname":<value>,
        "offsetFromUTCMillis":<value>,
        "state":<value>,
        "strideLengthRunning":<value>,
        "strideLengthWalking":<value>,
        "timezone":<value>,
        "waterUnit":<value>,
        "weight":<value>,
        "weightUnit":<value>
            }
        }
        """
        return self._get("/user/-/profile.json")

    def _get(self, service_uri, params={}):
        """
        service_uri: String
        params: Dict<String, String>
        """
        url =  self._api_host + service_uri
        params["access_token"] = self._access_token
        response = requests.request("GET", url, params=params)
        return response.json()
