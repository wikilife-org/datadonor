
from django.conf import settings
from django.db import models


class GlobalMoodLastWeek(models.Model):
    avg_mood=models.IntegerField(null=False)
    update_time = models.DateTimeField("last updated on", auto_now=True)


class UserMoodLastWeek(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL, related_name='mood_week')
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
    user=models.OneToOneField(settings.AUTH_USER_MODEL, related_name='sleep_week')
    sun=models.FloatField(null=False, default=0)
    mon=models.FloatField(null=False, default=0)
    tue=models.FloatField(null=False, default=0)
    wed=models.FloatField(null=False, default=0)
    thu=models.FloatField(null=False, default=0)
    fri=models.FloatField(null=False, default=0)
    sat=models.FloatField(null=False, default=0)
    update_time = models.DateTimeField("last updated on", auto_now=True)

    
class UserConditions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='conditions')
    condition_id = models.IntegerField()
    type_id = models.IntegerField(null=True)
    metric_id = models.IntegerField(null=True)
    log_id = models.IntegerField(null=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)

class UserComplaints(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='complaints')
    complaint_id = models.IntegerField()
    metric_id = models.IntegerField(null=True)
    log_id = models.IntegerField(null=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)

class UserOxygenSaturation(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='oxygen_saturation')
    execute_time = models.DateField(null=True)
    value = models.FloatField(null=True)
    device_log_id = models.CharField(null=True, max_length=256)
    provider = models.CharField(null=True, max_length=256)
    update_time = models.DateTimeField("last updated on", auto_now=True)

class UserBloodAlcoholContent(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='blood_alcohol_content')
    execute_time = models.DateField(null=True)
    value = models.FloatField(null=True)
    device_log_id = models.CharField(null=True, max_length=256)
    provider = models.CharField(null=True, max_length=256)
    update_time = models.DateTimeField("last updated on", auto_now=True)

class UserBloodGlucose(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='blood_glucose')
    execute_time = models.DateField(null=True)
    value = models.FloatField(null=True)
    device_log_id = models.CharField(null=True, max_length=256)
    provider = models.CharField(null=True, max_length=256)
    update_time = models.DateTimeField("last updated on", auto_now=True) 

class UserBodyTemperature(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='body_temperature')
    execute_time = models.DateField(null=True)
    value = models.FloatField(null=True)
    device_log_id = models.CharField(null=True, max_length=256)
    provider = models.CharField(null=True, max_length=256)
    update_time = models.DateTimeField("last updated on", auto_now=True) 

class UserHeartRate(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='heart_rate')
    execute_time = models.DateField(null=True)
    value = models.FloatField(null=True)
    device_log_id = models.CharField(null=True, max_length=256)
    provider = models.CharField(null=True, max_length=256)
    update_time = models.DateTimeField("last updated on", auto_now=True)    
  
class UserBloodType(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='blood_type')
    blood_type_id = models.IntegerField()
    metric_id = models.IntegerField()
    log_id = models.IntegerField()
    update_time = models.DateTimeField("last updated on", auto_now=True)
 
class UserEmotions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='emotions')
    emotion_id = models.IntegerField()
    metric_id = models.IntegerField(null=True)
    log_id = models.IntegerField(null=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)

class UserSleepLog(models.Model): 
    user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sleeps')
    execute_time = models.DateField(null=True)
    minutes = models.FloatField(null=True)
    device_log_id = models.CharField(null=True, max_length=256)
    provider = models.CharField(null=True, max_length=256)
    update_time = models.DateTimeField("last updated on", auto_now=True)
