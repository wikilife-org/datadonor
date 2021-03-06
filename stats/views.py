

from django.http.response import HttpResponse
from django.utils import simplejson
from physical.services.stats.services import PhysicalActivityDistributionService
from health.services.stats.services import HealthActivityDistributionService
from django.shortcuts import render_to_response
from django.template import RequestContext
from users.models import Profile
from physical.models import UserActivityLog
from nutrition.models import UserFoodLog
from health.models import UserSleepLog
from django.db.models.aggregates import Sum, Avg
from wikilife.clients.stats import Stats


def get_miles(request):
    dto = PhysicalActivityDistributionService().get_records_miles()
    
    return HttpResponse(simplejson.dumps(dto), mimetype="application/json")


def go_exercise_stats(request):
    total_dd_user = Profile.objects.count()
    total_exercise_log = UserActivityLog.objects.count()
    total_food_log = UserFoodLog.objects.count()
    total_sleep_log = UserSleepLog.objects.count()
    
    #Last_7_days miles
    client = Stats({"HOST":"http://api.wikilife.org"})
    total_wl_users = client.get_total_wl_users()["data"]["users"]["total"]
    dto_miles = PhysicalActivityDistributionService().get_records_miles_limit(days_offset=100)
    dto_hours = PhysicalActivityDistributionService().get_records_hour_limit(days_offset=100)
    #dto_steps = PhysicalActivityDistributionService()._get_global_distribution_steps_report_week()
    gender_m = Profile.objects.filter(gender="m").count()
    gender_f = Profile.objects.filter(gender="f").count()
    total_gender = gender_m + gender_f
    per_m = (gender_m * 100)/total_gender
    per_f = 100 - per_m
    gender = {"male":per_m, "female": per_f}
    #dto_sleep = HealthActivityDistributionService().get_global_distribution_sleep_month()
    #Last_7_days steps
    #Last_7_days hours
    
    #Gender distribution
    
    return render_to_response('stats/exercise.html',{"total_wl_users": total_wl_users,
                                                     "total_dd_users": total_dd_user,
                                                  "total_exercise_log": total_exercise_log,
                                                  "total_food_log": total_food_log,
                                                  "miles": dto_miles,
                                                  "hours": dto_hours,
                                                  #"steps": {},
                                                  "page": "exercise_stats",
                                                  "gender": gender,
                                                  "section": "exercise",
                                                  "total_sleep_log": total_sleep_log},RequestContext(request))
    

def go_exercise_data(request):
    total_exercise_log = UserActivityLog.objects.all().order_by("-execute_time")[:100]
    
    return render_to_response('stats/exercise_row.html',{"logs": total_exercise_log,"section": "exercise", "page": "exercise_data",
                                                  },RequestContext(request))
    
from health.utilities import get_conditions_rank, get_complaints_rank, get_emotions_rank, global_blood_type
from health.models import UserConditions, UserBloodType, UserComplaints, UserEmotions


def go_health_stats(request):
    condition_rank, total_conditions = get_conditions_rank()
    complaints_rank, total_complaints = get_complaints_rank()
    emotions_rank, total_emotions = get_emotions_rank()
    total_conditions_logs = UserConditions.objects.all().count()
    total_complaints_logs = UserComplaints.objects.all().count()
    total_blood_type_logs = UserBloodType.objects.all().count()
    total_emotions_logs = UserEmotions.objects.all().count()
    blood_types = global_blood_type()
    
    for blood in blood_types:
        blood["percentage"] = "%s"%round(blood["percentage"], 2)

    
    return render_to_response('stats/health.html',{"condition_rank": condition_rank[:5],
                                                  "complaints_rank": complaints_rank[:5],
                                                  "emotions_rank": emotions_rank[:5],
                                                  "blood_types": blood_types,
                                                  "total_conditions_logs": total_conditions_logs,
                                                  "total_complaints_logs": total_complaints_logs,
                                                  "total_blood_type_logs": total_blood_type_logs,
                                                  "total_emotions_logs": total_emotions_logs,
                                                  "page": "health_stats",
                                                  "section": "health",
                                                  },RequestContext(request))
    
    
def go_health_data(request):
    condition_rank, total_conditions = get_conditions_rank()
    complaints_rank, total_complaints = get_complaints_rank()
    emotions_rank, total_emotions = get_emotions_rank()
    
    condition_report = condition_rank[:30]
    for condition in condition_report:
        condition["percentage"] = "%s"%round(condition["percentage"], 2)
    
    complaints_report = complaints_rank[:30]
    for complaints in complaints_report:
        complaints["percentage"] = "%s"%round(complaints["percentage"], 2)
    
    emotion_report = emotions_rank[:30]
    for  emotion in emotion_report:
        emotion["percentage"] = "%s"%round(emotion["percentage"], 2)
    
    return render_to_response('stats/health_row.html',{"conditions": condition_report,
                                                       "complaints": complaints_report,
                                                       "emotions": emotion_report,
                                                        "page": "health_data",
                                                        "section": "health",
                                                  },RequestContext(request))
    
    

