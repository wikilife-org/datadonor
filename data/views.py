from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http.response import HttpResponse
from django.utils import simplejson
from django.contrib.auth.models import User
from social.services.utilities import *
from utils.date_util import get_last_sunday, get_last_year
from wikilife.clients.stats import Stats
import csv
from data.reports import _generate_export_json, _generate_export_xls


def download(request):
    ctx = {"last_sunday": get_last_sunday()[1], "last_year":get_last_year()[1]}
    
    return render_to_response('data/download.html',ctx,
                                  RequestContext(request))

def history_steps(request):
    client = Stats({"HOST":"http://api.wikilife.org"})
    steps_days = client.get_global_steps_one_year()["data"]
    return HttpResponse(simplejson.dumps(steps_days), mimetype="application/json")

def history_calories(request):
    client = Stats({"HOST":"http://api.wikilife.org"})
    calories_days = client.get_global_calories_burned_one_year()["data"]
    return HttpResponse(simplejson.dumps(calories_days), mimetype="application/json")

def history_distance(request):
    client = Stats({"HOST":"http://api.wikilife.org"})
    distance_days = client.get_global_distance_one_year()["data"]
    return HttpResponse(simplejson.dumps(distance_days), mimetype="application/json")

def history_steps_csv(request):
    client = Stats({"HOST":"http://api.wikilife.org"})
    steps_days = client.get_global_steps_one_year()["data"]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="steps.csv"'
    writer = csv.writer(response)
    writer.writerow(steps_days[0].keys())
    
    for row in steps_days:
        writer.writerow(row.values())
    return response

def history_distance_csv(request):
    client = Stats({"HOST":"http://api.wikilife.org"})
    distance_days = client.get_global_distance_one_year()["data"]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="distance.csv"'
    writer = csv.writer(response)
    writer.writerow(distance_days[0].keys())
    
    for row in distance_days:
        writer.writerow(row.values())
    return response

def history_calories_csv(request):
    client = Stats({"HOST":"http://api.wikilife.org"})
    calories_days = client.get_global_calories_burned_one_year()["data"]
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="calories.csv"'
    writer = csv.writer(response)
    writer.writerow(calories_days[0].keys())
    
    for row in calories_days:
        writer.writerow(row.values())
    return response
    
    
def export(request, user_id, format):
    user = User.objects.get(id=user_id)
    if format == "json":
        report_json = _generate_export_json(user)
        return HttpResponse(simplejson.dumps(report_json), mimetype="application/json")
    if format == "csv":
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="my_datadonors_data.csv"'
        """ writer = csv.writer(response)
        writer.writerow(report_json[0].keys())
        
        for row in report_json:
            writer.writerow(row.values())"""
        return response
    elif format == "xls":
        report_xls = _generate_export_xls(user)
        return report_xls
    





    