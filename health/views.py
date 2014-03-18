# coding=utf-8

from django.http.response import HttpResponse
from django.utils import simplejson
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from utilities import *
from health.models import *

ONE_MINUTE = 60
ONE_HOUR = ONE_MINUTE*60

#Cronical Conditions

def cronical_conditions_ranking_global_mock(request):
    data = [{"id":10, "name":"Cancer", 
             "types":[{"name":"Lung Cancer", "id":0}, 
                      {"name":"Melanoma", "id":1}, 
                      {"name":"Mouth Cancer", "id":2}], 
             "percentage":57},
            {"id":12, "name":"Respiratory Disease", 
             "types":[], 
             "percentage":23},
            {"id":23, "name":"HIV", 
             "types":[], 
             "percentage":5},
            {"id":3, "name":"Heart Disease", 
             "types":[], 
             "percentage":5},
            {"id":4, "name":"Diabetes", 
             "types":[{"name":"Type 1", "id":0}, {"name":"Type 2", "id":1}, {"name":"GDM", "id":2}], 
             "percentage":10},]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def cronical_conditions_by_user_mock(request):
    if request.method == 'POST':
        id_condition = request.POST["id_condition"]
        id_type = request.POST["id_type"]
    if request.method == 'DELETE':
        id_condition =  request.GET["id_condition"]
        
    data = [{"id_condition": 4, "name":"Diabetes", "id_type":1, "type_name": "Type 2"}]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")



def cronical_conditions_list_mock(request):
    data = [{"id":10, "name":"Cancer", 
             "types":[{"name":"Lung Cancer", "id":0}, 
                      {"name":"Melanoma", "id":1}, 
                      {"name":"Mouth Cancer", "id":2}], 
             "percentage":57},
            {"id":12, "name":"Respiratory Disease", 
             "types":[], 
             "percentage":23},
            {"id":23, "name":"HIV", 
             "types":[], 
             "percentage":5},
            {"id":3, "name":"Heart Disease", 
             "types":[], 
             "percentage":5},
            {"id":4, "name":"Diabetes", 
             "types":[{"name":"Type 1", "id":0}, {"name":"Type 2", "id":1}, {"name":"GDM", "id":2}], 
             "percentage":10},]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")



def cronical_conditions_ranking_global(request):
    data = get_conditions_rank()[:5]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def cronical_conditions_by_user(request):
    if request.method == 'POST':
        id_condition = request.POST["id_condition"]
        id_type = request.POST["id_type"] 
        c_name, t_name = get_conditions_name(id_condition, id_type)
        #UserConditions.objects.get_or_create(user=request.user)
    if request.method == 'DELETE':
        id_condition =  request.GET["id_condition"]
        
    data = [{"id_condition": 4, "name":"Diabetes", "id_type":1, "type_name": "Type 2"}]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def cronical_conditions_list(request):
    data = get_conditions()
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


#Complaints

def complaints_ranking_global_mock(request):
    data = [{"id":10, "name":"Runny Nose", 
             "percentage":57},
            {"id":12, "name":"Fatigue", 
             "percentage":23},
            {"id":23, "name":"Headache", 
             "percentage":5},
            {"id":3, "name":"Back Pain", 
             "percentage":5},
            {"id":4, "name":"Abdominal Pain", 
             "percentage":10},]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def complaints_list_mock(request):
    data = [{"id":10, "name":"Runny Nose", 
             "percentage":27},
            {"id":12, "name":"Fatigue", 
             "percentage":23},
            {"id":23, "name":"Headache", 
             "percentage":5},
            {"id":3, "name":"Back Pain", 
             "percentage":5},
            {"id":4, "name":"Abdominal Pain", 
             "percentage":10},
            {"id":40, "name":"Neck Pain", 
             "percentage":10},
            {"id":14, "name":"Leg Pain", 
             "percentage":10}]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def complaints_by_user_mock(request):
    if request.method == 'POST':
        id_complaint = request.POST["id_complaint"]

    if request.method == 'DELETE':
        id_complaint =  request.GET["id_complaint"]
        
    data = [{"id":10, "name":"Runny Nose", 
             "percentage":27},
            {"id":40, "name":"Neck Pain", 
             "percentage":10},
            {"id":4, "name":"Leg Pain", 
             "percentage":10}]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def complaints_ranking_global(request):
    data = get_complaints_rank()[:5]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def complaints_list(request):
    data = get_complaints()
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def complaints_by_user(request):
    data = []
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


#Blood Type

BLOOD_TYPE = {0:{"name": "I don't Know", "id":0, "percentage":35},
            1:{"name": "A+", "id":1, "percentage":20},
            2:{"name": "A-", "id":2, "percentage":5},
            3:{"name": "B+", "id":3, "percentage":10},
            4:{"name": "B-", "id":4, "percentage":5},
            5:{"name": "AB+", "id":5, "percentage":5},
            6:{"name": "AB-", "id":6, "percentage":10},
            7:{"name": "0+", "id":7,"percentage":3},
            8:{"name": "0-", "id":8, "percentage":2}}