from nutrition.services.utilities import get_global_bmi, global_weight, global_height
from nutrition.models import UserFoodLog
from nutrition.services.stats.services import NutritionDistributionService
from users.models import Profile

def go_nutrition_stats(request):
    # nutrients distribution
    # BMI gender distribution
    # Cant logs
    total_logs = UserFoodLog.objects.count()
    bmi = get_global_bmi()
    bmi_users_cant = Profile.objects.filter(weight__isnull =  False).count()
    bmi_dto = [{"x":'Men', "y": bmi["men"]["value"] },  {"x":'Women', "y": bmi["women"]["value"] }]
    data = NutritionDistributionService().get_nutrients_global_distribution(delta=100)
    print data
    return render_to_response('stats/nutrition.html',{
                                                    'bmi_based': bmi_users_cant,
                                                  "total_nutrition_logs": total_logs,
                                                  'data': data,
                                                  "bmi": bmi_dto,
                                                  "page": "nutrition_stats",
                                                  "section": "nutrition",
                                                  },RequestContext(request))


def go_nutrition_data(request):
    logs = UserFoodLog.objects.all()
    return render_to_response('stats/nutrition_row.html',{
                                                        "page": "nutrition_data",
                                                        "section": "nutrition",
                                                        "logs": logs,
                                                  },RequestContext(request))

from social.services.utilities import *
from social.models import SocialUserAggregatedData, DegreeLevel
    
def go_social_stats(request):
    count_logs = SocialUserAggregatedData.objects.all().count()
    education_logs = SocialUserAggregatedData.objects.filter(education_level_manual__isnull = False).count()
    work_logs = SocialUserAggregatedData.objects.filter(work_experience_years_manual__isnull = False).count()
    global_reach = global_social_reach()
    global_reach_dto = [{"x":'Facebook', "y": global_reach["facebook"]["count"] },
                        {"x":'Twitter', "y": global_reach["twitter"]["count"] },
                         {"x":'Google Plus', "y": global_reach["gmail"]["count"] },
                          {"x":'Foursquare', "y": global_reach["foursquare"]["count"] },
                           {"x":'Linkedin', "y": global_reach["linkedin"]["count"] },
                        ]
    global_sharing = global_social_sharing()
    education  = global_education()
    print education
    work = global_work()
    return render_to_response('stats/social.html',{
                                                        "page": "social_stats",
                                                        "section": "social",
                                                        "global_reach": global_reach_dto,
                                                        "global_sharing": global_sharing,
                                                        "global_education": education,
                                                        "count_logs": count_logs,
                                                        "education_logs": education_logs,
                                                        "work_logs": work_logs,
                                                        "global_work": work
                                                  },RequestContext(request))

def go_social_data(request):
    logs = SocialUserAggregatedData.objects.all()
    return render_to_response('stats/social_row.html',{
                                                        "page": "social_data",
                                                        "section": "social",
                                                        "logs": logs,
                                                  },RequestContext(request))
    

def go_contact(request):
    return render_to_response('stats/contact.html',{
                                                        
                                                        "section": "contact",
                                                  },RequestContext(request))
    

def go_meta(request):
    to_search = request.GET.get("to_search", None)
    return render_to_response('stats/meta.html',{"to_search":to_search,
                                                        "page": "meta_search",
                                                        "section": "meta",
                                                  },RequestContext(request))
    
import requests
import random

