# coding=utf-8

from physical.clients.runkeeper import RunkeeperClient
from physical.services.base_device_service import BaseDeviceService
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
from wikilife_utils.logs.log_creator import LogCreator
from wikilife_utils.parsers.date_parser import DateParser
from string import lower
from physical.models import UserActivityLog
from health.models import UserSleepLog
from datetime import datetime
from django.contrib.auth.models import User

RUNKEEPER_API = "http://api.runkeeper.com"
ACTIVITY_TYPE_NODE_ID_MAP = {
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

METERS_TO_MILES = 0.000621371192
SECONDS_TO_HOURS = 0.000277777778
MILES_TO_STEPS = 2300

class RunkeeperService(BaseDeviceService):

    _profile_source = "runkeeper"

    def pull_user_info(self, user_id, user_auth):
        client = RunkeeperClient(RUNKEEPER_API, user_auth["access_token"])
        profile = client.get_user_profile()
        profile_items = {}

        if "gender" in profile:
            profile_items["gender"] = lower(profile["gender"])

        if "birthday" in profile:
            profile_items["birthday"] = DateParser.from_datetime(profile["birthday"])

        """
        if "location" in profile:
            profile_items["location"] = profile["location"]
        """

        user = User.objects.get(id=user_id)
        self._update_profile(user, **profile_items)
        
        activities = client.get_user_fitness_activities()
        for item in activities["items"]:
            activity, created = UserActivityLog.objects.get_or_create(user=user, device_log_id=item["uri"])
            activity.type = item["type"].lower()
            
            activity.execute_time = datetime.strptime(item["start_time"], '%a, %d %b %Y %H:%M:%S')
            activity.provider = "runkeeper"
            
            if "duration" in item:
                activity.hours = round(float(item["duration"]) * SECONDS_TO_HOURS,2)
            if "total_distance" in item:
                activity.miles =  round(float(item["total_distance"]) * METERS_TO_MILES,2) 
            
            if activity.type in ["walking", "running"]:
                activity.steps = round(float(activity.miles * MILES_TO_STEPS))   
                
            activity.save()
        
        sleeps = client.get_user_sleep()
        for item in sleeps["items"]:
            activity, created = UserSleepLog.objects.get_or_create(user=user, device_log_id=item["uri"])
            
            activity.execute_time = datetime.strptime(item["timestamp"], '%a, %d %b %Y %H:%M:%S')
            activity.provider = "runkeeper"
            activity.minutes = round(float(item["total_sleep"]),2)  
            activity.save()

    def pull_user_activity(self, user_id, user_auth):
        #wikilife_token = self._get_wikilife_token(user_id)
        client = RunkeeperClient(RUNKEEPER_API, user_auth["access_token"])
        fitness_activities = client.get_user_fitness_activities()
        #self._log_fitness_activities(wikilife_token, fitness_activities["items"])
        return fitness_activities
        
    def pull_user_activity_(self, user_id, user_auth):
        wikilife_token = self._get_wikilife_token(user_id)
        client = RunkeeperClient(RUNKEEPER_API, user_auth["access_token"])
        fitness_activities = client.get_user_fitness_activities()
        self._log_fitness_activities(wikilife_token, fitness_activities["items"])
 
    def _log_fitness_activities(self, wikilife_token, items):
        for item in items:
            start_time = DateParser.from_datetime(item["start_time"])
            end_time = DateUtils.add_seconds(start_time, item["duration"])
            start = DateFormatter.to_datetime(start_time)
            end = DateFormatter.to_datetime(end_time)
            node_id = ACTIVITY_TYPE_NODE_ID_MAP[item["type"]]
            distance_km = item["total_distance"] * 1000
            calories = item["total_calories"]
            text = "%s %s km, %s calories" %(item["type"], distance_km, calories)
            source = "datadonor.runkeeper.%s" %item["source"]

            nodes = []
            nodes.append(LogCreator.create_log_node(self, node_id, 0, distance_km))
            nodes.append(LogCreator.create_log_node(self, node_id, 0, calories))

            log = LogCreator.create_log(self, 0, start, end, text, source, nodes)
            self._log_client.add_log(wikilife_token, log)
