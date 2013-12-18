
import math
from utils.oper import percentage
from social_auth.models import *


def global_social_reach():
    user_count = 0
    facebook_friend_count_total = 0
    twitter_followers_count_total = 0
    gplus_contacts_count_total = 0
    foursquare_friends_count_total = 0
    linkedin_connections_count_total = 0 
    
    for user_data in SocialUserAggregatedData.objects.all():
        user_count += 1
        facebook_friend_count_total += user_data.facebook_friend_count
        twitter_followers_count_total += user_data.twitter_followers_count
        gplus_contacts_count_total += user_data.gplus_contacts_count
        foursquare_friends_count_total += user_data.foursquare_friends_count
        linkedin_connections_count_total += user_data.linkedin_connections_count
        
    avg_facebook_friend_count_total = int(math.ceil(facebook_friend_count_total / user_count))
    avg_twitter_followers_count_total = int(math.ceil(twitter_followers_count_total / user_count))
    avg_gplus_contacts_count_total = int(math.ceil(gplus_contacts_count_total / user_count))
    avg_foursquare_friends_count_total = int(math.ceil(foursquare_friends_count_total / user_count))
    avg_linkedin_connections_count_total = int(math.ceil(linkedin_connections_count_total / user_count))

    total = avg_facebook_friend_count_total + avg_twitter_followers_count_total \
             + avg_linkedin_connections_count_total + avg_gplus_contacts_count_total \
             + avg_foursquare_friends_count_total
    f_per = percentage(avg_facebook_friend_count_total, total)
    l_per = percentage(avg_linkedin_connections_count_total, total)
    g_per = percentage(avg_gplus_contacts_count_total, total)
    t_per = percentage(avg_twitter_followers_count_total, total)
    fq_per = percentage(avg_foursquare_friends_count_total, total)
    
    return {"facebook":{"count": avg_facebook_friend_count_total, "percentage":f_per}, "twitter":{"count": avg_twitter_followers_count_total, "percentage":t_per},
                "gmail":{"count": avg_gplus_contacts_count_total, "percentage":g_per}, "foursquare":{"count": avg_foursquare_friends_count_total, "percentage":fq_per},
                "linkedin":{"count": avg_linkedin_connections_count_total, "percentage":l_per}}

def global_social_sharing():
    user_count = 0
    facebook_post_weekly_avg_total = 0
    facebook_likes_weekly_avg_total = 0
    twitter_tweets_count_last_seven_days_total = 0
    twitter_retweets_count_last_seven_days_total = 0
    
    for user_data in SocialUserAggregatedData.objects.all():
        user_count += 1
        facebook_post_weekly_avg_total += user_data.facebook_post_weekly_avg
        facebook_likes_weekly_avg_total += user_data.facebook_likes_weekly_avg
        twitter_tweets_count_last_seven_days_total += user_data.twitter_tweets_count_last_seven_days
        twitter_retweets_count_last_seven_days_total += user_data.twitter_retweets_count_last_seven_days
        
    avg_facebook_post_weekly_avg_total = int(math.ceil(facebook_post_weekly_avg_total / user_count))
    avg_facebook_likes_weekly_avg_total = int(math.ceil(facebook_likes_weekly_avg_total / user_count))
    avg_twitter_tweets_count_last_seven_days_total = int(math.ceil(twitter_tweets_count_last_seven_days_total / user_count))
    avg_twitter_retweets_count_last_seven_days_total = int(math.ceil(twitter_retweets_count_last_seven_days_total / user_count))

    return {"facebook":{"posts":avg_facebook_post_weekly_avg_total, "likes":avg_facebook_likes_weekly_avg_total}, 
            "twitter":{"tweets":avg_twitter_tweets_count_last_seven_days_total, "retweets":avg_twitter_retweets_count_last_seven_days_total}}

def global_education():
    
    elementary_total = 0
    junior_college_total = 0
    high_school_total = 0
    tech_total = 0
    university_total = 0
    master_total = 0
    phd_total = 0
    
    for user_data in SocialUserAggregatedData.objects.all():
        education_level = user_data.education_level_manual or user_data.education_level
        if education_level == 0:
            elementary_total += 1
        elif education_level == 1:
            junior_college_total += 1
        elif education_level == 2:
            high_school_total += 1
        elif education_level == 3:
            tech_total += 1
        elif education_level == 4:
            university_total += 1
        elif education_level == 5:
            master_total += 1
        elif education_level == 6:
            phd_total += 1
            
    total = elementary_total + junior_college_total + high_school_total + tech_total + university_total + master_total + phd_total
        
    return {6:{"percentage":percentage(phd_total, total), "key":"phd", "title": "PhD", "index":6},
            5:{"percentage":percentage(master_total, total), "key":"master", "title": "Master", "index":5},
            4:{"percentage":percentage(university_total, total), "key":"university", "title": "University", "index":4}, 
            3:{"percentage":percentage(tech_total, total), "key":"tech_institute", "title": "Technical Institute", "index":3},
            2:{"percentage":percentage(high_school_total, total), "key":"high_school", "title": "High School", "index":2},
            1:{"percentage":percentage(junior_college_total, total), "key":"junior_college", "title": "Junior College", "index":1},
            0:{"percentage":percentage(elementary_total, total), "key":"elemtary_school", "title": "Elementary School", "index":0}}


