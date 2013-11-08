
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
              "values":[{"name":"Slighty curlier hair", "id":"likely_blue", "percentage":65, "user_group":True},
                        {"name":"Straigher curlier hair", "id":"likely_brown","percentage":35, "user_group":False}],
              },
            {"name": "Malaria Resistance", 
              "id":8, 
              "values":[{"name":"Possibly resistant", "id":"possibly_resistant", "percentage":15, "user_group":True},
                        {"name":"Resistant", "id":"resistant","percentage":85, "user_group":False}],
              },
            {"name": "Norovirus Resistance", 
              "id":9, 
              "values":[{"name":"Not resistant", "id":"not_resistant", "percentage":15, "user_group":True},
                        {"name":"Resistant", "id":"resistant","percentage":85, "user_group":False}],
              },
            {"name": "Resistance to HIV/AIDS", 
              "id":10, 
              "values":[{"name":"Not resistance", "id":"not_resistance", "percentage":25,"user_group":True},
                        {"name":"Resistance", "id":"resistance","percentage":75, "user_group":False}],
              }
            ]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def genomics_drugs_mock(request):
    data = [{"name":"Alcohol consumption, smoking and risk of esophageal cancer", "id":0, "values":[
                        {"name":"Typical risk", "id":"typical_risk", "percentage":70},
                        {"name":"Substantially increased risk", "id":"subs_increased_risk", "percentage":25},
                        {"name":"Greatly increased risk", "id":"great_typical_risk", "percentage":5},]},
            {"name":"Oral contraceptives, hormone replacement therapy and risk of venous thromboembolism", "id":1, "values":[
                        {"name":"Normal", "id":"normal", "percentage":85},
                        {"name":"Reduced", "id":"reduced", "percentage":11},
                        {"name":"Unable", "id":"unable", "percentage":4}]
             }]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def genomics_risks_mock(request):
    data = [
            {"name":"Breast Cancer", "percentages":{"user":60, "all":90}},
            {"name":"Celiac Disease", "percentages":{"user":8, "all":13}},
            {"name":"Venous Thromb.", "percentages":{"user":60, "all":20}},
            {"name":"Melanoma", "percentages":{"user":16, "all":32}},
            {"name":"Coronary Heart Dis.", "percentages":{"user":6, "all":2}},
            {"name":"Lung Cancer", "percentages":{"user":1, "all":5}}]
    
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
