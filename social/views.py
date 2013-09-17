from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from social_auth import __version__ as version
from social_auth.utils import setting
from wikilife.wikilife_connector import WikilifeConnector
from django.http.response import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt

def comming(request):
    return render_to_response('splash/index.html', {'version': version},
                                  RequestContext(request))

def mock(request):
    return render_to_response('maquetas/index.html', {'version': version},
                                  RequestContext(request))

                        
def wizard(request):
    agent = request.META['HTTP_USER_AGENT']
    show_wizard =  request.user.is_authenticated() or request.session.get("user_agree", False)
    return render_to_response('wizard.html', {'version': version, 'show_wizard':show_wizard, 'agent':agent},
                                  RequestContext(request))

def home(request):
    """Home view, displays login mechanism"""

    ctx =  {'version': version}
        
    return render_to_response('landing.html', {'version': version},
                                  RequestContext(request))

def greg(request):
    return render_to_response('google7d1bd3580ebd5b1b.html', {},
                                  RequestContext(request))
def dashboard(request):
    """Login complete view, displays user data"""
    if not request.user.is_authenticated() or request.session.get("wizard_mode", False):
        return HttpResponseRedirect('/wizard/')
    ctx = {
        'user': request.user,
        'user_social':request.user.social_aggregated_data.social_reach(),
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    return render_to_response('data_donation.html', ctx, context_instance=RequestContext(request))

def end_wizard(request):
    request.session["wizard_mode"] = False
    return HttpResponseRedirect('/dashboard/')

def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version,
                                             'messages': messages},
                              RequestContext(request))


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
def iagree(request):
    if request.method == 'POST':
        request.session["user_agree"] = True
        request.session["wizard_mode"] = True
        return HttpResponse(simplejson.dumps({}), mimetype="application/json")
    return HttpResponseRedirect('/wizard/')


#TODO add sec token
def wikilife_push(request):
    WikilifeConnector().push()
    return HttpResponse("ok")

#TODO add sec token
def wikilife_pull(request):
    WikilifeConnector().pull()
    return HttpResponse("ok")