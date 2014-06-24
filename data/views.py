from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.http.response import HttpResponse
from django.utils import simplejson
from django.contrib.auth.models import User
from social.services.utilities import *
from utils.date_util import get_last_sunday

def download(request):
    ctx = {"last_sunday": get_last_sunday()[1]}
    return render_to_response('data/download.html',ctx,
                                  RequestContext(request))
