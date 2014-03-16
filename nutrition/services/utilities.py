
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
    
    return {"men":{"value":men_avg, "unit":"Lbs"}, "women":{"value":women_avg, "unit":"Lbs"}}


LIBS_TO_KG = 0.45359237
FT_TO_MT = 0.3048

def get_bmi(h,w):
    h_mt = 0
    w_kg = 0
    bmi = 0
    
    if h:
        h_mt = h * FT_TO_MT
    if w:
        w_kg = w * LIBS_TO_KG
    
    try:
        bmi = round(w_kg/ (h_mt*h_mt), 1)
    except:
        pass
    return bmi

def get_global_bmi():
    men_count = 0
    men_sum = 0
    men_avg = 0
    
    women_count = 0
    women_sum = 0
    women_avg = 0
    
    for profile in Profile.objects.all():
        if profile.height and profile.weight:
            if profile.gender == "m":
                men_count +=1
                men_sum +=get_bmi(profile.height, profile.weight)                   
            elif profile.gender == "f":
                women_count +=1
                women_sum +=get_bmi(profile.height, profile.weight)   
        
    
    try:
        men_avg = round(float(men_sum/men_count),1)
    except:
        pass
    
    try:
        women_avg = round(float(women_sum/women_count),1)
    except:
        pass
    
    return {"men":{"value":men_avg}, "women":{"value":women_avg}}
