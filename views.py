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
from reports.services.internal import get_new_users_distribution, get_device_by_users_distribution
from utils.commons import send_email_report
import base64
from django.contrib.auth.models import User
from django.contrib.auth import login
from users.models import ResarchKitBackendUser
from validate_email import validate_email

def news(request):
    return render_to_response('news.html',{},RequestContext(request))

def datadonors_researchkit_backend(request):
    context = {"show_thanks": False}
    if request.POST:
        email = request.POST.get("email","")
        is_valid= validate_email(email)
        if is_valid:
            ResarchKitBackendUser.objects.create(email=email)
            context["show_thanks"] = True
        else:
            context["error"] = True
        
    return render_to_response('backend/backend.html',context,RequestContext(request))

def datadonors_researchkit_backend_email(request):
    context = {"show_thanks": False}
    if request.POST:
        email = request.POST.get("email","")
        
        ResarchKitBackendUser.objects.create(email=email)
        context["show_thanks"] = True
        
    return render_to_response('backend/backend.html',context,RequestContext(request))

def datadonors_researchkit_backend_doc(request):
        
    return render_to_response('researchkit/documentation.html',{},RequestContext(request))

def new_users_report(request):
    total, result = get_new_users_distribution()
    total_user, result_devices = get_device_by_users_distribution()
    #send_email_report("jquintas@wikilife.org", result)
    return render_to_response('email/new_users_report.html',{"result_user":result, "result_devices":result_devices, "total_users":total_user},
                                  RequestContext(request))

def test_report(request):
    return render_to_response('email/report.html',{"user_id":base64.b64encode(str(1).encode('ascii'))},
                                  RequestContext(request))

def validate(request, user_encode):
    user_id = int(base64.b64decode(user_encode))
    user = User.objects.get(id=user_id)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return HttpResponseRedirect('/')

def send_test_email(request):
    send_email_report("jquintas@wikilife.org", "DataDonors Weekly Report", {"user_id":base64.b64encode(str(1).encode('ascii'))})
    return render_to_response('static/mission.html',{},
                                  RequestContext(request))

def app(request):
    return render_to_response('app/app.html',{},
                                  RequestContext(request))
def support_us(request):
    return render_to_response('static/support.html',{},
                                  RequestContext(request))

def mission(request):
    return render_to_response('static/mission.html',{},
                                  RequestContext(request))

def advisory(request):
    return render_to_response('static/advisory.html',{},
                                  RequestContext(request))

def team(request):
    return render_to_response('static/team.html',{},
                                  RequestContext(request))
    
def contact(request):
    return render_to_response('static/contact.html',{},
                                  RequestContext(request))
    
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
    if request.session.get("login_error", False):
        ctx["login_error"] = True
        del request.session["login_error"]
        request.session.modified = True
    return render_to_response('wizard.html',ctx ,
                                  RequestContext(request))

def terms(request):
    show_wizard =  request.user.is_authenticated() or request.session.get("user_agree", False)
    if show_wizard:
        return HttpResponseRedirect('/wizard/')
    return render_to_response('wizard.html', {'version': version, 'show_wizard':show_wizard,},
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


from mobi.decorators import detect_mobile

@detect_mobile
def home(request):
    if request.mobile:
        return HttpResponseRedirect('http://m.datadonors.org/')
    
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
