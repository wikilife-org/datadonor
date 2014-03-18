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


def comming(request):
    return render_to_response('splash/index.html', {'version': version},
                                  RequestContext(request))

def demo(request):
    return render_to_response('demo/index.html', {'version': version},
                                  RequestContext(request))

def wizard(request):
    agent = request.META['HTTP_USER_AGENT']
    show_wizard =  request.user.is_authenticated() or request.session.get("user_agree", False)
    return render_to_response('wizard.html', {'version': version, 'show_wizard':show_wizard, 'agent':agent},
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
    
def home(request):
    """Home view, displays login mechanism"""
    videos = request.GET.get('videos', None)
    ctx =  {'version': version}   
    return render_to_response('landing.html', {'can_share': True, 'version': version, 'videos':videos, "loop_times":range(1,79)},
                                  RequestContext(request))

def greg(request):
    return render_to_response('google7d1bd3580ebd5b1b.html', {},
                                  RequestContext(request))


from wikilife.clients.user  import User

def create_wikilife_user(profile):
    client = User({"HOST":"http://api.wikilife.org"})
    user_name = _create_user_name(client, profile.account_id)
    pin = "0000"
    gender = profile.gender
    birthdate = None
    height = profile.height
    weight = profile.weight 
    device_id = profile.device_id or "datadonors"
    timezone = profile.timezone or None
    city = profile.city or None
    region = profile.region or None
    country = profile.country or None
    success = client.create_account(user_name, pin, gender, birthdate, height, weight, device_id, timezone, city, region, country)

    if not success:
        raise UsersSyncException("Wikilife account creation failed for Datadonor profile.account_id: %s" %profile.account_id)

    token = client.login(user_name, pin)
    profile.wikilife_token = token
    profile.save()

def _create_user_name(client, unique_id):
    base_user_name = "datadonor_"
    user_name = "%s%s" %(base_user_name, unique_id)

    i = 1
    while not client.check_name(user_name):
        user_name = "%s%s_$s" %(base_user_name, unique_id, i)
        i += 1

    return user_name 

def dashboard(request):
    """Login complete view, displays user data"""
    if not request.user.is_authenticated() or request.session.get("wizard_mode", False):
        return HttpResponseRedirect('/wizard/')
    #else:
        #if not request.user.profile.wikilife_token:
            #pass
            #create_wikilife_user(request.user.profile)
            
    ctx = {
        'user': request.user,
        #'user_social':request.user.social_aggregated_data.social_reach(),
        'version': version,
        'last_login': request.session.get('social_auth_last_login_backend')
    }
    return render_to_response('dashboard/index.html', ctx, context_instance=RequestContext(request))

def end_wizard(request):
    request.session["wizard_mode"] = False
    return HttpResponseRedirect('/dashboard/')

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
        return HttpResponse(simplejson.dumps({}), mimetype="application/json")
    return HttpResponseRedirect('/wizard/')
