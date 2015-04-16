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
from health.utilities import get_conditions_rank, get_complaints_rank, get_emotions_rank

def report_global_physical_steps(request):
    pic = request.GET.get('pic', False)
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
    return render_to_response('dashboard/global_report_physical_steps.html',{"data":simplejson.dumps(data),"total_users":data["total_users"], "pic":pic, "avg":data["avg"]},
                                  RequestContext(request)) 


from utils.date_util import get_last_sunday,get_last_sunday_from_date, get_next_sunday_from_date
from datetime import date

def report_global_physical_miles(request):
    pic = request.GET.get('pic', False)
    date_info = get_last_sunday()
    from_date = request.GET.get('from', date_info[1])
    to_date = request.GET.get('to', date_info[2])
    
    prev_date = get_last_sunday_from_date(from_date)
    prev = {"from":prev_date[1], "to":prev_date[2]}
    
    
    if to_date <= date.today().strftime("%Y-%m-%d"):
        next_date = get_next_sunday_from_date(to_date)
        next = {"from":next_date[1], "to":next_date[2]}
    else:
        next = None
    dto = PhysicalActivityDistributionService().get_miles_distribution_global_by_date(from_date, to_date)
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
    return render_to_response('dashboard/global_report_physical_miles.html',{"data": simplejson.dumps(data),
                                                                             "total_users": data["total_users"], 
                                                                             "pic": pic, 
                                                                             "avg": data["avg"],
                                                                             "prev": prev,
                                                                             "next": next, "from": from_date, "to":to_date},
                                  RequestContext(request)) 

def report_global_physical_duration(request):
    pic = request.GET.get('pic', False)
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
    return render_to_response('dashboard/global_report_physical_duration.html',{"data":simplejson.dumps(data),"total_users":data["total_users"], "pic":pic, "avg":data["avg"]},
                                  RequestContext(request))

def report_global_social_education(request):
    pic = request.GET.get('pic', False)
    dto = global_education()
    
    return render_to_response('dashboard/global_report_social_education.html',{"data":simplejson.dumps({"global_data":dto}),"pic":pic,},
                                  RequestContext(request))


def report_global_social_work(request):
    pic = request.GET.get('pic', False)
    global_data, avg, total_users  = global_work()
    data = {"global_data":global_data, "avg":avg}
    
    return render_to_response('dashboard/global_report_social_work.html',{"data":simplejson.dumps(data), "total_users": total_users, "pic":pic,},
                                  RequestContext(request))


def report_global_health_condition(request):
    pic = request.GET.get('pic', False)
    data, total = get_conditions_rank()
    return render_to_response('dashboard/global_report_health_conditions.html',{"data":simplejson.dumps(data[:5]), "total_users": total, "pic":pic,},
                                  RequestContext(request))

def report_global_health_complaints(request):
    pic = request.GET.get('pic', False)
    data, total = get_complaints_rank()
    return render_to_response('dashboard/global_report_health_complaints.html',{"data":simplejson.dumps(data[:5]), "total_users": total, "pic":pic,},
                                  RequestContext(request))

def report_global_health_emotions(request):
    pic = request.GET.get('pic', False)
    data, total = get_emotions_rank()
    return render_to_response('dashboard/global_report_health_emotions.html',{"data":simplejson.dumps(data[:5]), "total_users": total, "pic":pic,},
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
  
import csv


def exercise_history(request):
    path = "/home/datadonor/static/datadonors.csv"
    data = []
    #open csv
    f = open(path)
    data_csv = csv.reader(f)
    
    count = 0
    for row in data_csv:
        print row
        count = count + 1

        data.append(row)

    return render_to_response('data/table.html',{"data":data},
                                  RequestContext(request))
    
    