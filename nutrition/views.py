from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http.response import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from nutrition.services.utilities import *

from nutrition.services.stats.services import NutritionDistributionService

def nutrition_nutrients(request):
    user = request.user
    global_data = NutritionDistributionService().get_nutrients_global_distribution()
    user_data = NutritionDistributionService().get_nutrients_user_distribution(user)
    
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


# Nutrients
def nutrition_nutrients_mock(request):

    user_data = {"protein":{"title":"Protein", "key":"protein", "percentage":30}, 
                 "fat":{"title":"Fat", "key":"fat", "percentage":20},
                 "carbs":{"title":"Carbs", "key":"carbs", "percentage":10},
                 "fiber":{"title":"Fiber", "key":"fiber", "percentage":7}}
    
    global_data = {"protein":{"title":"Protein", "key":"protein", "percentage":30}, 
                 "fat":{"title":"Fat", "key":"fat", "percentage":20},
                 "carbs":{"title":"Carbs", "key":"carbs", "percentage":15},
                 "fiber":{"title":"Fiber", "key":"fiber", "percentage":25}}
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nutrition_global_nutrients_mock(request):
    data = {"protein":{"title":"Protein", "key":"protein", "percentage":30}, 
                 "fat":{"title":"Fat", "key":"fat", "percentage":20},
                 "carbs":{"title":"Carbs", "key":"carbs", "percentage":15},
                 "fiber":{"title":"Fiber", "key":"fiber", "percentage":25}}

    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nutrition_user_nutrients_mock(request):
    data = {"protein":{"title":"Protein", "key":"protein", "percentage":30}, 
                 "fat":{"title":"Fat", "key":"fat", "percentage":20},
                 "carbs":{"title":"Carbs", "key":"carbs", "percentage":10},
                 "fiber":{"title":"Fiber", "key":"fiber", "percentage":7}}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def nutrition_user_nutrients(request):
    data = {}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nutrition_global_nutrients(request):
    data = NutritionDistributionService().get_nutrients_global_distribution()
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

#End Nutrients

#Weight

@csrf_exempt
def nutrition_weight_mock(request):
    if request.method == 'POST':
        unit = request.POST["unit"]
        value = request.POST["value"]
        user_data = {"value":value, "unit":unit}
    else:
        user_data = {"value":112, "unit":"Lbs"}
    global_data = {"men":{"value":120, "unit":"Lbs"}, "women":{"value":94, "unit":"Lbs"}}
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def nutrition_weight(request):
    if request.method == 'POST':
        unit = request.POST["unit"]
        value = request.POST["value"]
        
        request.user.profile.weight = value
        request.user.profile.save()
        user_data = {"value":value, "unit":unit}
    else:
        w = 0
        if request.user.profile and request.user.profile.weight:
            w = request.user.profile.weight
        user_data = {"value":w, "unit":"Lbs"}
        
    global_data = global_weight()
    
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@csrf_exempt
def nutrition_user_weight_mock(request):
    if request.method == 'POST':
        unit = request.POST["unit"]
        value = request.POST["value"]
        data = {"value":value, "unit":unit}
    else:
        data = {"value":0, "unit":"Lbs"}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nutrition_global_weight_mock(request):
    data = {"men":{"value":120, "unit":"Lbs"}, "women":{"value":94, "unit":"Lbs"}}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def nutrition_user_weight(request):
    if request.method == 'POST':
        unit = request.POST["unit"]
        value = request.POST["value"]
        data = {"value":value, "unit":unit}
    else:
        data = {"value":0, "unit":"Lbs"}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nutrition_global_weight(request):
    data = {"men":{"value":120, "unit":"Lbs"}, "women":{"value":94, "unit":"Lbs"}}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

#End Weight

#Height
@csrf_exempt
def nutrition_height_mock(request):
    if request.method == 'POST':
        unit = request.POST["unit"]
        value = request.POST["value"]
    
        user_data = {"value":value, "unit":unit}
    else:
        user_data = {"value":5.8, "unit":"Ft"}
    global_data = {"men":{"value":7.2, "unit":"Ft"}, "women":{"value":4.3, "unit":"Ft"}}
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def nutrition_height(request):
    if request.method == 'POST':
        unit = request.POST["unit"]
        value = request.POST["value"]
        request.user.profile.height = value
        request.user.profile.save()
        user_data = {"value":value, "unit":unit}
    else:
        h = 0
        if request.user.profile and request.user.profile.height:
            h = request.user.profile.height
        user_data = {"value":h, "unit":"Ft"}
    global_data = global_height()
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def nutrition_global_height_mock(request):
    data = {"men":{"value":7.2, "unit":"Ft"}, "women":{"value":4.3, "unit":"Ft"}}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nutrition_global_height(request):
    data = {"men":{"value":7.2, "unit":"Ft"}, "women":{"value":4.3, "unit":"Ft"}}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def nutrition_user_height(request):
    if request.method == 'POST':
        unit = request.POST["unit"]
        value = request.POST["value"]
        data = {"value":value, "unit":unit}
    else:
        data = {"value":0, "unit":"Ft"}

    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


@csrf_exempt
def nutrition_user_height_mock(request):
    if request.method == 'POST':
        unit = request.POST["unit"]
        value = request.POST["value"]
        data = {"value":value, "unit":unit}
    else:
        data = {"value":0, "unit":"Ft"}

    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
#End height

#BMI
def nutrition_bmi_mock(request):
    user_data = {"value":20}
    global_data = {"men":{"value":20}, "women":{"value":26}}
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nutrition_bmi(request):
    h = 0
    w = 0
    if request.user.profile and request.user.profile.height:
        h =request.user.profile.height

    if request.user.profile and request.user.profile.weight:
        w =request.user.profile.weight
        
    user_data = {"value":get_bmi(h, w)}
    global_data = get_global_bmi()
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nutrition_user_bmi_mock(request):
    data = {"value":20}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nutrition_user_bmi(request):
    data = {"value":20}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nutrition_global_bmi_mock(request):
    data = {"men":{"value":20}, "women":{"value":26}}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nutrition_global_bmi(request):
    data = {"men":{"value":20}, "women":{"value":26}}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
