

from django.http.response import HttpResponse
from django.utils import simplejson
from physical.services.stats.services import PhysicalActivityDistributionService
from django.shortcuts import render_to_response
from django.template import RequestContext


def get_miles(request):
    dto = PhysicalActivityDistributionService().get_records_miles()
    
    return HttpResponse(simplejson.dumps(dto), mimetype="application/json")


def go_stats(request):
    return render_to_response('stats/stats.html',{},RequestContext(request))