from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from social_auth import __version__ as version
from django.http.response import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login
from physical.services.stats.services import PhysicalActivityDistributionService
from utils.commons import last_week_user_actions
from social.services.utilities import global_education, global_work

def report_global_physical_steps(request):
    
    dto = PhysicalActivityDistributionService().get_steps_distribution_global()
    data = {
            "days": {
                     "sunday":     dto["sun"], 
                     "monday":    dto["mon"],
                     "tuesday":    dto["tue"], 
                     "wednesday": dto["wed"],
                     "thursday":  dto["thu"], 
                     "friday":    dto["fri"],
                     "saturday":  dto["sat"]
                     },
            "avg": dto["avg"],
            "total_users": dto["total_users"]

    }
    return render_to_response('dashboard/global_report_physical_steps.html',{"data":simplejson.dumps(data),"total_users":data["total_users"], "avg":data["avg"]},
                                  RequestContext(request)) 



def report_global_physical_miles(request):
    
    dto = PhysicalActivityDistributionService().get_miles_distribution_global()
    data = {
            "days": {
                     "sunday":     dto["sun"], 
                     "monday":    dto["mon"],
                     "tuesday":    dto["tue"], 
                     "wednesday": dto["wed"],
                     "thursday":  dto["thu"], 
                     "friday":    dto["fri"],
                     "saturday":  dto["sat"]
                     },
            "avg": dto["avg"],
            "total_users": dto["total_users"]

    }
    return render_to_response('dashboard/global_report_physical_miles.html',{"data":simplejson.dumps(data),"total_users":data["total_users"], "avg":data["avg"]},
                                  RequestContext(request)) 

def report_global_physical_duration(request):
    
    dto = PhysicalActivityDistributionService().get_hours_distribution_global()
    data = {
            "days": {
                     "sunday":     dto["sun"], 
                     "monday":    dto["mon"],
                     "tuesday":    dto["tue"], 
                     "wednesday": dto["wed"],
                     "thursday":  dto["thu"], 
                     "friday":    dto["fri"],
                     "saturday":  dto["sat"]
                     },
            "avg": dto["avg"],
            "total_users": dto["total_users"]

    }
    return render_to_response('dashboard/global_report_physical_duration.html',{"data":simplejson.dumps(data),"total_users":data["total_users"], "avg":data["avg"]},
                                  RequestContext(request))

def report_global_social_education(request):
    
    dto = global_education()
    
    return render_to_response('dashboard/global_report_social_education.html',{"data":simplejson.dumps({"global_data":dto})},
                                  RequestContext(request))


def report_global_social_education(request):
    
    global_data, avg = global_work()
    data = {"global_data":global_data, "avg":avg}
    
    return render_to_response('dashboard/global_report_social_education.html',{"data":simplejson.dumps(data)},
                                  RequestContext(request))
    
def report_for_user_full(request, user_id):
    user = User.objects.get(id=user_id)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    ctx = last_week_user_actions(user)
    return render_to_response('dashboard/user_report.html',ctx,
                                  RequestContext(request))
def report_for_user_exercise(request, user_id):
    user = User.objects.get(id=user_id)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return render_to_response('dashboard/physical.html',{},
                                  RequestContext(request))

def report_for_user_social(request, user_id):
    user = User.objects.get(id=user_id)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return render_to_response('dashboard/social.html',{},
                                  RequestContext(request))

def report_for_user_nutrition(request, user_id):
    user = User.objects.get(id=user_id)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return render_to_response('dashboard/nutrition.html',{},
                                  RequestContext(request))

def report_for_user_genomics(request, user_id):
    user = User.objects.get(id=user_id)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return render_to_response('dashboard/genomics.html',{},
                                  RequestContext(request))

def report_for_user_health(request, user_id):
    user = User.objects.get(id=user_id)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return render_to_response('dashboard/health.html',{},
                                  RequestContext(request))
  