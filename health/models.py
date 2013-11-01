
from django.conf import settings
from django.db import models


class GlobalMoodLastWeek(models.Model):
    avg_mood=models.IntegerField(null=False)
    update_time = models.DateTimeField("last updated on", auto_now=True)


class UserMoodLastWeek(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    avg_mood=models.IntegerField(null=False)
    update_time = models.DateTimeField("last updated on", auto_now=True)


class GlobalSleepDistributionLastWeek(models.Model):
    sun=models.FloatField(null=False, default=0)
    mon=models.FloatField(null=False, default=0)
    tue=models.FloatField(null=False, default=0)
    wed=models.FloatField(null=False, default=0)
    thu=models.FloatField(null=False, default=0)
    fri=models.FloatField(null=False, default=0)
    sat=models.FloatField(null=False, default=0)
    update_time = models.DateTimeField("last updated on", auto_now=True)


class UserSleepDistributionLastWeek(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    sun=models.FloatField(null=False, default=0)
    mon=models.FloatField(null=False, default=0)
    tue=models.FloatField(null=False, default=0)
    wed=models.FloatField(null=False, default=0)
    thu=models.FloatField(null=False, default=0)
    fri=models.FloatField(null=False, default=0)
    sat=models.FloatField(null=False, default=0)
    update_time = models.DateTimeField("last updated on", auto_now=True)
