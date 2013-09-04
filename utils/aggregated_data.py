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

from social.models import Profile, SocialUserAggregatedData, DegreeLevel


DEFAULT_EDUCATION_LEVEL = 0

def complete_twitter_social_info(user, twitter_followers_count, twitter_tweets_count_last_seven_days, twitter_retweets_count_last_seven_days):
    aggregated, created = SocialUserAggregatedData.objects.get_or_create(user=user)
    aggregated.user = user
    aggregated.twitter_followers_count = twitter_followers_count
    aggregated.twitter_tweets_count_last_seven_days = twitter_tweets_count_last_seven_days
    aggregated.twitter_retweets_count_last_seven_days = twitter_retweets_count_last_seven_days
    aggregated.save()
    

def complete_linkedin_social_info(user, linkedin_connections_count, work_experience_years, education_level, degree):
    aggregated, created = SocialUserAggregatedData.objects.get_or_create(user=user)
    aggregated.user = user
    aggregated.linkedin_connections_count = linkedin_connections_count
    aggregated.work_experience_years = work_experience_years
    aggregated.education_level = education_level
    aggregated.education_degree = degree
    aggregated.save()
    
  
def complete_foursquare_info(user, foursquare_friends_count):
    aggregated, created = SocialUserAggregatedData.objects.get_or_create(user=user)
    aggregated.user = user
    aggregated.foursquare_friends_count = foursquare_friends_count
    aggregated.save()

def complete_facebook_info(user, facebook_friend_count, facebook_post_weekly_avg, facebook_likes_weekly_avg):
    aggregated, created = SocialUserAggregatedData.objects.get_or_create(user=user)
    aggregated.user = user
    aggregated.facebook_friend_count = facebook_friend_count
    aggregated.facebook_post_weekly_avg = facebook_post_weekly_avg
    aggregated.facebook_likes_count_last_seven_days = facebook_likes_weekly_avg
    aggregated.save()   

def complete_google_info(user, gplus_contacts_count):
    aggregated, created = SocialUserAggregatedData.objects.get_or_create(user=user)
    aggregated.user = user
    aggregated.gplus_contacts_count = gplus_contacts_count
    aggregated.save()   

def get_level_of_education_by_degree(degree):
    degree, created = DegreeLevel.objects.get_or_create(title=degree)
    level = DEFAULT_EDUCATION_LEVEL
    d_level = degree.education_level()
    if degree and d_level[1] != 0:
        level = d_level[0]    
    return level


def complete_profile(user, email, birthdate, gender):
    profile, created = Profile.objects.get_or_create(user=user)
    
    if created or not profile.account_id:
        generated_uid = random_string(length=6,
                      allowed_chars='ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
        
        u_profile = None
        try:
            u_profile = Profile.objects.get(account_id=generated_uid)
        except:
            pass
        while u_profile is not None:
            generated_uid = random_string()
            try:
                u_profile = Profile.objects.get(account_id=generated_uid)
            except:
                pass
            
        profile.account_id = generated_uid
 
    if email:
        profile.email = email
    if birthdate:
        profile.birthdate = birthdate
        profile.age = calculate_age(birthdate)
    if gender:
        profile.gender = gender
    
    profile.save()

from datetime import date

def calculate_age(born):
    today = date.today()
    try: 
        birthday = born.replace(year=today.year)
    except ValueError: # raised when birth date is February 29 and the current year is not a leap year
        birthday = born.replace(year=today.year, day=born.day-1)
    if birthday > today:
        return today.year - born.year - 1
    else:
        return today.year - born.year
    