def go_meta_graph(request, meta_id=1):
    page = request.GET.get("page", 0)
        
    if meta_id == None:
        meta_id = 1
    url_childs = "http://api.wikilife.org/4/meta/children/%s?page=%s"%(meta_id, page)
    response_childs = requests.get(url_childs).json()
    response_childs["next_page"] = response_childs["pageIndex"] + 1
    response_childs["prev_page"] = response_childs["pageIndex"] - 1
    
    colores = ["info", "primary", "purple", "warning", "success", "danger"]
    url = "http://api.wikilife.org/4/meta/withmetrics/%s"%meta_id
    response = requests.get(url).json()

            
            
    name = response["name"]
    other_names = response["otherNames"].split(",")
    
    names = []
    
    for n in other_names:
        if n == " " or n == [] or n == "[]":
            continue
        names.append((n, random.choice(colores)))
        
    has = response["has"]
    has_ = []
    for h in has:
        has_.append((h["name"], random.choice(colores)))
    
    is_ = None
    try:
        css_class = ""
        is_ = response["is"][0]["name"]
        if is_ == "Food":
            css_class = "fa fa-cutlery"
        elif is_ == "Mood":
            css_class = "fa ion-happy"
        elif is_ == "Drug":
            css_class = "fa fa-circle-thin"
        elif is_ == "Exercise":
            css_class = "fa fa-child"
        elif is_ == "Complaints":
            css_class = "fa fa-stethoscope"
        elif is_ == "Conditions" or is_ == "Medical Conditions" :
            css_class = "fa ion-heart-broken"
    except:
        pass
    
    metrics = []
    for metric in response["metrics"]:
        metric["name"] = metric["name"].split("-")[0]
        metric["color"] = random.choice(colores)
        if metric["type"] != "NumericMetricNode":

            metric["type"] = "Text"
            if is_ != "Drug":
                options = metric["options"].split(",")
                default = int(metric["default"])
                metric["default"] = options[default]
            else:
                options = metric["options"].split(";")
                print options
                metric["default"] = options[0]
                metric["options"] = ", ".join(options)
                print metric["options"]
        
            metrics.append(metric)
    
    for metric in response["metrics"]:
        metric["name"] = metric["name"].split("-")[0]
        metric["color"] = random.choice(colores)
        if metric["type"] == "NumericMetricNode":
            metric["type"] = "Numeric"
            metrics.append(metric)
            
    ancestors_url = "http://api.wikilife.org/4/meta/ancestors/%s"%meta_id
    response_ancestors = requests.get(ancestors_url).json()
    response_ancestors.reverse()
    
    image_url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=pageimages&format=json&pithumbsize=400'%name
    response_image = requests.get(image_url).json()
    image_thumb_url = None
    try:
        image_thumb_url = response_image["query"]["pages"][response_image["query"]["pages"].keys()[0]]["thumbnail"]["source"]
    except:
        pass
    print metrics
    return render_to_response('stats/meta_detail.html',{"id": response['id'],
                                                        "childs":response_childs,
                                                        "image_thumb_url":image_thumb_url,
                                                        "ancestors": response_ancestors, 
                                                        "name": name,
                                                        "css_class": css_class,
                                                        "category": is_,
                                                        "names": names,
                                                        "has": has_,
                                                        "metrics": metrics,
                                                        "page": "meta_search",
                                                        "section": "meta",
                                                  },RequestContext(request))

    
def go_meta_detail(request, meta_id, slug=None):
    colores = ["info", "primary", "purple", "warning", "success", "danger"]
    url = "http://api.wikilife.org/4/meta/withmetrics/%s"%meta_id
    response = requests.get(url).json()

            
            
    name = response["name"]
    other_names = response["otherNames"].split(",")
    
    names = []
    
    for n in other_names:
        if n == " " or n == [] or n == "[]":
            continue
        names.append((n, random.choice(colores)))
        
    has = response["has"]
    has_ = []
    for h in has:
        has_.append((h["name"], random.choice(colores)))
        
    try:
        css_class = ""
        is_ = response["is"][0]["name"]
        if is_ == "Food":
            css_class = "fa fa-cutlery"
        elif is_ == "Mood":
            css_class = "fa ion-happy"
        elif is_ == "Drug":
            css_class = "fa fa-circle-thin"
        elif is_ == "Exercise":
            css_class = "fa fa-child"
        elif is_ == "Complaints":
            css_class = "fa fa-stethoscope"
        elif is_ == "Conditions" or is_ == "Medical Conditions" :
            css_class = "fa ion-heart-broken"
    except:
        pass
    
    metrics = []
    for metric in response["metrics"]:
        metric["name"] = metric["name"].split("-")[0]
        metric["color"] = random.choice(colores)
        if metric["type"] != "NumericMetricNode":

            metric["type"] = "Text"
            if is_ != "Drug":
                options = metric["options"].split(",")
                default = int(metric["default"])
                metric["default"] = options[default]
            else:
                options = metric["options"].split(";")
                print options
                metric["default"] = options[0]
                metric["options"] = ", ".join(options)
                print metric["options"]
        
            metrics.append(metric)
    
    for metric in response["metrics"]:
        metric["name"] = metric["name"].split("-")[0]
        metric["color"] = random.choice(colores)
        if metric["type"] == "NumericMetricNode":
            metric["type"] = "Numeric"
            metrics.append(metric)
            
    ancestors_url = "http://api.wikilife.org/4/meta/ancestors/%s"%meta_id
    response_ancestors = requests.get(ancestors_url).json()
    response_ancestors.reverse()
    
    image_url = 'https://en.wikipedia.org/w/api.php?format=json&action=query&titles=%s&prop=pageimages&format=json&pithumbsize=400'%name
    response_image = requests.get(image_url).json()
    image_thumb_url = None
    try:
        image_thumb_url = response_image["query"]["pages"][response_image["query"]["pages"].keys()[0]]["thumbnail"]["source"]
    except:
        pass
    print metrics
    return render_to_response('stats/meta_detail.html',{"image_thumb_url":image_thumb_url,
                                                        "ancestors": response_ancestors, 
                                                        "name": name,
                                                        "css_class": css_class,
                                                        "category": is_,
                                                        "names": names,
                                                        "has": has_,
                                                        "metrics": metrics,
                                                        "page": "meta_search",
                                                        "section": "meta",
                                                  },RequestContext(request))
    