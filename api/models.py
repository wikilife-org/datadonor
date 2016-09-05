
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save

class Location(models.Model):
    lat = models.CharField(max_length=100, blank=True, null=True)
    lon = models.CharField(max_length=100, blank=True, null=True)
    city= models.CharField(max_length=300, blank=True, null=True)
    region= models.CharField(max_length=300, blank=True, null=True)
    country= models.CharField(max_length=300, blank=True, null=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)

class WeatherByDay(models.Model):
    location = models.ForeignKey(Location, related_name="weather")
    temp_f= models.CharField(max_length=300, blank=True, null=True)
    temp_c= models.CharField(max_length=300, blank=True, null=True)
    weather= models.CharField(max_length=300, blank=True, null=True)
    icon = models.CharField(max_length=300, blank=True, null=True)
    date = models.DateField()
    update_time = models.DateTimeField("last updated on", auto_now=True)
    
class Log(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='logs', db_index=True)
    text = models.CharField(max_length=300, blank=True, null=True)
    location = models.ForeignKey(Location, related_name="location_logs", blank=True, null=True)
    weather = models.ForeignKey(WeatherByDay, related_name="weather_logs", blank=True, null=True)
    category= models.CharField(max_length=300, blank=True, null=True)
    wiki_node_name= models.CharField(max_length=300, blank=True, null=True)
    wiki_node_id= models.CharField(max_length=300, blank=True, null=True)
    source = models.CharField(max_length=300, blank=True, null=True, default="manual")
    image_url= models.CharField(max_length=300, blank=True, null=True)
    execute_time = models.DateTimeField("execute on", db_index=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)
    create_time = models.DateTimeField("created on", auto_now_add=True)
    
    class Meta:
        ordering = ["-execute_time",]
        
    def to_dict(self):
        result = {}
        result["log_id"] = self.id
        result["user_id"] = self.user.id
        result["text"] = self.text
        result["category"] = self.category
        result["wiki_node_name"] = self.wiki_node_name
        result["wiki_node_id"] = self.wiki_node_id
        result["image_url"] = self.image_url
        result["execute_time"] = self.execute_time.strftime("%Y-%m-%d %H:%M:%S")
        count = 0
        for data in self.data.all():
            count = count+1
            name = "prop%s_name"%count
            result[name] = data.unit
            name_value = "prop%s_value"%count
            result[name_value] = data.value
        result["weather_icon"] = None
        if self.weather != None:
            result["weather_icon"] = self.weather.icon
        return result
        
class Data(models.Model):
    log = models.ForeignKey(Log, related_name='data')
    #log_text_slug = models.CharField(max_length=300, blank=True, null=True)
    #log_category = models.CharField(max_length=300, blank=True, null=True)
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

