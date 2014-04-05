# coding=utf-8

from django.contrib.auth.models import User

from health.clients.withings import WithingsClient
from health.services.base_device_service import BaseDeviceService
from datetime import date, timedelta

WITHINGS_API = 'http://wbsapi.withings.net'


class WithingsService(BaseDeviceService):

    _profile_source = "withings"

    def pull_user_info(self, user_id, user_auth):
        user = User.objects.get(id=user_id)
        client = WithingsClient(WITHINGS_API, user_auth["access_token"])
        measures = client.get_measures()
        
        week_ago = date.today() - timedelta(days=7)
        height = None
        weight = None
        for measure in measures:
            if not height:
                height = measure.height
            if measure.weight and measure.date.date() > week_ago:
                weight = measure.weight

        if height:
            #convertir a mts to feets
            height = round(float(height*3.28084 ),2)
            user.profile.height = height
            user.profile.save()
            
        if weight:
            weight = round(float(weight*2.2046),0)
            user.profile.weight = weight
            user.profile.save()
