
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http.response import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

 
def genomics_traits_mock(request):
    data = {}
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
