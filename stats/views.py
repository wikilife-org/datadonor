

from django.http.response import HttpResponse
from django.utils import simplejson
from physical.services.stats.services import PhysicalActivityDistributionService
from django.shortcuts import render_to_response
from django.template import RequestContext
from users.models import Profile


def get_miles(request):
    dto = PhysicalActivityDistributionService().get_records_miles()
    
    return HttpResponse(simplejson.dumps(dto), mimetype="application/json")


def go_stats(request):
    total_dd_user = Profile.objects.count()
    return render_to_response('stats/index.html',{"total_dd_users": total_dd_user},RequestContext(request))