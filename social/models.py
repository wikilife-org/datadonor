# Define a custom User class to work with django-social-auth
from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    account_id = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255)
    age = models.IntegerField()
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(
        ('m', 'Male'), ('f', 'Female')), blank=True, null=True)
    create_time = models.DateTimeField("created on", auto_now_add=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)



class SocialUserAggregatedData(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    facebook_friend_count = models.IntegerField()
    facebook_post_count_last_seven_days = models.IntegerField()
    facebook_likes_count_last_seven_days = models.IntegerField()
    twitter_followers_count = models.IntegerField()
    twitter_tweets_count_last_seven_days = models.IntegerField()
    twitter_retweets_count_last_seven_days = models.IntegerField()
    gmail_contacts_count = models.IntegerField()
    linkedin_connections_count = models.IntegerField()
    foursquare_connections_count = models.IntegerField()
    education_level = models.IntegerField()
    work_experience_years = models.IntegerField()
    create_time = models.DateTimeField("created on", auto_now_add=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)

class GlobalEducationDistribution(models.Model):
    junior_collage = models.IntegerField()
    primary_school = models.IntegerField()
    high_school = models.IntegerField()
    technichal_institute = models.IntegerField()
    undergraduated_programs = models.IntegerField()
    master = models.IntegerField()
    phd_and_above = models.IntegerField()
    create_time = models.DateTimeField("created on", auto_now_add=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)

class SocialGlobalAggregatedData(models.Model):
    avg_facebook_friend_count = models.IntegerField()
    avg_facebook_post_count_last_seven_days = models.IntegerField()
    avg_facebook_likes_count_last_seven_days = models.IntegerField()
    avg_twitter_followers_count = models.IntegerField()
    avg_twitter_tweets_count_last_seven_days = models.IntegerField()
    avg_twitter_retweets_count_last_seven_days = models.IntegerField()
    avg_gmail_contacts_count = models.IntegerField()
    avg_linkedin_connections_count = models.IntegerField()
    avg_foursquare_connections_count = models.IntegerField()
    education = models.OneToOneField(GlobalEducationDistribution)
    avg_work_experience_years = models.IntegerField()
    create_time = models.DateTimeField("created on", auto_now_add=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)
