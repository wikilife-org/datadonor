# Define a custom User class to work with django-social-auth
from django.conf import settings
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    account_id = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=1, choices=(
        ('m', 'Male'), ('f', 'Female')), blank=True, null=True)
    create_time = models.DateTimeField("created on", auto_now_add=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)
    wikilife_token = models.CharField(max_length=255, unique=True, null=True) #TODO funca unique except is null ?


class SocialUserAggregatedData(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='social_aggregated_data', blank=True, null=True)
    facebook_friend_count = models.IntegerField(default=0)
    facebook_post_weekly_avg = models.IntegerField(default=0)
    facebook_likes_weekly_avg = models.IntegerField(default=0)
    twitter_followers_count = models.IntegerField(default=0)
    twitter_tweets_count_last_seven_days = models.IntegerField(default=0)
    twitter_retweets_count_last_seven_days = models.IntegerField(default=0)
    gplus_contacts_count = models.IntegerField(default=0)
    linkedin_connections_count = models.IntegerField(default=0)
    foursquare_friends_count = models.IntegerField(default=0)
    education_level = models.IntegerField(default=2)
    education_degree = models.CharField(max_length=250, blank=True, null=True)
    work_experience_years = models.IntegerField(default=0)
    create_time = models.DateTimeField("created on", auto_now_add=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)
    wikilife_ids = models.CharField(max_length=255, null=True)


class GlobalEducationDistribution(models.Model):
    elementary = models.IntegerField(default=0)
    high_school = models.IntegerField(default=0)
    junior_collage = models.IntegerField(default=0)
    tech = models.IntegerField(default=0)
    university = models.IntegerField(default=0)
    master = models.IntegerField(default=0)
    phd = models.IntegerField(default=0)
    create_time = models.DateTimeField("created on", auto_now_add=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)

    
class GlobalWorkExperinceDistribution(models.Model):
    range_15_25 = models.IntegerField(default=0)
    range_25_35 = models.IntegerField(default=0)
    range_36_45 = models.IntegerField(default=0)
    range_46_55 = models.IntegerField(default=0)
    range_56_65 = models.IntegerField(default=0)
    create_time = models.DateTimeField("created on", auto_now_add=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)

   
class SocialGlobalAggregatedData(models.Model):
    avg_facebook_friend_count = models.IntegerField(default=0)
    facebook_post_weekly_avg = models.IntegerField(default=0)
    facebook_likes_weekly_avg = models.IntegerField(default=0)
    avg_twitter_followers_count = models.IntegerField(default=0)
    avg_twitter_tweets_count_last_seven_days = models.IntegerField(default=0)
    avg_twitter_retweets_count_last_seven_days = models.IntegerField(default=0)
    gplus_contacts_count = models.IntegerField(default=0)
    avg_linkedin_connections_count = models.IntegerField(default=0)
    avg_foursquare_connections_count = models.IntegerField(default=0)
    education = models.OneToOneField(GlobalEducationDistribution)
    work_experience = models.OneToOneField(GlobalWorkExperinceDistribution)
    create_time = models.DateTimeField("created on", auto_now_add=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)

    class Meta:
        get_latest_by = 'update_time'


class DegreeLevel(models.Model):
    title = models.CharField(unique=True, max_length=250)
    elementary = models.IntegerField(default=0)
    high_school = models.IntegerField(default=0)
    junior_collage = models.IntegerField(default=0)
    tech = models.IntegerField(default=0)
    university = models.IntegerField(default=0)
    master = models.IntegerField(default=0)
    phd = models.IntegerField(default=0)
    
    def education_level(self):
        
        values = sorted([(0, self.elementary), (1, self.high_school), (2, self.junior_collage), 
                         (3, self.tech), (4, self.university), (5, self.master), 
                         (6, self.phd)],key=lambda x: x[1])
        
        return values[6]