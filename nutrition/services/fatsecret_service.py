# coding=utf-8

from nutrition.services.base_device_service import BaseDeviceService
from nutrition.clients.fatsecret import FatsecretClient
from datetime import datetime
from nutrition.models import *
from users.models import Profile
from django.contrib.auth.models import User


FATSECRET_API = "http://platform.fatsecret.com/rest/server.api"

class FatsecretService(BaseDeviceService):

    _profile_source = "fatsecret"

    def pull_user_info(self, user_id, user_auth):
        client = FatsecretClient(FATSECRET_API, user_auth["access_token"])
        
        wl_logs = []
        
        foods_logs = client.get_user_food_last_7_days()
        user = User.objects.get(id=user_id)
        dd_user_profile = Profile.objects.get(user=user)
        
        for log in foods_logs:
            food_date = log["food_entries"]["date"]
            #datetime.strptime(item["start_time"], '%a, %d %b %Y %H:%M:%S')
            for food in log["food_entries"]["food_entry"]:
                food_entry_id = food["food_entry_id"]
                carbs = food.get("carbohydrate", 0)
                protein = food.get("protein", 0)
                fat = food.get("fat", 0)
                fiber = food.get("fiber",0)
                
                food_log, created = UserFoodLog.objects.get_or_create(user=user, device_log_id=food_entry_id, provider=self._profile_source)
                food_log.provider = self._profile_source
                food_log.device_log_id = food_entry_id
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

    def _create_food_log(self, food):
        """
        wl_log = LogCreator.create_log(0, start, end, text, source, nodes)        
        return wl_log 
        """
        pass
                
    def pull_user_activity(self, user_id, user_auth):
        pass
