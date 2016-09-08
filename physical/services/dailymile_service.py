# coding=utf-8

from physical.clients.dailymile import DailymileClient
from physical.services.base_device_service import BaseDeviceService
from utils.date_util import DateUtils
#from wikilife_utils.formatters.date_formatter import DateFormatter
#from wikilife_utils.logs.log_creator import LogCreator
#from wikilife_utils.parsers.date_parser import DateParser
from string import lower
from physical.models import UserActivityLog
from health.models import UserSleepLog
from datetime import datetime
from django.contrib.auth.models import User
from users.models import Profile

DAILYMILE_API = 'https://api.dailymile.com/people'
ACTIVITY_TYPE_NODE_ID_MAP = {
    "running": 814, 
    "run": 814,
    "cycling": 536, 
    "mountain biking": 731, 
    "walking": 1011, 
    "hiking": 620, 
    "downhill skiing": 559, 
    "cross-country skiing": 518, 
    "snowboarding": 878, 
    "skating": 796,  
    "swimming": 921, 
    "rowing": 801, 
    "elliptical": 564
}

METERS_TO_MILES = 0.000621371192
SECONDS_TO_HOURS = 0.000277777778
MILES_TO_STEPS = 2300

class DailymileService(BaseDeviceService):

    _profile_source = "dailymile"

    def pull_user_info(self, user_id, user_auth):
        wl_logs = []

        user = User.objects.get(id=user_id)
        dd_user_profile = Profile.objects.get(user=user)
        client = DailymileClient(DAILYMILE_API, user_auth["access_token"])
        activities = client.get_user_activities()["entries"]
        for item in activities:
            if "workout" in item:
                activity, created = UserActivityLog.objects.get_or_create(user=user, device_log_id=item["id"])
                activity.type = item["workout"]["activity_type"].lower()

                activity.execute_time = datetime.strptime(item["at"][:10], '%Y-%m-%d')
                activity.provider = "dailymile"

                if "duration" in item["workout"]:
                    activity.hours = round(float(item["workout"]["duration"]) * SECONDS_TO_HOURS,2)
                if "distance" in item["workout"]:
                    if item["workout"]["distance"]["units"] == "miles":
                        activity.miles =  round(float(item["workout"]["distance"]["value"]),2) 
                    else:
                        activity.miles =  round(float(item["workout"]["distance"]["value"]) * METERS_TO_MILES,2) 

                if activity.type in ["walking", "running"]:
                    activity.steps = round(float(activity.miles * MILES_TO_STEPS))   

                activity.save(created=created)

                """if created:
                    wl_log = self._create_workout_log(item)
                    wl_logs.append(wl_log)"""

        """if len(wl_logs) > 0:
            self._send_logs_to_wl(dd_user_profile, wl_logs)"""

    """def _create_workout_log(self, item):
        act_type = item["workout"]["activity_type"].lower()
        text = "%s" %item["workout"]["activity_type"]
        source = "datadonor.dailymile"
        start = DateParser.from_datetime(item["at"])

        if "duration" in item["workout"]: 
            end = DateUtils.add_seconds(start, float(item["workout"]["duration"]))
        else:
            end = start

        nodes = []
        node_id = ACTIVITY_TYPE_NODE_ID_MAP[act_type]

        if "distance" in item["workout"]:
            if item["workout"]["distance"]["units"] == "miles":
                value = round(float(item["workout"]["distance"]["value"]) / METERS_TO_MILES, 2) 
            else:
                value = round(float(item["workout"]["distance"]["value"]) / 1000, 2) 

            metric_id = 2344
            nodes.append(LogCreator.create_log_node(node_id, metric_id, value))
            text = "%s, %s" %(text, ("%s km" %value))

        if act_type=="walking":
            metric_id = 2345
            value = round(value*1000*METERS_TO_MILES * MILES_TO_STEPS)
            nodes.append(LogCreator.create_log_node(node_id, metric_id, value))
            text = "%s, %s" %(text, ("%s steps" %value))

        wl_log = LogCreator.create_log(0, start, end, text, source, nodes)        
        return wl_log""" 


    ''' 
    def pull_user_info_(self, user_id, user_auth):
        client = DailymileClient(DAILYMILE_API, user_auth["access_token"])
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
    ''' 
    
    def pull_user_activity(self, user_id, user_auth):
        pass
    
    """def pull_user_activity(self, user_id, user_auth):
        #wikilife_token = self._get_wikilife_token(user_id)
        client = RunkeeperClient(RUNKEEPER_API, user_auth["access_token"])
        fitness_activities = client.get_user_fitness_activities()
        #self._log_fitness_activities(wikilife_token, fitness_activities["items"])
        return fitness_activities"""
    
    """
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
    """
