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
    user = User.object.get(user_id=user_id)
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
    GENETIC_TYPE = "genetics"
    
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
    
     
    traits = user.traits.all()
    drug_respone = user.drug_reponse.all()
    risks = user.risks.all()
    

    