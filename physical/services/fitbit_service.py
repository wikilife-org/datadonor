# coding=utf-8

from datetime import datetime
from django.contrib.auth.models import User
from health.models import UserSleepLog
from nutrition.models import UserFoodLog
from physical.clients.fitbit import FitbitClient
from physical.models import UserActivityLog
from physical.services.base_device_service import BaseDeviceService
from string import lower
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
from wikilife_utils.logs.log_creator import LogCreator
from wikilife_utils.parsers.date_parser import DateParser
from wikilife_utils.tests.date_utils_tests import DateUtilsTests

FITBIT_API = "https://api.fitbit.com"
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
MILISECONDS_TO_HOURS =  3600000
MILES_TO_STEPS = 2300
KILOMETROS_TO_MILES = 0.621371192

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

        wl_logs = []

        user = User.objects.get(id=user_id)
        dd_user_profile = self._update_profile(user, **profile_items)
        distanceUnit = profile.get("distanceUnit", "METRIC")
        foods = client.get_user_foods()
        for item in foods:
            for food in item["foods"]:
                food_entry_id = food["logId"]
                fdate = food["logDate"]
                carbs = food["nutritionalValues"].get("carbs", 0)
                protein = food["nutritionalValues"].get("protein", 0)
                fat = food["nutritionalValues"].get("fat", 0)
                fiber = food["nutritionalValues"].get("fiber",0)
                
                food_log, created = UserFoodLog.objects.get_or_create(user=user, device_log_id=food_entry_id, provider=self._profile_source)
                food_log.provider = self._profile_source
                food_log.device_log_id = food_entry_id
                food_log.protein = float(protein)
                food_log.carbs = float(carbs)
                food_log.fat = float(fat)
                food_log.fiber = float(fiber)
                food_log.execute_time = datetime.strptime(fdate, '%Y-%m-%d')
                food_log.save()
                
                """
                if created:
                    wl_log = self._create_food_log(food)
                    wl_logs.append(wl_log)
                """

        sleeps = client.get_user_sleep()
        for item in sleeps:
            for sleep in item["sleep"]:
                activity, created = UserSleepLog.objects.get_or_create(user=user, device_log_id=sleep["logId"])

                activity.execute_time = datetime.strptime(sleep["startTime"][:10], '%Y-%m-%d')
                activity.provider = "fitbit"
                activity.minutes = round(float(sleep["duration"]/ 60000),2)  
                activity.save()

                if created:
                    wl_log = self._create_sleep_log(sleep)
                    wl_logs.append(wl_log)

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
                    if distanceUnit == "en_GB":
                        activity_obj.miles =  round(float(activity["distance"] * KILOMETROS_TO_MILES),2) 
                    else:
                        activity_obj.miles =  round(float(activity["distance"]),2) 
                if "steps" in activity:
                    activity_obj.steps =  round(float(activity["steps"])) 

                activity_obj.save()

                if created:
                    wl_log = self._create_activity_log(activity, distanceUnit)
                    wl_logs.append(wl_log)

        if len(wl_logs) > 0:
            self._send_logs_to_wl(dd_user_profile, wl_logs)

    def _create_food_log(self, food):
        """
        wl_log = LogCreator.create_log(0, start, end, text, source, nodes)        
        return wl_log 
        """
        pass

    def _create_sleep_log(self, sleep):
        start = DateParser.from_datetime( sleep["startDate"] + " " + sleep["startTime"])
        duration_minutes = float(sleep["duration"])
        end = DateUtils.add_seconds(start, duration_minutes*60)
        text = "Sleep"
        source = "datadonor.fitbit"
        nodes = []
        node_id = 271229
        metric_id = 271233 #TODO Duration metric is deprecated
        nodes.append(LogCreator.create_log_node(node_id, metric_id, duration_minutes))
        wl_log = LogCreator.create_log(0, start, end, text, source, nodes)        
        return wl_log 

    def _create_activity_log(self, activity, distance_unit):
        act_name = activity["name"].lower()
        text = "%s" %activity["name"]
        source = "datadonor.fitbit"
        start = DateParser.from_datetime( activity["startDate"] + " " + activity["startTime"] )

        if "duration" in activity: 
            end = DateUtils.add_seconds(start, (float(activity["duration"])/1000))
        else:
            end = start

        nodes = []
        node_id = ACTIVITY_TYPE_NODE_ID_MAP[act_name]

        if "distance" in activity:
            if distance_unit == "en_GB":
                value = round(float(activity["distance"]), 2) 
            else:
                value = round(float(activity["distance"])/KILOMETROS_TO_MILES, 2) 

            metric_id = 2344
            nodes.append(LogCreator.create_log_node(node_id, metric_id, value))
            text = "%s, %s" %(text, ("%s km" %value))

        if act_name=="walking" and "steps" in activity:
            metric_id = 2345
            value = int(activity["steps"])
            nodes.append(LogCreator.create_log_node(node_id, metric_id, value))
            text = "%s, %s" %(text, ("%s steps" %value))
    
        if "calories" in activity:
            metric_id = 394
            value = int(activity["calories"])
            nodes.append(LogCreator.create_log_node(node_id, metric_id, value))
            text = "%s, %s" %(text, ("%s cal" %value))

        wl_log = LogCreator.create_log(0, start, end, text, source, nodes)        
        return wl_log 

    def pull_user_activity(self, user_id, user_auth):
        pass
