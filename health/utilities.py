
import math
from utils.commons import percentage
from social_auth.models import *
from datetime import date
from users.models import Profile
from health.models import *
from wikilife.clients.stats import  Stats
from conditions import conditions
from complaints import complaints
from emotions import emotions


def global_mood_avg():
    
    count = 0
    sum = 0
    avg = 0
        
    for profile in Profile.objects.all():
        mood = None
        try:
            mood = UserMoodLastWeek.objects.get(user=profile.user)
        except:
            pass
        if mood:
            count +=1
            sum +=mood.avg_mood                  
            
    
    try:
        avg = round(float(sum/count),0)
    except:
        pass
    
    return {"mood_avg": int(avg)}

"""
[{"name": "I don't Know", "id":0, "percentage":35},
            {"name": "A+", "id":1, "percentage":20},
            {"name": "A-", "id":2, "percentage":5},
            {"name": "B+", "id":3, "percentage":10},
            {"name": "B-", "id":4, "percentage":5},
            {"name": "AB+", "id":5, "percentage":5},
            {"name": "AB-", "id":6, "percentage":10},
            {"name": "0+", "id":7,"percentage":3},
            {"name": "0-", "id":8, "percentage":2}]
"""
def global_blood_type():
    dontnow = UserBloodType.objects.filter(blood_type_id=0).count()
    A_ = UserBloodType.objects.filter(blood_type_id=1).count()
    A__ = UserBloodType.objects.filter(blood_type_id=2).count()
    B_ = UserBloodType.objects.filter(blood_type_id=3).count()
    B__ = UserBloodType.objects.filter(blood_type_id=4).count()
    AB_ = UserBloodType.objects.filter(blood_type_id=5).count()
    AB__ = UserBloodType.objects.filter(blood_type_id=6).count()
    cero_ = UserBloodType.objects.filter(blood_type_id=7).count()
    cero__ = UserBloodType.objects.filter(blood_type_id=8).count()
    
    total = dontnow + A_ + A__ + B_ + B__ + AB_ + AB__ + cero_ + cero__
    
    dontnow_p = percentage(dontnow, total)
    A_p = percentage(A_, total)
    A__p = percentage(A__, total)
    B_p = percentage(B_, total)
    B__p = percentage(B__, total)
    AB_p = percentage(AB_, total)
    AB__p = percentage(AB__, total)
    cero_p = percentage(cero_, total)
    cero__p = percentage(cero__, total)
    
    return [{"name": "I don't Know", "id":0, "percentage":dontnow_p},
            {"name": "A+", "id":1, "percentage":A_p},
            {"name": "A-", "id":2, "percentage":A__p},
            {"name": "B+", "id":3, "percentage":B_p},
            {"name": "B-", "id":4, "percentage":B__p},
            {"name": "AB+", "id":5, "percentage":AB_p},
            {"name": "AB-", "id":6, "percentage":AB__p},
            {"name": "0+", "id":7,"percentage":cero_p},
            {"name": "0-", "id":8, "percentage":cero__p}]
    
    

def global_blood_type_dict():
    dontnow = UserBloodType.objects.filter(blood_type_id=0).count()
    A_ = UserBloodType.objects.filter(blood_type_id=1).count()
    A__ = UserBloodType.objects.filter(blood_type_id=2).count()
    B_ = UserBloodType.objects.filter(blood_type_id=3).count()
    B__ = UserBloodType.objects.filter(blood_type_id=4).count()
    AB_ = UserBloodType.objects.filter(blood_type_id=5).count()
    AB__ = UserBloodType.objects.filter(blood_type_id=6).count()
    cero_ = UserBloodType.objects.filter(blood_type_id=7).count()
    cero__ = UserBloodType.objects.filter(blood_type_id=8).count()
    
    total = dontnow + A_ + A__ + B_ + B__ + AB_ + AB__ + cero_ + cero__
    
    dontnow_p = percentage(dontnow, total)
    A_p = percentage(A_, total)
    A__p = percentage(A__, total)
    B_p = percentage(B_, total)
    B__p = percentage(B__, total)
    AB_p = percentage(AB_, total)
    AB__p = percentage(AB__, total)
    cero_p = percentage(cero_, total)
    cero__p = percentage(cero__, total)
    
    return {0:{"name": "I don't Know", "id":0, "percentage":dontnow_p},
            1:{"name": "A+", "id":1, "percentage":A_p},
            2:{"name": "A-", "id":2, "percentage":A__p},
            3:{"name": "B+", "id":3, "percentage":B_p},
            4:{"name": "B-", "id":4, "percentage":B__p},
            5:{"name": "AB+", "id":5, "percentage":AB_p},
            6:{"name": "AB-", "id":6, "percentage":AB__p},
            7:{"name": "0+", "id":7,"percentage":cero_p},
            8:{"name": "0-", "id":8, "percentage":cero__p}}