def bood_type_distribution_global_mock(request):
    data = [{"name": "I don't Know", "id":0, "percentage":35},
            {"name": "A+", "id":1, "percentage":20},
            {"name": "A-", "id":2, "percentage":5},
            {"name": "B+", "id":3, "percentage":10},
            {"name": "B-", "id":4, "percentage":5},
            {"name": "AB+", "id":5, "percentage":5},
            {"name": "AB-", "id":6, "percentage":10},
            {"name": "0+", "id":7,"percentage":3},
            {"name": "0-", "id":8, "percentage":2}]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def bood_type_by_user_mock(request):
    if request.method == 'POST':
        id_blood_type = int(request.POST["id_blood_type"])
        data = BLOOD_TYPE[id_blood_type]
    else:
        data = {"name": "B+", "id":3, "percentage":10}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def bood_type_distribution_global(request):
    data = global_blood_type()
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def bood_type_by_user(request):
    if request.method == 'POST':
        id_blood_type = int(request.POST["id_blood_type"])
        
        try:
            bt=UserBloodType.objects.get(user=request.user)
            bt.blood_type_id=id_blood_type
            bt.save()
        except:
            UserBloodType.objects.create(user=request.user, blood_type_id=id_blood_type, metric_id=0, log_id=0)
        
        data = global_blood_type_dict()[id_blood_type]
    else:
        try:
            bt=UserBloodType.objects.get(user=request.user)
            data= global_blood_type_dict()[bt.blood_type_id]
        except:
            data = {}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

#Sleep

def sleep_distribution_global_mock(request):
    data = {"days":{"sunday":{"hours": 11.2}, "monday":{"hours": 8.5 },
                    "tuesday":{"hours": 5 }, "wednesday":{"hours": 3.7 },
                    "thursday":{"hours": 3}, "friday":{"hours": 4.9},
                    "saturday":{"hours": 3}},
            "avg_hours":8.4}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def sleep_distribution_by_user_mock(request):
    if request.method == 'POST':
        pass
    data = {"days":{"sunday":{"hours": 9.2}, "monday":{"hours": 4.7 },
                    "tuesday":{"hours": 7 }, "wednesday":{"hours": 2 },
                    "thursday":{"hours": 6.8}, "friday":{"hours": 9.4},
                    "saturday":{"hours": 1.5}},
            "avg_hours":6.3}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def sleep_distribution_global(request):
    data = []
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def sleep_distribution_by_user(request):
    data = []
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


#Emotions

def emotions_ranking_global_mock(request):
    data = [{"id":10, "name":"Disappointed", 
             "percentage":57},
            {"id":12, "name":"Stressed", 
             "percentage":23},
            {"id":23, "name":"Sad", 
             "percentage":5},
            {"id":3, "name":"Angry", 
             "percentage":5},
            {"id":4, "name":"Euphoric", 
             "percentage":10},]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def emotions_by_user_mock(request):
    if request.method == 'POST':
        id_emotion = request.POST["id_emotion"]

    if request.method == 'DELETE':
        id_emotion =  request.GET["id_emotion"]
         
    data = [{"id_emotion": 10, "name":"Disappointed"}]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def emotions_list_mock(request):
    data = [{"id":10, "name":"Disappointed", 
             "percentage":57},
            {"id":12, "name":"Stressed", 
             "percentage":23},
            {"id":23, "name":"Sad", 
             "percentage":5},
            {"id":3, "name":"Angry", 
             "percentage":5},
            {"id":4, "name":"Euphoric", 
             "percentage":10},
            {"id":43, "name":"Happy", 
             "percentage":10},]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")



def emotions_ranking_global(request):
    data = get_emotions_rank()[:5]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def emotions_by_user(request):
    data = []
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def emotions_list(request):
    data = get_emotions()
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

#Mood

def mood_avg_global_mock(request):
    data = {"mood_avg": 8}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def mood_avg_by_user_mock(request):
    if request.method == 'POST':
        mood_avg = int(request.POST["mood_avg"])
    data = {"mood_avg": 5}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def mood_panda_activate_mock(request):
    if request.method == 'POST':
        panda_email = request.POST["email_mood_panda"]
        data = {"mood_avg":mood_avg}
    else:
        data = {"status": "ok", "mood_avg":5}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def mood_avg_global(request):
    data = global_mood_avg()
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def mood_avg_by_user(request):
    if request.method == 'POST':
        avg_mood = int(request.POST["mood_avg"])
        try:
            UserMoodLastWeek.objects.get(user=request.user)
        except:
            UserMoodLastWeek.objects.create(user=request.user, avg_mood=avg_mood)

    try:
        avg = UserMoodLastWeek.objects.get(user=request.user).avg_mood
    except:
        avg = 5
    data = {"mood_avg": avg}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def mood_panda_activate(request):
    data = []
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

