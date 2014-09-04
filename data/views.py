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


def download(request):
    ctx = {"last_sunday": get_last_sunday()[1], "last_year":get_last_year()[1]}
    
    return render_to_response('data/download.html',ctx,
                                  RequestContext(request))

def history_steps(request):
    client = Stats({"HOST":"http://api.wikilife.org"})
    steps_days = client.get_global_steps_one_year()["data"]
    return HttpResponse(simplejson.dumps(steps_days), mimetype="application/json")

def history_distance(request):
    client = Stats({"HOST":"http://api.wikilife.org"})
    distance_days = client.get_global_distance_one_year()["data"]
    return HttpResponse(simplejson.dumps(distance_days), mimetype="application/json")

def history_steps_csv(request):
    client = Stats({"HOST":"http://api.wikilife.org"})
    steps_days = client.get_global_steps_one_year()["data"]
    tmp_file = json_csv(steps_days)
    return HttpResponse(simplejson.dumps(tmp_file), mimetype="text/csv")

def history_distance_csv(request):
    client = Stats({"HOST":"http://api.wikilife.org"})
    distance_days = client.get_global_distance_one_year()["data"]
    tmp_file = json_csv(distance_days)
    return HttpResponse(simplejson.dumps(tmp_file), mimetype="text/csv")


def json_csv(json_file):
    output = csv.writer(open("test.csv", "wb+"))
    output.writerow(json_file[0].keys())
    
    for row in json_file:
        output.writerow(row.values())
    
    return output
    
    