"""def get_complaints():
    stats = Stats({"HOST":"http://api.wikilife.org"})
    conditions = stats.get_global_complaints()["data"]
    return conditions
    
def get_complaints_rank():
    stats = Stats({"HOST":"http://api.wikilife.org"})
    conditions = stats.get_global_complaints()["data"]
    newlist = sorted(conditions, key=lambda k: k['percentage'])
    newlist.reverse()
    return newlist"""


def get_complaints():
    result = []
    total_complaints = UserComplaints.objects.all().values_list('user', flat=True).distinct().count()
    
    for c in complaints:
        count = UserComplaints.objects.filter(complaint_id=c["id"]).count()
        c["percentage"] = percentage(count, total_complaints)
        result.append(c)
        
    newlist = sorted(result, key=lambda k: k['name'])
    
    return newlist

def get_complaint_percentage(id_complaint):
    total_complaints = UserComplaints.objects.all().values_list('user', flat=True).distinct().count()
    count = UserComplaints.objects.filter(complaint_id=id_complaint).count()
    return percentage(count, total_complaints)


def get_complaints_rank():
    total_complaints = UserComplaints.objects.all().values_list('user', flat=True).distinct().count()
    result = []
    for c in complaints:
        count = UserComplaints.objects.filter(complaint_id=c["id"]).count()
        c["percentage"] = percentage(count, total_complaints)
        result.append(c)
        
    newlist = sorted(result, key=lambda k: k['percentage'])
    newlist.reverse() 
    
    return newlist, total_complaints


def get_conditions():
    total_conditions = UserConditions.objects.all().values_list('user', flat=True).distinct().count()
    result = []
    for c in conditions:
        count = UserConditions.objects.filter(condition_id=c["id"]).count()
        c["percentage"] = percentage(count, total_conditions)
        result.append(c)
        
    newlist = sorted(result, key=lambda k: k['name'])
    
    return newlist


def get_conditions_rank():
    total_conditions = UserConditions.objects.all().values_list('user', flat=True).distinct().count()
    result = []
    for c in conditions:
        count = UserConditions.objects.filter(condition_id=c["id"]).count()
        c["percentage"] = percentage(count, total_conditions)
        result.append(c)
        
    newlist = sorted(result, key=lambda k: k['percentage'])
    newlist.reverse() 
    
    return newlist, total_conditions


def get_emotions_name(id_emotions):
    c_name = ""
    
    for c in emotions:
        if c["id"] == id_emotions:
            c_name = c["name"]
            break
        
    return c_name

def get_complaints_name(id_complaint):
    c_name = ""
    
    for c in complaints:
        if c["id"] == id_complaint:
            c_name = c["name"]
            break
        
    return c_name
def get_conditions_name(id_condition, id_type=None):
    c_name = ""
    t_name = ""
    
    for c in conditions:
        if c["id"] == id_condition:
            c_name = c["name"]
            if id_type:
                for t in type:
                    if t["id"] == id_type:
                        t_name = t["name"]
        
    return c_name, t_name

"""def get_emotions_rank():
    stats = Stats({"HOST":"http://api.wikilife.org"})
    conditions = stats.get_global_emotions()["data"]
    newlist = sorted(conditions, key=lambda k: k['percentage'])
    newlist.reverse()
    return newlist

def get_emotions():
    stats = Stats({"HOST":"http://api.wikilife.org"})
    conditions = stats.get_global_emotions()["data"]
    return conditions"""
    

def get_emotions():
    total_emotions = UserEmotions.objects.all().values_list('user', flat=True).distinct().count()
    result = []
    for c in emotions:
        count = UserEmotions.objects.filter(emotion_id=c["id"]).count()
        c["percentage"] = percentage(count, total_emotions)
        result.append(c)
        
    newlist = sorted(result, key=lambda k: k['name'])
    newlist.reverse() 
    
    return newlist


def get_emotions_rank():
    total_emotions = UserEmotions.objects.all().values_list('user', flat=True).distinct().count()
    result = []
    for c in emotions:
        count = UserEmotions.objects.filter(emotion_id=c["id"]).count()
        c["percentage"] = percentage(count, total_emotions)
        result.append(c)
        
    newlist = sorted(result, key=lambda k: k['percentage'])
    newlist.reverse() 
    
    return newlist
    
