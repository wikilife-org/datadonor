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
KILOMETROS_TO_MILES = 0.621371192

class JawboneService(BaseDeviceService):

    _profile_source = "jawbone"
    def pull_user_info(self, user_id, user_auth):
        client = JawboneClient(JAWBONE_API,user_auth["access_token"])
        """
        {u'meta': {u'code': 200, u'message': u'OK', u'user_xid': u'0GV2QrCjzTS1s1O-CtgPEQ', u'time': 1398451930},
         u'data': {u'xid': u'0GV2QrCjzTS1s1O-CtgPEQ', 
                    u'weight': 57.0, u'gender': True, 
                    u'image': u'', u'height': 1.66, 
                    u'last': u'Macgibbon', u'first': u'Romina'}}
        """
        profile = client.get_user_information()

        user = User.objects.get(id=user_id)
        
        foods = client.get_user_meals()
        if foods["data"]["size"]>0:
            for food in foods["data"]["items"]:
                food_entry_id = food["xid"]
                fdate = "%s"%food["date"]
                carbs = food["details"]["carbohydrate"]
                protein = food["details"]["protein"]
                fat = food["details"]["fat"]
                fiber = food["details"]["fiber"]
                
                food_log, created = UserFoodLog.objects.get_or_create(user=user, device_log_id=food_entry_id, provider=self._profile_source)
                food_log.provider = self._profile_source
                food_log.device_log_id = food_entry_id
                food_log.protein = float(protein)
                food_log.carbs = float(carbs)
                food_log.fat = float(fat)
                food_log.fiber = float(fiber)
                food_log.execute_time = datetime.strptime(fdate, '%Y%m%d')
                food_log.save()
                
        sleeps = client.get_user_sleep_list()
        if sleeps["data"]["size"]>0:
            for sleep in sleeps["data"]["items"]:
                activity, created = UserSleepLog.objects.get_or_create(user=user, device_log_id=sleep["xid"])
                activity.execute_time = datetime.strptime("%s"%sleep["date"], '%Y%m%d')
                activity.provider = "jawbone"
                activity.minutes = round(float(sleep["details"]["duration"]/ 60),2)  
                activity.save()
                 
        activities = client.get_user_moves()
        if activities["data"]["size"]>0:
            for activity in activities["data"]["items"]:
                activity_obj, created = UserActivityLog.objects.get_or_create(user=user, device_log_id=activity["xid"])
                activity_obj.type = activity["type"].lower()
                
                activity_obj.execute_time = datetime.strptime("%s"%activity["date"], '%Y%m%d')
                activity_obj.provider = "jawbone"
                
                if "active_time" in activity["details"]:
                    activity_obj.hours = round((float(activity["details"]["active_time"]) / 60) /60,2)
                if "km" in activity["details"]:
                    activity_obj.miles =  round(float(activity["details"]["km"] * KILOMETROS_TO_MILES),2) 
                if "steps" in activity["details"]:
                    activity_obj.steps =  round(float(activity["details"]["steps"])) 

                activity_obj.save()
    