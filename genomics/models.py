
from django.conf import settings
from django.db import models


class UserTrait(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, related_name='traits')
    #descrition = models.CharField(max_length=255)
    report_id = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

class UserDrugResponse(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, related_name='drug_reponse')
    report_id = models.CharField(max_length=255)
    value = models.CharField(max_length=255)

class UserRisk(models.Model):
    user= models.ForeignKey(settings.AUTH_USER_MODEL, related_name='risks')
    report_id = models.CharField(max_length=255)
    population_risk = models.FloatField()
    value = models.FloatField()
