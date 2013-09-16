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


def comming(request):
    return render_to_response('splash/index.html', {'version': version},
                                  RequestContext(request))

def mock(request):
    return render_to_response('maquetas/index.html', {'version': version},
                                  RequestContext(request))

                        
def wizard(request):
    agent = request.META['HTTP_USER_AGENT']
    return render_to_response('wizard.html', {'version': version, 'agent':agent},
                                  RequestContext(request))

def home(request):
    """Home view, displays login mechanism"""

    ctx =  {'version': version}
        
    return render_to_response('landing.html', {'version': version},
                                  RequestContext(request))

def greg(request):
    return render_to_response('google7d1bd3580ebd5b1b.html', {},
                                  RequestContext(request))
def donate(request):
    """Login complete view, displays user data"""
    ctx = {
        'user': request.user,
        'user_social':request.user.social_aggregated_data.social_reach(),
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    return render_to_response('data_donation.html', ctx, context_instance=RequestContext(request))


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


def form(request):
    if request.method == 'POST' and request.POST.get('username'):
        name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        request.session['saved_username'] = request.POST['username']
        backend = request.session[name]['backend']
        return redirect('socialauth_complete', backend=backend)
    return render_to_response('form.html', {}, RequestContext(request))


def form2(request):
    if request.method == 'POST' and request.POST.get('first_name'):
        request.session['saved_first_name'] = request.POST['first_name']
        name = setting('SOCIAL_AUTH_PARTIAL_PIPELINE_KEY', 'partial_pipeline')
        backend = request.session[name]['backend']
        return redirect('socialauth_complete', backend=backend)
    return render_to_response('form2.html', {}, RequestContext(request))


def close_login_popup(request):
    return render_to_response('close_popup.html', {}, RequestContext(request))


#TODO add sec token
def wikilife_push(request):
    WikilifeConnector().push()
    return HttpResponse("ok")

#TODO add sec token
def wikilife_pull(request):
    WikilifeConnector().pull()
    return HttpResponse("ok")