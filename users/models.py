# coding=utf-8

from django.conf import settings
from django.db import models

class ResarchKitBackendUser(models.Model):
    email = models.CharField(max_length=255, blank=False, null=False)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    account_id = models.CharField(max_length=255, unique=True, null=False)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(
        ('m', 'Male'), ('f', 'Female')), blank=True, null=True)
    age_range= models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField("created on", auto_now_add=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)
    height = models.FloatField(blank=True,null=True)
    weight = models.FloatField(blank=True,null=True)
    device_id = models.CharField(max_length=255, blank=True,null=True)
    timezone = models.CharField(max_length=255, blank=True,null=True)
    city = models.CharField(max_length=255, blank=True,null=True)
    region = models.CharField(max_length=255, blank=True,null=True)
    country = models.CharField(max_length=255,blank=True, null=True)
    
    first_name_source = models.CharField(max_length=255, blank=True, null=True)
    last_name_source = models.CharField(max_length=255, blank=True, null=True)
    email_source = models.CharField(max_length=64, blank=True,null=True)
    age_source = models.CharField(max_length=64, blank=True,null=True)
    date_of_birth_source = models.CharField(max_length=64, blank=True,null=True)
    gender_source = models.CharField(max_length=64, blank=True,null=True)
    height_source = models.CharField(max_length=64, blank=True,null=True)
    weight_source = models.CharField(max_length=64, blank=True,null=True)
    timezone_source = models.CharField(max_length=64, blank=True,null=True)
    city_source = models.CharField(max_length=64, blank=True,null=True)
    region_source = models.CharField(max_length=64, blank=True,null=True)
    country_source = models.CharField(max_length=64, blank=True,null=True)
    
    agree_tos = models.BooleanField(default=True)
    wikilife_token = models.CharField(max_length=255, blank=True,null=True)
    wikilife_ready = models.BooleanField(default=False)
    sent_welcome_email = models.BooleanField(default=False)
    send_weekly_email  = models.BooleanField(default=False)
    
    def __unicode__(self):
        return u"{0}".format(self.email)


class Contact(models.Model):
    from_email = models.EmailField()
    subject = models.CharField(max_length=300)
    content = models.TextField()
    
    def __unicode__(self):
        return u"{0}".format(self.from_email)
    