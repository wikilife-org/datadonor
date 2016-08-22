
from django.conf import settings
from django.db import models

from api.models import Log, Data

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
    
    def save(self, *args, **kwargs):
        if self.id is None:
            category = "Exercise"
            text = self.type.title() if self.type else category
            image_url = "https://s3.amazonaws.com/datadonors-app/default-exercise.jpg"
            log = Log.objects.create(user=self.user, 
                               execute_time=self.execute_time, 
                               text=text,
                               source=self.provider,
                               category=category,
                               image_url=image_url)
            if self.miles:
                Data.objects.create(log=log, unit="miles", value=self.miles, slug_unit="miles")
            if self.hours:
                Data.objects.create(log=log, unit="hours", value=self.hours, slug_unit="hours")
            if self.steps:
                Data.objects.create(log=log, unit="steps", value=self.steps, slug_unit="steps")
                
        super(UserActivityLog, self).save(*args, **kwargs)
        