def global_work():
    
    total_user_count = 0
    total_years_count = 0
    total_avg = 0
    age_range_dict = { "15-25":{"key": "15-25", "value": 0, "sum":0, "count":0}, 
                    "26-35":{"key": "26-35", "value": 0, "sum":0, "count":0}, 
                    "36-45":{"key": "36-45", "value": 0, "sum":0, "count":0}, 
                    "46-55":{"key": "46-55", "value": 0, "sum":0, "count":0}, 
                    "56-65":{"key": "56-65", "value": 0, "sum":0, "count":0}}
    
    for user_data in SocialUserAggregatedData.objects.all():
        years =  user_data.work_experience_years_manual or user_data.work_experience_years
        if years:
            if user_data.user.profile.date_of_birth:
                total_user_count += 1
                total_years_count += years
                
                age_range = get_age_range(user_data.user.profile.date_of_birth)
                age_range_dict[age_range]["sum"] += years
                age_range_dict[age_range]["count"] += 1

    total_avg = int(math.ceil(total_years_count / total_user_count))
    
    age_range_dict["15-25"]["value"] = int(math.ceil(age_range_dict["15-25"]["sum"] / age_range_dict["15-25"]["count"]))
    del age_range_dict["15-25"]["sum"]
    del age_range_dict["15-25"]["count"]
    age_range_dict["26-35"]["value"] = int(math.ceil(age_range_dict["26-35"]["sum"] / age_range_dict["26-35"]["count"]))
    del age_range_dict["26-35"]["sum"]
    del age_range_dict["26-35"]["count"]
    age_range_dict["36-45"]["value"] = int(math.ceil(age_range_dict["36-45"]["sum"] / age_range_dict["36-45"]["count"]))
    del age_range_dict["36-45"]["sum"]
    del age_range_dict["36-45"]["count"]
    age_range_dict["46-55"]["value"] = int(math.ceil(age_range_dict["46-55"]["sum"] / age_range_dict["46-55"]["count"]))
    del age_range_dict["46-55"]["sum"]
    del age_range_dict["46-55"]["count"]
    age_range_dict["56-65"]["value"] = int(math.ceil(age_range_dict["56-65"]["sum"] / age_range_dict["56-65"]["count"]))
    del age_range_dict["56-65"]["sum"]
    del age_range_dict["56-65"]["count"]
    
    return age_range_dict, total_avg
    
def is_valid_education(education_level):
    valid = False
    try:
        education_level = int(education_level)
        valid = education_level>= 0 and education_level<=6
    except:
        pass
    
    return valid

def is_valid_working_experience(working_experience):
    valid = False
    try:
        working_experience = int(working_experience)
        valid = working_experience>= 0 and working_experience<=60
    except:
        pass
    
    return valid

def update_degree(degree, level):

    degree, created = DegreeLevel.objects.get_or_create(title=degree)
    if level == 0:
        degree.elementary += 1
    elif level == 1:
        degree.high_school += 1
    elif level == 2:
        degree.junior_collage += 1
    elif level == 3:
        degree.tech += 1
    elif level == 4:
        degree.university += 1
    elif level == 5:
        degree.master += 1
    elif level == 6:
        degree.phd += 1
    
    degree.save()
    
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
    
def get_age_range(birth_date):
    age_range = "26-35"
    if birth_date:
        age = calculate_age(birth_date)
        if age>=15 and age <=25:
            age_range = "15-25"
        elif age>=26 and age <=35:
            age_range = "26-35"
        elif age>=36 and age <=45:
            age_range = "36-45"
        elif age>=46 and age <=55:
            age_range = "46-55"
        elif age>=56 and age <=65:
            age_range = "56-65"
    
    return age_range
        


###### MOCK SECTION #############
# Will be deleted after deployment
#################################


def get_social_reach_mock():
    return {"user_data" : {"facebook":{"count": 23, "percentage":20}, "twitter":{"count": 10, "percentage":20},
                "gmail":{"count": 310, "percentage":20}, "foursquare":{"count": 20, "percentage":20},
                "linkedin":{"count": 20, "percentage":20}},
            "global_data":{"facebook":{"count": 2, "percentage":20}, "twitter":{"count": 18, "percentage":10},
                "gmail":{"count": 206, "percentage":10}, "foursquare":{"count": 50, "percentage":40},
                "linkedin":{"count": 20, "percentage":20}}}
    

def global_social_sharing_mock():
    return {"facebook":{"posts":134, "likes":44}, "twitter":{"tweets":99, "retweets":12}}

def user_social_sharing_mock():
    return {"facebook":{"posts":34, "likes":40}, "twitter":{"tweets":10, "retweets":10}}
