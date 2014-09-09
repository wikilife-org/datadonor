from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http.response import HttpResponse
from django.utils import simplejson
from django.contrib.auth.models import User
from social.services.utilities import *
from utils.date_util import get_last_sunday, get_last_year
from wikilife.clients.stats import Stats
import csv


def download(request):
    ctx = {"last_sunday": get_last_sunday()[1], "last_year":get_last_year()[1]}
    
    return render_to_response('data/download.html',ctx,
                                  RequestContext(request))

def history_steps(request):
    client = Stats({"HOST":"http://api.wikilife.org"})
    steps_days = client.get_global_steps_one_year()["data"]
    return HttpResponse(simplejson.dumps(steps_days), mimetype="application/json")

def history_calories(request):
    client = Stats({"HOST":"http://api.wikilife.org"})
    calories_days = client.get_global_calories_burned_one_year()["data"]
    return HttpResponse(simplejson.dumps(calories_days), mimetype="application/json")

def history_distance(request):
    client = Stats({"HOST":"http://api.wikilife.org"})
    distance_days = client.get_global_distance_one_year()["data"]
    return HttpResponse(simplejson.dumps(distance_days), mimetype="application/json")

def history_steps_csv(request):
    client = Stats({"HOST":"http://api.wikilife.org"})
    steps_days = client.get_global_steps_one_year()["data"]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="steps.csv"'
    writer = csv.writer(response)
    writer.writerow(steps_days[0].keys())
    
    for row in steps_days:
        writer.writerow(row.values())
    return response

def history_distance_csv(request):
    client = Stats({"HOST":"http://api.wikilife.org"})
    distance_days = client.get_global_distance_one_year()["data"]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="distance.csv"'
    writer = csv.writer(response)
    writer.writerow(distance_days[0].keys())
    
    for row in distance_days:
        writer.writerow(row.values())
    return response

def history_calories_csv(request):
    client = Stats({"HOST":"http://api.wikilife.org"})
    calories_days = client.get_global_calories_burned_one_year()["data"]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="calories.csv"'
    writer = csv.writer(response)
    writer.writerow(calories_days[0].keys())
    
    for row in calories_days:
        writer.writerow(row.values())
    return response
    
    
def export(request, user_id, format):
    user = User.objects.get(id=user_id)
    report_json = _generate_export(user)
    if format == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="my_datadonors_data.csv"'
        writer = csv.writer(response)
        writer.writerow(report_json[0].keys())
        
        for row in report_json:
            writer.writerow(row.values())
        return response
    else:
        return HttpResponse(simplejson.dumps(report_json), mimetype="application/json")



from physical.models import UserActivityLog
from datetime import date, datetime, time, timedelta
import time
from health.utilities import *


