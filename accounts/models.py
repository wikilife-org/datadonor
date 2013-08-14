from django.conf import settings
from django.db import models

class BaseAccount(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    account_id = models.CharField(max_length=255)
    
class FacebookAccount(BaseAccount):
    about_me = models.TextField(blank=True, null=True)
    facebook_id = models.BigIntegerField(blank=True, unique=True, null=True)
    access_token = models.TextField(
        blank=True, help_text='Facebook token for offline access', null=True)
    facebook_name = models.CharField(max_length=255, blank=True, null=True)
    facebook_profile_url = models.TextField(blank=True, null=True)
    website_url = models.TextField(blank=True, null=True)
    blog_url = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(
        ('m', 'Male'), ('f', 'Female')), blank=True, null=True)
    raw_data = models.TextField(blank=True, null=True)


class TwitterAccount(BaseAccount):
    
    pass
