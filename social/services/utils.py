from social_auth.models import *
from utils.c import calculate_age

def global_social_reach():
    return {"facebook":{"count": 20, "percentage":20}, "twitter":{"count": 20, "percentage":10},
                "gmail":{"count": 20, "percentage":10}, "foursquare":{"count": 20, "percentage":40},
                "linkedin":{"count": 20, "percentage":20}}

def global_social_sharing():
    return {"facebook":{"posts":134, "likes":44}, "twitter":{"tweets":99, "retweets":12}}


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
