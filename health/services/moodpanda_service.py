# coding=utf-8

from django.contrib.auth.models import User

from health.clients.mood_panda import MoodPandaClient
from health.services.base_device_service import BaseDeviceService
from health.models import UserMoodLastWeek
from datetime import date, timedelta


class MoodPandaService(BaseDeviceService):

    _profile_source = "moodpanda"

    def pull_user_info(self, user_id, user_auth):
        user = User.objects.get(id=user_id)
        client = MoodPandaClient(user_email=user.profile.email)
        mood = client.get_avg_mood_last_30_days()
        try:
            obj = UserMoodLastWeek.objects.get(user=user)
            obj.avg_mood = mood
            obj.save()
        except:
            obj = UserMoodLastWeek.objects.create(user=user, avg_mood=mood)
 