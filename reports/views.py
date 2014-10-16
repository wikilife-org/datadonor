from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from social_auth import __version__ as version
from django.http.response import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import login
from utils.commons import last_week_user_actions


def report_for_global_physical_steps(request):
    
    url = "/physical/exercise/steps/distribution/global/"
    return render_to_response('dashboard/global_report_pysical_steps.html',{"url":url},
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
  