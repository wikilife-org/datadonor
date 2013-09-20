from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from social_auth import __version__ as version
from social_auth.utils import setting
from wikilife.wikilife_connector import WikilifeConnector
from django.http.response import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

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

def home(request):
    """Home view, displays login mechanism"""

    ctx =  {'version': version}
        
    return render_to_response('landing.html', {'version': version},
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
        'user_social':request.user.social_aggregated_data.social_reach(),
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


def social_reach(request):

    user_data = {"facebook":{"count": 20, "percentage":20}, "twitter":{"count": 20, "percentage":20},
                "gmail":{"count": 20, "percentage":20}, "foursquare":{"count": 20, "percentage":20},
                "linkedin":{"count": 20, "percentage":20}}
    
    global_data = {"facebook":{"count": 20, "percentage":20}, "twitter":{"count": 20, "percentage":10},
                "gmail":{"count": 20, "percentage":10}, "foursquare":{"count": 20, "percentage":40},
                "linkedin":{"count": 20, "percentage":20}}
    
    data = {"user_data":user_data, "global_data":global_data}
    
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def social_sharing(request):
    
    user_data = {"facebook":{"posts":225, "likes":80}, "twitter":{"tweets":22, "retweets":11}}
    global_data = {"facebook":{"posts":134, "likes":44}, "twitter":{"tweets":99, "retweets":12}}
    data = {"user_data":user_data, "global_data":global_data}
    
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def social_education(request):
    if request.method == "POST":
        education_level = request.POST["education_level"]
        data = {}
        
    else:
        user_data = {"user_level": "under_program"}
        global_data = {"phd":{"percentage":8, "key":"phd", "title": "PhD", "index":6},
                       "master":{"percentage":10, "key":"master", "title": "Master", "index":5},
                       "under_program":{"percentage":23, "key":"under_program", "title": "Undergraduate Programs", "index":4}, 
                       "tech_inst":{"percentage":5, "key":"tech_inst", "title": "Technical Institute", "index":3},
                       "high_school":{"percentage":3, "key":"high_school", "title": "High School", "index":2},
                       "junior_college":{"percentage":57, "key":"junior_college", "title": "Junior College", "index":1},
                       "primary_school":{"percentage":3, "key":"primary_school", "title": "Primary School", "index":0}}
        data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def social_work(request):
    if request.method == 'POST':
        working_experience = request.POST["working_experience"]
        data = {}
    else:
        user_data = {"user_experience": {"key": "26-35", "value":40}}
        global_data = {"15-25":{"key": "15-25", "value":20}, 
                        "26-35":{"key": "26-35", "value":50}, 
                        "36-45":{"key": "36-45", "value":60}, 
                        "46-55":{"key": "46-55", "value":70}, 
                        "56-65":{"key": "56-65", "value":80}}
        data = {"user_data":user_data, "global_data":global_data, "avg":10}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def physical_exercise(request):

    data = [{"title": "Running", "key":"running", "global_times":4, "user_times":5 }, 
     {"title": "Walking", "key":"walking", "global_times":3, "user_times":1 },
     {"title": "Eliptical", "key":"Eliptical", "global_times":1, "user_times": 2}]
    
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def physical_user_exercise(request):

    data = [{"title": "Bike riding", "message":"every day"}, 
     {"title": "Snowboard", "message":"1 time per week"},
     {"title": "Downhill Skiing", "message":"1 times per year"},
     {"title": "Weight lifting", "message":"4 per year"}]
    
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def physical_steps_distribution(request):
    data = {"days":{"sunday":{"user_steps": 4000, "global_steps":2000}, "monday":{"user_steps": 3000, "global_steps":1000},
                    "tuesday":{"user_steps": 3000, "global_steps":1000}, "wednesday":{"user_steps": 3000, "global_steps":3000},
                    "thursday":{"user_steps": 5000, "global_steps":3000}, "friday":{"user_steps": 3000, "global_steps":2000},
                    "saturday":{"user_steps": 5000, "global_steps":3050}},
            "global_avg_steps":3000,
            "user_avg_steps": 2000}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def physical_miles_distribution(request):
    data = {"days":{"sunday":{"user_miles": 300, "global_miles":300}, "monday":{"user_miles": 300, "global_miles":300},
                    "tuesday":{"user_miles": 300, "global_miles":300}, "wednesday":{"user_miles": 300, "global_miles":300},
                    "thursday":{"user_miles": 300, "global_miles":300}, "friday":{"user_miles": 300, "global_miles":300},
                    "saturday":{"user_miles": 300, "global_miles":300}},
            "global_avg_miles":300,
            "user_avg_miles": 200}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def physical_hours_distribution(request):
    data = {"days":{"sunday":{"user_hours": 300, "global_hours":300}, "monday":{"user_hours": 300, "global_hours":300},
                    "tuesday":{"user_hours": 300, "global_hours":300}, "wednesday":{"user_hours": 300, "global_hours":300},
                    "thursday":{"user_hours": 300, "global_hours":300}, "friday":{"user_hours": 300, "global_hours":300},
                    "saturday":{"user_hours": 300, "global_hours":300}},
            "global_avg_hours":300,
            "user_avg_hours": 200}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")



def health_nutrients(request):
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

def health_weight(request):
    if request.method == 'POST':
        unit = request.POST["unit"]
        value = request.POST["value"]
        data = {}
    else:
        user_data = {"value":112, "unit":"Lbs"}
        global_data = {"men":{"value":120, "unit":"Lbs"}, "women":{"value":94, "unit":"Lbs"}}
        data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def health_height(request):
    if request.method == 'POST':
        unit = request.POST["unit"]
        value = request.POST["value"]
        data = {}
    else:
        user_data = {"value":5.8, "unit":"Ft"}
        global_data = {"men":{"value":7.2, "unit":"Ft"}, "women":{"value":4.3, "unit":"Ft"}}
        data = {"user_data":user_data, "global_data":global_data}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def health_bmi(request):
    user_data = {"value":22}
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


#TODO add sec token
def wikilife_push(request):
    WikilifeConnector().push()
    return HttpResponse("ok")

#TODO add sec token
def wikilife_pull(request):
    WikilifeConnector().pull()
    return HttpResponse("ok")