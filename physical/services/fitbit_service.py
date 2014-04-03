# coding=utf-8

from physical.clients.fitbit import FitbitClient
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
from nutrition.models import UserFoodLog

FITBIT_API = "https://api.fitbit.com"
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
MILISECONDS_TO_HOURS =  3600000
MILES_TO_STEPS = 2300

class FitbitService(BaseDeviceService):

    _profile_source = "fitbit"
    def pull_user_info_(self, user_id, user_auth):
        pass
    
    def pull_user_info(self, user_id, user_auth):
        client = FitbitClient(FITBIT_API,user_auth["access_token"])
        profile = client.get_user_profile()["user"]
        profile_items = {}
        
        #TODO: Se puede sacar mucha mas info para el profile
        #dict: {u'user': {u'weight': 188.4, u'memberSince': u'2011-07-18', 
        #u'locale': u'es_ES', u'strideLengthWalking': 29.881889763779526, 
        #u'height': 72.00787401574803, u'strideLengthRunning': 37.48031496062992, 
        #u'glucoseUnit': u'METRIC', u'timezone': u'America/Argentina/Buenos_Aires', 
        #u'avatar150': u'https://d6y8z.png', u'city': u'Buenos Aires',
        # u'dateOfBirth': u'1984-04-20', u'foodsLocale': u'en_US',
        # u'distanceUnit': u'en_US', u'heightUnit': u'en_US',
        # u'offsetFromUTCMillis': -10800000, u'fullName': u'Joaquin Quintas',
        # u'nickname': u'joa_q', u'displayName': u'Joaquin',
        # u'gender': u'MALE', u'weightUnit': u'METRIC',
        # u'avatar': u'https://d6y32Dsquare.png',
        # u'waterUnit': u'en_US', u'country': u'AR', u'encodedId': u'226ZXF'}}
        if "gender" in profile:
            if "male" == lower(profile["gender"]):
                profile_items["gender"] = "m"
            elif "female" == lower(profile["gender"]):
                profile_items["gender"] = "f"
                


        """
        if "location" in profile:
            profile_items["location"] = profile["location"]
        """

        user = User.objects.get(id=user_id)
        self._update_profile(user, **profile_items)

        foods = client.get_user_foods()
        for item in foods:
            for food in item["foods"]:
                food_entry_id = food["logId"]
                fdate = food["logDate"]
                carbs = food["nutritionalValues"]["carbs"]
                protein = food["nutritionalValues"]["protein"]
                fat = food["nutritionalValues"]["fat"]
                fiber = food["nutritionalValues"]["fiber"]
                
                food_log, created = UserFoodLog.objects.get_or_create(user=user, device_log_id=food_entry_id, provider=self._profile_source)
                food_log.provider = self._profile_source
                food_log.device_log_id = food_entry_id
                food_log.protein = float(protein)
                food_log.carbs = float(carbs)
                food_log.fat = float(fat)
                food_log.fiber = float(fiber)
                food_log.execute_time = datetime.strptime(fdate, '%Y-%m-%d')
                food_log.save()
                
        sleeps = client.get_user_sleep()
        for item in sleeps:
            for sleep in item["sleep"]:
                activity, created = UserSleepLog.objects.get_or_create(user=user, device_log_id=sleep["logId"])
                
                activity.execute_time = datetime.strptime(sleep["startTime"][:10], '%Y-%m-%d')
                activity.provider = "fitbit"
                activity.minutes = round(float(sleep["duration"]/ 60000),2)  
                activity.save()
                 
        activities = client.get_user_fitness_activities()
        for item in activities:
            for activity in item["activities"]:
                #{u'activityParentName': u'Walking', u'description': u'5.0 mph, speed walking', 
                #u'isFavorite': False, u'distance': 20, 
                #u'lastModified': u'2014-04-03T14:36:46.000-03:00', u'logId': 64346624, 
                #u'hasStartTime': True, u'calories': 641, u'activityParentId': 90013,
                # u'activityId': 17231,
                # u'steps': 42407, u'startTime': u'00:00', u'duration': 3720000, 
                #u'startDate': u'2014-04-02', u'name': u'Walking'}
                activity_obj, created = UserActivityLog.objects.get_or_create(user=user, device_log_id=activity["logId"])
                activity_obj.type = activity["name"].lower()
                
                activity_obj.execute_time = datetime.strptime(activity["startDate"], '%Y-%m-%d')
                activity_obj.provider = "fitbit"
                
                if "duration" in activity:
                    activity_obj.hours = round(float(activity["duration"]) / MILISECONDS_TO_HOURS,2)
                if "distance" in activity:
                    activity_obj.miles =  round(float(activity["distance"]),2) 
                if "steps" in activity:
                    activity_obj.steps =  round(float(activity["steps"])) 

                activity_obj.save()

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
