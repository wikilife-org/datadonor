# coding=utf-8

from django.contrib.auth.models import User

from health.clients.moodsy import MoodsyClient
from health.services.base_device_service import BaseDeviceService
from datetime import date, timedelta


class MoodsyService(BaseDeviceService):

    _profile_source = "moodsy"

    def pull_user_info(self, user_id, user_auth):
        user = User.objects.get(id=user_id)
        client = MoodsyClient(user_auth["access_token"])
        