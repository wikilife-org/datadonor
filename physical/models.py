
from django.conf import settings
from django.db import models

RUNNING_WL_ACT_ID = 814
WALKING_WL_ACT_ID = 1011
ELLIPTICAL_WL_ACT_ID = 564

STEPS_ACT_CODE = "steps"
MILES_ACT_CODE = "miles"
HOURS_ACT_CODE = "hours"


class GlobalPhysicalActivity(models.Model):
    act_wl_id=models.IntegerField(null=False)
    act_wl_name=models.CharField(max_length=64, null=False)
    tpw=models.FloatField(null=False)
    update_time = models.DateTimeField("last updated on", auto_now=True)


class UserPhysicalActivity(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, related_name='physical_activity')
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
    user=models.OneToOneField(settings.AUTH_USER_MODEL, related_name='physical_distribution')
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

class UserActivityLog(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='physical_activities')
    execute_time = models.DateField(null=True)
    miles = models.FloatField(null=True)
    hours = models.FloatField(null=True)
    steps = models.FloatField(null=True)
    activity_count = models.FloatField(null=False)
    nike_fuel = models.FloatField(null=False)
    active_energy = models.FloatField(null=False)
    type = models.CharField(null=True, max_length=256)
    device_log_id = models.CharField(null=True, max_length=256)
    provider = models.CharField(null=True, max_length=256)
    update_time = models.DateTimeField("last updated on", auto_now=True)
    