
from django.contrib.auth.models import User
from django.http.response import HttpResponse
from django.utils import simplejson
from users.models import Profile
from health.models import UserBloodType, UserOxygenSaturation, UserBloodAlcoholContent, UserBloodGlucose, UserBodyTemperature, UserHeartRate
from physical.models import UserActivityLog
from nutrition.models import UserFoodLog
import re, random, string
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.forms.models import model_to_dict
from bson import json_util
import logging
from os import path
from api.models import *

logger = logging.getLogger('datadonors')

file_log_handler = logging.FileHandler(path.join(path.dirname(__file__),'../logs/rest.log'))
logger.addHandler(file_log_handler)

# nice output format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_log_handler.setFormatter(formatter)

 
TYPE_DICT = {}
TYPE_DICT["gender"] = {"model":Profile, "field":"gender", "key":'user'}
TYPE_DICT["bmi"] = {"model":Profile, "field":"bmi", "key":'user'}
TYPE_DICT["weight"] = {"model":Profile, "field":"weight", "key":'user'}
TYPE_DICT["height"] = {"model":Profile, "field":"height", "key":'user'}
TYPE_DICT["date_of_birth"] = {"model":Profile, "field":"date_of_birth", "key":'user'}

TYPE_DICT["blood_type"] = {"model":UserBloodType, "field":"value", "key":'user'}
TYPE_DICT["oxygen_saturation"] = {"model":UserOxygenSaturation, "field":"value", "key":'user'}
TYPE_DICT["blood_glucose"] = {"model":UserBloodGlucose, "field":"value", "key":'user'}
TYPE_DICT["blood_alcohol_content"] = {"model":UserBloodAlcoholContent, "field":"value", "key":'user'}
TYPE_DICT["body_temperature"] = {"model":UserBodyTemperature, "field":"value", "key":'user'}
TYPE_DICT["heart_rate"] = {"model":UserHeartRate, "field":"value", "key":'user'}

TYPE_DICT["step_count"] = {"model":UserActivityLog, "field":"steps", "key":'execute_datetime', "add":True}
TYPE_DICT["distance"] = {"model":UserActivityLog,"field":"miles", "key":'execute_datetime', "add":True}
TYPE_DICT["activity_count"] = {"model":UserActivityLog, "field":"activity_count", "key":'execute_datetime', "add":True}
TYPE_DICT["nike_fuel"] = {"model":UserActivityLog, "field":"nike_fuel", "key":'execute_datetime', "add":True}
TYPE_DICT["active_energy"] = {"model":UserActivityLog, "field":"active_energy", "key":'execute_datetime', "add":True}

TYPE_DICT["fat_total"] = {"model":UserFoodLog, "field":"fat", "key":'execute_datetime', "add":True}
TYPE_DICT["fiber"] = {"model":UserFoodLog, "field":"fiber", "key":'execute_datetime', "add":True}
TYPE_DICT["sugar"] = {"model":UserFoodLog, "field":"sugar", "key":'execute_datetime', "add":True}
TYPE_DICT["calories"] = {"model":UserFoodLog, "field":"calories", "key":'execute_datetime', "add":True}
TYPE_DICT["protein"] = {"model":UserFoodLog,"field":"protein", "key":'execute_datetime', "add":True}
TYPE_DICT["carbohydrates"] = {"model":UserFoodLog, "field":"carbs", "key":'execute_datetime', "add":True}


from social_auth.models import UserSocialAuth
from social_auth.backends import get_backend

from social.util.social_service_locator import SocialServiceLocator
from api.services import user_registration, upload_image, process_text, process_location, process_data, process_log,\
    get_user_timeline
from api.models import Log, Data, TextData

@csrf_exempt
def register(request):
    if request.method == 'POST':
        #valid_user
        #print request.POST
        #print request.POST.get("facebook")
        
        #post_content = request.POST
        post_content = simplejson.loads(request.body)
        #info es un array
        if not ("facebook" not in post_content.keys() or "twitter" not in post_content.keys() or "linkedin" not in post_content.keys()):
            return HttpResponse(simplejson.dumps({"message": "Missing social auth token ", "status": "error", "data":{}}), mimetype="application/json")
        
        
        user_id = user_registration(post_content)
        data = {"user_id": user_id}     
        
    else:
        logger.info(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}))
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    
    logger.info(simplejson.dumps({"message": "Registration done!", "status": "success", "data":{}}))
    return HttpResponse(simplejson.dumps({"message": "Registration done!", "status": "success", "data":data}), mimetype="application/json")  

@csrf_exempt
def add_device(request):
    result = {}
    #append device access_token to user
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

