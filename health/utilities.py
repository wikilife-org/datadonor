
import math
from utils.commons import percentage
from social_auth.models import *
from datetime import date
from users.models import Profile
from health.models import *

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
