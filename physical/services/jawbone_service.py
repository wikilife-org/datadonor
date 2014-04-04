# coding=utf-8

from physical.clients.jawbone import JawboneClient
from physical.services.base_device_service import BaseDeviceService

from string import lower
from physical.models import UserActivityLog
from health.models import UserSleepLog
from datetime import datetime
from django.contrib.auth.models import User
from nutrition.models import UserFoodLog

JAWBONE_API = 'https://jawbone.com/nudge/api/v.1.1/' 
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

class JawboneService(BaseDeviceService):

    _profile_source = "jawbone"
    def pull_user_info(self, user_id, user_auth):
        client = JawboneClient(JAWBONE_API,user_auth["access_token"])
        profile = client.get_user_information()
    
    def pull_user_info_(self, user_id, user_auth):
        profile = client.get_user_information()
        profile_items = {}
        
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
        pass
