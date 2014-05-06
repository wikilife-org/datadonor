# coding=utf-8

from physical.clients.moves import MovesClient
from physical.services.base_device_service import BaseDeviceService

from string import lower
from physical.models import UserActivityLog
from health.models import UserSleepLog
from datetime import datetime
from django.contrib.auth.models import User
from nutrition.models import UserFoodLog

MOVES_API = 'https://api.moves-app.com/api/1.1'

METERS_TO_MILES = 0.000621371192
MILISECONDS_TO_HOURS =  3600000
MILES_TO_STEPS = 2300
KILOMETROS_TO_MILES = 0.621371192

class MovesService(BaseDeviceService):

    _profile_source = "moves"
    def pull_user_info(self, user_id, user_auth):
        client = MovesClient(MOVES_API,user_auth["access_token"])
        
        """
        duration: duration of the activity in seconds
        distance (optional): distance for the activity in meters (if applicable)
        steps (optional): step count for the activity (if applicable)
        """
        
        user = User.objects.get(id=user_id)              
        activities = client.get_activities()

        for day in activities:
            if day["summary"]:
                for activity in day["summary"]:
                    device_log_id = activity["group"] + "_" + day["date"]
                    activity_obj, created = UserActivityLog.objects.get_or_create(user=user, device_log_id=device_log_id)
                    activity_obj.type = activity["group"].lower()
                    
                    activity_obj.execute_time = datetime.strptime(day["date"], '%Y%m%d')
                    activity_obj.provider = "moves"
                    
                    if "duration" in activity:
                        activity_obj.hours = round((float(activity["duration"]) / 60) /60,2)
                    if "distance" in activity:
                        activity_obj.miles =  round(float(activity["distance"] * METERS_TO_MILES),2) 
                    if "steps" in activity:
                        activity_obj.steps =  round(float(activity["steps"])) 
        
                    activity_obj.save()
        