@csrf_exempt
def delete_device(request):
    post_content = simplejson.loads(request.body)
    user_id = post_content["user_id"]
    log_id = post_content["log_id"]
    try:
        user = User.objects.get(id=int(user_id))
    except:
        return HttpResponse(simplejson.dumps({"status":"error", "message":"Invalid user"}), mimetype="application/json")
    
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

@csrf_exempt
def add_log(request):
    post_content = simplejson.loads(request.body)
    user_id = post_content["user_id"]
    try:
        user = User.objects.get(id=int(user_id))
    except:
        return HttpResponse(simplejson.dumps({"status":"error", "message":"Invalid user"}), mimetype="application/json")
    
    try:
        time_str = post_content["time"] #YYYY-MM-DD HH:MM:SS
    except:
       return HttpResponse(simplejson.dumps({"status":"error", "message":"Missing Time value"}), mimetype="application/json")
    
    try:
       date_object = datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
       post_content["time_obj"] = date_object
    except:
       return HttpResponse(simplejson.dumps({"status":"error", "message":"Invalid time format, use YYYY-MM-DD HH:MM:SS" }), mimetype="application/json")
    

    log_id = process_log(post_content, user)
    result = {"log_id":log_id}
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

@csrf_exempt
def add_image(request):
    post_content = simplejson.loads(request.body)
    try:
        log_id = int(post_content["log_id"])
        log = Log.objects.get(id=log_id)
        
    except:
        return HttpResponse(simplejson.dumps({"status":"error", "message": "Invalid LogId"}), mimetype="application/json")
    
    
    try:
        url = upload_image(post_content["image"], log_id)

    except:
        return HttpResponse(simplejson.dumps({"status":"error"}), mimetype="application/json")
    

    log.image_url = url
    log.save()
    
    return HttpResponse(simplejson.dumps({"status":"ok", "image_url":url}), mimetype="application/json")
    
@csrf_exempt
def edit_log(request):
    result = {}
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

@csrf_exempt
def delete_log(request):
    result = {}
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

@csrf_exempt
def get_timeline(request):
    from_id = request.GET.get("from_id", None)
    user_id = request.GET.get("user_id", None)
    if not user_id:
        return HttpResponse(simplejson.dumps({"status":"error", "message": "Missing user_id parameter"}), mimetype="application/json")
    limit = request.GET.get("limit", 10)
    result = get_user_timeline(user_id, from_id, limit)

    return HttpResponse(simplejson.dumps(result), mimetype="application/json")

@csrf_exempt
def get_profile(request):
    result = {}
    return HttpResponse(simplejson.dumps(result), mimetype="application/json")



def process(user, opr, value, date_):
    if opr["key"] == "user":
        obj = opr["model"].objects.get_or_create(user=user)[0]
    elif opr["key"] == "execute_datetime":
        obj = opr["model"].objects.get_or_create(user=user, execute_time=date_)[0]
    if "add" in opr:
        v = getattr(obj, opr["field"]) or 0
        value = v + value
    setattr(obj, opr["field"], value)
    obj.save()
    return obj

@csrf_exempt
def log(request):
    """
    {"userId": USER_ID,
     "type": TYPE,
     "nodeId": NODE_ID,
     "metricId": METRIC_ID,
     "value":VALUE,
     "executeDateTime": DATE_TIME
     
     }
    """
    if request.method == 'POST':
        #valid_user
        data = simplejson.loads(request.body)
        #info es un array
        for info in data:
            user_id = info["userId"]
            try:
                user = Profile.objects.get(account_id=user_id).user
            except:
                return HttpResponse(simplejson.dumps({"message": "Invalid User: %s"%user_id, "status": "error", "data":{}}), mimetype="application/json")
            
            #valid_type
            try:
                type = info["type"]
                opr = TYPE_DICT[type]
            except:
                return HttpResponse(simplejson.dumps({"message": "Invalid Type: %s"%type, "status": "error", "data":{}}), mimetype="application/json")
            
            try:
                value = float(info["value"])
            except:
                pass
            
            date_ = datetime.strptime(info["executeDateTime"], '%Y-%m-%d %H:%M:%S')
            obj = process(user, opr, value, date_)

    else:
        logger.info(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}))
        return HttpResponse(simplejson.dumps({"message": "Not implemented method", "status": "error", "data":{}}), mimetype="application/json")
    
    logger.info(simplejson.dumps({"message": "Datadonated!", "status": "success", "data":{}}))
    return HttpResponse(simplejson.dumps({"message": "Datadonated!", "status": "success", "data":{}}), mimetype="application/json")  
  

