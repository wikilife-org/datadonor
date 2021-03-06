from django.http import HttpResponseRedirect
from social.models import SocialGlobalAggregatedData

def redirect_to_form(*args, **kwargs):
    if not kwargs['request'].session.get('saved_username') and \
       kwargs.get('user') is None:
        return HttpResponseRedirect('/form/')


def username(request, *args, **kwargs):
    if kwargs.get('user'):
        username = kwargs['user'].username
    else:
        username = request.session.get('saved_username')
    return {'username': username}


def redirect_to_form2(*args, **kwargs):
    if not kwargs['request'].session.get('saved_first_name'):
        return HttpResponseRedirect('/form2/')


def first_name(request, *args, **kwargs):
    if 'saved_first_name' in request.session:
        user = kwargs['user']
        user.first_name = request.session.get('saved_first_name')
        user.save()

def social_aggretated_data(request, *args, **kwargs):
    try:
        social_global = SocialGlobalAggregatedData.objects.latest()
    except:
        social_global = SocialGlobalAggregatedData()
        
    return {'social_global': social_global}

