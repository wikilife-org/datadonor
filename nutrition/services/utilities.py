
import math
from utils.commons import percentage
from social_auth.models import *
from datetime import date
from users.models import Profile

def global_height():
    
    men_count = 0
    men_sum = 0
    men_avg = 0
    
    women_count = 0
    women_sum = 0
    women_avg = 0
    
    for profile in Profile.objects.all():
        if profile.height:
            if profile.gender == "m":
                men_count +=1
                men_sum +=profile.height                   
            elif profile.gender == "f":
                women_count +=1
                women_sum +=profile.height
        
    
    try:
        men_avg = float(men_sum/men_count)
    except:
        pass
    
    try:
        women_avg = float(women_sum/women_count)
    except:
        pass
    
    return {"men":{"value":men_avg, "unit":"Ft"}, "women":{"value":women_avg, "unit":"Ft"}}


def global_weight():
    
    men_count = 0
    men_sum = 0
    men_avg = 0
    
    women_count = 0
    women_sum = 0
    women_avg = 0
    
    for profile in Profile.objects.all():
        if profile.weight:
            if profile.gender == "m":
                men_count +=1
                men_sum +=profile.weight                   
            elif profile.gender == "f":
                women_count +=1
                women_sum +=profile.weight
        
    
    try:
        men_avg = float(men_sum/men_count)
    except:
        pass
    
    try:
        women_avg = float(women_sum/women_count)
    except:
        pass
    
    return {"men":{"value":men_avg, "unit":"Ft"}, "women":{"value":women_avg, "unit":"Ft"}}
