# coding=utf-8

from django.contrib.auth.models import User

from health.clients.ihealth import IhealthClient
from health.services.base_device_service import BaseDeviceService
from datetime import date, timedelta
from utils.date_util import DateUtils
#from wikilife_utils.formatters.date_formatter import DateFormatter
#from wikilife_utils.logs.log_creator import LogCreator
#from wikilife_utils.parsers.date_parser import DateParser
from string import lower
from physical.models import UserActivityLog
from health.models import UserSleepLog
from datetime import datetime
from django.contrib.auth.models import User
from nutrition.models import UserFoodLog


IHEALTH_API = 'https://api.ihealthlabs.com:8443/OpenApiV2/'

KILOMETROS_TO_MILES = 0.621371192


class IhealthService(BaseDeviceService):

    _profile_source = "ihealth"

    def pull_user_info(self, user_id, user_auth):
        user = User.objects.get(id=user_id)
        client = IhealthClient(IHEALTH_API, user_auth["access_token"])
        activities = client.get_user_activity()
        distanceUnit = activities.get("DistanceUnit", 0)
        """
        
        Unit    Value
        km    0
        mile    1
        """
        for activity in activities["ARDataList"]:
            """
            {
            "Calories": 109,
            "DataID": "e34032089471451b926a6a4*****",
            "DistanceTraveled": 0.36088,
            "Lat": 19.579758571265153,
            "Lon": 86.49735491466585,
            "MDate": 1362483513,
            "Note": "",
            "Steps": 694
            },
            """
            activity_obj, created = UserActivityLog.objects.get_or_create(user=user, device_log_id=activity["DataID"])
            activity_obj.type = "running"
            
            activity_obj.execute_time = datetime.fromtimestamp(activity["MDate"])
            activity_obj.provider = self._profile_source

            if "DistanceTraveled" in activity:
                if distanceUnit == 0:
                    activity_obj.miles =  round(float(activity["DistanceTraveled"] * KILOMETROS_TO_MILES),2) 
                else:
                    activity_obj.miles =  round(float(activity["DistanceTraveled"]),2) 
            if "Steps" in activity:
                activity_obj.steps =  round(float(activity["Steps"])) 

            activity_obj.save()

        sleeps = client.get_user_sleep()["SRDataList"]
        for item in sleeps:
            for sleep in item["sleep"]:
                activity, created = UserSleepLog.objects.get_or_create(user=user, device_log_id=sleep["DataID"])
                
                activity.execute_time = datetime.strptime(datetime.fromtimestamp(["StartTime"]), '%Y-%m-%d')
                activity.provider = self._profile_source
                activity.minutes = round(float(sleep["HoursSlept"] * 60),2)  
                activity.save()