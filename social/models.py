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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='social_aggregated_data', blank=True, null=True)
    facebook_friend_count = models.IntegerField(default=0)
    facebook_post_count_last_seven_days = models.IntegerField(default=0)
    facebook_likes_count_last_seven_days = models.IntegerField(default=0)
    twitter_followers_count = models.IntegerField(default=0)
    twitter_tweets_count_last_seven_days = models.IntegerField(default=0)
    twitter_retweets_count_last_seven_days = models.IntegerField(default=0)
    gmail_contacts_count = models.IntegerField(default=0)
    linkedin_connections_count = models.IntegerField(default=0)
    foursquare_friends_count = models.IntegerField(default=0)
    education_level = models.IntegerField(default=2)
    education_degree = models.CharField(max_length=250, blank=True, null=True)
    work_experience_years = models.IntegerField(default=0)
    create_time = models.DateTimeField("created on", auto_now_add=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)

class GlobalEducationDistribution(models.Model):
    junior_collage = models.IntegerField()
    primary_school = models.IntegerField()
    high_school = models.IntegerField()
    technichal_institute = models.IntegerField()
    undergraduated_programs = models.IntegerField()
    master = models.IntegerField()
    phd = models.IntegerField()
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

class DegreeLevel(models.Model):
    title = models.CharField(unique=True, max_length=250)
    primary = models.IntegerField(default=0)
    junior = models.IntegerField(default=0)
    high = models.IntegerField(default=0)
    tech = models.IntegerField(default=0)
    under = models.IntegerField(default=0)
    master = models.IntegerField(default=0)
    phd = models.IntegerField(default=0)
    
    def education_level(self):
        
        values = sorted([(0, self.primary), (1, self.junior), (2, self.high), 
                         (3, self.tech), (4, self.under), (5, self.master), 
                         (6, self.phd)],key=lambda x: x[1])
        
        return values[6]