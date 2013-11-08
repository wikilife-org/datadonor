
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http.response import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

 
def genomics_traits_mock(request):
    data = [ {"name": "Alcohol Flush Reaction", 
              "id":0, 
              "values":[{"name":"Flushes", "id":"flushes", "percentage":60, "user_group":True},
                        {"name":"Do not flush", "id":"does_not_flush","percentage":40, "user_group":False}],
              },
            {"name": "Lactose Intolerance", 
              "id":1, 
              "values":[{"name":"Likely intolerance", "id":"likely_intolerance", "percentage":80, "user_group":True},
                        {"name":"Likely tolerance", "id":"likely_tolerance","percentage":20, "user_group":False}],
              },
            {"name": "Smoking Behavior", 
              "id":2, 
              "values":[{"name":"Likely to smoke more", "id":"likely_smoke_more", "percentage":10, "user_group":True},
                        {"name":"Typical", "id":"typical","percentage":90, "user_group":False}],
              },
            {"name": "Bitter Taste Perception", 
              "id":3, 
              "values":[{"name":"Can taste", "id":"can_taste", "percentage":15, "user_group":True},
                        {"name":"Unlikely to taste", "id":"unlikely_taste","percentage":85, "user_group":False}],
              }
            ,
            {"name": "Earwax Type", 
              "id":4, 
              "values":[{"name":"Dry", "id":"dry", "percentage":20, "user_group":True},
                        {"name":"Wet", "id":"wet","percentage":80, "user_group":False}],
              },
            {"name": "Muscle Performance", 
              "id":5, 
              "values":[{"name":"Likely sprinter", "id":"likely_sprinter", "percentage":95, "user_group":True},
                        {"name":"Unlikely sprinter", "id":"unlikely_sprinter","percentage":05, "user_group":False}],
              },
            {"name": "Eye Color", 
              "id":6, 
              "values":[{"name":"Likely blue", "id":"likely_blue", "percentage":60, "user_group":True},
                        {"name":"Likely brown", "id":"likely_brown","percentage":40, "user_group":False}],
              },
            {"name": "Hair Curl", 
              "id":7, 
              "values":[{"name":"Likely blue", "id":"likely_blue", "percentage":60, "user_group":True},
                        {"name":"Likely brown", "id":"likely_brown","percentage":40, "user_group":False}],
              },
            {"name": "Eye Color", 
              "id":8, 
              "values":[{"name":"Likely blue", "id":"likely_blue", "percentage":60, "user_group":True},
                        {"name":"Likely brown", "id":"likely_brown","percentage":40, "user_group":False}],
              },
            {"name": "Eye Color", 
              "id":9, 
              "values":[{"name":"Likely blue", "id":"likely_blue", "percentage":60, "user_group":True},
                        {"name":"Likely brown", "id":"likely_brown","percentage":40, "user_group":False}],
              },
            {"name": "Eye Color", 
              "id":10, 
              "values":[{"name":"Likely blue", "id":"likely_blue", "percentage":60,"user_group":True},
                        {"name":"Likely brown", "id":"likely_brown","percentage":40, "user_group":False}],
              },
            {"name": "Eye Color", 
              "id":11, 
              "values":[{"name":"Likely blue", "id":"likely_blue", "percentage":60, "user_group":True},
                        {"name":"Likely brown", "id":"likely_brown","percentage":40, "user_group":False}],
              }
            ]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def genomics_drugs_mock(request):
    data = {}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def genomics_risks_mock(request):
    data = {}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def genomics_traits(request):
    data = {}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def genomics_drugs(request):
    data = {}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def genomics_risks(request):
    data = {}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
