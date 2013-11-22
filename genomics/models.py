
from django.conf import settings
from django.db import models


class UserTrait(models.Model):
    user= models.OneToOneField(settings.AUTH_USER_MODEL, related_name='traits')
    report_id = models.CharField()
    value = models.CharField()

class UserDrugResponse(models.Model):
    user= models.OneToOneField(settings.AUTH_USER_MODEL, related_name='drug_reponse')
    report_id = models.CharField()
    value = models.CharField()

class UserRisk(models.Model):
    user= models.OneToOneField(settings.AUTH_USER_MODEL, related_name='risks')
    report_id = models.CharField()
    value = models.CharField()
