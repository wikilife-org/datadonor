# coding=utf-8

from datetime import datetime
from django.contrib.auth.models import User
from health.models import UserSleepLog
from nutrition.models import *
from physical.clients.bodymedia import BodymediaClient
from physical.models import UserActivityLog
from physical.services.base_device_service import BaseDeviceService
from string import lower
from users.models import Profile
from wikilife_utils.date_utils import DateUtils
from wikilife_utils.formatters.date_formatter import DateFormatter
from wikilife_utils.logs.log_creator import LogCreator
from wikilife_utils.parsers.date_parser import DateParser


BODYMEDIA_API = 'http://api.bodymedia.com/v2/json'
METERS_TO_MILES = 0.000621371192
SECONDS_TO_HOURS = 0.000277777778
MILES_TO_STEPS = 2300


class BodymediaService(BaseDeviceService):

    _profile_source = "bodymedia"

    def pull_user_info(self, user_id, user_auth):
        client = BodymediaClient(BODYMEDIA_API, user_auth["access_token"])

        wl_logs = []

        user = User.objects.get(id=user_id)
        dd_user_profile = Profile.objects.get(user=user)

        steps = client.get_user_steps()
        for item in steps["items"]:
            device_log_id = self._profile_source +"_steps_" +item["date"]
            activity, created = UserActivityLog.objects.get_or_create(user=user, device_log_id=device_log_id)
            
            activity.execute_time = datetime.strptime(item["date"], '%Y%m%d')
            activity.provider = "bodymedia"
            activity.steps = round(float(item["totalSteps"]))
            activity.save()

            if created:
                wl_log = self._create_step_log(item)
                wl_logs.append(wl_log)

        sleeps = client.get_user_sleep()
        for item in sleeps["items"]:
            device_log_id = self._profile_source +"_sleep_" +item["date"]
            activity, created = UserSleepLog.objects.get_or_create(user=user, device_log_id=device_log_id)

            activity.execute_time = datetime.strptime(item["date"], '%Y%m%d')
            activity.provider = "bodymedia"
            activity.minutes = round(float(item["totalSleep"]),2)  
            activity.save()

            if created:
                wl_log = self._create_sleep_log(item)
                wl_logs.append(wl_log)

        nutrients = client.get_user_nutrition()
        for item in nutrients["items"]:
            food_date = datetime.strptime(item["mealDay"]["date"], '%Y%m%d')
            food_entry_id = self._profile_source +"_nutrients_" +item["mealDay"]["date"]
            carbs = 0.0
            protein = 0.0
            fat = 0.0
            fiber = 0.0
            for food in item["mealDay"]["nutrients"]:
                if food["code"] == "CARBOHYDRATE":
                    carbs = food["totalAmount"]
                if food["code"] == "DIETARY_FIBER,_TOTAL":
                    fiber = food["totalAmount"]
                if food["code"] == "FAT,_TOTAL":
                    fat = food["totalAmount"]
                if food["code"] == "PROTEIN":
                    protein = food["totalAmount"]
            
            food_log, created = UserFoodLog.objects.get_or_create(user=user, device_log_id=food_entry_id, provider=self._profile_source)
            food_log.provider = self._profile_source
            food_log.protein = float(protein)
            food_log.carbs = float(carbs)
            food_log.fat = float(fat)
            food_log.fiber = float(fiber)
            food_log.execute_time = food_date
            food_log.save()

            """
            if created:
                wl_log = self._create_food_log(item)
                wl_logs.append(wl_log)
            """

        if len(wl_logs) > 0:
            self._send_logs_to_wl(dd_user_profile, wl_logs)

    def _create_step_log(self, steps):
        total_steps = int(steps["totalSteps"])
        text = "Walking %s steps" %total_steps 
        source = "datadonor.bodymedia"
        start = DateParser.from_datetime(steps["date"])
        end = start

        nodes = []
        node_id = 1011
        metric_id = 2345
        value = total_steps
        nodes.append(LogCreator.create_log_node(node_id, metric_id, value))
        text = "%s, %s" %(text, ("%s steps" %value))

        wl_log = LogCreator.create_log(0, start, end, text, source, nodes)        
        return wl_log 

    def _create_sleep_log(self, sleep):
        total_sleep_minutes = round(float(sleep["totalSleep"]), 2)
        text = "Sleep %s minutes" %total_sleep_minutes 
        source = "datadonor.bodymedia"
        start = DateParser.from_datetime(sleep["date"])
        end = DateUtils.add_seconds(start, total_sleep_minutes*60)

        nodes = []
        node_id = 271229
        metric_id = 271233 #TODO Duration metric is deprecated
        nodes.append(LogCreator.create_log_node(node_id, metric_id, total_sleep_minutes))
        wl_log = LogCreator.create_log(0, start, end, text, source, nodes)        
        return wl_log 
            
    def _create_food_log(self, food):
        """
        wl_log = LogCreator.create_log(0, start, end, text, source, nodes)        
        return wl_log 
        """
        pass

    def pull_user_activity(self, user_id, user_auth):
        pass
    