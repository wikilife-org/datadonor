
from django.conf import settings
from django.db import models


RUNNING_WL_ACT_ID = 0
WALKING_WL_ACT_ID = 0
ELLIPTICAL_WL_ACT_ID = 0

STEPS_ACT_CODE = "steps"
MILES_ACT_CODE = "miles"
HOURS_ACT_CODE = "hours"


class GlobalPhysicalActivity(models.Model):
    act_wl_id=models.IntegerField(null=False)
    act_wl_name=models.CharField(max_length=64, null=False)
    tpw=models.FloatField(null=False)
    update_time = models.DateTimeField("last updated on", auto_now=True)


class UserPhysicalActivity(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    act_wl_id=models.IntegerField(null=False)
    tpw=models.FloatField(null=False)
    update_time = models.DateTimeField("last updated on", auto_now=True)


class GlobalDistributionLastWeek(models.Model):
    act_code=models.CharField(max_length=16, null=False)
    sun=models.FloatField(null=False, default=0)
    mon=models.FloatField(null=False, default=0)
    tue=models.FloatField(null=False, default=0)
    wed=models.FloatField(null=False, default=0)
    thu=models.FloatField(null=False, default=0)
    fri=models.FloatField(null=False, default=0)
    sat=models.FloatField(null=False, default=0)
    avg=models.FloatField(null=False, default=0)
    update_time = models.DateTimeField("last updated on", auto_now=True)


class UserDistributionLastWeek(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    act_code=models.CharField(max_length=16, null=False)
    sun=models.FloatField(null=False, default=0)
    mon=models.FloatField(null=False, default=0)
    tue=models.FloatField(null=False, default=0)
    wed=models.FloatField(null=False, default=0)
    thu=models.FloatField(null=False, default=0)
    fri=models.FloatField(null=False, default=0)
    sat=models.FloatField(null=False, default=0)
    avg=models.FloatField(null=False, default=0)
    update_time = models.DateTimeField("last updated on", auto_now=True)