def _generate_export(user):
    
    PHYSICAL_TYPE = "physical"
    HEALTH_TYPE = "health"
    SOCIAL_TYPE = "social"
    NUTRITION_TYPE = "nutrition"
    GENOMICS_TYPE = "genomics"
    PROFILE_TYPE = "profile"
    
    export = {}    
    act_logs = UserActivityLog.objects.filter(user=user)
    for activity in act_logs:
        if PHYSICAL_TYPE not in export[activity.execute_time.strftime("%Y-%m-%d")]:
            export[activity.execute_time.strftime("%Y-%m-%d")][PHYSICAL_TYPE] = []
        export[activity.execute_time.strftime("%Y-%m-%d")][PHYSICAL_TYPE].append( {"activity_type": activity.type, \
                                                                              "miles":activity.miles, "hours":activity.hours,\
                                                                               "steps": activity.steps, "source":activity.provider,\
                                                                                "time": activity.execute_time.strftime("%HH:%MM:%SS")})
    
    conditions = user.conditions.all()
    for condition in conditions:
        if HEALTH_TYPE not in export[condition.update_time.strftime("%Y-%m-%d")]:
            export[condition.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE] = {}
        if "conditions" not in export[condition.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]:
            export[condition.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]["cronical_conditions"] = []
        c_name, t_name = get_conditions_name(condition.condition_id, condition.type_id)
        export[condition.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]["cronical_conditions"].append({"condition_name": c_name, "condition_type":t_name, \
                                                                                                       "source":"manual_input"})
        
    
    complaints = user.complaints.all()

    for complaint in complaints:
        if HEALTH_TYPE not in export[complaint.update_time.strftime("%Y-%m-%d")]:
            export[complaint.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE] = {}
        if "complaints" not in export[complaint.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]:
            export[complaint.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]["complaints"] = []
        
        c_name = get_complaints_name(complaint.complaint_id)
        export[complaint.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]["complaints"].append({"complaint_name": c_name, "source":"manual_input"})
        
    emotions = user.emotions.all()

    for emotion in emotions:
        if HEALTH_TYPE not in export[emotion.update_time.strftime("%Y-%m-%d")]:
            export[emotion.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE] = {}
        if "emotions" not in export[emotion.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]:
            export[emotion.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]["emotions"] = []
        
        c_name = get_emotions_name(emotion.emotion_id)
        export[emotion.update_time.strftime("%Y-%m-%d")][HEALTH_TYPE]["emotions"].append({"emotion_name": c_name, "source":"manual_input"})

    foods = user.foods.filter()
    for food in foods:
        if NUTRITION_TYPE not in export[food.execute_time.strftime("%Y-%m-%d")]:
            export[food.execute_time.strftime("%Y-%m-%d")][NUTRITION_TYPE] = {}
        if "nutrients" not in export[food.execute_time.strftime("%Y-%m-%d")][NUTRITION_TYPE]:
            export[food.execute_time.strftime("%Y-%m-%d")][NUTRITION_TYPE]["nutrients"] = []
        
        export[food.execute_time.strftime("%Y-%m-%d")][NUTRITION_TYPE]["nutrients"].append({"time": food.execute_time.strftime("%HH:%MM:%SS"), \
                                                                                           "protein":food.protein, "fats":food.fats, "carbs":food.carbs,
                                                                                           "fiber":food.fiber, "source":food.provider})
    
     
    social = user.social_aggregated_data.filter()
    for s in social:
        if SOCIAL_TYPE not in export[s.update_time.strftime("%Y-%m-%d")]:
            export[s.update_time.strftime("%Y-%m-%d")][SOCIAL_TYPE] = {}
        
        if s.facebook_friend_count:
            export[s.update_time.strftime("%Y-%m-%d")][SOCIAL_TYPE]["facebook"] = {"time": s.update_time.strftime("%HH:%MM:%SS"), \
                                                                                "facebook_friend_count":s.facebook_friend_count, \
                                                                                "facebook_post_weekly_avg":s.facebook_post_weekly_avg,\
                                                                                "facebook_likes_weekly_avg":s.facebook_likes_weekly_avg,
                                                                                "source":"facebook"}
        if s.twitter_followers_count:
            export[s.update_time.strftime("%Y-%m-%d")][SOCIAL_TYPE]["twitter"] = {"time": s.update_time.strftime("%HH:%MM:%SS"), \
                                                                                "twitter_followers_count":s.twitter_followers_count, \
                                                                                "twitter_tweets_count_last_seven_days":s.twitter_tweets_count_last_seven_days,\
                                                                                "twitter_retweets_count_last_seven_days":s.twitter_retweets_count_last_seven_days,
                                                                                "source":"twitter"}
        if s.gplus_contacts_count:
            export[s.update_time.strftime("%Y-%m-%d")][SOCIAL_TYPE]["google_plus"] = {"time": s.update_time.strftime("%HH:%MM:%SS"), \
                                                                                      "gplus_contacts_count":s.gplus_contacts_count, \
                                                                                      "source":"google_plus"} 
        
        if s.linkedin_connections_count:
            export[s.update_time.strftime("%Y-%m-%d")][SOCIAL_TYPE]["linkedin"] = {"time": s.update_time.strftime("%HH:%MM:%SS"), \
                                                                                   "linkedin_connections_count":s.linkedin_connections_count, \
                                                                                   "source":"linkedin"}  
        if s.foursquare_friends_count:
            export[s.update_time.strftime("%Y-%m-%d")][SOCIAL_TYPE]["foursquare"] = {"time": s.update_time.strftime("%HH:%MM:%SS"), \
                                                                                     "foursquare_friends_count":s.foursquare_friends_count, \
                                                                                     "source":"foursquare"}         
    
    profile = user.profile.filter()
    for p in profile:
        if PROFILE_TYPE not in export[p.update_time.strftime("%Y-%m-%d")]:
            export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE] = {}
        
        if p.first_name:
            export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE]["first_name"] = {"value":p.first_name , "source":p.first_name_source}
        if p.last_name:
            export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE]["last_name"] = {"value":p.last_name, "source":p.last_name_source}
        if p.email:
            export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE]["email"] = {"value":p.email, "source":p.email_source}
        if p.age:
            export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE]["age"] = {"value": p.age, "source":p.age_source}
        if p.date_of_birth:
            export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE]["date_of_birth"] ={"value": p.date_of_birth.strftime("%Y-%m-%d"), "source":p.date_of_birth_source} 
        if p.gender:
            export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE]["gender"] = {"value": p.gender, "source":p.gender_source}
        if p.height:
            export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE]["height"] = {"value": p.height, "source":p.height_source}
        if p.weight:
            export[p.update_time.strftime("%Y-%m-%d")][PROFILE_TYPE]["weight"] = {"value": p.weight, "source":p.weight_source}
    
    return export
       

    