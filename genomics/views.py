
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http.response import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from genomics.utilities import *
 
def genomics_traits_global_mock(request):
    data = [ {"name": "Alcohol Flush Reaction", 
              "id":0, 
              "values":[{"name":"Flushes", "percentage":60},
                        {"name":"Do not flush", "percentage":40}],
              },
            {"name": "Lactose Intolerance", 
              "id":1, 
              "values":[{"name":"Likely intolerance", "percentage":80},
                        {"name":"Likely tolerance","percentage":20}],
              },
            {"name": "Smoking Behavior", 
              "id":2, 
              "values":[{"name":"Likely to smoke more", "percentage":10},
                        {"name":"Typical","percentage":90}],
              },
            {"name": "Bitter Taste Perception", 
              "id":3, 
              "values":[{"name":"Can taste",  "percentage":15},
                        {"name":"Unlikely to taste", "percentage":85}],
              }
            ,
            {"name": "Earwax Type", 
              "id":4, 
              "values":[{"name":"Dry", "percentage":20},
                        {"name":"Wet", "percentage":80}],
              },
            {"name": "Muscle Performance", 
              "id":5, 
              "values":[{"name":"Likely sprinter", "percentage":95},
                        {"name":"Unlikely sprinter", "percentage":05}],
              },
            {"name": "Eye Color", 
              "id":6, 
              "values":[{"name":"Likely blue", "percentage":60},
                        {"name":"Likely brown","percentage":40}],
              },
            {"name": "Hair Curl", 
              "id":7, 
              "values":[{"name":"Slighty curlier hair", "percentage":65},
                        {"name":"Straigher curlier hair","percentage":35}],
              },
            {"name": "Malaria Resistance", 
              "id":8, 
              "values":[{"name":"Possibly resistant", "percentage":15},
                        {"name":"Resistant", "percentage":85}],
              },
            {"name": "Norovirus Resistance", 
              "id":9, 
              "values":[{"name":"Not resistant", "percentage":15},
                        {"name":"Resistant","percentage":85}],
              },
            {"name": "Resistance to HIV/AIDS", 
              "id":10, 
              "values":[{"name":"Not resistant", "percentage":25},
                        {"name":"Partially resistant", "percentage":75}],
              }
            ]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def genomics_traits_by_user_mock(request):
    data = [ {
              "id":0, 
              "value":"Flushes",
              },
            {
              "id":1, 
              "value":"Likely intolerance",
              },
            { 
              "id":2, 
              "value":"Likely to smoke more",
              },
            {
              "id":3, 
              "value":"Can taste",
              }
            ,
            {
              "id":4, 
              "value":"Dry",
              },
            { 
              "id":5, 
              "value":"Likely sprinter",
              },
            {
              "id":6, 
              "value":"Likely blue",
              },
            {
              "id":7, 
              "value":"Slighty curlier hair",
              },
            { 
              "id":8, 
              "value":"Possibly resistant",
              },
            {
              "id":9, 
              "value":"Not resistant",
              },
            { 
              "id":10, 
              "value":"Not resistant",
              }
            ]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def genomics_drugs_global_mock(request):
    data = [{"name":"Alcohol consumption, smoking and risk of esophageal cancer", "id":0, "values":[
                        {"name":"Typical risk", "percentage":70},
                        {"name":"Substantially increased risk",  "percentage":25},
                        {"name":"Greatly increased risk", "percentage":5},]},
            
                        {"name":"Oral contraceptives, hormone replacement therapy and risk of venous thromboembolism", "id":1, "values":[
                        {"name":"Normal",  "percentage":85},
                        {"name":"Reduced",  "percentage":11},
                        {"name":"Unable", "percentage":4}]
             }]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def genomics_drugs_by_user_mock(request):
    data = [{"id":0, "value":"Greatly increased risk"},
            {"id":1, "value":"Unable"}]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def genomics_risks_global_mock(request):
    data = [
            {"name":"Breast Cancer", "id":0, "percentage":90},
            {"name":"Celiac Disease","id":1, "percentage":13},
            {"name":"Venous Thromb.", "id":2, "percentage":20},
            {"name":"Melanoma", "id":3, "percentage":32},
            {"name":"Coronary Heart Dis.", "id":4, "percentage":2},
            {"name":"Lung Cancer", "id":5, "percentage":5}]
    
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def genomics_risks_by_user_mock(request):
    data = [
            {"id":0, "percentage":60},
            {"id":1, "percentage":8},
            {"id":2, "percentage":60},
            {"id":3, "percentage":16},
            {"id":4, "percentage":6},
            {"id":5, "percentage":1}]
    
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def genomics_traits_global(request):
    

    data = [ get_traits_alcohol_distribution(),
             get_traits_lactose_distribution(),
             get_traits_smoking_distribution(),
             get_traits_bitter_distribution(),
            get_traits_earwax_distribution(),
            {"name": "Muscle Performance", 
              "id":5, 
              "values":[{"name":"Likely sprinter", "percentage":95},
                        {"name":"Unlikely sprinter", "percentage":05}],
              },
            {"name": "Eye Color", 
              "id":6, 
              "values":[{"name":"Likely blue", "percentage":60},
                        {"name":"Likely brown","percentage":40}],
              },
            {"name": "Hair Curl", 
              "id":7, 
              "values":[{"name":"Slighty curlier hair", "percentage":65},
                        {"name":"Straigher curlier hair","percentage":35}],
              },
            {"name": "Malaria Resistance", 
              "id":8, 
              "values":[{"name":"Possibly resistant", "percentage":15},
                        {"name":"Resistant", "percentage":85}],
              },
            {"name": "Norovirus Resistance", 
              "id":9, 
              "values":[{"name":"Not resistant", "percentage":15},
                        {"name":"Resistant","percentage":85}],
              },
            {"name": "Resistance to HIV/AIDS", 
              "id":10, 
              "values":[{"name":"Not resistant", "percentage":25},
                        {"name":"Partially resistant", "percentage":75}],
              }
            ]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def genomics_traits_by_user(request):
    alcohol_trait = request.user.traits.get(user=request.user, report_id="alcoholflush").value
    lactose = request.user.traits.get(user=request.user, report_id="lactose").value
    smokingbehavior = request.user.traits.get(user=request.user, report_id="smokingbehavior").value
    bittertaste = request.user.traits.get(user=request.user, report_id="bittertaste").value
    earwax = request.user.traits.get(user=request.user, report_id="earwax").value
    
    
    data = [ {
              "id":0, 
              "value":alcohol_trait,
              },
            {
              "id":1, 
              "value":lactose,
              },
            { 
              "id":2, 
              "value":smokingbehavior,
              },
            {
              "id":3, 
              "value":bittertaste,
              }
            ,
            {
              "id":4, 
              "value":earwax,
              },
            { 
              "id":5, 
              "value":"Likely sprinter",
              },
            {
              "id":6, 
              "value":"Likely blue",
              },
            {
              "id":7, 
              "value":"Slighty curlier hair",
              },
            { 
              "id":8, 
              "value":"Possibly resistant",
              },
            {
              "id":9, 
              "value":"Not resistant",
              },
            { 
              "id":10, 
              "value":"Not resistant",
              }
            ]
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def genomics_drugs_global(request):
    data = {}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")

def genomics_drugs_by_user(request):
    data = {}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def genomics_risks_global(request):
    data = {}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def genomics_risks_by_user(request):
    data = {}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")
