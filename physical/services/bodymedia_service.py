# coding=utf-8

from physical.clients.bodymedia import BodymediaClient
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

BODYMEDIA_API = 'http://api.bodymedia.com/v2/json'
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

class BodymediaService(BaseDeviceService):

    _profile_source = "bodymedia"

    def pull_user_info(self, user_id, user_auth):
        client = BodymediaClient(BODYMEDIA_API, user_auth["access_token"])
        
        user = User.objects.get(id=user_id)
         
        steps = client.get_user_steps()
        for item in steps["items"]:
            device_log_id = self._profile_source +"_steps_" +item["date"]
            activity, created = UserActivityLog.objects.get_or_create(user=user, device_log_id=device_log_id)
            
            activity.execute_time = datetime.strptime(item["date"], '%Y%m%d')
            activity.provider = "bodymedia"
            activity.steps = round(float(item["totalSteps"]))
            activity.save()
        
        sleeps = client.get_user_sleep()
        for item in sleeps["items"]:
            device_log_id = self._profile_source +"_sleep_" +item["date"]
            activity, created = UserSleepLog.objects.get_or_create(user=user, device_log_id=device_log_id)
            
            activity.execute_time = datetime.strptime(item["date"], '%Y%m%d')
            activity.provider = "bodymedia"
            activity.minutes = round(float(item["totalSleep"]),2)  
            activity.save()
            
    def pull_user_activity(self, user_id, user_auth):
        pass
        
    def pull_user_activity_(self, user_id, user_auth):
        pass
 
