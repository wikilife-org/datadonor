
from django.conf import settings
from django.db import models

class UserFoodLog(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, related_name='foods')
    execute_time = models.DateField(null=True)
    protein = models.FloatField(null=True)
    fat = models.FloatField(null=True)
    fiber = models.FloatField(null=True)
    carbs = models.FloatField(null=True)
    group = models.CharField(null=True, max_length=256)
    device_log_id = models.CharField(null=True, max_length=256)
    provider = models.CharField(null=True, max_length=256)
    update_time = models.DateTimeField("last updated on", auto_now=True)