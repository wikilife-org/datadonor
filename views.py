from django.http import HttpResponseRedirect
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.messages.api import get_messages
from social_auth import __version__ as version
from django.http.response import HttpResponse
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from utils.user_linked_data import refresh_user_data


def comming(request):
    return render_to_response('splash/index.html', {'version': version},
                                  RequestContext(request))

def demo(request):
    return render_to_response('demo/index.html', {'version': version},
                                  RequestContext(request))

def wizard(request):
    agent = request.META['HTTP_USER_AGENT']
    show_wizard =  request.user.is_authenticated() or request.session.get("user_agree", False)
    if request.user.is_authenticated() and not request.session.get("wizard_mode", False):
        return HttpResponseRedirect('/')
    ctx = {'version': version, 'show_wizard':show_wizard, 'agent':agent}
    if request.user.is_authenticated() and (request.user.profile.gender == None or request.user.profile.gender == "") :
        ctx["no_gender"] = True
    return render_to_response('wizard.html',ctx ,
                                  RequestContext(request))

def terms(request):
    show_wizard =  request.user.is_authenticated() or request.session.get("user_agree", False)
    if show_wizard:
        return HttpResponseRedirect('/wizard/')
    return render_to_response('wizard.html', {'version': version, 'show_wizard':show_wizard, 'agent':agent},
                                  RequestContext(request))

def privacy(request):
    return render_to_response('static/privacy.html',{},
                                  RequestContext(request))

def tos(request):
    return render_to_response('static/tos.html',{},
                                  RequestContext(request))

def learn_more(request):
    return render_to_response('static/learn_more.html',{},
                                  RequestContext(request))

def about(request):
    if  not request.user.is_authenticated():
        return HttpResponseRedirect('/')
    videos = request.GET.get('videos', None)
    return render_to_response('landing.html', {'can_share': True, 'version': version, 'videos':videos, "loop_times":range(1,79)},
                              RequestContext(request))
def home(request):
    """Home view, displays login mechanism"""
    videos = request.GET.get('videos', None)
    ctx =  {'version': version}
    if request.user.is_authenticated():
        #refresh_user_data(request.user)
        ctx = {
            'user': request.user,
            #'user_social':request.user.social_aggregated_data.social_reach(),
            'version': version,
            'last_login': request.session.get('social_auth_last_login_backend')
        }
        return render_to_response('dashboard/index.html', ctx, context_instance=RequestContext(request))
    if request.session.get("wizard_mode", False):
        return HttpResponseRedirect('/wizard/')

    context = {'can_share': True, 'version': version, 'videos':videos, "loop_times":range(1,79)}
    if request.session.get("login_error", False):
        context["login_error"] = True
        del request.session["login_error"]
        request.session.modified = True

    return render_to_response('landing.html', context,
                                  RequestContext(request))

def greg(request):
    return render_to_response('google7d1bd3580ebd5b1b.html', {},
                                  RequestContext(request))


def dashboard(request):
    return HttpResponseRedirect('/')

def end_wizard(request):
    request.session["wizard_mode"] = False
    request.session.modified = True
    return HttpResponseRedirect('/')

def error(request):
    """Error view"""
    messages = get_messages(request)
    return render_to_response('error.html', {'version': version,
                                             'messages': messages},
                              RequestContext(request))

def user_account(request):

    data = {"logged":request.user.is_authenticated(),
    "accounts": [a.provider for a in request.user.social_auth.all()]}
    return HttpResponse(simplejson.dumps(data), mimetype="application/json")


def logout(request):
    """Logs out user"""
    auth_logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
def iagree(request):
    if request.method == 'POST':
        request.session["user_agree"] = True
        request.session["wizard_mode"] = True
        request.session.modified = True
        return HttpResponse(simplejson.dumps({}), mimetype="application/json")
    return HttpResponseRedirect('/wizard/')
