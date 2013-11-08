from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http.response import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt


# Nutrients
def nutrition_nutrients_mock(request):

    user_data = {"protein":{"title":"Protein", "key":"protein", "percentage":90}, 
                 "fat":{"title":"Fat", "key":"fat", "percentage":2},
                 "carbs":{"title":"Carbs", "key":"carbs", "percentage":1},
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
    data = {"protein":{"title":"Protein", "key":"protein", "percentage":90}, 
                 "fat":{"title":"Fat", "key":"fat", "percentage":2},
                 "carbs":{"title":"Carbs", "key":"carbs", "percentage":1},
                 "fiber":{"title":"Fiber", "key":"fiber", "percentage":7}}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nutrition_nutrients(request):

    user_data = {"protein":{"title":"Protein", "key":"protein", "percentage":90}, 
                 "fat":{"title":"Fat", "key":"fat", "percentage":1},
                 "carbs":{"title":"Carbs", "key":"carbs", "percentage":2},
                 "fiber":{"title":"Fiber", "key":"fiber", "percentage":7}}
    
    global_data = {"protein":{"title":"Protein", "key":"protein", "percentage":30}, 
                 "fat":{"title":"Fat", "key":"fat", "percentage":20},
                 "carbs":{"title":"Carbs", "key":"carbs", "percentage":15},
                 "fiber":{"title":"Fiber", "key":"fiber", "percentage":25}}
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nutrition_user_nutrients(request):
    data = {}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nutrition_global_nutrients(request):
    data = {}
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
        user_data = {"value":value, "unit":unit}
    else:
        user_data = {"value":0, "unit":"Lbs"}
    global_data = {"men":{"value":120, "unit":"Lbs"}, "women":{"value":94, "unit":"Lbs"}}
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
        user_data = {"value":value, "unit":unit}
    else:
        user_data = {"value":0, "unit":"Ft"}
    global_data = {"men":{"value":7.2, "unit":"Ft"}, "women":{"value":4.3, "unit":"Ft"}}
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
    user_data = {"value":20}
    global_data = {"men":{"value":20}, "women":{"value":26}}
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
