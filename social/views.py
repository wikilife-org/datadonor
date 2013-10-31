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
from social.services.utils import *

def comming(request):
    return render_to_response('splash/index.html', {'version': version},
                                  RequestContext(request))

def mock(request):
    return render_to_response('maquetas/index.html', {'version': version},
                                  RequestContext(request))

                        
def wizard(request):
    agent = request.META['HTTP_USER_AGENT']
    show_wizard =  request.user.is_authenticated() or request.session.get("user_agree", False)
    return render_to_response('wizard.html', {'version': version, 'show_wizard':show_wizard, 'agent':agent},
                                  RequestContext(request))

def terms(request):
    show_wizard =  request.user.is_authenticated() or request.session.get("user_agree", False)
    if show_wizard:
        return HttpResponseRedirect('/wizard/')
    return render_to_response('wizard.html', {'version': version, 'show_wizard':show_wizard, 'agent':agent},
                                  RequestContext(request))

def home(request):
    """Home view, displays login mechanism"""
    videos = request.GET.get('videos', None)
    ctx =  {'version': version}   
    return render_to_response('landing.html', {'version': version, 'videos':videos},
                                  RequestContext(request))

def greg(request):
    return render_to_response('google7d1bd3580ebd5b1b.html', {},
                                  RequestContext(request))
def dashboard(request):
    """Login complete view, displays user data"""
    if not request.user.is_authenticated() or request.session.get("wizard_mode", False):
        return HttpResponseRedirect('/wizard/')
    ctx = {
        'user': request.user,
        #'user_social':request.user.social_aggregated_data.social_reach(),
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    return render_to_response('data_donation.html', ctx, context_instance=RequestContext(request))

def end_wizard(request):
    request.session["wizard_mode"] = False
    return HttpResponseRedirect('/dashboard/')

def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version,
                                             'messages': messages},
                              RequestContext(request))

def user_account(request):

    data = {"logged":request.user.is_authenticated(), 
    "accounts": [a.provider for a in request.user.social_auth.all()]}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


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

@csrf_exempt
def social_work(request):
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
def social_education(request):
    if request.method == "POST":
        education_level = request.POST["education_level"]
        #Validate value
        if is_valid_education(education_level):
        #save Value
            request.user.social_aggregated_data.education_level = int(education_level)
            request.user.social_aggregated_data.save()
            update_degree(request.user.social_aggregated_data.education_degree, int(education_level))

    user_data = {"user_level": request.user.social_aggregated_data.education_level}
    global_data = {6:{"percentage":8, "key":"phd", "title": "PhD", "index":6},
                   5:{"percentage":10, "key":"master", "title": "Master", "index":5},
                   4:{"percentage":23, "key":"university", "title": "University", "index":4}, 
                   3:{"percentage":5, "key":"tech_institute", "title": "Technical Institute", "index":3},
                   2:{"percentage":3, "key":"high_school", "title": "High School", "index":2},
                   1:{"percentage":57, "key":"junior_college", "title": "Junior College", "index":1},
                   0:{"percentage":3, "key":"elemtary_school", "title": "Elementary School", "index":0}}
    data = {"user_data":user_data, "global_data":global_data}
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

    user_data = {"user_level": 3}
    global_data = {6:{"percentage":8, "key":"phd", "title": "PhD", "index":6},
                   5:{"percentage":10, "key":"master", "title": "Master", "index":5},
                   4:{"percentage":23, "key":"university", "title": "University", "index":4}, 
                   3:{"percentage":5, "key":"tech_institute", "title": "Technical Institute", "index":3},
                   2:{"percentage":3, "key":"high_school", "title": "High School", "index":2},
                   1:{"percentage":57, "key":"junior_college", "title": "Junior College", "index":1},
                   0:{"percentage":3, "key":"elemtary_school", "title": "Elementary School", "index":0}}
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")



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

@csrf_exempt
def nutrition_weight(request):
    if request.method == 'POST':
        unit = request.POST["unit"]
        value = request.POST["value"]
        data = {}
    else:
        user_data = {"value":112, "unit":"Lbs"}
        global_data = {"men":{"value":120, "unit":"Lbs"}, "women":{"value":94, "unit":"Lbs"}}
        data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def nutrition_height(request):
    if request.method == 'POST':
        unit = request.POST["unit"]
        value = request.POST["value"]
        data = {}
    else:
        user_data = {"value":5.8, "unit":"Ft"}
        global_data = {"men":{"value":7.2, "unit":"Ft"}, "women":{"value":4.3, "unit":"Ft"}}
        data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nutrition_bmi(request):
    user_data = {"value":20}
    global_data = {"men":{"value":20}, "women":{"value":26}}
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def nutrition_nutrients(request):

    user_data = {"protein":{"title":"Protein", "key":"protein", "percentage":15}, 
                 "fat":{"title":"Fat", "key":"fat", "percentage":30},
                 "carbs":{"title":"Carbs", "key":"carbs", "percentage":30},
                 "fiber":{"title":"Fiber", "key":"fiber", "percentage":25}}
    
    global_data = {"protein":{"title":"Protein", "key":"protein", "percentage":30}, 
                 "fat":{"title":"Fat", "key":"fat", "percentage":20},
                 "carbs":{"title":"Carbs", "key":"carbs", "percentage":15},
                 "fiber":{"title":"Fiber", "key":"fiber", "percentage":25}}
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def nutrition_weight(request):
    if request.method == 'POST':
        unit = request.POST["unit"]
        value = request.POST["value"]
        data = {}
    else:
        user_data = {"value":112, "unit":"Lbs"}
        global_data = {"men":{"value":120, "unit":"Lbs"}, "women":{"value":94, "unit":"Lbs"}}
        data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

@csrf_exempt
def nutrition_height(request):
    if request.method == 'POST':
        unit = request.POST["unit"]
        value = request.POST["value"]
        data = {}
    else:
        user_data = {"value":5.8, "unit":"Ft"}
        global_data = {"men":{"value":7.2, "unit":"Ft"}, "women":{"value":4.3, "unit":"Ft"}}
        data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def nutrition_bmi(request):
    user_data = {"value":20}
    global_data = {"men":{"value":20}, "women":{"value":26}}
    data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
def iagree(request):
    if request.method == 'POST':
        request.session["user_agree"] = True
        request.session["wizard_mode"] = True
        return HttpResponse(simplejson.dumps({}), mimetype="application/json")
    return HttpResponseRedirect('/wizard/')