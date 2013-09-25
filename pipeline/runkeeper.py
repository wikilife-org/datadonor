"""
Runkeeper
http://developer.runkeeper.com/healthgraph/overview
"""

from utils.client import oauth_req, dsa_urlopen, build_consumer_oauth_request
import requests
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter


RUNKEEPER_API = ""


def runkeeper_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "runkeeper":
        data = kwargs.get('response')
        print data
        
        """
        access_token = None 
        backend = None
        client = RunkeeperClient(RUNKEEPER_API, access_token, backend)
        #TODO >> wikilife logs or local datadonor data ?
        """

class RunkeeperClient(object):
    PAGE_SIZE = 25

    _api_host = None
    _backend = None
    _access_token = None
    _user_info = None

    def __init__(self, api_host, access_token, backend):
        self._api_host = api_host
        self._access_token = access_token
        self._backend = backend
        self._user_info = self._get_user_info()

    def get_user_info(self):
        return self._user_info

    def get_user_profile(self):
        url =  self._api_host + self._user_info["profile"]
        request = build_consumer_oauth_request(self._backend, self._access_token, url)
        response = requests.request("GET", url, headers=request.to_header())
        return response.json()
    
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

        url =  self._api_host + self._user_info[activity_code]
        request = build_consumer_oauth_request(self._backend, self._access_token, url)

        params = {}
        params["page"] = 0 
        params["pageSize"] = self.PAGE_SIZE 
        params["noEarlierThan"] = DateFormatter.to_date(date_from)
        params["noLaterThan"] = DateFormatter.to_date(date_to)

        raw_response = requests.request("GET", url, headers=request.to_header(), params=params)
        response = raw_response.json()
        result["items"] = response["items"]

        while (params["page"]+1)*self.PAGE_SIZE < response["size"]:
            params["page"] += 1
            raw_response = requests.request("GET", url, headers=request.to_header(), params=params)
            response = raw_response.json()
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
        url =  self.RUNKEEPER_API + "/user"
        request = build_consumer_oauth_request(self._backend, self._access_token, url)
        response = requests.request("GET", url, headers=request.to_header())
        return response.json()

