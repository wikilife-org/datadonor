"""
Runkeeper
http://developer.runkeeper.com/healthgraph/overview
"""

from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
import requests
from wikilife_utils.logs.log_creator import LogCreator
from wikilife_utils.parsers.date_parser import DateParser
from wikilife.client.logs import Logs


RUNKEEPER_API = "http://api.runkeeper.com"


def runkeeper_info(request, *args, **kwargs):
    backend = kwargs.get('backend')
    social_user = kwargs.get('social_user')
    result = {}
    if backend.name == "runkeeper":
        data = kwargs.get('response')
        client = RunkeeperClient(RUNKEEPER_API, data["access_token"], backend)
        
        profile = client.get_user_profile()
        fitness_activities = client.get_user_fitness_activities()
        wikilife_token = None
        log_fitness_activities(wikilife_token, fitness_activities["items"])
        
        print ""
        """
        #TODO >> wikilife logs or local datadonor data ?
        
        'nutrition': '/nutrition',
        'weight': '/weight',
        'settings': '/settings',
        'userID': 24084903, 'strength_training_activities': '/strengthTrainingActivities',
        'background_activities': '/backgroundActivities',
        'change_log': '/changeLog',
        'fitness_activities': '/fitnessActivities',
        'sleep': '/sleep',
        'records': '/records',
        'team': '/team',
        'general_measurements': '/generalMeasurements',
        'diabetes': '/diabetes'
        """


activity_type_node_id_map = {
    "Running": 0, 
    "Cycling": 0, 
    "Mountain Biking": 0, 
    "Walking": 0, 
    "Hiking": 0, 
    "Downhill Skiing": 0, 
    "Cross-Country Skiing": 0, 
    "Snowboarding": 0, 
    "Skating": 0, 
    "Swimming": 0, 
    "Wheelchair": 0, 
    "Rowing": 0, 
    "Elliptical": 0, 
    "Other": 0
}

wikilife_logs_client = Logs(logger, wikilife_settings)
wikilife_logs_creator = LogCreator()

def log_fitness_activities(wikilife_token, items):
    for item in items:
        start_time = DateParser.from_datetime(item["start_time"])
        end_time = DateUtils.add_seconds(start_time, item["duration"])
        start = DateFormatter.to_datetime(start_time)
        end = DateFormatter.to_datetime(end_time)
        node_id = activity_type_node_id_map[item["type"]]
        distance_km = item["total_distance"] * 1000
        calories = item["total_calories"]
        text = "%s %s km, %s calories" %(item["type"], distance_km, calories)
        source = "datadonor.runkeeper.%s" %item["source"]

        nodes = []
        nodes.append(wikilife_logs_creator.create_log_node(self, node_id, 0, distance_km))
        nodes.append(wikilife_logs_creator.create_log_node(self, node_id, 0, calories))

        log = wikilife_logs_creator.create_log(self, 0, start, end, text, source, nodes)
        wikilife_logs_client.add_log(wikilife_token, log)


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
