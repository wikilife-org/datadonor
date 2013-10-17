from social_auth.models import *

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