# Define a custom User class to work with django-social-auth
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.crypto import get_random_string as random_string
from utils.oper import percentage, send_email
from users.models import Profile


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
    education_level_manual = models.IntegerField(default=2)
    education_degree = models.CharField(max_length=250, blank=True, null=True)
    work_experience_years = models.IntegerField(default=0)
    work_experience_years_manual = models.IntegerField(default=0)
    create_time = models.DateTimeField("created on", auto_now_add=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)
    wikilife_ids = models.CharField(max_length=255, null=True)

    def social_reach(self):
        f_count = self.facebook_friend_count or 0
        t_count = self.twitter_followers_count or 0
        l_count = self.linkedin_connections_count or 0
        g_count = self.gplus_contacts_count or 0
        fq_count = self.foursquare_friends_count or 0

        total = f_count + t_count + l_count + g_count + fq_count
        f_per = percentage(f_count, total)
        l_per = percentage(l_count, total)
        g_per = percentage(g_count, total)
        t_per = percentage(t_count, total)
        fq_per = percentage(fq_count, total)
        
        data = {"facebook":{"count": f_count, "percentage":f_per}, "twitter":{"count": t_count, "percentage":t_per},
                "gmail":{"count": g_count, "percentage":g_per}, "foursquare":{"count": fq_count, "percentage":fq_per},
                "linkedin":{"count": l_count, "percentage":l_per}}

        return data
    
    def social_sharing(self):
        return {"facebook":{"posts":self.facebook_post_weekly_avg, "likes":self.facebook_likes_weekly_avg},
        "twitter":{"tweets":self.twitter_tweets_count_last_seven_days, "retweets":self.twitter_retweets_count_last_seven_days}}


class GlobalEducationDistribution(models.Model):
    elementary = models.FloatField(default=0.0)
    high_school = models.FloatField(default=0.0)
    junior_college = models.FloatField(default=0.0)
    tech = models.FloatField(default=0.0)
    university = models.FloatField(default=0.0)
    master = models.FloatField(default=0.0)
    phd = models.FloatField(default=0.0)
    create_time = models.DateTimeField("created on", auto_now_add=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)

    class Meta:
        get_latest_by = 'update_time'
        #MyModel.objects.latest() you will get the latest instance based on the date/time field.
        #And when I tested your code using sample data, it indeed did.
    
class GlobalWorkExperinceDistribution(models.Model):
    range_15_25 = models.IntegerField(default=0)
    range_26_35 = models.IntegerField(default=0)
    range_36_45 = models.IntegerField(default=0)
    range_46_55 = models.IntegerField(default=0)
    range_56_65 = models.IntegerField(default=0)
    create_time = models.DateTimeField("created on", auto_now_add=True)
    update_time = models.DateTimeField("last updated on", auto_now=True)

    class Meta:
        get_latest_by = 'update_time'

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

# method for updating
def create_user_social(sender, instance, **kwargs):

    profile, created  = Profile.objects.get_or_create(user=instance)
    if created:
        #Send email
        send_email(instance.email, "email/welcome.html", "email/welcome.txt")
    if created or profile.user == None:
        profile.user = instance
        profile.save()

    if created or not profile.account_id:
        generated_uid = random_string(length=6,
                      allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        
        u_profile = None
        try:
            u_profile = Profile.objects.get(account_id=generated_uid)
        except:
            pass
        
        while u_profile is not None:
            generated_uid = random_string(length=6,
                      allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
            try:
                u_profile = Profile.objects.get(account_id=generated_uid)
            except:
                pass
            
        profile.account_id = generated_uid
        profile.save()
     
    
    """social, created = SocialUserAggregatedData.objects.get_or_create(user=instance)
    if created or social.user == None:
        social.user = instance
        social.save()"""
     
    
post_save.connect(create_user_social, sender=User, dispatch_uid="create_user_social")
