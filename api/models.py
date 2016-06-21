
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class Location(models.Model):
    lat = models.IntegerField( blank=True, null=True)
    long = models.IntegerField( blank=True, null=True)
    city= models.CharField(max_length=300, blank=True, null=True)
    region= models.CharField(max_length=300, blank=True, null=True)
    country= models.CharField(max_length=300, blank=True, null=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)

class WeatherByDay(models.Model):
    location = models.ForeignKey(Location, related_name="weather")
    temp_f= models.CharField(max_length=300, blank=True, null=True)
    temp_c= models.CharField(max_length=300, blank=True, null=True)
    weather= models.CharField(max_length=300, blank=True, null=True)
    date = models.DateField()
    update_time = models.DateTimeField("last updated on", auto_now=True)
    
class Log(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='logs')
    text = models.CharField(max_length=300, blank=True, null=True)
    location = models.ForeignKey(Location, related_name="location_logs", blank=True, null=True)
    weather = models.ForeignKey(WeatherByDay, related_name="weather_logs")
    category= models.CharField(max_length=300, blank=True, null=True)
    wiki_node_name= models.CharField(max_length=300, blank=True, null=True)
    wiki_node_id= models.CharField(max_length=300, blank=True, null=True)
    image_url= models.CharField(max_length=300, blank=True, null=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)
    

class Data(models.Model):
    log = models.ForeignKey(Log, related_name='data')
    unit = models.CharField(max_length=300, blank=True, null=True)
    slug_unit = models.CharField(max_length=350, blank=True, null=True)
    value = models.IntegerField( blank=True, null=True)
    wiki_node_id = models.CharField(max_length=300, blank=True, null=True)
    wiki_node_name = models.CharField(max_length=300, blank=True, null=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)
    
class TextData(models.Model):
    log = models.ForeignKey(Log, related_name='text_data')
    unit = models.CharField(max_length=300, blank=True, null=True)
    slug_unit = models.CharField(max_length=350, blank=True, null=True)
    value = models.IntegerField( blank=True, null=True)
    wiki_node_id = models.CharField(max_length=300, blank=True, null=True)
    wiki_node_name = models.CharField(max_length=300, blank=True, null=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)

