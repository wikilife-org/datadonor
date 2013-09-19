# Define a custom User class to work with django-social-auth
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
try:
    from django.utils.crypto import get_random_string as random_string
except ImportError:  # django < 1.4
    # Implementation borrowed from django 1.4
    def random_string(length=6,
                      allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'):
        if not using_sysrandom:
            random.seed(hashlib.sha256('%s%s%s' % (random.getstate(),
                                                   time.time(),
                                                   settings.SECRET_KEY))
                               .digest())
        return ''.join([random.choice(allowed_chars) for i in range(length)])
    
from utils.oper import percentage, social_reach_graph

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
    height = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    device_id = models.CharField(max_length=255, null=True)
    timezone = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    region = models.CharField(max_length=255, null=True)
    country = models.CharField(max_length=255, null=True)
    wikilife_token = models.CharField(max_length=255, null=True)
    wikilife_ready = models.BooleanField(default=False)
    agree_tos = models.BooleanField(default=True)


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
        
        
        
        #data = social_reach_graph(  (f_per, f_count), (t_per, t_count), 
        #                            (g_per, g_count), (l_per, l_count), 
        #                            (fq_per, fq_count))
        
        data = {"facebook":{"count": f_count, "percentage":f_per}, "twitter":{"count": t_count, "percentage":t_per},
                "gmail":{"count": g_count, "percentage":g_per}, "foursquare":{"count": fq_count, "percentage":fq_per},
                "linkedin":{"count": l_count, "percentage":l_per}}
        return data

    

class GlobalEducationDistribution(models.Model):
    elementary = models.FloatField(default=0.0)
    high_school = models.FloatField(default=0.0)
    junior_collage = models.FloatField(default=0.0)
    tech = models.FloatField(default=0.0)
    university = models.FloatField(default=0.0)
    master = models.FloatField(default=0.0)
    phd = models.FloatField(default=0.0)
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

# method for updating
def create_user_social(sender, instance, **kwargs):

     
     profile, created  = Profile.objects.get_or_create(user=instance)
     if created or profile.user != None:
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
     
     social, created = SocialUserAggregatedData.objects.get_or_create(user=instance)
     if created or social.user != None:
         social.user = instance
         social.save()
     
    
post_save.connect(create_user_social, sender=User, dispatch_uid="create_user_social")
