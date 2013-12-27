from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from social_auth import __version__ as version
from social_auth.utils import setting
from django.http.response import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from social.services.utilities import *
from social.models import GlobalWorkExperinceDistribution


def social_reach(request):
    user_data = request.user.social_aggregated_data.social_reach()
    global_data = global_social_reach()
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def social_sharing(request):
    user_data = request.user.social_aggregated_data.social_sharing()
    global_data = global_social_sharing()
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


EDUCATION_LEVELS = {6:"phd",
            5:"master",
            4:"university", 
           3:"tech_institute",
            2:"high_school",
            1:"junior_college",
            0:"elementary_school"}

@csrf_exempt
def social_education(request):
    if request.method == "POST":
        education_level = request.POST["education_level"]
        #Validate value
        valid, education_level = is_valid_education(education_level)
        if valid:
        #save Value
            request.user.social_aggregated_data.education_level_manual = int(education_level)
            request.user.social_aggregated_data.save()
            if request.user.social_aggregated_data.education_degree:
                update_degree(request.user.social_aggregated_data.education_degree, int(education_level))
    
    if request.user.social_aggregated_data.education_level_manual is not None:
        level = request.user.social_aggregated_data.education_level_manual
    else:
        level = request.user.social_aggregated_data.education_level
    
    user_data = {"user_level": EDUCATION_LEVELS[level]}
    global_data = global_education()
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def social_work(request):
    if request.method == 'POST':
        working_experience = request.POST["working_experience"]
        #Validate value
        if is_valid_working_experience(working_experience):
        #save Value
            request.user.social_aggregated_data.work_experience_years_manual = int(working_experience)
            request.user.social_aggregated_data.save()
    
    years = request.user.social_aggregated_data.work_experience_years_manual or \
                        request.user.social_aggregated_data.work_experience_years
    
    age_range = get_age_range(request.user.profile.date_of_birth)
    user_data = {"user_experience": {"key": age_range, "value":years}}
    
    """
    last_distribution = GlobalWorkExperinceDistribution.objects.latest()
    
    global_data = { "15-25":{"key": "15-25", "value": last_distribution.range_15_25}, 
                    "26-35":{"key": "26-35", "value": last_distribution.range_26_35}, 
                    "36-45":{"key": "36-45", "value": last_distribution.range_36_45}, 
                    "46-55":{"key": "46-55", "value": last_distribution.range_46_55}, 
                    "56-65":{"key": "56-65", "value": last_distribution.range_56_65}}
    """
    
    global_data, avg = global_work()
    data = {"user_data":user_data, "global_data":global_data, "avg":avg}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def social_reach_mock(request):
    data = get_social_reach_mock()
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def social_sharing_mock(request):
    global_data = global_social_sharing_mock()
    user_data = user_social_sharing_mock()
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def social_work_mock(request):
    if request.method == 'POST':
        working_experience = request.POST["working_experience"]

    user_data = {"user_experience": {"key": "26-35", "value":40}}
    global_data = {"15-25":{"key": "15-25", "value":20}, 
                    "26-35":{"key": "26-35", "value":50}, 
                    "36-45":{"key": "36-45", "value":60}, 
                    "46-55":{"key": "46-55", "value":70}, 
                    "56-65":{"key": "56-65", "value":80}}
    data = {"user_data":user_data, "global_data":global_data, "avg":10}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def social_education_mock(request):
    if request.method == "POST":
        education_level = request.POST["education_level"]
        user_data = {"user_level": education_level}
    else:
        
        user_data = {"user_level": 'junior_college'}
    global_data = {6:{"percentage":8, "key":"phd", "title": "PhD", "index":6},
                       5:{"percentage":10, "key":"master", "title": "Master", "index":5},
                       4:{"percentage":23, "key":"university", "title": "University", "index":4}, 
                       3:{"percentage":5, "key":"tech_institute", "title": "Technical Institute", "index":3},
                       2:{"percentage":3, "key":"high_school", "title": "High School", "index":2},
                       1:{"percentage":57, "key":"junior_college", "title": "Junior College", "index":1},
                       0:{"percentage":3, "key":"elemtary_school", "title": "Elementary School", "index":0}}
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

